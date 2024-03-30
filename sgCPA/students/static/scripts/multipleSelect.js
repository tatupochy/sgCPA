document.addEventListener('DOMContentLoaded', function() {
    const selectElement = document.querySelector('#multiple-select-field');
    const width = selectElement.dataset.width ? selectElement.dataset.width : selectElement.classList.contains('w-100') ? '100%' : 'style';
    const placeholder = selectElement.dataset.placeholder;

    // Inicializar Select2
    // const select = new select(selectElement, {
    //     theme: "bootstrap-5",
    //     width: width,
    //     placeholder: placeholder,
    //     closeOnSelect: false
    // });
     Select2(selectElement, {
        theme: "bootstrap-5",
        width: width,
        placeholder: placeholder,
        closeOnSelect: false
    });

    // // Escuchar cambios en el elemento select para actualizar Select2
    // selectElement.addEventListener('change', function() {
    //     select.triggerChange();
    // });
});