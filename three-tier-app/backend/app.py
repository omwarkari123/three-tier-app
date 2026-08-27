"""
TIER 2: BACKEND (API layer)
A tiny Flask REST API that reads/writes tasks in Postgres.
This is the piece that will get containerized, pushed to a registry,
and deployed as a Kubernetes Deployment + Service.
"""

import os
import time
import psycopg2
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allows the frontend (different origin) to call this API

# Pull DB connection info from environment variables (never hardcode secrets!)
# In docker-compose these come from the "environment:" block.
# In Kubernetes these will come from a ConfigMap/Secret.
DB_HOST = os.environ.get("DB_HOST", "db")
DB_NAME = os.environ.get("DB_NAME", "tasksdb")
DB_USER = os.environ.get("DB_USER", "taskuser")
DB_PASS = os.environ.get("DB_PASS", "taskpass")


def get_connection():
    """Retries a few times so the API doesn't crash if the DB
    container isn't ready yet (a very common real-world race condition)."""
    for attempt in range(10):
        try:
            return psycopg2.connect(
                host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS
            )
        except psycopg2.OperationalError:
            print(f"DB not ready yet, retrying... ({attempt + 1}/10)")
            time.sleep(3)
    raise Exception("Could not connect to database after 10 attempts")


def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            done BOOLEAN DEFAULT FALSE
        );
    """)
    conn.commit()
    cur.close()
    conn.close()


@app.route("/health")
def health():
    """Used by Docker/Kubernetes liveness & readiness probes."""
    return jsonify({"status": "ok"}), 200


@app.route("/tasks", methods=["GET"])
def get_tasks():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, title, done FROM tasks ORDER BY id;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    tasks = [{"id": r[0], "title": r[1], "done": r[2]} for r in rows]
    return jsonify(tasks)


@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.get_json()
    title = data.get("title", "").strip()
    if not title:
        return jsonify({"error": "title is required"}), 400

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks (title) VALUES (%s) RETURNING id;", (title,))
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"id": new_id, "title": title, "done": False}), 201


@app.route("/tasks/<int:task_id>", methods=["PUT"])
def toggle_task(task_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE tasks SET done = NOT done WHERE id = %s;", (task_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"status": "updated"})


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id = %s;", (task_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"status": "deleted"})


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
