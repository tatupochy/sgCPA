const d = document;

d.addEventListener('DOMContentLoaded', () => {
    const deleteButton = d.getElementById('delete')
    const buttons = d.querySelectorAll('.btn-danger')
    const addButton = d.getElementById('add')
    const editButtons = d.querySelectorAll('.editar')


    buttons.forEach(button => {
        button.addEventListener('click', () => {
            deleteButton.dataset.id = button.dataset.id;
        })
    })

    deleteButton.addEventListener('click', async(e) => {
        const id = deleteButton.dataset.id
        await fetch(`eliminar/${id}`)
        const tbody = d.getElementById('tbody')
        const elementToDelete = d.getElementById(id);
        if(elementToDelete) tbody.removeChild(elementToDelete)
    })

    addButton.addEventListener('click', () => {
        window.location.href = '/registrar_alumno'
    })

    editButtons.forEach(editButton => {
        editButton.addEventListener('click', () => {
            const id = editButton.dataset.id;
            window.location.href = `/editar_alumno/${id}`
        })
    })
})
