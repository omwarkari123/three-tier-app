# Three-Tier App DevOps Guide

This guide explains, step by step, how to run, automate, deploy, monitor, and scale this project using real DevOps tools.

This project already fits a modern DevOps workflow because it contains:
- Frontend static app served by Nginx
- Flask backend API
- PostgreSQL database
- Docker-based local setup
- Kubernetes manifests
- GitHub Actions workflow

The final goal is to take this app from local development to:
- a real hosted server
- Docker automation
- domain + HTTPS
- monitoring
- cloud deployment
- security
- infrastructure as code

---

## 1. Project Architecture

This app follows a standard three-tier setup:

Browser -> Nginx Frontend -> Flask Backend -> PostgreSQL Database

### Components
- Frontend: static HTML, CSS, JS served by Nginx
- Backend: Flask API in [backend/app.py](backend/app.py)
- Database: PostgreSQL container from [docker-compose.yml](docker-compose.yml)
- Kubernetes manifests: [k8s](k8s)
- CI workflow: [.github/workflows/ci.yml](.github/workflows/ci.yml)

This is a perfect project for learning real DevOps because it has all key concerns:
- networking
- containerization
- service discovery
- environment variables
- health checks
- deployment automation
- monitoring
- cloud infrastructure

---

## 2. What DevOps Tools You Should Use

### Core tools
- Git + GitHub
- Docker
- Docker Compose
- Linux server administration
- Nginx
- GitHub Actions
- AWS services
- PostgreSQL
- Monitoring tools
- Terraform
- Kubernetes

### Tool categories
1. Source control and automation
   - GitHub
   - GitHub Actions
2. Containerization
   - Docker
   - Docker Compose
3. Deployment
   - Linux server
   - Nginx
   - SSL with Let’s Encrypt
4. Cloud
   - EC2, ECR, VPC, IAM, Route53, RDS, CloudWatch
5. Monitoring
   - Prometheus
   - Grafana
   - Alertmanager
6. Security
   - Trivy
   - Snyk
   - GitHub Dependabot
   - Secrets Manager
7. Infrastructure as Code
   - Terraform
8. Cloud-native orchestration
   - Kubernetes
   - Helm
   - ArgoCD

---

## 3. Best Deployment Option for This Project

For this app, the most practical production setup is:

- Ubuntu VPS or AWS EC2
- Docker Compose for orchestration
- Nginx reverse proxy
- Let’s Encrypt SSL certificate
- Domain name attached to the server
- GitHub Actions to automate deployment

This is the best choice for learning because it is simple, real, and professional.

### Why this is a good fit
- The app already runs in containers
- The database and backend are simple to manage
- You can test production-like behavior without Kubernetes complexity
- You can attach a domain and HTTPS easily
- You can later move to AWS ECR, Kubernetes, or Terraform

---

## 4. Recommended Production Architecture

```text
User
  |
  v
Domain Name (example.com)
  |
  v
Nginx (reverse proxy + SSL)
  |
  +--> Frontend container
  |
  +--> Backend container
         |
         v
      PostgreSQL container
```

### In a cloud setup
```text
GitHub
  |
  v
GitHub Actions
  |
  v
Build Docker images
  |
  v
Push to ECR or GHCR
  |
  v
Deploy on EC2 or Kubernetes
  |
  v
Backend -> RDS/Postgres
```

---

## 5. Local Development Setup (Start Here)

Before deploying, ensure the app runs locally.

### Run the app locally
```bash
cd three-tier-app
docker compose up --build
```

Then open:
- Frontend: http://localhost:8080
- Backend health: http://localhost:5000/health

### Important concepts to understand
- Compose creates a shared private network for containers
- The backend container uses DB_HOST=db
- The frontend uses Nginx reverse proxy to backend
- database persistence uses a named volume
- health checks ensure DB readiness before backend starts

---

## 6. CI/CD with GitHub Actions

This app is already close to a good CI setup. The workflow should:
- run on push to main
- run on pull request
- validate Python syntax
- install backend dependencies
- build Docker images
- run Docker Compose config
- start containers
- test health endpoints
- stop containers after validation

