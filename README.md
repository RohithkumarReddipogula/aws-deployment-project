# AWS EC2 Deployment — RAG System API

Production deployment of a FastAPI inference API on AWS EC2.
Exposes performance results from a Hybrid RAG system achieving
93% Recall@10 on 8.84 million MS MARCO passages.

Live API:      http://3.71.32.203:8000
API Docs:      http://3.71.32.203:8000/docs
Health Check:  http://3.71.32.203:8000/health
System Info:   http://3.71.32.203:8000/info

---

## System Architecture

    Client Request
          |
          v
    Internet Gateway
          |
          v
    AWS Security Group
    (port 22 SSH, port 8000 API)
          |
          v
    EC2 Instance — t3.micro
    eu-central-1 Frankfurt
          |
          v
    Ubuntu 24.04 LTS
          |
          v
    systemd Service Manager
    (auto-restart on failure)
          |
          v
    Python Virtual Environment
          |
          v
    uvicorn ASGI Server
          |
          v
    FastAPI Application
    |           |           |
    v           v           v
   GET /      GET /health  GET /info
   Overview   Monitoring   Performance

---

## Infrastructure Overview

    +--------------------------------------------------+
    |                  AWS Cloud                       |
    |                                                  |
    |  +--------------------------------------------+ |
    |  |         EC2 Instance (t3.micro)            | |
    |  |         eu-central-1 Frankfurt             | |
    |  |                                            | |
    |  |  OS: Ubuntu 24.04 LTS                      | |
    |  |  RAM: 1 GB                                 | |
    |  |  Storage: 20 GB EBS gp3                    | |
    |  |  vCPU: 2                                   | |
    |  |                                            | |
    |  |  +--------------------------------------+  | |
    |  |  |    systemd Service Manager           |  | |
    |  |  |    rag-api.service                   |  | |
    |  |  |    Restart=on-failure                |  | |
    |  |  |    RestartSec=5                      |  | |
    |  |  +--------------------------------------+  | |
    |  |              |                             | |
    |  |              v                             | |
    |  |  +--------------------------------------+  | |
    |  |  |    uvicorn ASGI server               |  | |
    |  |  |    0.0.0.0:8000                      |  | |
    |  |  +--------------------------------------+  | |
    |  |              |                             | |
    |  |              v                             | |
    |  |  +--------------------------------------+  | |
    |  |  |    FastAPI Application               |  | |
    |  |  |    3 REST endpoints                  |  | |
    |  |  |    OpenAPI / Swagger docs            |  | |
    |  |  |    CORS middleware                   |  | |
    |  |  +--------------------------------------+  | |
    |  +--------------------------------------------+ |
    |                                                  |
    |  +--------------------------------------------+ |
    |  |    Security Group (launch-wizard-1)        | |
    |  |    Inbound: TCP 22 (SSH)  0.0.0.0/0       | |
    |  |    Inbound: TCP 8000 (API) 0.0.0.0/0      | |
    |  +--------------------------------------------+ |
    +--------------------------------------------------+

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| / | GET | System overview and key RAG results |
| /health | GET | Uptime, server info, process status |
| /info | GET | Full performance metrics and portfolio |
| /docs | GET | Interactive Swagger UI |
| /openapi.json | GET | OpenAPI schema |

---

## Sample API Responses

Root endpoint — http://3.71.32.203:8000

    {
        "name": "AI-Powered RAG System",
        "author": "Rohith Kumar Reddipogula",
        "deployment": "AWS EC2 t3.micro Frankfurt",
        "results": {
            "recall_at_10": "93.0%",
            "mrr": "1.0",
            "optimal_alpha": 0.70,
            "corpus": "8.84M MS MARCO passages"
        }
    }

Health endpoint — http://3.71.32.203:8000/health

    {
        "status": "healthy",
        "uptime_seconds": 3672.4,
        "uptime_human": "1h 1m",
        "server": {
            "cloud": "AWS EC2",
            "instance": "t3.micro",
            "region": "eu-central-1 Frankfurt"
        },
        "process_manager": "systemd managed"
    }

---

## Deployment Process — Step by Step

Step 1 — Launch EC2 Instance

    Region:    eu-central-1 Frankfurt
    AMI:       Ubuntu Server 24.04 LTS
    Type:      t3.micro (2 vCPU, 1 GB RAM)
    Storage:   20 GB EBS gp3
    Key pair:  RSA .pem format

Step 2 — Security Group Configuration

    Rule 1: SSH   TCP port 22   Source 0.0.0.0/0
    Rule 2: API   TCP port 8000 Source 0.0.0.0/0

