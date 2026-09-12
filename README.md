# Argocd-and-Observability
A sample application that has custom metrics and pushes to kube-prometheus-stack . Deployment is done via Argocd.

ArgoCD Directory Structure

```text
.
├── Application
│   ├── application code
│   │   ├── Dockerfile
│   │   ├── README.md
│   │   ├── file_monitor.py
│   │   └── requirements.txt
│   ├── apps
│   │   ├── base
│   │   │   ├── file-monitor
│   │   │   │   └── versions
│   │   │   │       └── file-monitor-1.0.0
│   │   │   │           ├── kustomization.yaml
│   │   │   │           └── values.yaml
│   │   │   └── kube-prometheus-stack
│   │   │       └── versions
│   │   │           └── kube-prometheus-stack-88.3.0
│   │   │               ├── kustomization.yaml
│   │   │               └── values.yaml
│   │   └── overlays
│   │       ├── dev-cluster
│   │       |    ├── dev-file-monitor
│   │       |    │   ├── dev-app
│   │       |    │   │   ├── dev-values.yaml
│   │       |    │   │   └── kustomization.yaml
│   │       |    │   ├── dev-resources
│   │       |    │   │   ├── dev-app-podmonitor.yaml
│   │       |    │   │   └── kustomization.yaml
│   │       |    │   └── kustomization.yaml
│   │       |    ├── dev-kube-prometheus-stack
│   │       |    │   ├── dev-kube-prometheus-stack
│   │       |    │   │   ├── kustomization.yaml
│   │       |    │   │   └── values-dev.yaml
│   │       |    │   ├── dev-kube-prometheus-stack-resources
│   │       |    │   │   ├── dashboard-1786864897559.json
│   │       |    │   │   ├── kustomization.yaml
│   │       |    │   │   ├── log_file_count_alert.yaml
│   │       |    │   │   └── txt_file_count_alert.yaml
│   │       |    │   └── kustomization.yaml
│   │       |    └── kustomization.yaml
|   |       └── prod-cluster/.. #same structure as  dev-cluster # kept for extensibility (multi environment/cluster)
│   └── helm-charts
│       ├── file-monitor-charts
│       │   └── file-monitor-0.1.0
│       │       ├── Chart.yaml
│       │       ├── templates
│       │       └── values.yaml
│       └── kube-prometheus-stack  
│           ├── Chart.lock
│           ├── Chart.yaml
│           ├── README.md
│           ├── charts
│           ├── templates
│           └── values.yaml
├── README.md
└── argocd
    ├── helm-charts
    │   ├── Chart.lock
    │   ├── Chart.yaml
    │   ├── README.md
    │   ├── charts
    │   ├── templates
    │   └── values.yaml
    └── resources
        ├── app-project.yaml
        ├── argocd-application.yaml
        └── argocd-repo-secret.yaml

```
