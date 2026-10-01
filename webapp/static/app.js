const form = document.getElementById('student-form');
const tableBody = document.getElementById('student-table-body');
const dashboard = document.getElementById('dashboard');
const message = document.getElementById('message');
const resetButton = document.getElementById('reset-button');
const searchInput = document.getElementById('search-input');

let allStudents = [];
let editingId = null;

async function fetchStudents() {
  const response = await fetch('/api/students');
  allStudents = await response.json();
  renderStudents(allStudents);
}

async function fetchDashboard() {
  const response = await fetch('/api/dashboard');
  const data = await response.json();
  renderDashboard(data);
}

function renderStudents(students) {
  tableBody.innerHTML = '';

  if (!students.length) {
    tableBody.innerHTML = '<tr><td colspan="6">Nenhum estudante encontrado.</td></tr>';
    return;
  }

  students.forEach((student) => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${student.id}</td>
      <td>${student.name}</td>
      <td>${student.nationality}</td>
      <td>${student.generation}</td>
      <td>${student.accommodation}</td>
      <td>
        <button type="button" class="edit-btn" data-action="edit" data-id="${student.id}">Editar</button>
        <button type="button" class="action-btn" data-action="delete" data-id="${student.id}">Excluir</button>
      </td>
    `;
    tableBody.appendChild(row);
  });

  tableBody.querySelectorAll('button[data-action]').forEach((button) => {
    button.addEventListener('click', async () => {
      const id = Number(button.dataset.id);
      const action = button.dataset.action;

      if (action === 'delete') {
        await deleteStudent(id);
      }

      if (action === 'edit') {
        prepareEdit(id);
      }
    });
  });
}

function renderDashboard(items) {
  dashboard.innerHTML = '';

  items.forEach((item) => {
    const card = document.createElement('div');
    card.className = 'dashboard-item';
    card.innerHTML = `
      <span>${item.label}</span>
      <strong>${item.value}</strong>
    `;
    dashboard.appendChild(card);
  });
}

function prepareEdit(id) {
  const student = allStudents.find((item) => item.id === id);
  if (!student) return;

  editingId = id;
  document.getElementById('name').value = student.name;
  document.getElementById('nationality').value = student.nationality;
  document.getElementById('generation').value = student.generation;
  document.getElementById('accommodation').value = student.accommodation;

  const submitButton = form.querySelector('button[type="submit"]');
  submitButton.textContent = 'Atualizar';
  message.textContent = 'Editando estudante selecionado.';
}

async function deleteStudent(id) {
  const response = await fetch(`/api/students/${id}`, { method: 'DELETE' });
  if (response.ok) {
    message.textContent = 'Estudante excluído com sucesso.';
    if (editingId === id) {
      resetFormState();
    }
    fetchStudents();
    fetchDashboard();
  }
}

function resetFormState() {
  editingId = null;
  form.reset();
  const submitButton = form.querySelector('button[type="submit"]');
  submitButton.textContent = 'Salvar';
}

form.addEventListener('submit', async (event) => {
  event.preventDefault();

  const wasEditing = editingId !== null;
  const formData = new FormData(form);
  const payload = Object.fromEntries(formData.entries());

  const url = wasEditing ? `/api/students/${editingId}` : '/api/students';
  const method = wasEditing ? 'PUT' : 'POST';

  const response = await fetch(url, {
    method,
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });

  if (response.ok) {
    resetFormState();
    message.textContent = wasEditing
      ? 'Estudante atualizado com sucesso.'
      : 'Estudante cadastrado com sucesso.';
    fetchStudents();
    fetchDashboard();
  } else {
    const error = await response.json();
    message.textContent = error.detail || 'Erro ao salvar estudante.';
  }
});

resetButton.addEventListener('click', () => {
  resetFormState();
  message.textContent = 'Campos limpos.';
});

searchInput.addEventListener('input', (event) => {
  const term = event.target.value.trim().toLowerCase();

  const filteredStudents = allStudents.filter((student) =>
    student.name.toLowerCase().includes(term)
  );

  renderStudents(filteredStudents);
});

fetchStudents();
fetchDashboard();
