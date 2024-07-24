document.addEventListener('DOMContentLoaded', () => {

    function differenceInDays(date1, date2) {
        const oneDayInMilliseconds = 24 * 60 * 60 * 1000; // Un día en milisegundos
        const differenceInMilliseconds = date1.getTime() - date2.getTime();
        return differenceInMilliseconds / oneDayInMilliseconds;
    }

    // Verifica si la diferencia entre date1 y date2 es mayor a n días
    function isMoreThanNDaysApart(date1, date2, n) {
        return differenceInDays(date1, date2) > n;
    }


    const d = document;

    const curso = d.getElementById('id_course')
    const id_enrollment_amount = d.getElementById('id_enrollment_amount')
    const id_fee_amount = d.getElementById('id_fee_amount')
    const minStudentsNumber = d.getElementById('minStudentsNumber')
    const maxStudentsNumber = d.getElementById('maxStudentsNumber')
    // const id_enrollment_date = d.getElementById('id_enrollment_date')
    const today = new Date().toISOString().split('T')[0];
    const space_available = d.getElementById('space_available')
    const student_quantity = d.getElementById('student_quantity')
    const ci_button = d.getElementById('ci_button')
    const ci_input = d.getElementById('ci_input')
    const create_enrollment_button = d.getElementById('create_enrollment_button')
    const enrollment_form = d.getElementById('enrollment_form')
    const student_id = d.getElementById('student_id')
    const notFoundStudent = d.getElementById('notFoundStudent')

    const enrollment_start = d.getElementById('enrollment_start_date');
    const enrollment_end = d.getElementById('enrollment_end_date');

    const start_date = d.getElementById('start_date');
    const end_date = d.getElementById('end_date');

    const succes_message = d.getElementById('succes_message');


    let courseId;
    let student_list;

    curso.addEventListener('change', async (e) => {
        const value = e.target.value;
        courseId = value;
        const url = `/obtener_curso/${value}`
        const response = await fetch(url)
        const { course_data } = await response.json()
        // enrollment_start.disabled = false;
        enrollment_end.disabled = false;
        create_enrollment_button.disabled = false;
        id_enrollment_amount.value = course_data.enrollment_amount;
        id_fee_amount.value = course_data.fee_amount;
        minStudentsNumber.value = course_data.minStudentsNumber;
        maxStudentsNumber.value = course_data.maxStudentsNumber;
        space_available.value = course_data.space_available;
        start_date.value = course_data.start_date;
        end_date.value = course_data.end_date;

   


    })



    const errorTimeouts = {}; // Objeto para almacenar los timeouts

    enrollment_form.addEventListener('submit', async(e) => {
        e.preventDefault();
        let validation = true; // Inicializa la validación como verdadera
    
        const enrollment_start_date = new Date(enrollment_start.value);
        const enrollment_end_date = new Date(enrollment_end.value);
        const start_date_date = new Date(start_date.value);
        const end_date_date = new Date(end_date.value);
    
        // Función para mostrar mensajes de error con timeout
        const showErrorWithTimeout = (element, message) => {
            const errorSpan = element.nextElementSibling;
            errorSpan.textContent = message;
    
            // Si existe un timeout anterior, cancelarlo
            if (errorTimeouts[element.id]) {
                clearTimeout(errorTimeouts[element.id]);
            }
    
            // Establecer un nuevo timeout para limpiar el mensaje después de 2 segundos
            errorTimeouts[element.id] = setTimeout(() => {
                errorSpan.textContent = '';
                delete errorTimeouts[element.id]; // Limpiar referencia del timeout
            }, 7000);
        };
    
        // Validaciones
        if (enrollment_start_date > enrollment_end_date) {
            showErrorWithTimeout(enrollment_end, 'La fecha fin de matriculación no puede ser menor a la fecha inicio de matriculación');
            validation = false;
        }
    
        if (enrollment_start_date > start_date_date) {
            showErrorWithTimeout(enrollment_start, 'La fecha inicio de matriculación no puede ser mayor a la fecha de inicio de clases');
            validation = false;
        }
    
        if (isMoreThanNDaysApart(enrollment_end_date, start_date_date, 10)) {
            showErrorWithTimeout(enrollment_end, 'La fecha fin de matriculación no puede ser mayor a una semana y media después del inicio de clases');
            validation = false;
        }
    
        // Si todas las validaciones son correctas, proceder con el envío del formulario
        if (validation) {
            try {
                // Crear objeto FormData para enviar los datos del formulario
                const formData = new FormData(enrollment_form);
    
                // Enviar la solicitud
                create_enrollment_button.disabled = true;
                const response = await fetch(enrollment_form.action, {
                    method: 'POST',
                    body: formData
                });

                console.log(response)
    
                if (response.ok) {
                    succes_message.textContent = 'Matrícula creada con éxito';
                    console.log(response)
                    const json = await response.json()
                    console.log(json)
                    
                     setTimeout(() => {
                        window.location.href = `/enrollments/${json.id}`;
                    }, 2000);
                } else {
                    throw new Error('Error en el envío del formulario');
                }
            } catch (error) {
                console.error('Error:', error);
                
            }
        }
    })

})
