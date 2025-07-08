 🚀 Automated EC2 Deployment with GitHub Actions, Terraform, Docker, Prometheus & Grafana

This project demonstrates a **complete DevOps pipeline**:

✅ Automatically create AWS EC2 infrastructure with Terraform  
✅ Build and deploy a Dockerized Nginx app  
✅ Use GitHub Actions for CI/CD  
✅ Monitor with Prometheus & Grafana  

---url

## 📂 Folder Structure

```

.
├── .github
│   └── workflows
│       └── deploy.yaml           # GitHub Actions workflow
├── app
│   ├── Dockerfile                # Docker image for Nginx
│   └── html
│       └── index.html            # Web page content
├── infra
│   ├── main.tf                   # Terraform EC2 config
│   ├── outputs.tf
│   ├── provider.tf
│   ├── terraform.tfvars          # Variables (key pair, region)
│   ├── userdata.sh               # User data script (install Docker)
│   └── variables.tf
├── monitoring
│   ├── docker-compose.yml        # Prometheus + Grafana
│   └── prometheus.yml            # Prometheus scrape config
└── README.md

````

---

## ⚙️ Prerequisites

✅ AWS Account  
✅ EC2 key pair (`.pem`) created in AWS  
✅ Docker Hub account (username & access token)  
✅ Terraform installed locally  
✅ Git installed  

---

## 🛠️ Setup Steps

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/cloudwifi/my-new-project-for-GithubActionn.git
cd my-new-project-for-GithubActionn
````

---

### 2️⃣ Configure Terraform Variables

Edit `infra/terraform.tfvars`:

```hcl
aws_region    = "ap-south-1"
instance_type = "t2.micro"
key_name      = "your-key-pair-name"
```

> ℹ️ **IMPORTANT:**
> Replace `your-key-pair-name` with the actual name of your AWS key pair.

---

### 3️⃣ Initialize Terraform

```bash
cd infra
terraform init
```

---

### 4️⃣ Apply Terraform

```bash
terraform apply
```

✅ This will:

* Provision an EC2 instance
* Install Docker
* Start Prometheus and Grafana containers

---

### 5️⃣ Configure GitHub Secrets

In **Settings > Secrets and variables > Actions**, add:

| Name              | Description                        |
| ----------------- | ---------------------------------- |
| `DOCKER_USERNAME` | Your Docker Hub username           |
| `DOCKER_PASSWORD` | Your Docker Hub token or password  |
| `EC2_HOST`        | EC2 Public IP (e.g., `ec2-...`)    |
| `EC2_USER`        | `ubuntu`                           |
| `EC2_SSH_KEY`     | Private key content of `.pem` file |

✅ **Tip:**
To get the `.pem` content, open in Notepad and copy everything.

---

### 6️⃣ Deploy with GitHub Actions

Whenever you **push to `main`**, the workflow will:

* Build the Docker image
* Push to Docker Hub
* SSH into EC2 and run the container

✅ To trigger manually:

```bash
git add .
git commit -m "Trigger deployment"
git push
```

---

## 🌐 Access the Application

* **App URL:**

  ```
  http://<EC2-Public-IP>
  ```

* **Grafana:**

  ```
  http://<EC2-Public-IP>:3000
  ```

  Default credentials: `admin` / `admin` (you’ll be prompted to change)

---

## 📊 Monitoring with Grafana

**Prometheus collects:**

* Docker container metrics
* (Optional) Node metrics if you add Node Exporter

**Grafana visualizes:**

* CPU, Memory, Disk
* Container health

✅ To import a Docker monitoring dashboard:

1. Log in to Grafana
2. Click ➕ **Create > Import**
3. Use **Dashboard ID `893`**

---

## 💡 Next Steps & Enhancements

* Install Node Exporter for EC2 system metrics
* Add Blackbox Exporter for HTTP health checks
* Create Grafana alerts (email or Slack)
* Automate domain names & HTTPS with Certbot

---

## 🙏 Acknowledgments

* [Terraform](https://www.terraform.io/)
* [Docker](https://www.docker.com/)
* [GitHub Actions](https://docs.github.com/actions)
* [Prometheus](https://prometheus.io/)
* [Grafana](https://grafana.com/)

---

## 📝 License

MIT

````

---

✅ **How to use this:**
1. **Copy everything above**
2. Create or overwrite `README.md` in your project root
3. Commit and push:

```bash
git add README.md
git commit -m "Add project README"
git push
````

