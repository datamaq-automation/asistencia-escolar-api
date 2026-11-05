const API_PREFIX = '/api/v1';

const formatAlumno = (alumno) => `
  <tr>
    <td>${alumno.id}</td>
    <td>${alumno.nombre_completo}</td>
    <td>${alumno.ciclo}</td>
    <td>${alumno.anio}</td>
    <td>${alumno.division}</td>
    <td>${alumno.turno}</td>
  </tr>
`;

const listAlumnos = async () => {
  const anio = document.getElementById('filtro-anio').value;
  const division = document.getElementById('filtro-division').value;
  const params = new URLSearchParams();

  if (anio) params.append('anio', anio);
  if (division) params.append('division', division);

  const response = await fetch(`${API_PREFIX}/alumnos?${params.toString()}`);
  const data = await response.json();
  const tbody = document.getElementById('alumnos-table-body');

  tbody.innerHTML = (data.alumnos || []).map(formatAlumno).join('');
};

const consultarAlertas = async () => {
  const limite = document.getElementById('limite-alertas').value || 5;
  const response = await fetch(`${API_PREFIX}/reportes/alertas?limite=${limite}`);
  const data = await response.json();
  const container = document.getElementById('alertas-container');

  if (!data.alertas || data.alertas.length === 0) {
    container.innerHTML = '<div class="alert alert-light mb-0">No hay alertas para este límite.</div>';
    return;
  }

  container.innerHTML = data.alertas.map((alerta) => `
    <div class="list-group-item">
      <div class="d-flex justify-content-between align-items-center">
        <strong>${alerta.nombre_completo}</strong>
        <span class="badge bg-danger rounded-pill">${alerta.cantidad_faltas_injustificadas}</span>
      </div>
      <small class="text-muted">Alumno ID: ${alerta.alumno_id}</small>
    </div>
  `).join('');
};

document.getElementById('alumno-form').addEventListener('submit', async (event) => {
  event.preventDefault();
  const form = event.currentTarget;
  const payload = {
    nombre: form.nombre.value.trim(),
    apellido: form.apellido.value.trim(),
    ciclo: form.ciclo.value,
    anio: form.anio.value,
    division: form.division.value,
  };

  const response = await fetch(`${API_PREFIX}/alumnos`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  const result = await response.json();
  if (!response.ok) {
    alert(result.detalle || 'No se pudo registrar el alumno');
    return;
  }

  form.reset();
  await listAlumnos();
  alert(`Alumno registrado: ${result.nombre_completo}`);
});

document.getElementById('filtrar-alumnos').addEventListener('click', listAlumnos);
document.getElementById('refresh-alumnos').addEventListener('click', listAlumnos);
document.getElementById('refresh-alertas').addEventListener('click', consultarAlertas);

document.getElementById('asistencia-form').addEventListener('submit', async (event) => {
  event.preventDefault();
  const form = event.currentTarget;
  const raw = form.registros.value.trim();

  let registros;
  try {
    registros = JSON.parse(raw);
  } catch (error) {
    alert('La lista de asistencia debe ser un JSON válido.');
    return;
  }

  const payload = {
    anio: form.anio.value,
    division: form.division.value,
    fecha: form.fecha.value,
    registros,
  };

  const response = await fetch(`${API_PREFIX}/asistencia`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  const result = await response.json();
  if (!response.ok) {
    alert(result.detalle || 'No se pudo registrar la asistencia');
    return;
  }

  form.reset();
  await consultarAlertas();
  alert(`Asistencia registrada: ${result.cantidad_registrados} alumnos`);
});

listAlumnos();
consultarAlertas();
