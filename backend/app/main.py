"""Evoxim AI Experience Platform — FastAPI application."""

from __future__ import annotations

import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

from app.database import init_db
from app.api import discovery, leads, proposals, analytics

app = FastAPI(
    title="Evoxim AI Experience Platform",
    description=(
        "Backend API for Evoxim — Collective Communication. "
        "Supports prospect discovery, AI-assisted recommendations, "
        "proposal generation, and admin dashboard."
    ),
    version="1.0.0",
)

# CORS
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(discovery.router)
app.include_router(leads.router)
app.include_router(proposals.router)
app.include_router(analytics.router)


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/")
def root():
    return {
        "name": "Evoxim AI Experience Platform",
        "version": "1.0.0",
        "status": "running",
    }


@app.get("/health")
def health():
    return {"status": "ok"}
