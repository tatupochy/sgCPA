document.addEventListener('DOMContentLoaded', () => {

    // Función para calcular la diferencia en días entre dos fechas
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

    const start_date = d.getElementById('start_date')
    const end_date = d.getElementById('end_date')
    const enrollment_start_date = d.getElementById('enrollment_start_date')
    const enrollment_end_date = d.getElementById('enrollment_end_date')
    
    const form = d.getElementById('cursoForm')
    
    form.addEventListener('submit', (e) => {
        let isValid = true; // Flag para rastrear si todas las validaciones son exitosas

        e.preventDefault()
        const errors = d.querySelectorAll('.error-message')

        errors.forEach(error => {
            error.textContent = '';
        })

        const startDateValue = new Date(start_date.value);
        const endDateValue = new Date(end_date.value);
        const enrollmentStartDateValue = new Date(enrollment_start_date.value);
        const enrollmentEndDateValue = new Date(enrollment_end_date.value);


        if (startDateValue > endDateValue) {
            const errorSpan = start_date.nextElementSibling;
            errorSpan.textContent = 'La fecha inicio de clases no puede ser mayor a la fecha fin de clases'
            isValid = false;
        }

        if (enrollmentStartDateValue > enrollmentEndDateValue) {
            const errorSpan = enrollment_start_date.nextElementSibling;
            errorSpan.textContent = 'La fecha inicio de matriculacion no puede ser mayor a la fecha fin de matriculacion'
            isValid = false;
        }


        if (isMoreThanNDaysApart(enrollmentEndDateValue, startDateValue, 7)) {
            const errorSpan = enrollment_end_date.nextElementSibling;
            errorSpan.textContent = 'La fecha fin de matriculacion no puede ser mayor a una semana despues del inicio de clases'
            isValid = false;
        }

        if (enrollmentStartDateValue >= startDateValue) {
            const errorSpan = enrollment_start_date.nextElementSibling;
            errorSpan.textContent = 'La fecha inicio de matriculacion no puede ser mayor o igual a la fecha de inicio de clases'
            isValid = false;
        }

        if(isValid){
            form.submit()
        }

    })


})