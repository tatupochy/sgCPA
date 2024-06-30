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

    const d = document;
    const fecha = d.getElementById('fecha');
    const curso = d.getElementById('curso');
    const tabla_asistencias = d.getElementById('asistencias_body');
    const csrftoken = getCookie('csrftoken');
    const headers = {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken
    };

    let table;

    curso.addEventListener('change', async (e) => {
        const curso = e.target.value;
        fecha.disabled = true;
        fecha.innerHTML = '';
        tabla_asistencias.innerHTML = '';  // Limpia la tabla cuando se cambia el curso
        const response = await fetch(`/obtener_fechas_curso/${curso}`);
        const { fechas } = await response.json();
        if (fechas.length > 0) {
            const fragment = d.createDocumentFragment();
            const defaultOption = d.createElement('option');
            defaultOption.textContent = 'Seleccionar una fecha';
            defaultOption.selected = true;
            defaultOption.disabled = true;
            fragment.append(defaultOption);
            fechas.map((fecha) => {
                const parts = fecha.split('/');
                const currentDate = new Date();
                const fechaDate = new Date(parts[2], parts[1] - 1, parts[0]);
                if (fechaDate <= currentDate) {
                    const option = d.createElement('option');
                    option.text = fecha;
                    option.value = fecha;
                    fragment.append(option);
                }
            });
            fecha.append(fragment);
            fecha.disabled = false;
        } else {
            fecha.disabled = true;
            fecha.innerHTML = '';
        }
    });

    fecha.addEventListener('change', async (e) => {
        const value = e.target.value;
        const courseId = d.getElementById('curso').value;
        const body = JSON.stringify({ value });
        const response = await fetch(`/obtener_asistencias/${courseId}`, { method: 'POST', headers, body });
        const { asistencias } = await response.json();

        // Limpia el contenido actual de la tabla antes de agregar nuevos datos
        tabla_asistencias.innerHTML = '';
        if (table) {
            // Destruye la instancia previa de DataTables si existe
            table.clear().destroy();
        }

        const fragment = d.createDocumentFragment();
        if (asistencias.length > 0) {
            asistencias.map(asistencia => {
                const tr = d.createElement('tr');
                const tdName = d.createElement('td');
                const tdLastName = d.createElement('td');
                const tdCi = d.createElement('td');
                const tdAttendance = d.createElement('td');
                tdName.textContent = asistencia.nombre;
                tdLastName.textContent = asistencia.apellido;
                tdCi.textContent = asistencia.ci;
                tdAttendance.textContent = asistencia.presente;
                tr.append(tdName);
                tr.append(tdLastName);
                tr.append(tdCi);
                tr.append(tdAttendance);
                fragment.append(tr);
            });
        }
        tabla_asistencias.append(fragment);

        // Inicializa DataTables de nuevo con los nuevos datos
        table = $('#asistencias_table').DataTable({
            dom: 'Bfrtip',
            searching: true,
            buttons: [
                'copy', 'excel', 'csv',
                {
                    text: 'PDF',
                    action: function ( e, dt, button, config ) {
                        const courseId = d.getElementById('curso').value;
                        const fecha = d.getElementById('fecha').value;
                        
                        fetch(`/descargar_asistencias_pdf/`, {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                                'X-CSRFToken': csrftoken
                            },
                            body: JSON.stringify({ curso_id: courseId, fecha: fecha })
                        })
                        .then(response => response.blob())
                        .then(blob => {
                            const url = window.URL.createObjectURL(blob);
                            const a = document.createElement('a');
                            a.href = url;
                            a.download = `asistencias_${courseId}_${fecha}.pdf`;
                            document.body.appendChild(a);
                            a.click();
                            a.remove();
                        })
                        .catch(error => console.error('Error al generar el PDF:', error));
                    }
                }

            ]
        });
    });
});
