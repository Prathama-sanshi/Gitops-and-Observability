#!/bin/bash
set -euo pipefail
echo "Installing FluxCD..."
cd Helm-chart/flux2/
pwd
echo "Patching existing Flux CRDs to allow Helm adoption..."
# 1. Get all CRDs containing 'fluxcd.io'
# 2. Add the tracking label Helm requires
# 3. Add the tracking annotations Helm requires
for crd in $(kubectl get crd -o jsonpath='{.items[*].metadata.name}' | tr ' ' '\n' | grep 'fluxcd.io'); do
    echo "Adopting CRD: $crd"
    kubectl label crd "$crd" app.kubernetes.io/managed-by=Helm --overwrite
    kubectl annotate crd "$crd" meta.helm.sh/release-name=fluxcd meta.helm.sh/release-namespace=flux-system --overwrite
done

helm upgrade --install fluxcd . \
  -f values.yaml \
  -n flux-system \
  --create-namespace \
  --force

echo "Applying GitRepository..."
# --- 1. Check for GITHUB_TOKEN ---
if [ -z "${GITHUB_TOKEN:-}" ]; then
    echo "❌ Error: GITHUB_TOKEN environment variable is not set."
    echo "Please run: export GITHUB_TOKEN='your_token_here' before running this script."
    exit 1
fi
cd ../../Resources
pwd
kubectl apply -f GitRepository.yaml
kubectl create secret generic git-credentials -n flux-system --from-literal=username=oauth2 --from-literal=password=$GITHUB_TOKEN
kubectl apply -f kustomization.yaml
echo "FluxCD setup completed!"
