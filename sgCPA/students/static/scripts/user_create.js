$(document).ready(function() {
    // Escuchar el evento de cambio en el campo id_person
    $('#id_person').on('change', function() {
        console.log('Cambio');
        console.log($('#id_person').val());
        if ($('#id_person').val() == '') {
            $('#id_username').val('');
            $('#id_password').val('');
            $('#id_password2').val('');
        } else {
            // Obtener el objeto seleccionado
            var person = $('#id_person option:selected').text();
            // Dividir el texto en nombre y apellido
            var names = person.split(' ');
            // Construir el nombre de usuario usando la primera letra del nombre y el apellido
            var username = names[0].charAt(0) + names[1];
            // Establecer el valor del campo de nombre de usuario
            $('#id_username').val(username.toLowerCase());

            var password = names[0].charAt(0) + names[1] + '123';
            $('#id_password').val(password.toLowerCase());
            $('#id_password2').val(password.toLowerCase());
        }
    });

    // Ejecutar el evento de cambio una vez al cargar la página
    $('#id_person').change();
});