Step 3 — Connect via SSH

    ssh -i rohith-key.pem ubuntu@3.71.32.203

Step 4 — Server Setup

    sudo apt update && sudo apt upgrade -y
    sudo apt install python3-pip python3-venv git -y
    git clone https://github.com/RohithkumarReddipogula/AI-Powered-Rag-System.git
    cd AI-Powered-Rag-System
    python3 -m venv venv
    source venv/bin/activate
    pip install --no-cache-dir fastapi uvicorn openai

Step 5 — systemd Service Configuration

    sudo tee /etc/systemd/system/rag-api.service << EOF
    [Unit]
    Description=RAG FastAPI Service
    After=network.target

    [Service]
    User=ubuntu
    WorkingDirectory=/home/ubuntu/AI-Powered-Rag-System
    Environment=PATH=/home/ubuntu/AI-Powered-Rag-System/venv/bin
    ExecStart=/home/ubuntu/AI-Powered-Rag-System/venv/bin/uvicorn simple_api:app --host 0.0.0.0 --port 8000
    Restart=on-failure
    RestartSec=5

    [Install]
    WantedBy=multi-user.target
    EOF

    sudo systemctl daemon-reload
    sudo systemctl enable rag-api
    sudo systemctl start rag-api

Step 6 — Verify Deployment

    sudo systemctl status rag-api
    curl http://localhost:8000/health

---

## Production Operations

Check service status:

    sudo systemctl status rag-api

View live logs:

    sudo journalctl -u rag-api -f

Restart service:

    sudo systemctl restart rag-api

Stop service:

    sudo systemctl stop rag-api

Check resource usage:

    free -h
    df -h
    top

---

## Why systemd Over Manual Process Management

Running uvicorn directly in the terminal stops when the SSH
session closes. systemd solves three production problems:

1. Auto-start on server reboot — service starts automatically
   when the EC2 instance reboots without manual intervention

2. Auto-restart on crash — if the process crashes unexpectedly
   systemd restarts it within 5 seconds (RestartSec=5)

3. Log management — systemd captures all stdout and stderr logs
   accessible via journalctl for debugging and monitoring

---

## What I Learned

Deploying to AWS EC2 exposed the gap between demo deployment
and production deployment.

HuggingFace Spaces abstracts away networking, process management,
and containerisation. On EC2 every layer is configured manually.
This hands-on experience with Linux server administration,
security group rules, and systemd taught me what ML infrastructure
teams deal with daily.

The key production insight: a process that is not managed by
systemd or a supervisor is not production-ready. It will die
the moment the SSH session closes or the server reboots.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Cloud | AWS EC2 |
| OS | Ubuntu 24.04 LTS |
| Process manager | systemd |
| ASGI server | uvicorn |
| API framework | FastAPI |
| Language | Python 3.11 |
| Auth | SSH key pair (RSA) |
| Networking | AWS Security Groups |
| Storage | EBS gp3 20 GB |

---

## Related Projects

| Project | Description | Live |
|---------|-------------|------|
| [Hybrid RAG System](https://github.com/RohithkumarReddipogula/AI-Powered-Rag-System) | BM25 + dense embeddings · 93% Recall@10 · 8.84M passages | [Demo](https://huggingface.co/spaces/ROHITHKUMARREDDIOGULa/Hybrid-RAG-API) · [API](https://rohith2026-hybrid-rag-api.hf.space/docs) |
| [AI Agent System](https://github.com/RohithkumarReddipogula/ai-agent-project) | ReAct agent · LangGraph · 3 tools | [Demo](https://rohith2026-ai-agent-react.hf.space) |
| [LLM Fine-Tuning](https://github.com/RohithkumarReddipogula/llm-finetune-project) | QLoRA · TinyLlama 1.1B · HuggingFace Hub | [Model](https://huggingface.co/Rohith2026/nlp-rag-expert) |
| [LLM Evaluation](https://github.com/RohithkumarReddipogula/llm-evaluation-project) | RAGAS · 5 metrics · Streamlit dashboard | [Dashboard](https://huggingface.co/spaces/ROHITHKUMARREDDIOGULa/llm-evaluation-dashboard) |
| AWS Deployment (this) | EC2 · systemd · FastAPI · Production API | [API](http://3.71.32.203:8000/docs) |

---

## Author

Rohith Kumar Reddipogula
MSc Data Science — University of Europe for Applied Sciences, Berlin

LinkedIn: https://linkedin.com/in/rohith-kumar-reddipogula-a6692030b
GitHub: https://github.com/RohithkumarReddipogula
HuggingFace: https://huggingface.co/Rohith2026
Email: rohithkumar336699@gmail.com
