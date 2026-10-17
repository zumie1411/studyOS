const API_BASE = "http://127.0.0.1:8000";

function switchTab(tabId) {
  document.querySelectorAll(".tab-pane").forEach(pane => pane.classList.remove("active"));
  document.querySelectorAll(".nav-item").forEach(btn => btn.classList.remove("active"));

  document.getElementById(`tab-${tabId}`).classList.add("active");
  event.target.classList.add("active");

  if (tabId === "dashboard") loadDashboard();
  if (tabId === "planner") loadPlanner();
  if (tabId === "subjects") loadSubjects();
  if (tabId === "tasks") { loadTasks(); populateSubjectSelect(); }
}

async function loadDashboard() {
  const [tasksRes, examsRes] = await Promise.all([
    fetch(`${API_BASE}/tasks/`),
    fetch(`${API_BASE}/exams/`)
  ]);
  const tasks = await tasksRes.json();
  const exams = await examsRes.json();

  document.getElementById("metric-tasks").innerText = tasks.length;
  document.getElementById("metric-exams").innerText = exams.length;

  const urgentList = document.getElementById("urgent-tasks-list");
  urgentList.innerHTML = tasks
    .filter(t => t.status === "pending")
    .slice(0, 5)
    .map(t => `<li class="list-item"><span>${t.title}</span><span class="badge urgent">Due: ${new Date(t.deadline).toLocaleDateString()}</span></li>`)
    .join("") || "<li class='list-item'>No pending tasks.</li>";

  const examsList = document.getElementById("upcoming-exams-list");
  examsList.innerHTML = exams
    .slice(0, 5)
    .map(e => `<li class="list-item"><span>Subject ID #${e.subject_id}</span><span class="badge">${new Date(e.exam_date).toLocaleDateString()}</span></li>`)
    .join("") || "<li class='list-item'>No exams scheduled.</li>";
}

async function loadPlanner() {
  const time = document.getElementById("planner-time").value || 180;
  const isRecovery = document.getElementById("recovery-mode-toggle").checked;

  const res = await fetch(`${API_BASE}/planner/today?available_minutes=${time}&recovery=${isRecovery}`);
  const data = await res.json();

  document.getElementById("plan-time-breakdown").innerText = 
    `Allocated: ${data.total_allocated}m / ${data.available_minutes}m capacity`;

  const scheduledContainer = document.getElementById("scheduled-plan-list");
  scheduledContainer.innerHTML = data.schedule.map(item => `
    <li class="list-item">
      <div>
        <strong>${item.title}</strong> (${item.subject_name})
        <div style="font-size:0.75rem; color:#64748b;">${item.reason}</div>
      </div>
      <div>
        <span class="badge ${item.reason.includes('Recovery') ? 'recovery' : 'urgent'}">${item.allocated_minutes} mins</span>
        <button class="btn" onclick="markTaskStatus(${item.task_id}, 'completed')">✓</button>
        <button class="btn" onclick="markTaskStatus(${item.task_id}, 'missed')">Missed</button>
      </div>
    </li>
  `).join("") || "<li class='list-item'>Nothing scheduled. You are caught up!</li>";

  const overflowContainer = document.getElementById("overflow-plan-list");
  overflowContainer.innerHTML = data.overflow_tasks.map(item => `
    <li class="list-item">
      <span>${item.title} (${item.allocated_minutes}m)</span>
      <span class="badge">Score: ${item.urgency_score}</span>
    </li>
  `).join("") || "<li class='list-item'>No tasks in overflow.</li>";
}

async function markTaskStatus(taskId, status) {
  await fetch(`${API_BASE}/tasks/${taskId}/status?status=${status}`, { method: "PATCH" });
  loadPlanner();
}

async function loadSubjects() {
  const res = await fetch(`${API_BASE}/subjects/`);
  const subjects = await res.json();
  const container = document.getElementById("subjects-container");

  container.innerHTML = subjects.map(s => `
    <div class="panel">
      <h3>${s.name}</h3>
      <p style="font-size:0.8rem; color:#64748b;">${s.semester}</p>
      <div style="margin-top: 8px;">
        <small><strong>Topics:</strong> ${s.topics.length}</small>
      </div>
    </div>
  `).join("") || "<p>No subjects added yet.</p>";
}

async function handleCreateSubject(e) {
  e.preventDefault();
  const name = document.getElementById("subj-name").value;
  const semester = document.getElementById("subj-sem").value;

  await fetch(`${API_BASE}/subjects/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, semester })
  });

  e.target.reset();
  loadSubjects();
}

async function populateSubjectSelect() {
  const res = await fetch(`${API_BASE}/subjects/`);
  const subjects = await res.json();
  const select = document.getElementById("task-subject-id");
  select.innerHTML = '<option value="">Select Subject</option>' + 
    subjects.map(s => `<option value="${s.id}">${s.name}</option>`).join("");
}

async function loadTasks() {
  const res = await fetch(`${API_BASE}/tasks/`);
  const tasks = await res.json();
  const list = document.getElementById("all-tasks-list");

  list.innerHTML = tasks.map(t => `
    <li class="list-item">
      <div>
        <strong>${t.title}</strong>
        <div style="font-size:0.75rem; color:#64748b;">Due: ${new Date(t.deadline).toLocaleString()}</div>
      </div>
      <div>
        <span class="badge">${t.status}</span>
      </div>
    </li>
  `).join("") || "<li class='list-item'>No tasks recorded.</li>";
}

async function handleCreateTask(e) {
  e.preventDefault();
  const payload = {
    subject_id: parseInt(document.getElementById("task-subject-id").value),
    title: document.getElementById("task-title").value,
    deadline: new Date(document.getElementById("task-deadline").value).toISOString(),
    estimated_minutes: parseInt(document.getElementById("task-duration").value),
    priority: parseInt(document.getElementById("task-priority").value),
    status: "pending"
  };

  await fetch(`${API_BASE}/tasks/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });

  e.target.reset();
  loadTasks();
}

document.addEventListener("DOMContentLoaded", () => {
  loadDashboard();
});