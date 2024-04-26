import * as yup from 'https://cdn.jsdelivr.net/npm/yup@1.4.0/+esm';

const d = document;

d.addEventListener('DOMContentLoaded', () => {
    const form = d.getElementById('form');
    let formSubmitted = false; // Bandera para indicar si el formulario ha sido enviado

    // const schema = yup.object().shape({
    //     name: yup.string().required('El nombre es requerido'),
    //     lastName: yup.string().required('El apellido es requerido'),
    //     birthDate: yup.string().required('La fecha de nacimiento es requerida'),
    //     inscriptionDate: yup.string().required('La fecha de inscripcion es obligatoria'),
    //     ciNumber: yup.string().required('El número de cédula es requerido'),
    //     phone: yup.string().required('El número de teléfono es requerido'),
    //     city: yup.string().required('La ciudad es requerida'),
    //     email: yup.string().email('Ingresa un correo electrónico válido').required('El correo electrónico es requerido'),
    //     fatherPhone: yup.string().required('El número de teléfono del padre es requerido'),
    //     motherPhone: yup.string().required('El número de teléfono de la madre es requerido'),
    // });

    // Función para mostrar mensajes de error
    // const displayError = (inputName, errorMessage) => {
    //     const field = document.getElementById(inputName);
    //     if (field) {
    //         let errorElement = field.nextElementSibling;
    //         if (!errorElement || !errorElement.classList.contains('error-message')) {
    //             errorElement = document.createElement('span');
    //             errorElement.classList.add('error-message');
    //             errorElement.style.color = 'red'; // Establecer el color del mensaje de error en rojo
    //             field.parentNode.insertBefore(errorElement, field.nextSibling);
    //         }
    //         errorElement.textContent = errorMessage;
    //     }
    //     field.classList.add('is-invalid')
    // };

    // Función para limpiar mensajes de error
    // const clearErrors = () => {
    //     const errorElements = document.querySelectorAll('.error-message');
    //     errorElements.forEach(element => {
    //         const inputField = element.previousElementSibling;
    //         element.textContent = '';
    //         inputField.classList.remove('is-invalid')
    //     });
    // };

    // Función para validar el formulario
    // const validateForm = (focusInputs = true) => {

    //     const formData = {
    //         name: form.elements['name'].value,
    //         lastName: form.elements['lastName'].value,
    //         birthDate: form.elements['birthDate'].value,
    //         inscriptionDate: form.elements['inscriptionDate'].value,
    //         ciNumber: form.elements['ciNumber'].value,
    //         phone: form.elements['phone'].value,
    //         city: form.elements['city'].value,
    //         email: form.elements['email'].value,
    //         fatherPhone: form.elements['fatherPhone'].value,
    //         motherPhone: form.elements['motherPhone'].value,
    //     };

    //     clearErrors(); // Limpiar mensajes de error antes de validar

    //     schema.validate(formData, { abortEarly: false })
    //         .then(async () => {
    //             if (focusInputs) {
    //                 const res = await fetch(form.action, {
    //                     method: 'POST',
    //                     body: new FormData(form)
    //                 })
    //                 if (!res.ok) {
    //                     const error = d.createElement('div')
    //                     error.textContent = 'Error en uno de los campos enviados.'
    //                     error.style.color = 'red'
    //                     error.style.textAlign = 'center'
    //                     form.append(error)

    //                     setTimeout(() => {
    //                         error.remove();
    //                     }, 3000)
    //                 } else {
    //                     const success = d.createElement('div')
    //                     success.textContent = 'Alumno Actualizado correctamente!'
    //                     success.style.color = 'green'
    //                     success.style.textAlign = 'center'
    //                     form.append(success)
    //                     // form.reset()

    //                     setTimeout(() => {
    //                         window.location.href = '/listado_alumnos'
    //                         success.remove();
    //                     }, 500)
    //                 }
    //             }
    //         })
    //         .catch(errors => {
    //             if (errors.inner.length > 0) {
    //                 errors.inner.forEach((error, index) => {
    //                     const inputName = error.path;
    //                     const errorMessage = error.message;
    //                     displayError(inputName, errorMessage);
    //                     if (focusInputs) {
    //                         const firstErrorField = d.getElementById(errors.inner[0].path);
    //                         firstErrorField.focus()
    //                     }
    //                 });
    //             }
    //         });
    // };

    // Evento submit del formulario
    // form.addEventListener('submit', (e) => {
    //     e.preventDefault();
    //     formSubmitted = true; // Establecer la bandera de formulario enviado a true
    //     validateForm();
    // });

    // // Evento input de cada campo de entrada
    // const inputs = form.querySelectorAll('input');
    // inputs.forEach(input => {
    //     input.addEventListener('input', () => {
    //         if (formSubmitted) { // Ejecutar las validaciones solo si el formulario ha sido enviado al menos una vez
    //             validateForm(false); // No enfocar los inputs en el evento input
    //         }
    //     });
    // });
});
