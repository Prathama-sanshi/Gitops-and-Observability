# 🚀 Introduction:

This repository demonstrates a complete GitOps-driven Kubernetes deployment platform running on WSL. It showcases the deployment of a custom Prometheus-instrumented application, a production-ready observability stack, and automated infrastructure management using both ArgoCD and FluxCD(check branches). The project leverages Helm, Kustomize, GitHub Actions self-hosted runners, and GitOps best practices to enable consistent, automated application delivery and lifecycle management.

### 🚀 GitOps & Observability

* **Prometheus Instrumentation:** Developed a Python file-monitoring application using the **Prometheus client library** to expose custom application metrics on /metrics via port 8000.
* **Containerization & Helm Packaging:** Dockerized the core application and packaged it into a customizable **Helm chart** complete with ConfigMaps, liveness/readiness probes, Horizontal Pod Autoscalers (HPA), and strict CPU/memory resource limits.
* **Observability Stack Integration:** Deployed the **kube-prometheus-stack** in-cluster and configured automated metric scraping from the application instances utilizing a targeted Kubernetes **PodMonitor** custom resource.
* **Alerting as Code:** Coded proactive alerting thresholds directly into the infrastructure repository using Prometheus operator **PrometheusRule** CRDs.
* **GitOps Automation:** Automated the entire end-to-end infrastructure and application deployment lifecycle with **ArgoCD** and **FluxCD**, For ArgoCD  **app-of-apps** architectural pattern alongside **Kustomize-based** environment overlays for development is used and for FluxCD

  
### 🚀 Prerequisites
* WSL version: 2.7.13.0 or higher
* Docker version: 29.3.0 or higher
* Minikube version: v1.38.0  or higher
* FluxCD CLI version: 2.9.5 or higher (Helm chart: 2.19.0)
* ArgoCD CLI version: v3.5.1+109ca7c (Helm chart:  10.3.3)

## 🚀 Infrastructure Setup

We are going to deploy the custom application, observability stack, and GitOps agent in our WSL environment.

To accomplish this, we first need to create a self-hosted GitHub Actions runner on the local WSL machine.

### Step 1: Log in to GitHub
Sign in to your GitHub account using a web browser.

### Step 2: Navigate to Self-Hosted Runners
1. Open your GitHub repository.
2. Go to **Settings** → **Actions** → **Runners**.
3. Select **Self-hosted runners**.

### Step 3: Create a New Runner
1. Click **New self-hosted runner**.
2. Select the appropriate operating system and architecture for your WSL environment.
3. Copy the generated setup commands.
4. Run the commands in your local WSL terminal to register the runner with the repository.

### Step 4: Verify the Runner
After the configuration is complete, start the runner by executing:
Whenever you are running GitHub pipeline use this below command to host your runner in local WSL.
```bash
./run.sh
```

<img width="595" height="155" alt="image" src="https://github.com/user-attachments/assets/38c4425f-9d14-434f-af66-69ce07dcf8e3" />


## 1.Deploy Application via FluxCD
* To deploy custom application (file-monitor) and observability via FluxCD follow the following steps:
    * Step: 1.Run Pipeline FluxCD Setup
        * This will preform the sanity check for docker, minikube and fluxcd cli versions.
        * This will helm install fluxcd in flux-system namespace.
        * You can verify by doing kubectl get pods -n flux-system in cluster
        * This creates gitrepository CR and its secret along with kustomization CR.
        * It uses Kustomization CR path to watch the changes in repository.
    * Step: 2.Run Pipeline FluxCD Gitops Deployment.
        * This will clone the flucd-obs repo
        * It uncomments out entry of desired application(pipeline inputes) under path ./Application/apps/overlays/dev-cluster/kustomization.yaml.
        * When FluxCD reconciles the Kustomization, it processes the referenced HelmRelease resources and deploys the application to the Kubernetes cluster.
        * The application is then automatically deployed and managed by FluxCD.
    * Step: 3.Run Pipeline FluxCD Gitops Undeployment
        * This will clone the flucd-obs repo
        * And comments out entry of desired application under path ./Application/apps/overlays/dev-cluster/kustomization.yaml.
        * When FluxCD kustomization renders the charts, it picks the changes and applies it to cluster (deletes if not present)
        * During the next reconciliation cycle, FluxCD detects the change and updates the cluster state accordingly.
        * Resources that are no longer referenced are removed from the cluster.
        * The application is successfully undeployed by FluxCD.
    * Step: 4.Run Pipeline FluxCD Uninstall - cleanup
        * This will helm uninstall the FluxCD
        * Delete the FluxCD Custom Resources and related configurations.
        * Cleans up all Flux-managed resources to restore the cluster to its pre-installation state.
