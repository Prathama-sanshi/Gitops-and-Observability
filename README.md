### 🚀 GitOps & Observability

* **Prometheus Instrumentation:** Developed a Python file-monitoring application using the **Prometheus client library** to expose custom application metrics on /metrics via port 8000.
* **Containerization & Helm Packaging:** Dockerized the core application and packaged it into a customizable **Helm chart** complete with ConfigMaps, liveness/readiness probes, Horizontal Pod Autoscalers (HPA), and strict CPU/memory resource limits.
* **Observability Stack Integration:** Deployed the **kube-prometheus-stack** in-cluster and configured automated metric scraping from the application instances utilizing a targeted Kubernetes **PodMonitor** custom resource.
* **Alerting as Code:** Coded proactive alerting thresholds directly into the infrastructure repository using Prometheus operator **PrometheusRule** CRDs.
* **GitOps Automation:** Automated the entire end-to-end infrastructure and application deployment lifecycle with **ArgoCD**, leveraging the **app-of-apps** architectural pattern alongside **Kustomize-based** environment overlays for development.
