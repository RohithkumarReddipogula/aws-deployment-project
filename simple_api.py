"""
RAG System API — AWS EC2 Deployment
Author: Rohith Kumar Reddipogula
MSc Data Science — University of Europe for Applied Sciences, Berlin

Production FastAPI inference API deployed on AWS EC2 t3.micro
eu-central-1 Frankfurt with systemd auto-restart.

Endpoints:
    GET /        System overview and key results
    GET /health  Uptime and server information
    GET /info    Full performance metrics and portfolio
    GET /docs    Interactive OpenAPI documentation
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import time
import platform

app = FastAPI(
    title="RAG System API",
    description=(
        "Hybrid BM25 + E5 Retrieval-Augmented Generation System. "
        "Achieves 93% Recall@10 and MRR=1.0 on 8.84M MS MARCO passages. "
        "Deployed on AWS EC2 Frankfurt with systemd auto-restart."
    ),
    version="1.0.0",
    contact={
        "name": "Rohith Kumar Reddipogula",
        "email": "rohithkumar336699@gmail.com",
    },
)

# Allow cross-origin requests from any client
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

start_time = time.time()


@app.get("/", tags=["Overview"])
def root():
    """
    System overview — key results from the Hybrid RAG system.
    Returns performance metrics and links to all portfolio projects.
    """
    return {
        "name": "AI-Powered RAG System",
        "version": "1.0.0",
        "author": "Rohith Kumar Reddipogula",
        "thesis": "MSc Data Science — University of Europe for Applied Sciences Berlin 2026",
        "deployment": {
            "cloud": "AWS EC2",
            "instance": "t3.micro",
            "region": "eu-central-1 Frankfurt",
            "process_manager": "systemd",
        },
        "results": {
            "recall_at_10": "93.0%",
            "mrr": "1.0 — perfect",
            "improvement_over_baseline": "11.4%",
            "optimal_alpha": 0.70,
            "corpus_size": "8.84M MS MARCO passages",
            "index_size_mb": 4.46,
        },
        "links": {
            "api_docs": "/docs",
            "health": "/health",
            "info": "/info",
            "rag_demo": "https://rohith2026-hybrid-rag-demo.hf.space",
            "rag_api": "https://rohith2026-hybrid-rag-api.hf.space/docs",
            "github": "https://github.com/RohithkumarReddipogula",
        },
    }


@app.get("/health", tags=["Monitoring"])
def health():
    """
    Health check endpoint — use for readiness probes and uptime monitoring.
    Returns server details, uptime, and process manager status.
    """
    uptime = time.time() - start_time
    hours = int(uptime // 3600)
    minutes = int((uptime % 3600) // 60)
    seconds = int(uptime % 60)

    return {
        "status": "healthy",
        "uptime_seconds": round(uptime, 1),
        "uptime_human": f"{hours}h {minutes}m {seconds}s",
        "server": {
            "cloud": "AWS EC2",
            "instance_type": "t3.micro",
            "region": "eu-central-1 Frankfurt",
            "os": platform.system(),
            "os_release": platform.release(),
            "python_version": platform.python_version(),
            "architecture": platform.machine(),
        },
        "service": {
            "manager": "systemd",
            "restart_policy": "on-failure",
            "restart_delay_seconds": 5,
        },
    }


@app.get("/info", tags=["Overview"])
def info():
    """
    Full system information — research context, performance metrics,
    technical stack, and complete portfolio links.
    """
    return {
        "research": {
            "title": "Hybrid Retrieval-Augmented Generation with BM25 and Dense Embeddings",
            "institution": "University of Europe for Applied Sciences, Berlin",
            "degree": "MSc Data Science",
            "year": 2026,
        },
        "system": {
            "description": (
                "Hybrid RAG combining BM25 sparse retrieval with Microsoft "
                "E5-base-v2 dense embeddings using FAISS for vector search. "
                "Optimal fusion weight alpha=0.70 validated statistically."
            ),
        },
        "performance": {
            "recall_at_10": "93.0%",
            "mrr": "1.0 — perfect",
            "improvement_over_bm25_baseline": "11.4%",
            "statistical_validation": "paired t-test p=0.002",
            "optimal_fusion_weight": "alpha=0.70",
            "corpus_size": "8.84M MS MARCO passages",
            "index_size_compressed_mb": 4.46,
            "index_size_original_gb": 27.0,
            "compression_ratio": "6x",
        },
        "stack": {
            "retrieval": ["BM25 (rank-bm25)", "FAISS", "E5-base-v2"],
            "api": ["FastAPI", "uvicorn", "pydantic"],
            "deployment": ["AWS EC2", "Ubuntu 24.04", "systemd"],
            "language": "Python 3.11",
        },
        "portfolio": {
            "rag_demo": "https://rohith2026-hybrid-rag-demo.hf.space",
            "rag_api": "https://rohith2026-hybrid-rag-api.hf.space/docs",
            "ai_agent": "https://rohith2026-ai-agent-react.hf.space",
            "llm_evaluation": "https://rohith2026-llm-evaluation-dashboard.hf.space",
            "fine_tuned_model": "https://huggingface.co/Rohith2026/nlp-rag-expert",
            "github": "https://github.com/RohithkumarReddipogula",
            "linkedin": "https://linkedin.com/in/rohith-kumar-reddipogula-a6692030b",
        },
    }
