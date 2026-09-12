### 🚀 FluxCD & Observability

A sample application that has custom metrics and pushes to kube-prometheus-stack . Deployment is done via FluxCD. 

Directory Structure:


# Directory Structure of Application deployment via FluxCD:

```text
fluxcd-obs/
├── Application/    
│   ├── application code/   
│   │   ├── Dockerfile
│   │   ├── README.md       <- Read about application
│   │   ├── file_monitor.py
│   │   └── requirements.txt
│   ├── apps/                        <- Kustomize base and overlay pattern
│   │   ├── base/                    
│   │   │   ├── file-monitor/                  # App-1: file-monitor (base configuration for all environments)
│   │   │   │   └── versions/
│   │   │   │       └── file-monitor-1.0.0/   # If new version is launched, add new folder and point site here.
│   │   │   │           ├── kustomization.yaml
│   │   │   │           └── values.yaml        <- references the file-monitor helm chart path, kustomization handles rendering.
│   │   │   └── kube-prometheus-stack/         # App-2: kube-prometheus-stack (base configuration for all environments)
│   │   │       └── versions/                
│   │   │           └── kube-prometheus-stack-88.3.0/
│   │   │               ├── kustomization.yaml
│   │   │               └── values.yaml
│   │   └── overlays/                         # Multi-environment (dev and prod)
│   │       └── dev-cluster/                     -> DEV env
│   │           ├── dev-file-monitor/                      -> APP 1: file monitor in dev environment 
│   │           │   ├── dev-app/
│   │           │   │   ├── dev-values.yaml                -> Dev-only values
│   │           │   │   └── kustomization.yaml
│   │           │   └── dev-resources/                     -> App 1 k8s resources
│   │           │       ├── dev-app-podmonitor.yaml
│   │           │       └── kustomization.yaml
│   │           ├── dev-kube-prometheus-stack/             -> APP 2:  dev-kube-prometheus-stack in dev environment 
│   │           │   ├── dev-kube-prometheus-stack/
│   │           │   │   ├── kustomization.yaml
│   │           │   │   └── values-dev.yaml                -> Dev-only values
│   │           │   └── dev-kube-prometheus-stack-resources/ -> App 2 k8s resources
│   │           │       ├── dashboard-1786864897559.json
│   │           │       ├── kustomization.yaml
│   │           │       ├── log_file_count_alert.yaml
│   │           │       └── txt_file_count_alert.yaml
│   │           └── kustomization.yaml
│   └── helm-charts/                                -> Helm charts for file-monitor (app 1) and kube-prometheus-stack (app 2)
│       ├── file-monitor-charts/
│       │   └── file-monitor-0.1.0/
│       │       ├── .helmignore
│       │       ├── Chart.yaml
│       │       ├── values.yaml
│       │       └── templates/
│       │           ├── NOTES.txt
│       │           ├── _helpers.tpl
│       │           ├── configmap.yaml
│       │           ├── deployment.yaml
│       │           ├── hpa.yaml
│       │           ├── httproute.yaml
│       │           ├── ingress.yaml
│       │           ├── service.yaml
│       │           ├── serviceaccount.yaml
│       │           └── tests/
│       │               └── test-connection.yaml
│       └── kube-prometheus-stack/
│           ├── .helmignore
│           ├── Chart.lock
│           ├── Chart.yaml
│           ├── README.md
│           └── charts/
│               └── crds/
│                   ├── Chart.yaml
│                   ├── README.md
│                   ├── crds/
│                   ├── files/
│                   └── templates/
├── FluxCD/                                 <- FluxCD-related deployment and resource files
│   ├── Helm-chart/                         <- Helm charts for deploying FluxCD controllers
│   │   └── flux2/                          <- Main Helm chart for FluxCD GitOps controller
│   │       ├── Chart.yaml
│   │       ├── values.yaml
│   │       └── (other FluxCD helm chart files)
│   └── Resources/                          <- FluxCD resources
│       ├── GitRepository.yaml              <- Defines a FluxCD GitRepository resource
│       └── kustomization.yaml              <- Kustomize configuration for Flux resources
```
