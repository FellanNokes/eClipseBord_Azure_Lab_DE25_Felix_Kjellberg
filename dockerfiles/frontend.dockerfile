FROM python:3.13-slim

# everything in frontend folder goes into /app folder, which is created if it didn't exist before
COPY frontend/ /app/

# install uv
RUN pip install --no-cache-dir uv

# cd working dir to /app
WORKDIR /app

# installs all dependencies specified in pyproject.toml without dev packages
RUN uv sync --no-dev

# change working directory to where we have api.py
WORKDIR /app/src/frontend

# 0.0.0.0 -> accept connections from local machine to external
CMD [ "uv" , "run", "streamlit", "run","dashboard.py", "--server.address", "0.0.0.0"]