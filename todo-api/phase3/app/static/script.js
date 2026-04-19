const API_URL = 'http://127.0.0.1:5000/api';

document.addEventListener('DOMContentLoaded', () => {
    fetchUsers();
    fetchCategories();
    if (localStorage.getItem('currentUserId')) {
        const savedUser = localStorage.getItem('currentUserId');
        document.getElementById('user-switcher').value = savedUser;
        fetchTasks();
    }
    document.getElementById('task-form').addEventListener('submit', addTask);
});

function getHeaders() {
    return { 'Content-Type': 'application/json', 'User-ID': localStorage.getItem('currentUserId') || '' };
}

function setCurrentUser(userId) {
    localStorage.setItem('currentUserId', userId);
    fetchTasks();
}

async function fetchUsers() {
    const res = await fetch(`${API_URL}/users`);
    const data = await res.json();
    const switcher = document.getElementById('user-switcher');
    switcher.innerHTML = '<option value="" disabled selected>Select User</option>';
    data.users.forEach(user => {
        switcher.innerHTML += `<option value="${user._id}">${user.username}</option>`;
    });
}

async function fetchTasks() {
    const userId = localStorage.getItem('currentUserId');
    if (!userId) return;
    const res = await fetch(`${API_URL}/tasks`, { headers: getHeaders() });
    const data = await res.json();
    const list = document.getElementById('tasks-list');
    list.innerHTML = '';
    
    data.tasks.forEach(task => {
        list.innerHTML += `
            <div class="task-card ${task.completed ? 'task-completed' : ''}">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <input type="checkbox" ${task.completed ? 'checked' : ''} onchange="toggleTaskStatus('${task._id}', this.checked)">
                    <strong>${task.title}</strong>
                </div>
                <div>
                    <button onclick='openViewModal(${JSON.stringify(task)})' style="width:auto; padding:5px 10px; background:blue;">View</button>
                    <button onclick='openEditModal(${JSON.stringify(task)})' style="width:auto; padding:5px 10px; background:gray;">Edit</button>
                    <button onclick="deleteTask('${task._id}')" style="width:auto; padding:5px 10px; background:red;">X</button>
                </div>
            </div>`;
    });
}

async function toggleTaskStatus(id, isCompleted) {
    await fetch(`${API_URL}/tasks/${id}`, { method: 'PUT', headers: getHeaders(), body: JSON.stringify({ completed: isCompleted }) });
    fetchTasks();
}

async function fetchCategories() {
    const res = await fetch(`${API_URL}/categories`);
    const data = await res.json();
    ['task-category', 'edit-category'].forEach(id => {
        const sel = document.getElementById(id);
        sel.innerHTML = '<option value="" disabled selected>Select</option>';
        data.categories.forEach(c => sel.innerHTML += `<option value="${c._id}">${c.name}</option>`);
    });
}

async function addTask(e) {
    e.preventDefault();
    const taskData = {
        title: document.getElementById('task-title').value,
        description: document.getElementById('task-description').value,
        category_id: document.getElementById('task-category').value,
        priority: parseInt(document.getElementById('task-priority').value),
        user_id: localStorage.getItem('currentUserId')
    };
    await fetch(`${API_URL}/tasks`, { method: 'POST', headers: getHeaders(), body: JSON.stringify(taskData) });
    document.getElementById('task-form').reset();
    fetchTasks();
}

async function createCategory() {
    const name = document.getElementById('new-category-name').value;
    if(!name) return;
    await fetch(`${API_URL}/categories`, { method: 'POST', headers: getHeaders(), body: JSON.stringify({name}) });
    document.getElementById('new-category-name').value = '';
    fetchCategories();
}

function openEditModal(task) {
    document.getElementById('edit-task-id').value = task._id;
    document.getElementById('edit-title').value = task.title;
    document.getElementById('edit-description').value = task.description || '';
    document.getElementById('edit-category').value = task.category_id;
    document.getElementById('edit-priority').value = task.priority;
    document.getElementById('edit-modal').style.display = 'flex';
}

function openViewModal(task) {
    document.getElementById('view-title').innerText = task.title;
    document.getElementById('view-description').innerText = task.description || 'N/A';
    document.getElementById('view-category').innerText = task.category_id;
    document.getElementById('view-priority').innerText = task.priority;
    document.getElementById('view-modal').style.display = 'flex';
}

function closeModal(id) { document.getElementById(id).style.display = 'none'; }

async function saveEdit() {
    const id = document.getElementById('edit-task-id').value;
    const data = {
        title: document.getElementById('edit-title').value,
        description: document.getElementById('edit-description').value,
        category_id: document.getElementById('edit-category').value,
        priority: parseInt(document.getElementById('edit-priority').value)
    };
    await fetch(`${API_URL}/tasks/${id}`, { method: 'PUT', headers: getHeaders(), body: JSON.stringify(data) });
    closeModal('edit-modal');
    fetchTasks();
}

async function deleteTask(id) {
    if (!confirm('Are you sure?')) return;
    await fetch(`${API_URL}/tasks/${id}`, { method: 'DELETE', headers: getHeaders() });
    fetchTasks();
}

async function createUser() {
    const username = document.getElementById('new-username').value;
    const email = document.getElementById('new-email').value;
    const password = document.getElementById('new-password').value;
    
    if (!username || !email || !password) {
        alert("Please fill all fields");
        return;
    }

    const userData = { username, email, password };

    const res = await fetch(`${API_URL}/users`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(userData)
    });

    if (res.ok) {
        document.getElementById('new-username').value = '';
        document.getElementById('new-email').value = '';
        document.getElementById('new-password').value = '';
        alert("User created successfully!");
        fetchUsers(); 
    } else {
        const error = await res.json();
        alert(error.error || "Failed to create user");
    }
}