### Result After Deployment :
1] See HelmRelease in flux-system namespace
<img width="1699" height="118" alt="image" src="https://github.com/user-attachments/assets/c08bd6c3-e962-4c22-9f84-65c6087fdda7" />

2] Verify Pods:
<img width="1014" height="98" alt="image" src="https://github.com/user-attachments/assets/276985ff-9f05-4e5a-9060-05ad02ebc5bb" />

3]Verify App Resources:

<img width="768" height="75" alt="image" src="https://github.com/user-attachments/assets/df87e569-38ed-4c77-8e6b-6da49163b4f7" />


4] Un-deploy Scenario: 
* As soon as the flux picks the latest commit, the pod goes into terminating state
<img width="1699" height="134" alt="image" src="https://github.com/user-attachments/assets/566d21c0-4806-4d1f-b5e7-c4a7591d3915" />

<img width="1079" height="97" alt="image" src="https://github.com/user-attachments/assets/bd6fa97d-cabe-4134-803f-9289e7a00e67" />



## 2.Deploy Application via ArgoCD
* To deploy custom application (file-monitor) and observability via ArgoCD follow the following steps:
    * Step: 1.Run Pipeline ArgoCD Setup
        * This will preform the sanity check for docker, minikube versions.
        * This will helm install argocd in argocd namespace.
        * You can verify by doing kubectl get pods -n argocd in cluster
        * This creates AppProject and Application CR.
        * pre-requisite : create a git secret that connect github via ssh. 
    * Step: 2.Run Pipeline ArgoCD Gitops Deployment.
        * This will clone the argocd-obs repo
        * It uncomments out entry of desired application(pipeline inputes) under path ./Application/apps/overlays/dev-cluster/kustomization.yaml.
        * When ArgoCD reconciles the Kustomization, it processes the referenced Application resources and deploys the application to the Kubernetes cluster.
        * The application is then automatically deployed and managed by ArgoCD.
    * Step: 3.Run Pipeline ArgoCD Gitops Undeployment
        * This will clone the argocd-obs repo
        * And comments out entry of desired application under path ./Application/apps/overlays/dev-cluster/kustomization.yaml.
        * When argocd kustomization renders the charts, it picks the changes and applies it to cluster (deletes if not present)
        * During the next reconciliation cycle, argocd detects the change and updates the cluster state accordingly.
        * Resources that are no longer referenced are removed from the cluster.
        * The application is successfully undeployed by argocd.
    * Step: 4.Run Pipeline Argocd Uninstall - cleanup
        * This will helm uninstall the ArgoCD
        * Delete the ArgoCD Custom Resources and related configurations.
        * Cleans up all argocd-managed resources to restore the cluster to its pre-installation state.
          
Helmrelease and architectural pattern alongside **Kustomize-based** environment overlays for developments is used.

# Observability Dashboards
* Grafana Dashboard:
<img width="1586" height="818" alt="image" src="https://github.com/user-attachments/assets/4ba9fa75-efc1-4e3d-b187-d927dc4b433f" />
* Prometheus Alerts:
<img width="1597" height="644" alt="image" src="https://github.com/user-attachments/assets/91aa1dcc-71ae-44dd-86d4-906a7d124219" />
* Prometheus Targets:
<img width="1593" height="357" alt="image" src="https://github.com/user-attachments/assets/c44f87dd-46b4-4ea8-9bbd-01bc9d6fe349" />