### Why GitHub Actions is important
It automates the whole validation process and makes your app production-ready.

### CI workflow idea
```yaml
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  workflow_dispatch:

jobs:
  validate-and-build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install backend dependencies
        working-directory: ./backend
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Validate backend syntax
        run: python -m compileall backend

      - name: Validate Docker Compose
        run: docker compose config

      - name: Build backend image
        run: docker build -t three-tier-backend:ci ./backend

      - name: Build frontend image
        run: docker build -t three-tier-frontend:ci ./frontend

      - name: Start containers
        run: docker compose up -d --build

      - name: Health check
        run: |
          for i in {1..30}; do
            if curl -fsS http://localhost:5000/health >/dev/null 2>&1 && curl -fsS http://localhost:8080 >/dev/null 2>&1; then
              echo "Stack healthy"
              exit 0
            fi
            sleep 5
          done
          echo "Stack unhealthy"
          exit 1

      - name: Stop containers
        if: always()
        run: docker compose down -v
```

This is a good GitHub Actions setup for your app.

---

## 7. Production Deployment on a Linux Server

### Best option
Use a VPS such as:
- DigitalOcean
- Hetzner
- AWS EC2
- Linode
- Vultr

### Recommended server
- OS: Ubuntu 22.04 LTS
- RAM: 2 GB or 4 GB
- CPU: 2 vCPU
- Storage: 20 GB+

### Step-by-step server setup

#### Step 1: Create the server
Create a Linux server with Ubuntu.

#### Step 2: Connect via SSH
```bash
ssh ubuntu@your_server_ip
```

#### Step 3: Install Docker
```bash
sudo apt update
sudo apt install -y ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo $VERSION_CODENAME) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo usermod -aG docker $USER
```

Then log out and log in again.

#### Step 4: Clone the repo on the server
```bash
cd /home/ubuntu
git clone https://github.com/your-user/three-tier-app.git
cd three-tier-app
```

#### Step 5: Create environment variables
Create a `.env` file:
```env
DB_HOST=db
DB_NAME=tasksdb
DB_USER=taskuser
DB_PASS=taskpass
```

#### Step 6: Run the app with Docker Compose
```bash
docker compose up -d --build
```

#### Step 7: Check the containers
```bash
docker compose ps
```

#### Step 8: Check backend health
```bash
curl http://localhost:5000/health
```

#### Step 9: Check frontend
```bash
curl http://localhost:8080
```

This proves your app is live on the server.

---

## 8. Domain Name and HTTPS Setup

After deployment, attach a domain.

### Domain steps
At your DNS provider:
- Create an A record for your root domain
- Example: `example.com` -> server IP
- Create a CNAME for `www` -> `example.com`

### Example DNS
- A record: `@` -> `203.0.113.10`
- CNAME: `www` -> `example.com`

### Install Nginx
```bash
sudo apt install nginx -y
```

### Nginx config example
```nginx
server {
    listen 80;
    server_name example.com www.example.com;

    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Test Nginx
```bash
sudo nginx -t
sudo systemctl reload nginx
```

### Install SSL with Certbot
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d example.com -d www.example.com
```

This automatically configures HTTPS and redirect from HTTP to HTTPS.

### Final result
Your app becomes available at:
- https://example.com
- https://www.example.com

---

## 9. GitHub Actions Deployment to Server

This is the automation step you want for real deployment.

### What this workflow does
- pushes code to GitHub
- builds Docker images
- connects to the server via SSH
- pulls latest code or image
- restarts Docker Compose

### Deployment workflow example
```yaml
name: Deploy to VPS

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build backend image
        run: |
          docker build -t ghcr.io/${{ github.repository_owner }}/three-tier-backend:${{ github.sha }} ./backend

      - name: Build frontend image
        run: |
          docker build -t ghcr.io/${{ github.repository_owner }}/three-tier-frontend:${{ github.sha }} ./frontend

      - name: Login to GHCR
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Push images
        run: |
          docker push ghcr.io/${{ github.repository_owner }}/three-tier-backend:${{ github.sha }}
          docker push ghcr.io/${{ github.repository_owner }}/three-tier-frontend:${{ github.sha }}

      - name: Deploy to server
        uses: appleboy/ssh-action@v1.0.3
        with:
          host: ${{ secrets.SERVER_HOST }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          script: |
            cd /home/ubuntu/three-tier-app
            git pull origin main || true
            docker compose pull
            docker compose up -d --remove-orphans
            docker compose ps
```

