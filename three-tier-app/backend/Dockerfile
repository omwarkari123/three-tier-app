# --- Backend Dockerfile ---
# Small, single-stage image. Good enough for learning; later you can
# practice multi-stage builds to shrink this further.

FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]
