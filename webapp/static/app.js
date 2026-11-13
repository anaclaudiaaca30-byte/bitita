const form = document.getElementById('student-form');
const table = document.querySelector('.table-wrap table');
const tableBody = document.getElementById('student-table-body');
const tableMessage = document.getElementById('table-message');
const dashboard = document.getElementById('dashboard');
const dashboardTableBody = document.getElementById('dashboard-table-body');
const message = document.getElementById('message');
const errorMessage = document.getElementById('error-message');
const resetButton = document.getElementById('reset-button');
const searchInput = document.getElementById('search-input');
const nameInput = document.getElementById('name');
const institutionalAccommodationInput = document.getElementById(
  'institutional_accommodation'
);

let allStudents = [];
let editingId = null;

function announceSuccess(text) {
  errorMessage.textContent = '';
  message.textContent = text;
}

function announceError(text) {
  message.textContent = '';
  errorMessage.textContent = text;
}

async function getErrorMessage(response) {
  const error = await response.json().catch(() => ({}));

  if (Array.isArray(error.detail)) {
    return error.detail.map((item) => item.msg).join('. ');
  }

  return error.detail || 'Ocorreu um erro. Tente novamente.';
}

function addCell(row, value) {
  const cell = document.createElement('td');
  cell.textContent = value;
  row.appendChild(cell);
  return cell;
}

function applySearch() {
  const term = searchInput.value.trim().toLocaleLowerCase('pt-BR');

  const filteredStudents = allStudents.filter((student) =>
    student.name.toLocaleLowerCase('pt-BR').includes(term)
  );

  renderStudents(filteredStudents);

  if (term) {
    tableMessage.textContent =
      `${filteredStudents.length} estudante(s) encontrado(s).`;
  } else {
    tableMessage.textContent = allStudents.length
      ? `${allStudents.length} estudante(s) carregado(s).`
      : 'Nenhum estudante cadastrado.';
  }
}

async function fetchStudents() {
  table.setAttribute('aria-busy', 'true');
  tableMessage.textContent = 'Carregando estudantes...';

  try {
    const response = await fetch('/api/students');

    if (!response.ok) {
      throw new Error(await getErrorMessage(response));
    }

    allStudents = await response.json();
    applySearch();
    return true;
  } catch (error) {
    allStudents = [];
    renderStudents([]);
    tableMessage.textContent = 'Não foi possível carregar os estudantes.';
    announceError(`Erro ao carregar estudantes: ${error.message}`);
    return false;
  } finally {
    table.setAttribute('aria-busy', 'false');
  }
}

async function fetchDashboard() {
  dashboard.setAttribute('aria-busy', 'true');
  dashboard.textContent = 'Carregando resumo...';
  dashboardTableBody.replaceChildren();

  const loadingRow = document.createElement('tr');
  addCell(loadingRow, 'Carregando resumo...').colSpan = 2;
  dashboardTableBody.appendChild(loadingRow);

  try {
    const response = await fetch('/api/dashboard');

    if (!response.ok) {
      throw new Error(await getErrorMessage(response));
    }

    renderDashboard(await response.json());
    return true;
  } catch (error) {
    dashboard.textContent = 'Não foi possível carregar o resumo.';
    dashboardTableBody.replaceChildren();

    const row = document.createElement('tr');
    addCell(row, 'Não foi possível carregar o resumo.').colSpan = 2;
    dashboardTableBody.appendChild(row);

    announceError(`Erro ao carregar o dashboard: ${error.message}`);
    return false;
  } finally {
    dashboard.setAttribute('aria-busy', 'false');
  }
}

function renderStudents(students) {
  tableBody.replaceChildren();

  if (!students.length) {
    const row = document.createElement('tr');
    addCell(row, 'Nenhum estudante encontrado.').colSpan = 7;
    tableBody.appendChild(row);
    return;
  }

  students.forEach((student) => {
    const row = document.createElement('tr');

    addCell(row, String(student.id));
    addCell(row, student.name);
    addCell(row, student.nationality);
    addCell(row, student.generation);
    addCell(row, student.accommodation);
    addCell(
      row,
      student.institutional_accommodation || 'Não informado'
    );

    const actions = addCell(row, '');

    const editButton = document.createElement('button');
    editButton.type = 'button';
    editButton.className = 'edit-btn';
    editButton.dataset.action = 'edit';
    editButton.dataset.id = student.id;
    editButton.textContent = 'Editar';
    editButton.setAttribute(
      'aria-label',
      `Editar estudante ${student.name}`
    );

    const deleteButton = document.createElement('button');
    deleteButton.type = 'button';
    deleteButton.className = 'action-btn';
    deleteButton.dataset.action = 'delete';
    deleteButton.dataset.id = student.id;
    deleteButton.textContent = 'Excluir';
    deleteButton.setAttribute(
      'aria-label',
      `Excluir estudante ${student.name}`
    );

    actions.append(editButton, deleteButton);
    tableBody.appendChild(row);
  });
}

