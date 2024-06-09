// document.getElementById('curso').addEventListener('change', function() {
//     var cursoId = this.value;
//     var mesesContainer = document.getElementById('meses-container');
//     var mesSelect = document.getElementById('mes');

//     if (cursoId) {
//         fetch(`/obtener_meses_curso/${cursoId}/`)
//             .then(response => response.json())
//             .then(json => console.log(json))
//             // .then(data => {
//             //     mesSelect.innerHTML = '<option value="">Seleccione un mes</option>';
//             //     data.meses_curso.forEach(function(mes) {
//             //         var option = document.createElement('option');
//             //         option.value = mes[0];
//             //         option.text = mes[1];
//             //         mesSelect.appendChild(option);
//             //     });
//             //     mesesContainer.style.display = 'block';
//             // });
//     } else {
//         mesesContainer.style.display = 'none';
//     }
// });

// document.addEventListener('DOMContentLoaded', function() {
//     if (document.getElementById('mes').options.length > 1) {
//         document.getElementById('meses-container').style.display = 'block';
//     }
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


    const d = document;
    const fecha = d.getElementById('fecha')
    const curso = d.getElementById('curso')
    curso.addEventListener('change', async(e) => {
        const curso = e.target.value;
        fecha.disabled = true;
        fecha.innerHTML = ''
        const response = await fetch(`/obtener_fechas_curso/${curso}`)
        const {fechas} = await response.json()
        if(fechas.length > 0){
            const fragment = d.createDocumentFragment()
            const defaultOption = d.createElement('option')
            defaultOption.textContent = 'Seleccionar una fecha'
            defaultOption.selected = true;
            fragment.append(defaultOption)
            fechas.map((fecha) => {
                const option = d.createElement('option')
                option.text = fecha
                option.value = fecha
                fragment.append(option)
            })
            fecha.append(fragment)
            fecha.disabled = false;
        }else{
            fecha.disabled = true;
            fecha.innerHTML = ''
        }

    })

    fecha.addEventListener('change', async(e) => {
        const value = e.target.value
        const csrftoken = getCookie('csrftoken');
        const courseId = d.getElementById('curso').value
        const response = await fetch(`/obtener_asistencias/${courseId}`, 
            {method: 'POST', headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            }, body: JSON.stringify({value}), 
            }
        )
        const {asistencias} = await response.json()
        const tabla_asistencias = d.getElementById('asistencias_body')
        const fragment = d.createDocumentFragment()
        if(asistencias.length > 0){
            asistencias.map(asistencia => { 
                const tr = d.createElement('tr')
                const tdName = d.createElement('td')
                const tdLastName = d.createElement('td')
                const tdCi = d.createElement('td')
                const tdAttendance = d.createElement('td')
                console.log(asistencia)
                tdName.textContent = asistencia.nombre;
                tdLastName.textContent  = asistencia.apellido
                tdCi.textContent  = asistencia.ci
                tdAttendance.textContent  = asistencia.presente
                tr.append(tdName)
                tr.append(tdLastName)
                tr.append(tdCi)
                tr.append(tdAttendance)
                fragment.append(tr)
            })
            tabla_asistencias.innerHTML = ''; // Limpiar la tabla antes de agregar nuevos datos
            tabla_asistencias.append(fragment)
        }else{
            tabla_asistencias.innerHTML = ''; // Limpiar la tabla antes de agregar nuevos datos
        }
    })
   
})