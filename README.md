# Abogadazo

Abogadazo is a recovery-stage project for consulting Mexican traffic-law information. The repository preserves the previous React interface, two API/service implementations, legal reference material, an agent registry, and a PostgreSQL schema so that redevelopment can start from a clear base.

## Repository layout

```text
frontend/              React single-page application
backend/node-api/      Express/PostgreSQL user and administrator API
ai/                    Flask/LangChain legal-assistant service
  scripts/             Utility for rebuilding the vector index
data/
  agents/              Registry of authorized traffic agents (CSV)
  legal-sources/       PDF legal/reference sources retained from the project
  legal-embeddings/    Existing FAISS index built from legal sources
database/schema.sql    PostgreSQL schema
```

## Technologies retained

- React, React Router, Bootstrap, Axios, Recharts, and Create React App tooling
- Node.js, Express, PostgreSQL (`pg`), and EJS
- Python, Flask, LangChain, Ollama, FAISS, and PostgreSQL (`psycopg2`)

## Current status

This is an organized recovery baseline, not a verified working deployment. The frontend contains stale hard-coded service URLs. The Node API and Python service overlap around PostgreSQL but are not integrated as one application. The AI service requires a local Ollama installation/models and the preserved FAISS index. See the source before attempting to run or deploy any component.

Database credentials are intentionally not stored in the repository. Copy the appropriate `.env.example` file to `.env` and provide `DATABASE_URL` locally when working with either backend service.

## Suggested next step

Choose one backend path (the Flask legal-assistant service or the Express API), define its API contract with the React client, and then add safe configuration plus a minimal local development setup before restoring features.
