### 🚀 Prerequisites
* WSL version: 2.7.13.0 or higher
* Docker version: 29.3.0 or higher
* Minikube version: v1.38.0  or higher
* FluxCD CLI version: 2.9.5 or higher (Helm chart: 2.19.0)
* ArgoCD CLI version: v3.5.1+109ca7c (Helm chart:  10.3.3)

### 🚀 Introduction:
# 1.Deploy Application via FluxCD
* To deploy custom application (file-monitor) and observability via FluxCD follow the following steps:
    * Step: 1.Run Pipeline FluxCD Setup
        * This will preform the sanity check for docker, minikube and fluxcd cli versions.
        * This will helm install fluxcd in flux-system namespace.
        * You can verify by doing kubectl get pods -n flux-system
        * This creates gitrepository CRD and its secret along with kustomization CRD.
        * It uses Kustomization CRD path to watch the changes in repository.
    * Step: 2.Run Pipeline FluxCD Gitops Deployment.
        * This will clone the flucd-obs repo
        * And uncomments the desired application under path ./Application/apps/overlays/dev-cluster/kustomization.yaml.
        * When FluxCD kustomization renders the charts, it see the helmrelease and deployes in the cluster.
        * The Application gets deployed via FluxCD.
    * Step: 3.Run Pipeline FluxCD Gitops Undeployment
        * This will clone the flucd-obs repo
        * And comments the desired application under path ./Application/apps/overlays/dev-cluster/kustomization.yaml.
        * When FluxCD kustomization renders the charts, it picks the changes and applies it to cluster (deletes if not present)
        * The Application gets deployed via ArgoCD.
    * Step: 4.Run Pipeline Flux Uninstall - cleanup
        * This will helm uninstall the FluxCD
        * Delete the Flux resources.

### 🚀 GitOps & Observability

* **Prometheus Instrumentation:** Developed a Python file-monitoring application using the **Prometheus client library** to expose custom application metrics on /metrics via port 8000.
* **Containerization & Helm Packaging:** Dockerized the core application and packaged it into a customizable **Helm chart** complete with ConfigMaps, liveness/readiness probes, Horizontal Pod Autoscalers (HPA), and strict CPU/memory resource limits.
* **Observability Stack Integration:** Deployed the **kube-prometheus-stack** in-cluster and configured automated metric scraping from the application instances utilizing a targeted Kubernetes **PodMonitor** custom resource.
* **Alerting as Code:** Coded proactive alerting thresholds directly into the infrastructure repository using Prometheus operator **PrometheusRule** CRDs.
* **GitOps Automation:** Automated the entire end-to-end infrastructure and application deployment lifecycle with **ArgoCD** and **FluxCD**, For ArgoCD  **app-of-apps** architectural pattern alongside **Kustomize-based** environment overlays for development is used and for FluxCD Helmrelease and architectural pattern alongside **Kustomize-based** environment overlays for developments is used.

