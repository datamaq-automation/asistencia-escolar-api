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

const renderHistorial = (historial) => {
  const container = document.getElementById('historial-container');

  if (!historial.acciones || historial.acciones.length === 0) {
    container.innerHTML = '<div class="alert alert-light mb-0">No hay acciones registradas para este alumno.</div>';
    return;
  }

  container.innerHTML = historial.acciones.map((accion) => `
    <div class="list-group-item">
      <div class="d-flex justify-content-between align-items-center">
        <strong>${accion.tipo_accion}</strong>
        <span class="badge bg-secondary">${accion.rol_autor}</span>
      </div>
      <div class="small text-muted mt-1">${accion.fecha}</div>
      <div class="mt-2">${accion.descripcion}</div>
      <div class="small text-muted mt-1">Por: ${accion.realizado_por}</div>
    </div>
  `).join('');
};

const renderSeguimiento = (seguimiento) => {
  const container = document.getElementById('seguimiento-container');

  if (!seguimiento.alumnos_en_seguimiento || seguimiento.alumnos_en_seguimiento.length === 0) {
    container.innerHTML = '<div class="alert alert-light mb-0">No hay alumnos en seguimiento para este límite.</div>';
    return;
  }

  container.innerHTML = seguimiento.alumnos_en_seguimiento.map((alumno, index) => `
    <div class="accordion-item">
      <h2 class="accordion-header" id="heading-${index}">
        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapse-${index}">
          ${alumno.nombre_completo} · ${alumno.anio} ${alumno.division}
        </button>
      </h2>
      <div id="collapse-${index}" class="accordion-collapse collapse" data-bs-parent="#seguimiento-container">
        <div class="accordion-body">
          <p class="mb-2"><strong>Faltas injustificadas:</strong> ${alumno.cantidad_faltas_injustificadas}</p>
          <ul class="mb-0">
            ${(alumno.acciones || []).map((accion) => `<li>${accion.tipo_accion} - ${accion.descripcion}</li>`).join('') || '<li>Sin acciones registradas.</li>'}
          </ul>
        </div>
      </div>
    </div>
  `).join('');
};

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

const consultarHistorial = async () => {
  const alumnoId = document.getElementById('historial-alumno-id').value;
  if (!alumnoId) {
    alert('Ingresá el ID del alumno para consultar el historial.');
    return;
  }

  const response = await fetch(`${API_PREFIX}/alumnos/${alumnoId}/acciones`);
  const data = await response.json();

  if (!response.ok) {
    alert(data.detalle || 'No se pudo consultar el historial');
    return;
  }

  renderHistorial(data);
};

const consultarSeguimiento = async () => {
  const limite = document.getElementById('limite-seguimiento').value || 5;
  const response = await fetch(`${API_PREFIX}/reportes/seguimiento?limite=${limite}`);
  const data = await response.json();

  if (!response.ok) {
    alert(data.detalle || 'No se pudo consultar el seguimiento');
    return;
  }

  renderSeguimiento(data);
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
document.getElementById('consultar-historial').addEventListener('click', consultarHistorial);
document.getElementById('refresh-seguimiento').addEventListener('click', consultarSeguimiento);

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
  await consultarSeguimiento();
  alert(`Asistencia registrada: ${result.cantidad_registrados} alumnos`);
});

document.getElementById('accion-form').addEventListener('submit', async (event) => {
  event.preventDefault();
  const form = event.currentTarget;
  const payload = {
    alumno_id: Number(form.alumno_id.value),
    tipo_accion: form.tipo_accion.value,
    descripcion: form.descripcion.value.trim(),
    realizado_por: form.realizado_por.value.trim(),
    rol_autor: form.rol_autor.value,
  };

  const response = await fetch(`${API_PREFIX}/acciones`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  const result = await response.json();
  if (!response.ok) {
    alert(result.detalle || 'No se pudo registrar la acción');
    return;
  }

  form.reset();
  document.getElementById('historial-alumno-id').value = payload.alumno_id;
  await consultarHistorial();
  await consultarSeguimiento();
  alert(`Acción registrada para el alumno ${payload.alumno_id}`);
});

listAlumnos();
consultarAlertas();
consultarSeguimiento();
