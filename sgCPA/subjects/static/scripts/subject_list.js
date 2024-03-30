const d = document;

d.addEventListener('DOMContentLoaded', () => {
    const deleteButton = d.getElementById('delete')
    const buttons = d.querySelectorAll('.btn-danger')
    const searchButton = d.getElementById('searchButton')
    const searchInput = d.getElementById('searchInput')

    searchButton.addEventListener('click', async(e) => {
        const value = searchInput.value;
        if(value){
            window.location.href = `/listado_materias/buscar/${value}`
        }else{
            window.location.href = `/listado_materias`
        }
    })


    buttons.forEach(button => {
        button.addEventListener('click', () => {
            deleteButton.dataset.id = button.dataset.id;
        })
    })

    deleteButton.addEventListener('click', async(e) => {
        const id = deleteButton.dataset.id
        await fetch(`/eliminar_materia/${id}`)
        window.location.reload()
    })
})
