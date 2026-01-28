FROM python:3.11-slim

WORKDIR /app

# (必要な場合のみ) ビルド系依存
RUN apt-get update && apt-get install -y --no-install-recommends gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# リポジトリ全体をコピー（漏れを防ぐ）
COPY . .

# 非root実行
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# Healthcheck は一旦外す（/ が 500 になり得るため）
# HEALTHCHECK ... （必要なら /healthz を作って叩く）

CMD ["gunicorn", "app:app", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "--workers", "1", "--timeout", "120"]
