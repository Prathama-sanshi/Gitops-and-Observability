# 🚀 Introduction:

This repository demonstrates a comprehensive GitOps-driven Kubernetes deployment platform running on WSL (Windows Subsystem for Linux). It includes:

* **Custom Application Deployment:** A Prometheus-instrumented application, fully integrated with Fluent Bit for log shipping, is deployed via  GitOps (ArgoCD and FluxCD).
 * **Production-Grade Observability Stack:** Automated deployment of Prometheus, Alertmanager, Grafana, and related monitoring resources, along with an ElasticSearch and Kibana logging and visualization stack. Alerting rules and dashboards are managed as code using PrometheusRule CRs for alert management and Grafana dashboard for visualization, ensuring all observability configurations are version-controlled, reproducible, and auditable.
* **Automated Infrastructure Management:** GitOps workflows powered by both ArgoCD and FluxCD (see respective branches), enabling declarative, version-controlled cluster and application lifecycle management.
* **CI/CD Integration:** Utilizes GitHub Actions with self-hosted runners to facilitate automated builds, testing, and continuous delivery.
* **Best Practices:** Implements modern GitOps methodologies for repeatable, auditable, and scalable infrastructure and application delivery.

### 🎯Purpose  
- This project provides a reference implementation for building and operating GitOps-driven Kubernetes platforms with integrated observability, leveraging industry-standard tools for automated deployments, monitoring, logging, and lifecycle management.
- It places a strong emphasis on observability by design: the custom application is built to explicitly control what is exposed through the `/metrics` endpoint and forwarded to the observability stack. Metrics are collected through targeted PodMonitor custom resources (CRs), while logs are processed by a Fluent Bit sidecar with custom parser logic before being shipped to Elasticsearch. This approach provides greater control and security compared to traditional scrape-based configurations, where broader system or pod-level telemetry may be collected indiscriminately.
-  It demonstrates recommended repository structures, deployment patterns, observability integration, CI/CD automation, and GitOps best practices, enabling users to adopt, learn, or extend production-aligned GitOps architectures in their own environments.
- It showcases GitOps implementations using both ArgoCD and FluxCD, leveraging Helm charts and Kustomize base/overlay patterns to enable reusable, environment-specific, and scalable application deployments.
  
### 🏗️ Architecture Highlights

- GitOps Controllers: ArgoCD and FluxCD
- Package Management: Helm Charts
- Configuration Management : Kustomize (Base/Overlay)
- Monitoring: Prometheus, Alertmanager, Grafana
- Logging: Fluent Bit, Elasticsearch, Kibana [EFK stack]
- CI/CD: GitHub Actions with Self-Hosted Runner
- Kubernetes Platform: Minikube on WSL

### 🚀 Design Discussion.
1] Controlled Observability :
```text
Prometheus
    ↓
PodMonitor [Application PodMonitor - pod label based]
    ↓
Pod Labels
    ↓
file-monitor pod [Custom APP]
```
* Why not use serviceMonitor?
The Service Monitor are used for Maximum scalability, but currently our focus is on controlled observability. Even in case of ServiceMonitor , it essentially scrapes same Metrics as that of PodMonitor, but it makes easy for large number of workloads which make it ideal for production use case.

2] Controlled Logging: 
```text
File-Monitor [Custom Application]
│
├── Application Container
│      │
│      └── Application Logs [/app/logs - shared volume]
│
└── Fluent Bit Sidecar [/app/logs - shared volume]
       │
       ├── Custom Parser
       ├── Log Filtering
       └── Elasticsearch
                │
                ▼
             Kibana
```
* Why FluentBit sidecar and not Daemonset?

- The design goal of this project was controlled application-specific log processing, rather than cluster-wide log collection. For that reason, I intentionally chose the Fluent Bit sidecar pattern instead of a DaemonSet-based deployment.
- In a DaemonSet architecture, Fluent Bit runs once per node and collects logs from all containers on that node. While this approach is resource-efficient and commonly used in production environments, it was not aligned with the observability objectives of this project.
- With the sidecar approach, each application pod contains a dedicated Fluent Bit container that processes only that application's logs. The sidecar uses custom parser configurations, provided through a ConfigMap, to parse, enrich, and forward application-specific logs to Elasticsearch. This gives the application explicit control over what log data is collected and how it is processed before being shipped to the logging backend.
- The primary tradeoff of this design is resource consumption at scale. For example, if a node hosts 10 application pods, the sidecar model results in 10 Fluent Bit containers running on that node. In contrast, a DaemonSet-based deployment would require only a single Fluent Bit instance per node, making it significantly more resource-efficient and easier to manage in large-scale environments.