### GitHub Secrets you need
- SERVER_HOST
- SERVER_USER
- SSH_PRIVATE_KEY

These are essential for secure deployment.

---

## 10. AWS DevOps Path for This App

AWS is a very strong area for improving your DevOps skills.

### AWS services relevant to this app
- EC2: host the app
- ECR: store Docker images
- IAM: manage permissions
- VPC: network isolation
- Security Groups: firewall rules
- RDS: managed PostgreSQL
- Route53: domain names
- ACM: SSL certs
- CloudWatch: metrics and logs
- Secrets Manager: DB passwords

### Best beginner AWS architecture
- EC2 runs Docker Compose
- ECR stores backend and frontend images
- RDS hosts PostgreSQL database
- Route53 points domain to EC2
- ACM provides HTTPS
- CloudWatch monitors logs and metrics

### Example architecture
```text
GitHub Actions -> ECR -> EC2 -> App containers -> RDS Postgres
                      |
                      +-> CloudWatch monitoring
                      |
                      +-> Route53 + ACM for domain
```

This is a realistic professional setup.

---

## 11. Monitoring and Observability

Monitoring is one of the most important DevOps areas.

### Why monitoring matters
Without monitoring, you will not know:
- if the app is down
- if database is failing
- if API latency is high
- if CPU or memory is overloaded
- if bad requests are increasing

### Tools to use
- Prometheus: metrics collection
- Grafana: dashboards
- Alertmanager: alert handling
- Node Exporter: system metrics
- Postgres Exporter: database metrics
- Nginx exporter: frontend metrics
- CloudWatch: AWS metrics

### For this app, monitor
- app uptime
- backend health endpoint
- response times
- CPU usage
- RAM usage
- storage use
- database health
- HTTP error rate

### Useful alerts
- backend down for 2 minutes
- health endpoint failing
- CPU above 80%
- memory above 85%
- database connection errors
- Nginx 5xx errors

### Prometheus + Grafana setup idea
- Prometheus scrapes metrics from backend
- Grafana displays:
  - request count
  - latency
  - CPU
  - memory
  - database health

---

## 12. Logging Strategy

Logs are just as important as metrics.

### Collect logs from
- backend Flask app
- frontend Nginx
- PostgreSQL
- host system

### Good options
- Loki + Grafana
- ELK stack
- OpenSearch
- CloudWatch Logs

### Practical logging flow
```text
Application logs -> Log collector -> Dashboard -> Alerting
```

---

## 13. Security Best Practices

Security is part of DevOps.

### Use these practices
- Never commit secrets to GitHub
- Store secrets in GitHub Actions secrets
- Store production credentials in server `.env` or AWS Secrets Manager
- Use IAM least privilege
- Use Security Groups
- Enable HTTPS for all production traffic
- Run container security scans
- Keep Docker images updated

### Tools for security
- Trivy
- Snyk
- Dependabot
- AWS IAM
- Secrets Manager

### Example security scan
```bash
trivy image your-backend-image
trivy image your-frontend-image
```

This finds vulnerabilities before deploy.

---

## 14. Infrastructure as Code with Terraform

Terraform helps automate cloud infrastructure.

### Good use cases for this project
- Create EC2 instance
- Create VPC and subnets
- Create security groups
- Create ECR repositories
- Create IAM policies
- Create Route53 records
- Create RDS database

### Why Terraform matters
It helps you manage infrastructure in a repeatable, version-controlled way.

### Example Terraform resources
- `aws_instance`
- `aws_security_group`
- `aws_ecr_repository`
- `aws_db_instance`
- `aws_route53_record`
- `aws_vpc`

Terraform is a must-have skill for modern DevOps.

---

## 15. Kubernetes Path for This App

Your repo already includes Kubernetes manifests in [k8s](k8s). This is excellent for a DevOps portfolio.

