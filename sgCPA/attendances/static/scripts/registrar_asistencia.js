//sgCPA\attendances\static\scripts\registrar_asistencia.js
// Función para actualizar la lista de alumnos
async function actualizarListaAlumnos(cursoId) {
    const response = await fetch(`/alumnos_por_curso/${cursoId}`);
    const alumnos = await response.json();
    const table = document.getElementById("tabla-asistencia");
    table.innerHTML = ""; // Limpiar contenido anterior de la tabla

    for (let i = 0; i < alumnos.length; i++) {
        const alumno = alumnos[i];
        const row = document.createElement("tr");

        const cellNombre = document.createElement("td");
        cellNombre.textContent = alumno.nombre;

        const cellApellido = document.createElement("td");
        cellApellido.textContent = alumno.apellido;
        
        const cellCi = document.createElement("td");
        cellCi.textContent = alumno.ci;


        const cellCheckbox = document.createElement("td");
        const checkbox = document.createElement("input");
        checkbox.type = "checkbox";
        checkbox.name = "presente_" + alumno.id;
        checkbox.value = "presente";
        checkbox.addEventListener('change', function() {
            checkbox.value = this.checked ? 'true' : 'false'; // Establecer el valor del checkbox como 'true' o 'false' según esté marcado o desmarcado
        });
        cellCheckbox.appendChild(checkbox);

        row.appendChild(cellNombre);
        row.appendChild(cellApellido);
        row.appendChild(cellCi);
        row.appendChild(cellCheckbox);
        table.appendChild(row);
    }
}

// Agregar un evento `change` al campo de selección de curso
$('#curso').change(function() {
    var cursoId = $(this).val();
    actualizarListaAlumnos(cursoId);
});

// Actualizar la lista de alumnos al cargar la página
$(document).ready(function() {
    var cursoId = $('#curso').val();
    actualizarListaAlumnos(cursoId);
});


document.addEventListener('DOMContentLoaded', () => {
    const d = document;
    const select = d.getElementById('curso')
    const inputFecha = d.getElementById('fecha')

    select.addEventListener('change', async(e) => {
        const target = e.target.value;
        const curso = await fetch(`/obtener_curso/${target}`)
        const { rango } = await curso.json()
        const inicio = rango.inicio
        const fin = rango.fin
        const today = new Date().toISOString().split('T')[0];
        if(curso){
            inputFecha.disabled = false
            inputFecha.min = inicio;
            inputFecha.max = fin;
            inputFecha.value = today;
        }else{
            inputFecha.disabled = true
        }

    })
})