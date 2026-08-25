# syntax=docker/dockerfile:1
FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements-streamlit.txt .

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements-streamlit.txt

COPY streamlit/app.py .
COPY streamlit/pages ./pages
COPY streamlit/assets ./assets
COPY streamlit/assets ./pages/assets
COPY streamlit/style_lateral.py .

# Criar usuário não-root
RUN useradd -m -u 1000 streamlit && chown -R streamlit:streamlit /app
USER streamlit

EXPOSE 8501

# Configurações via ENV (mais rápido)
ENV STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD curl -fsS http://localhost:8501/_stcore/health || exit 1

CMD ["streamlit", "run", "app.py"]