### Why Kubernetes is useful
It teaches:
- deployment management
- scaling
- service discovery
- rolling upgrades
- readiness and liveness probes
- secrets and config maps

### Kubernetes concepts to practice
- Deployment
- Service
- ConfigMap
- Secret
- Ingress
- Pod autoscaling
- Liveness probe
- Readiness probe

### Example deployment topics
- Deploy backend and database separately
- Use secret for database credentials
- Expose frontend using a Service or Ingress
- Add health checks
- Scale backend with HPA

### Best progression
- Learn Docker Compose first
- Learn Kubernetes second
- Then use EKS or local Kubernetes like Kind or Minikube

---

## 16. Recommended Learning Order

If your goal is to learn DevOps properly, follow this order:

### Stage 1: Foundation
- Git
- GitHub
- Linux basics
- Docker
- Docker Compose

### Stage 2: Automation
- GitHub Actions
- Nginx
- SSL/TLS
- Hosting a simple server

### Stage 3: Cloud
- EC2
- ECR
- IAM
- Route53
- Domain setup

### Stage 4: Monitoring
- Prometheus
- Grafana
- Alertmanager
- Logs

### Stage 5: Infrastructure as Code
- Terraform

### Stage 6: Advanced DevOps
- Kubernetes
- Helm
- ArgoCD
- GitOps

This is the most realistic and effective order.

---

## 17. Best Practical Final Setup for This Project

If you want a strong, production-like setup for this application, do this:

### Option A: Best for learning and portfolio
- GitHub repo
- GitHub Actions CI/CD
- Ubuntu VPS
- Docker Compose
- Nginx reverse proxy
- Let’s Encrypt SSL
- custom domain
- Prometheus + Grafana
- AWS ECR later

### Option B: Best for cloud-native practice
- GitHub Actions
- ECR
- EC2 or EKS
- RDS Postgres
- Route53 and ACM
- Terraform
- Kubernetes
- monitoring

### My recommendation
Start with Option A, then move to Option B.

That sequence is practical and keeps the project manageable.

---

## 18. Common Mistakes to Avoid

- Hardcoding secrets in the app
- Missing health checks
- Not using environment variables
- Forgetting to expose backend correctly
- Not setting up SSL
- Not securing the server
- Not creating backups of database data
- Using too many tools before mastering basics
- Trying to jump into Kubernetes before Docker and Compose are understood

---

## 19. Final Roadmap for You

### Month 1
- Learn Git, GitHub, Linux
- Run Docker Compose locally
- Build CI pipeline
- Deploy to VPS

### Month 2
- Add Nginx, SSL, domain
- Add monitoring with Prometheus/Grafana
- Add AWS EC2 and ECR

### Month 3
- Add Terraform
- Add AWS RDS and Secrets Manager
- Prepare GitOps/Kubernetes practice

This gives you a real DevOps progression, not just random tool learning.

---

## 20. What to Do Next

### Immediate next steps
1. Deploy the app locally with Docker Compose
2. Build a proper GitHub Actions CI pipeline
3. Deploy to a Linux VPS
4. Point a domain to the server
5. Set up Nginx + SSL
6. Add monitoring
7. Learn AWS basics
8. Add Terraform
9. Move to Kubernetes later

---

## 21. Summary

This app is a very good DevOps project because it contains everything you need to learn:
- containerization
- networking
- deployment automation
- infrastructure
- monitoring
- cloud practices
- security
- scalability

If you follow the order above, you will build strong real-world DevOps skills.

For this project, the best beginner-to-professional path is:

GitHub + Docker + Nginx + VPS + Domain + SSL + GitHub Actions + Monitoring + AWS + Terraform + Kubernetes

That is the complete DevOps journey for your app.

---

## 22. Project Files You Should Use as Reference

- [docker-compose.yml](docker-compose.yml)
- [backend/app.py](backend/app.py)
- [backend/Dockerfile](backend/Dockerfile)
- [frontend/nginx.conf](frontend/nginx.conf)
- [frontend/Dockerfile](frontend/Dockerfile)
- [.github/workflows/ci.yml](.github/workflows/ci.yml)
- [k8s](k8s)

This guide is your practical DevOps roadmap for this application.
