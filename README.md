# eClipseBord
 
A fullstack dashboard for exploring historical and upcoming solar eclipses, built with FastAPI, Streamlit, and deployed to Azure.
 
## Overview
 
eClipseBord lets you explore solar eclipse data (NASA eclipse catalog), filter by year, see where eclipses occur on a map, and view the distribution of eclipse types and shadow path widths.
 
## Architecture
 
The project went through three stages:
 
### 1. Local development
 
The project is structured as a **uv workspace** with three members:
 
```
eClipseBord_Azure_Lab_DE25_Felix_Kjellberg/
├─ backend/      FastAPI service that reads and serves the cleaned eclipse dataset
├─ frontend/     Streamlit dashboard that consumes the backend API
├─ eda/          Exploratory data analysis notebook, not deployed
├─ data/         Raw dataset (solar.csv)
└─ pyproject.toml (workspace root)
```
 
Each member has its own `pyproject.toml` and dependencies, but they share a single `.venv` and `uv.lock` resolved from the workspace root. This keeps backend, frontend, and EDA dependencies isolated from each other while still being managed together.
 
- **Backend** (FastAPI): loads `solar.csv`, cleans it (snake_case columns, parses year from calendar date, converts latitude/longitude to numeric coordinates, handles missing values), and exposes it through a REST endpoint (`/eclipse/solar`).
- **Frontend** (Streamlit): fetches data from the backend over HTTP, lets the user filter by year range, and renders summary metrics, a map (via pydeck), and bar charts (eclipse type distribution, path width distribution).
- **EDA**: a separate notebook used to explore the dataset before building the cleaning logic in the backend. Not containerized or deployed, purely for local exploration.
During local development, backend and frontend were run as two separate processes (`uv run uvicorn` and `uv run streamlit run`), with the frontend pointed at the backend via a `BACKEND_URL` environment variable (defaulting to `http://127.0.0.1:8000` when not set).
 
### 2. Dockerization
 
Backend and frontend were each containerized with their own Dockerfile:
 
- Each Dockerfile copies in its respective project folder, installs dependencies with `uv sync --no-dev`, and runs the service (`uvicorn` for backend, `streamlit run` for frontend).
- A `docker-compose.yaml` at the root builds and runs both containers together for local testing, with the frontend container's `BACKEND_URL` pointed at the backend container's service name (`http://backend:8000`) instead of `localhost`, since containers on the same Docker network address each other by service name.
This step verified that the whole application worked identically inside containers as it did running natively, before moving to the cloud.
 
### 3. Azure deployment
 
Once verified locally, both images were pushed to an **Azure Container Registry (ACR)**. From there:
 
- **Backend** was deployed as an **Azure Container App**, pulling its image directly from ACR.
- **Frontend** was deployed as an **Azure Web App** (container-based), also pulling its image from ACR.
- The frontend's `BACKEND_URL` environment variable was set in the Azure Web App configuration to point at the backend Container App's public URL, connecting the two services in the cloud the same way `docker-compose` connected them locally.
> **Note:** to save on Azure resources, the resource group used for this deployment has since been deleted. The architecture above reflects how the services were connected while they were live.
 
## Data
 
The dataset is NASA's solar eclipse catalog, covering thousands of eclipses across several millennia (ancient BCE dates through the year 3000), including eclipse type, magnitude, geographic location, and shadow path details.
 
## LLM usage
 
Parts of this project (notably the map visualization using pydeck) were built with help from an LLM. This is noted directly as a comment in the relevant source file.