function renderDashboard(items) {
  dashboard.replaceChildren();
  dashboardTableBody.replaceChildren();

  if (!items.length) {
    const emptyMessage = document.createElement('p');
    emptyMessage.className = 'empty-state';
    emptyMessage.textContent = 'Nenhum dado disponível.';
    dashboard.appendChild(emptyMessage);

    const row = document.createElement('tr');
    addCell(row, 'Nenhum dado disponível.').colSpan = 2;
    dashboardTableBody.appendChild(row);
    return;
  }

  items.forEach((item) => {
    const card = document.createElement('div');
    card.className = 'dashboard-item';

    const label = document.createElement('span');
    label.textContent = item.label;

    const value = document.createElement('strong');
    value.textContent = String(item.value);

    card.append(label, value);
    dashboard.appendChild(card);

    const row = document.createElement('tr');
    addCell(row, item.label);
    addCell(row, String(item.value));
    dashboardTableBody.appendChild(row);
  });
}

function prepareEdit(id) {
  const student = allStudents.find((item) => item.id === id);

  if (!student) return;

  editingId = id;
  nameInput.value = student.name;
  document.getElementById('nationality').value = student.nationality;
  document.getElementById('generation').value = student.generation;
  document.getElementById('accommodation').value = student.accommodation;

  institutionalAccommodationInput.value =
    student.institutional_accommodation || 'Não informado';

  form.querySelector('button[type="submit"]').textContent = 'Atualizar';
  announceSuccess(`Editando estudante ${student.name}.`);
  nameInput.focus();
}

function resetFormState() {
  editingId = null;
  form.reset();
  institutionalAccommodationInput.value = 'Não informado';
  form.querySelector('button[type="submit"]').textContent = 'Salvar';
}

async function deleteStudent(id, button) {
  const student = allStudents.find((item) => item.id === id);

  if (!student) return;

  const confirmed = window.confirm(
    `Deseja excluir o estudante ${student.name}? ` +
    'Esta ação não pode ser desfeita.'
  );

  if (!confirmed) {
    button.focus();
    return;
  }

  button.disabled = true;

  try {
    const response = await fetch(`/api/students/${id}`, {
      method: 'DELETE',
    });

    if (!response.ok) {
      throw new Error(await getErrorMessage(response));
    }

    if (editingId === id) {
      resetFormState();
    }

    const [studentsLoaded, dashboardLoaded] = await Promise.all([
      fetchStudents(),
      fetchDashboard(),
    ]);

    if (studentsLoaded && dashboardLoaded) {
      announceSuccess(
        `Estudante ${student.name} excluído com sucesso.`
      );
    } else {
      announceError(
        `Estudante ${student.name} excluído, mas não foi possível ` +
        'atualizar todos os dados exibidos.'
      );
    }

    document.getElementById('table-title').focus();
  } catch (error) {
    button.disabled = false;
    announceError(`Erro ao excluir estudante: ${error.message}`);
  }
}

tableBody.addEventListener('click', async (event) => {
  const button = event.target.closest('button[data-action]');

  if (!button) return;

  const id = Number(button.dataset.id);

  if (button.dataset.action === 'delete') {
    await deleteStudent(id, button);
  } else if (button.dataset.action === 'edit') {
    prepareEdit(id);
  }
});

form.addEventListener('submit', async (event) => {
  event.preventDefault();

  if (!form.reportValidity()) return;

  const submitButton = form.querySelector('button[type="submit"]');
  const wasEditing = editingId !== null;
  const payload = Object.fromEntries(new FormData(form).entries());

  payload.institutional_accommodation =
    institutionalAccommodationInput.value || 'Não informado';

  const url = wasEditing
    ? `/api/students/${editingId}`
    : '/api/students';

  submitButton.disabled = true;

  try {
    const response = await fetch(url, {
      method: wasEditing ? 'PUT' : 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error(await getErrorMessage(response));
    }

    resetFormState();

    const [studentsLoaded, dashboardLoaded] = await Promise.all([
      fetchStudents(),
      fetchDashboard(),
    ]);

    if (studentsLoaded && dashboardLoaded) {
      announceSuccess(
        wasEditing
          ? 'Estudante atualizado com sucesso.'
          : 'Estudante cadastrado com sucesso.'
      );
    } else {
      announceError(
        'Dados salvos, mas não foi possível atualizar ' +
        'todas as informações exibidas.'
      );
    }

    nameInput.focus();
  } catch (error) {
    announceError(`Erro ao salvar estudante: ${error.message}`);
  } finally {
    submitButton.disabled = false;
  }
});

resetButton.addEventListener('click', () => {
  resetFormState();
  announceSuccess('Campos limpos.');
  nameInput.focus();
});

searchInput.addEventListener('input', applySearch);

fetchStudents();
fetchDashboard();