## Architecture Diagram
```text
┌──────────────────────────────────────────────────────────────┐
│                     GitHub Repository                        │
│   (Helm Charts, Kustomize Overlays, GitOps Manifests)        │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│                   GitHub Actions Pipeline                    │
│                 (Self-Hosted Runner on WSL)                  │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│                     Minikube Kubernetes                      │
│                        Cluster (WSL)                         │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Namespace: flux-system                                 │  │
│  │--------------------------------------------------------│  │
│  │ FluxCD Controllers                                     │  │
│  │ GitRepository CR                                       │  │
│  │ Kustomization CR                                       │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Namespace: argocd (Optional)                           │  │
│  │--------------------------------------------------------│  │
│  │ ArgoCD Server                                          │  │
│  │ Application Controller                                 │  │
│  │ AppProject CR                                          │  │
│  │ Application CR  (App of Apps)                          │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Namespace: observability                               │  │
│  │--------------------------------------------------------│  │
│  │ kube-prometheus-stack                                  │  │
│  │ • Prometheus                                           │  │
│  │ • Alertmanager                                         │  │
│  │ • Grafana                                              │  │
│  │ • PrometheusRule CRs                                   │  │                                                   
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Namespace: logging                                     │  │
│  │--------------------------------------------------------│  │
│  │ Elasticsearch                                          │  │
│  │ Kibana                                                 │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Namespace: dev                                         │  │
│  │--------------------------------------------------------│  │
│  │ File-Monitor Application                               │  │
│  │ Fluent Bit Sidecar (Controlled Logging)                │  │
│  │ PodMonitor CRs  (Controlled Monitoring)                │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
└──────────────────────────────────────────────────────────────┘
                              │
            ┌─────────────────┴─────────────────┐
            │                                   │
            ▼                                   ▼
┌──────────────────────┐          ┌─────────────────────────┐
│ Prometheus           │          │ Fluent Bit Sidecar      │
│  - (PodMonitor-based)│          │ Custom Parser Logic     |
|  -  Alerts           │          | embedded in ConfigMap   |
└──────────┬───────────┘          └─────────────┬───────────┘
           │                                    │
           ▼                                    ▼
┌──────────────────────┐          ┌─────────────────────────┐
│ Grafana Dashboards   │          │ Elasticsearch           │
|                      │          └─────────────┬───────────┘
└──────────────────────┘                        │
                                                ▼
                                       ┌───────────────────┐
                                       │ Kibana Dashboards │
                                       └───────────────────┘

```

### 🚀 Prerequisites
* WSL version: 2.7.13.0 or higher
* Docker version: 29.3.0 or higher
* Minikube version: v1.38.0  or higher
* FluxCD CLI version: 2.9.5 or higher (Helm chart: 2.19.0)
* ArgoCD CLI version: v3.5.1+109ca7c (Helm chart:  10.3.3)

## 🚀 Infrastructure Setup

We will deploy the custom application, observability stack, and Elasticsearch-Kibana stack through GitOps controllers (ArgoCD and FluxCD) in a local WSL environment.
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
Whenever you run a GitHub Actions workflow, start the self-hosted runner on your local WSL environment using the following command:
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
        * It uncomments out entry of desired application(pipeline inputs) under path ./Application/apps/overlays/dev-cluster/kustomization.yaml.
        * When FluxCD reconciles the Kustomization, it processes the referenced HelmRelease resources and deploys the application to the Kubernetes cluster.
        * The application is then automatically deployed and managed by FluxCD.
    * Step: 3.Run Pipeline FluxCD Gitops Undeployment
        * This will clone the flucd-obs repo
        * And comments out entry of desired application under path ./Application/apps/overlays/dev-cluster/kustomization.yaml.
        * When FluxCD reconciles the Kustomization resource, it detects the repository change and applies the updated desired state to the cluster.
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

5] self-hosted runner logs:
<img width="1038" height="485" alt="image" src="https://github.com/user-attachments/assets/e921a683-e5a5-4346-80b1-9d40643ea9ef" />


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
        * It uncomments out entry of desired application(pipeline inputs) under path ./Application/apps/overlays/dev-cluster/kustomization.yaml.
        * When ArgoCD synchronizes the Application resource, it renders the Kustomize manifests and applies the desired state to the cluster.
        * The application is then automatically deployed and managed by ArgoCD.
    * Step: 3.Run Pipeline ArgoCD Gitops Undeployment
        * This will clone the argocd-obs repo
        * And comments out entry of desired application under path ./Application/apps/overlays/dev-cluster/kustomization.yaml.
        * When ArgoCD synchronizes the Application resource, it renders the Kustomize manifests and applies the updated desired state to the cluster.
        * During the next synchronization cycle, argocd detects the change and updates the cluster state accordingly.
        * Resources that are no longer referenced are removed from the cluster.
        * The application is successfully undeployed by argocd.
    * Step: 4.Run Pipeline Argocd Uninstall - cleanup
        * This will helm uninstall the ArgoCD
        * Delete the ArgoCD Custom Resources and related configurations.
        * Cleans up all argocd-managed resources to restore the cluster to its pre-installation state.
### Result After Deployment :

1] CLI status:

<img width="629" height="122" alt="image" src="https://github.com/user-attachments/assets/4a62a76c-a876-4f4f-ba3d-3ccc57e18e71" />

2] UI status:

<img width="1864" height="533" alt="image" src="https://github.com/user-attachments/assets/b61e864f-8bd9-4c61-829c-3dbd1425039c" />

        
3] Parent APP :

<img width="697" height="486" alt="image" src="https://github.com/user-attachments/assets/8c5c075f-61ae-4cb5-9600-576c1b1b598b" />


4] File monitor

<img width="1401" height="330" alt="image" src="https://github.com/user-attachments/assets/a76eea0d-1362-4402-a0e3-6499c643b54e" />

5] ElasticSearch and Kibana:

<img width="1399" height="423" alt="image" src="https://github.com/user-attachments/assets/99fdc7ba-9514-444f-80d3-b335f8973c68" />

# Observability Dashboards
* Grafana Dashboard:
<img width="1586" height="818" alt="image" src="https://github.com/user-attachments/assets/4ba9fa75-efc1-4e3d-b187-d927dc4b433f" />
* Prometheus Alerts:
<img width="1597" height="644" alt="image" src="https://github.com/user-attachments/assets/91aa1dcc-71ae-44dd-86d4-906a7d124219" />
* Prometheus Targets:
<img width="1593" height="357" alt="image" src="https://github.com/user-attachments/assets/c44f87dd-46b4-4ea8-9bbd-01bc9d6fe349" />

# Kibana Dashboards

<img width="1866" height="638" alt="image" src="https://github.com/user-attachments/assets/08bdcd5d-d7a6-4c05-9856-7376049d83b5" />

