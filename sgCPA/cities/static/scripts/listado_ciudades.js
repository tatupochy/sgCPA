const d = document;

d.addEventListener('DOMContentLoaded', () => {
    const buttons = d.querySelectorAll('.btn-danger')
    const addButton = d.getElementById('add')
    const editButtons = d.querySelectorAll('.editar')
    const searchButton = d.getElementById('searchButton')
    const searchInput = d.getElementById('searchInput')

    searchButton.addEventListener('click', async(e) => {
        const value = searchInput.value;
        if(value){
            window.location.href = `/listado_ciudades/buscar/${value}`
        }else{
            window.location.href = `/listado_ciudades`
        }
    })


    buttons.forEach(button => {
        button.addEventListener('click', (e) => {
            const id = e.target.dataset.id
            window.location.href = `/borrar_ciudad/${id}`
        })
    })


    addButton.addEventListener('click', () => {
        window.location.href = '/registrar_ciudad'
    })

    editButtons.forEach(editButton => {
         editButton.addEventListener('click', () => {
             const id = editButton.dataset.id;
             window.location.href = `/editar_ciudad/${id}`
         })
     })
})
