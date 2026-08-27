# 3-Tier Task App — Your DevOps Practice Ground

A deliberately simple app so you can focus on the **DevOps process**, not the app logic.

```
Browser → [Frontend: Nginx, static HTML/JS] → [Backend: Flask API] → [DB: Postgres]
              Tier 1                              Tier 2                Tier 3
```

Why this design:
- **Frontend** = pure static files served by Nginx, which also reverse-proxies `/api`
  to the backend. This is the same pattern your ShareTask Ingress/ALB setup uses,
  just simplified to one Nginx container.
- **Backend** = a single Flask file. No frameworks-within-frameworks, so you can
  read the whole thing in 5 minutes and know exactly what each DevOps step is
  actually deploying.
- **Database** = plain Postgres, no ORM — so you can inspect the schema directly
  with `psql` while practicing.

---

## Stage 0 — Run it locally (baseline)

```bash
cd three-tier-app
docker compose up --build
```
Open `http://localhost:8080`. Add a task, refresh, delete it.

**Learn here:** multi-container networking, service discovery by container name
(`DB_HOST=db` works because Compose puts all services on one network and uses
the service name as the DNS hostname), healthchecks (`depends_on: condition:
service_healthy`), and named volumes for persistence.

**Try breaking it on purpose:**
- Remove `depends_on` and watch the backend crash-loop before Postgres is ready
  (this is why `app.py` has a retry loop — that's a real production pattern).
- Delete the `db-data` volume and see your tasks disappear.

---

## Stage 1 — Containerize properly

You already have working Dockerfiles. Practice tasks:
1. Add a `.dockerignore` to each service.
2. Convert the backend Dockerfile to a **multi-stage build** to shrink the image.
3. Run `docker scout quickview` or `trivy image` against both images and fix any
   flagged CVEs — this is a real interview topic (image scanning).
4. Tag and push both images to Docker Hub or ECR:
   ```bash
   docker build -t <you>/three-tier-backend:v1 ./backend
   docker build -t <you>/three-tier-frontend:v1 ./frontend
   docker push <you>/three-tier-backend:v1
   docker push <you>/three-tier-frontend:v1
   ```

---

## Stage 2 — Kubernetes

The `k8s/` folder has manifests for all three tiers. Since you already run
EKS for ShareTask, practice this on **Minikube or Kind** first — cheaper and
faster to iterate.

```bash
kind create cluster --name practice
# edit k8s/backend.yaml and k8s/frontend.yaml with your pushed image tags
kubectl apply -f k8s/
kubectl get pods -w
kubectl port-forward svc/frontend 8080:80
```

**Concepts to deliberately practice:**
- Secrets vs ConfigMaps (the DB creds are in a Secret — inspect it with
  `kubectl get secret db-secret -o yaml` and decode the base64).
- Readiness vs liveness probes — kill the backend's `/health` route on purpose
  and watch Kubernetes restart the pod.
- Scaling: `kubectl scale deployment backend --replicas=4`.
- Swap the DB's `emptyDir` for a real `PersistentVolumeClaim` (data currently
  disappears if the Postgres pod restarts — fix that yourself as an exercise).
- `kubectl logs`, `kubectl describe pod`, `kubectl exec -it <pod> -- sh` for
  troubleshooting — the hands-on style you already prefer.

---

## Stage 3 — CI/CD

Since your ShareTask pipeline is Jenkins-based, do this one in **GitHub Actions**
instead so you get exposure to both. Rough pipeline:

1. On push to `main`: build both Docker images.
2. Push images to Docker Hub/ECR, tagged with the Git SHA.
3. Update the image tag in `k8s/backend.yaml` / `k8s/frontend.yaml`
   (`sed` or `yq`), commit, and let ArgoCD/kubectl apply pick it up —
   or just `kubectl apply` directly from the pipeline for now.

This gives you a second CI/CD tool under your belt without touching your
main portfolio project.

---

## Stage 4 — Infrastructure as Code

Write a small Terraform module that provisions just what this app needs:
a VPC (or reuse a default one), an EKS node group or a single EC2 instance
running Docker Compose for a cheaper option, and an ECR repo per image.
Keep it much smaller than your ShareTask Terraform — the goal here is
repetition of the core resource blocks until they're muscle memory.

---

## Stage 5 — Observability

Point your existing Prometheus/Grafana stack at this app:
- Add a `/metrics` endpoint to the Flask backend using `prometheus_flask_exporter`.
- Scrape it, build a Grafana panel for request rate and latency.
- Trigger an alert by hammering the API with `hey` or `ab` (Apache Bench).

---

## Suggested order for you specifically

Given where your notes say you are (strong on Docker networking and
Prometheus theory, GitOps/Argo CD still unstarted): do **Stage 2 on Kind**
first, then loop back and use this same app as your Argo CD hands-on project —
it's small enough that a broken sync is easy to diagnose.
