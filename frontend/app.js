const API = 'http://127.0.0.1:5000/api';
let token = localStorage.getItem('token') || null;
let socket = null;
let isLogin = true;

// ── AUTH ──────────────────────────────────────────

function toggleAuth() {
  isLogin = !isLogin;
  document.getElementById('auth-title').textContent = isLogin ? 'Login' : 'Register';
  document.getElementById('auth-btn').textContent   = isLogin ? 'Login' : 'Register';
  document.getElementById('register-field').style.display = isLogin ? 'none' : 'block';
  document.querySelector('.switch').innerHTML = isLogin
    ? "Don't have an account? <span onclick='toggleAuth()'>Register</span>"
    : "Already have an account? <span onclick='toggleAuth()'>Login</span>";
}

async function handleAuth() {
  const email    = document.getElementById('email').value.trim();
  const password = document.getElementById('password').value.trim();

  if (isLogin) {
    const res  = await fetch(`${API}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });
    const data = await res.json();
    if (res.ok) {
      token = data.access_token;
      localStorage.setItem('token', token);
      showApp();
    } else {
      alert(data.error || 'Login failed');
    }
  } else {
    const username = document.getElementById('username').value.trim();
    const res = await fetch(`${API}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, email, password })
    });
    const data = await res.json();
    if (res.ok) {
      alert('Registered! Please login.');
      toggleAuth();
    } else {
      alert(data.error || 'Registration failed');
    }
  }
}

function logout() {
  localStorage.removeItem('token');
  token = null;
  if (socket) socket.disconnect();
  document.getElementById('app-section').style.display  = 'none';
  document.getElementById('auth-section').style.display = 'block';
}

// ── APP ───────────────────────────────────────────

function showApp() {
  document.getElementById('auth-section').style.display = 'none';
  document.getElementById('app-section').style.display  = 'block';
  connectSocket();
  loadTasks();
  loadAnalytics();
}

function connectSocket() {
  socket = io('http://127.0.0.1:5000', { auth: { token } });

  socket.on('connected', (data) => console.log(data.message));

  socket.on('task_updated', () => {
    loadTasks();
    loadAnalytics();
    showNotification('Task updated in real time');
  });

  socket.on('task_deleted', () => {
    loadTasks();
    loadAnalytics();
    showNotification('Task deleted');
  });
}

// ── TASKS ─────────────────────────────────────────

async function loadTasks() {
  const res   = await fetch(`${API}/tasks/`, { headers: authHeader() });
  const tasks = await res.json();
  renderTasks(tasks);
}

function renderTasks(tasks) {
  const list = document.getElementById('task-list');
  if (!tasks.length) { list.innerHTML = ''; return; }

  list.innerHTML = tasks.map(t => `
    <div class="task-item ${t.priority}">
      <div class="task-info">
        <h3>${t.title}</h3>
        <p>${t.description || ''}</p>
        <div class="task-badges">
          <span class="badge">${t.priority}</span>
          <span class="badge">${t.status}</span>
        </div>
      </div>
      <div class="task-actions">
        ${t.status !== 'completed'
          ? `<button class="btn-complete" onclick="markComplete(${t.id})">✓ Done</button>`
          : ''}
        <button class="btn-delete" onclick="deleteTask(${t.id})">✕ Delete</button>
      </div>
    </div>
  `).join('');
}

async function addTask() {
  const title    = document.getElementById('task-title').value.trim();
  const desc     = document.getElementById('task-desc').value.trim();
  const priority = document.getElementById('task-priority').value;
  const status   = document.getElementById('task-status').value;

  if (!title) { alert('Title is required'); return; }

  await fetch(`${API}/tasks/`, {
    method: 'POST',
    headers: { ...authHeader(), 'Content-Type': 'application/json' },
    body: JSON.stringify({ title, description: desc, priority, status })
  });

  document.getElementById('task-title').value = '';
  document.getElementById('task-desc').value  = '';
}

async function markComplete(id) {
  await fetch(`${API}/tasks/${id}`, {
    method: 'PATCH',
    headers: { ...authHeader(), 'Content-Type': 'application/json' },
    body: JSON.stringify({ status: 'completed' })
  });
}

async function deleteTask(id) {
  await fetch(`${API}/tasks/${id}`, {
    method: 'DELETE',
    headers: authHeader()
  });
}

// ── ANALYTICS ────────────────────────────────────

async function loadAnalytics() {
  const res  = await fetch(`${API}/analytics/`, { headers: authHeader() });
  const data = await res.json();

  document.getElementById('stat-total').textContent     = data.total;
  document.getElementById('stat-completed').textContent = data.completed;
  document.getElementById('stat-pending').textContent   = data.pending;
  document.getElementById('stat-pct').textContent       = data.completion_percentage + '%';
}

// ── HELPERS ───────────────────────────────────────

function authHeader() {
  return { 'Authorization': `Bearer ${token}` };
}

function showNotification(msg) {
  const n = document.createElement('div');
  n.className = 'notification';
  n.textContent = msg;
  document.body.appendChild(n);
  setTimeout(() => n.classList.add('show'), 10);
  setTimeout(() => { n.classList.remove('show'); setTimeout(() => n.remove(), 300); }, 3000);
}

// ── INIT ──────────────────────────────────────────

if (token) showApp();