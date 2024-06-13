//sgCPA\attendances\static\scripts\registrar_asistencia.js
// Función para actualizar la lista de alumnos
// async function actualizarListaAlumnos(cursoId) {
//     const response = await fetch(`/alumnos_por_curso/${cursoId}`);
//     const alumnos = await response.json();
//     const table = document.getElementById("tabla-asistencia");
//     table.innerHTML = ""; // Limpiar contenido anterior de la tabla

//     for (let i = 0; i < alumnos.length; i++) {
//         const alumno = alumnos[i];
//         const row = document.createElement("tr");

//         const cellNombre = document.createElement("td");
//         cellNombre.textContent = alumno.nombre;

//         const cellApellido = document.createElement("td");
//         cellApellido.textContent = alumno.apellido;
        
//         const cellCi = document.createElement("td");
//         cellCi.textContent = alumno.ci;


//         const cellCheckbox = document.createElement("td");
//         const checkbox = document.createElement("input");
//         checkbox.type = "checkbox";
//         checkbox.name =  alumno.id;
//         checkbox.value = "presente";
//         checkbox.disabled = true;
//         checkbox.addEventListener('change', function() {
//             checkbox.value = this.checked ? 'True' : 'False'; // Establecer el valor del checkbox como 'true' o 'false' según esté marcado o desmarcado
//         });
//         cellCheckbox.appendChild(checkbox);

//         row.appendChild(cellNombre);
//         row.appendChild(cellApellido);
//         row.appendChild(cellCi);
//         row.appendChild(cellCheckbox);
//         table.appendChild(row);
//     }
// }

// // Agregar un evento `change` al campo de selección de curso
// $('#curso').change(function() {
//     var cursoId = $(this).val();
//     actualizarListaAlumnos(cursoId);
// });

// // Actualizar la lista de alumnos al cargar la página
// $(document).ready(function() {
//     var cursoId = $('#curso').val();
//     actualizarListaAlumnos(cursoId);
// });


document.addEventListener('DOMContentLoaded', () => {


    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
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
    const select = d.getElementById('curso')
    const inputFecha = d.getElementById('fecha')
    const tabla_asistencias = d.getElementById('asistencias_body')

    select.addEventListener('change', async(e) => {
        const target = e.target.value;
        const curso = await fetch(`/obtener_fechas_curso/${target}`)
        const { fechas }  = await curso.json()
        const today = new Date().toISOString().split('T')[0];
        if(curso){
            inputFecha.disabled = false
            inputFecha.value = today;
            const fragment = d.createDocumentFragment()
            fechas.map((fecha, index) => {
                const option = d.createElement('option')
                option.text = fecha
                option.value = fecha
                fragment.append(option)
            })
            inputFecha.append(fragment)
            
        }else{
            inputFecha.disabled = true
        }
    })

    inputFecha.addEventListener('change', async(e) => {
        const inputs = tabla_asistencias.querySelectorAll('tbody tr td input')
        const curso = d.getElementById('curso').value
        const body = JSON.stringify({value: e.target.value})
        const response = await fetch(`/obtener_asistencias/${curso}`, {method: 'POST', headers, body})
        const {asistencias} = await response.json()
        tabla_asistencias.innerHTML = ''
        const fragment = d.createDocumentFragment()
        if(asistencias.length > 0){
            asistencias.map(asistencia => { 
                console.log(asistencia)
                const tr = d.createElement('tr')
                const tdName = d.createElement('td')
                const tdLastName = d.createElement('td')
                const tdCi = d.createElement('td')
                const tdAttendance = d.createElement('td')
                const checkbox = d.createElement('input')
                checkbox.type = 'checkbox'
                checkbox.checked = asistencia.presente == 'A' ? false : true
                checkbox.name =  asistencia.id_alumno;
                tdName.textContent = asistencia.nombre;
                tdLastName.textContent  = asistencia.apellido
                tdCi.textContent  = asistencia.ci
                tdAttendance.append(checkbox)
                tr.append(tdName)
                tr.append(tdLastName)
                tr.append(tdCi)
                tr.append(tdAttendance)
                fragment.append(tr)
            })
            tabla_asistencias.append(fragment)
        }else{
            tabla_asistencias.innerHTML = ''; // Limpiar la tabla antes de agregar nuevos datos
        }

        if(inputFecha){
            inputs.forEach((input) => input.disabled = false)
        }else{
            inputs.forEach((input) => input.disabled = true)
        }
    })

})