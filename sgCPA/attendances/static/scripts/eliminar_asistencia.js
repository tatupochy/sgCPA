document.addEventListener('DOMContentLoaded', function() {
    const deleteButtons = document.querySelectorAll('.delete-button');

    deleteButtons.forEach(button => {
        button.addEventListener('click', async function() {
            const asistenciaId = button.dataset.asistenciaId;

            try {
                // Obtener el token CSRF del elemento csrfmiddlewaretoken en el formulario HTML
                const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

                // Enviar la solicitud DELETE para eliminar la asistencia
                const response = await fetch(`/eliminar_asistencia/${asistenciaId}/`, {
                    method: 'DELETE',
                    headers: {
                        'X-CSRFToken': csrfToken
                    }
                });

                // Verificar si la eliminación fue exitosa
                if (response.ok) {
                    // Recargar la página para actualizar la lista de asistencias
                    window.location.reload();
                    // Mostrar mensaje de confirmación
                    document.getElementById('mensaje-confirmacion').style.display = 'block';
                    setTimeout(function() {
                        document.getElementById('mensaje-confirmacion').style.display = 'none';
                    }, 3000); // 3000 milisegundos = 3 segundos
                    
                } else {
                    // Manejar errores de eliminación
                    console.error('Error al eliminar la asistencia');
                    alert('Error al eliminar la asistencia');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Error al eliminar la asistencia');
            }
        });
    });
});
