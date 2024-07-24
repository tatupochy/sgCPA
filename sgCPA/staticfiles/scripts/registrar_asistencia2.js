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
    const form = d.getElementById('attendanceForm2');
    const successMessage = d.getElementById('successMessage2');

    select.addEventListener('change', async(e) => {
        const target = e.target.value;
        console.log( target)
        const cursoResponse = await fetch(`/obtener_fechas_curso2/${target}`);
        console.log( cursoResponse)
        const { fecha } = await cursoResponse.json();

        if (fecha) {
            inputFecha.disabled = false;
            inputFecha.innerHTML = '';

            const option = d.createElement('option');
            option.text = fecha;
            option.value = fecha;
            option.selected = true;
            inputFecha.append(option);

            inputFecha.value = fecha;

            const event = new Event('change');
            inputFecha.dispatchEvent(event);
        } else {
            inputFecha.disabled = true;
            inputFecha.innerHTML = '<option>Seleccionar fecha</option>';
        }
    });

    inputFecha.addEventListener('change', async(e) => {
        const inputs = tabla_asistencias.querySelectorAll('tbody tr td input');
        const curso = d.getElementById('curso').value;
        console.log( curso )
        const body = JSON.stringify({ value: e.target.value });
        const response = await fetch(`/obtener_asistencias/${curso}`, { method: 'POST', headers, body });
        const { asistencias } = await response.json();
        console.log( { asistencias } )
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
                checkbox.checked = (asistencia.presente == 'A' || asistencia.presente == 'Indefinido') ? false : true;
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
            tabla_asistencias.innerHTML = '';
        }

        if (inputFecha) {
            inputs.forEach((input) => input.disabled = false);
        } else {
            inputs.forEach((input) => input.disabled = true);
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


});
