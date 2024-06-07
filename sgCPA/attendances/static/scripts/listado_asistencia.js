document.getElementById('curso').addEventListener('change', function() {
    var cursoId = this.value;
    var mesesContainer = document.getElementById('meses-container');
    var mesSelect = document.getElementById('mes');

    if (cursoId) {
        fetch(`/obtener_meses_curso/${cursoId}/`)
            .then(response => response.json())
            .then(data => {
                mesSelect.innerHTML = '<option value="">Seleccione un mes</option>';
                data.meses_curso.forEach(function(mes) {
                    var option = document.createElement('option');
                    option.value = mes[0];
                    option.text = mes[1];
                    mesSelect.appendChild(option);
                });
                mesesContainer.style.display = 'block';
            });
    } else {
        mesesContainer.style.display = 'none';
    }
});

document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('mes').options.length > 1) {
        document.getElementById('meses-container').style.display = 'block';
    }
});


document.addEventListener('DOMContentLoaded', () => {
    const d = document;
    const select = d.getElementById('mes')
    select.addEventListener('change', async(e) => {
        const value = e.target.value;
        console.log(value)
    })
})