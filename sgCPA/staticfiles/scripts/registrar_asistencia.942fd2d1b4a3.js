document.addEventListener('DOMContentLoaded', () => {

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrftoken = getCookie('csrftoken');
    const headers = {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken
    }

    const d = document;
    const select = d.getElementById('curso');
    const inputFecha = d.getElementById('fecha');
    const tabla_asistencias = d.getElementById('asistencias_body');
    const form = d.getElementById('attendanceForm');
    const successMessage = d.getElementById('successMessage');


    select.addEventListener('change', async(e) => {
        const target = e.target.value;
        const cursoResponse = await fetch(`/obtener_fechas_curso/${target}`);
        const { fechas } = await cursoResponse.json();
        const today = new Date().toISOString().split('T')[0];
        
        if (fechas.length > 0) {
            inputFecha.disabled = false;
            inputFecha.innerHTML = '';
            fechas.forEach(fecha => {
                const parts = fecha.split('/');
                const fechaDate = new Date(parts[2], parts[1] - 1, parts[0]);
                if (fechaDate <= new Date()) {
                    const option = d.createElement('option');
                    option.text = fecha;
                    option.value = fecha;
                    inputFecha.append(option);
                }
            });
            inputFecha.value = today;
            const event = new Event('change');
            inputFecha.dispatchEvent(event);
        } else {
            inputFecha.disabled = true;
            inputFecha.innerHTML = '<option>Seleccionar fecha</option>';
        }
    });

    inputFecha.addEventListener('change', async(e) => {
        const curso = select.value;
        const fechaSeleccionada = e.target.value;
        const body = JSON.stringify({ value: fechaSeleccionada });
        
        try {
            const response = await fetch(`/obtener_asistencias/${curso}`, {
                method: 'POST',
                headers,
                body
            });
            
            if (!response.ok) {
                console.error('Error en la respuesta:', response.statusText);
                return;
            }

            const data = await response.json();
            const { asistencias } = data;
            console.log( { asistencias })
            tabla_asistencias.innerHTML = '';
            const fragment = d.createDocumentFragment();
            

            if (asistencias.length > 0) {
                asistencias.forEach(asistencia => {
                    const tr = d.createElement('tr');
                    const tdName = d.createElement('td');
                    const tdLastName = d.createElement('td');
                    const tdCi = d.createElement('td');
                    const tdAttendance = d.createElement('td');
                    const checkbox = d.createElement('input');
                    checkbox.type = 'checkbox';
                    checkbox.checked = asistencia.presente === 'P';
                    checkbox.name = asistencia.id_alumno;
                    tdName.textContent = asistencia.nombre;
                    tdLastName.textContent = asistencia.apellido;
                    tdCi.textContent = asistencia.ci;
                    tdAttendance.append(checkbox);
                    tr.append(tdName);
                    tr.append(tdLastName);
                    tr.append(tdCi);
                    tr.append(tdAttendance);
                    fragment.append(tr);
                });
                tabla_asistencias.append(fragment);
            } else {
                tabla_asistencias.innerHTML = ''; // Limpiar la tabla antes de agregar nuevos datos
            }
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    });

   // mensaje de confirmacion cuando se guarda
   form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(form);
    const response = await fetch(form.action, {
        method: 'POST',
        body: formData,
        headers: { 'X-CSRFToken': csrftoken }
    });

    if (response.ok) {
        successMessage.classList.remove('d-none');
        setTimeout(() => {
            successMessage.classList.add('d-none');
        }, 4000);
    } else {
        console.error('Error en la respuesta del servidor:', response.statusText);
    }
});


} );
