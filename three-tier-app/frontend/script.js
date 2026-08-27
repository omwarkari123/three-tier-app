// TIER 1: FRONTEND
// Calls the backend through the "/api" path. Nginx (see nginx.conf)
// reverse-proxies "/api/*" to the backend container, so the browser
// never needs to know the backend's host/port directly.
const API_URL = "/api";

const form = document.getElementById("task-form");
const input = document.getElementById("task-input");
const list = document.getElementById("task-list");

async function loadTasks() {
  const res = await fetch(`${API_URL}/tasks`);
  const tasks = await res.json();
  list.innerHTML = "";
  tasks.forEach((task) => {
    const li = document.createElement("li");
    if (task.done) li.classList.add("done");

    const span = document.createElement("span");
    span.textContent = task.title;
    span.onclick = () => toggleTask(task.id);

    const btn = document.createElement("button");
    btn.textContent = "Delete";
    btn.onclick = () => deleteTask(task.id);

    li.appendChild(span);
    li.appendChild(btn);
    list.appendChild(li);
  });
}

async function addTask(title) {
  await fetch(`${API_URL}/tasks`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title }),
  });
  loadTasks();
}

async function toggleTask(id) {
  await fetch(`${API_URL}/tasks/${id}`, { method: "PUT" });
  loadTasks();
}

async function deleteTask(id) {
  await fetch(`${API_URL}/tasks/${id}`, { method: "DELETE" });
  loadTasks();
}

form.addEventListener("submit", (e) => {
  e.preventDefault();
  const title = input.value.trim();
  if (title) {
    addTask(title);
    input.value = "";
  }
});

loadTasks();