---
📈 Extended Monitoring (Logs + Metrics)
This project includes advanced monitoring capabilities using Prometheus, Grafana, Loki, Promtail, and Node Exporter.

🔧 Use Loki + Promtail + Grafana
This is the recommended stack for log monitoring:

Component	Purpose
Loki	Stores logs (like Prometheus for logs)
Promtail	Collects logs from your app/host
Grafana	Visualizes logs (via Loki)

🛠️ Step-by-Step Setup
1. 🐳 Install Loki and Promtail Using Docker Compose

Inside your monitoring/ folder, update your docker-compose.yml:

version: '3'

services:
  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    volumes:
      - grafana-storage:/var/lib/grafana

  loki:
    image: grafana/loki:2.9.4
    ports:
      - "3100:3100"
    command: -config.file=/etc/loki/local-config.yaml

  promtail:
    image: grafana/promtail:2.9.4
    volumes:
      - /var/log:/var/log
      - ./promtail-config.yaml:/etc/promtail/config.yaml
    command: -config.file=/etc/promtail/config.yaml

volumes:
  grafana-storage:
  
2.Create promtail-config.yaml in monitoring/ folder:

server:
  http_listen_port: 9080
  grpc_listen_port: 0

positions:
  filename: /tmp/positions.yaml

clients:
  - url: http://loki:3100/loki/api/v1/push

scrape_configs:
  - job_name: system
    static_configs:
      - targets:
          - localhost
        labels:
          job: varlogs
          __path__: /var/log/*.log
This collects logs like /var/log/syslog, /var/log/docker.log, etc.

3. 🚀 Start All Services
Run from inside your monitoring/ folder:

bash
Copy
Edit
docker-compose up -d

4. 📊 Connect Loki to Grafana
Visit Grafana: http://<EC2_PUBLIC_IP>:3000

Go to Settings → Data Sources → Add data source

Choose Loki

Set the URL to: http://loki:3100

Click Save & Test


📝 To Monitor App Logs
If you want to monitor logs specifically from your Dockerized app, update the Promtail config to:

yaml
Copy
Edit
scrape_configs:
  - job_name: myapp
    static_configs:
      - targets:
          - localhost
        labels:
          job: myapp
          __path__: /var/lib/docker/containers/*/*.log

✅ Metrics Monitoring (System & Containers)
Prometheus scrapes metrics from:

Docker containers

The EC2 host via Node Exporter

Grafana visualizes these metrics using dashboards

📌 To view system-level metrics:

Access Grafana: http://<EC2-Public-IP>:3000

Login with default credentials (admin / admin)

Go to ➕ Create > Import

Use Dashboard ID 1860 for Node Exporter / Linux host overview

✅ Logs Monitoring with Loki + Promtail + Grafana
Logs are captured in real-time from your EC2 instance:

Promtail collects logs from /var/log/ and Docker containers

Loki stores and indexes these logs

Grafana queries and visualizes logs via the Loki data source

📌 To explore logs:

Go to Grafana → Explore

Select Loki as data source

Query:

arduino
Copy
Edit
{job="varlogs"}
Or:

arduino
Copy
Edit
{job="myapp"}
You’ll see logs from system files or your Dockerized app instantly!

🧩 Services Running on EC2
Service	Port	Description
Nginx App	80	Your deployed app
Prometheus	9090	Metrics monitoring
Grafana	3000	Dashboards for metrics/logs
Loki	3100	Log aggregation
Node Exporter	9100	EC2 system metrics

