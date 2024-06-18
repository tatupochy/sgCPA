document.addEventListener('DOMContentLoaded', () => {
    const d = document;

    const curso = d.getElementById('id_course')
    const student_table = d.getElementById('student_table').querySelector('tbody')
    const id_enrollment_amount = d.getElementById('id_enrollment_amount')
    const id_fee_amount = d.getElementById('id_fee_amount')
    const minStudentsNumber = d.getElementById('minStudentsNumber')
    const maxStudentsNumber = d.getElementById('maxStudentsNumber')
    const id_enrollment_date = d.getElementById('id_enrollment_date')
    const today = new Date().toISOString().split('T')[0];
    const space_available = d.getElementById('space_available')
    const student_quantity = d.getElementById('student_quantity')
    const ci_button = d.getElementById('ci_button')
    const ci_input = d.getElementById('ci_input')

    let courseId;
    let student_list;

    curso.addEventListener('change', async (e) => {
        const value = e.target.value;
        courseId = value;
        id_enrollment_date.value = today;
        id_enrollment_date.max = today;
        if (value) {
            id_enrollment_date.disabled = false;
        } else {
            id_enrollment_date.disabled = true;
        }
        const url = `/obtener_curso/${value}`
        const response = await fetch(url)
        const { course_data } = await response.json()
        id_enrollment_date.min = course_data.enrollment_start_date;
        id_enrollment_amount.value = course_data.enrollment_amount;
        id_fee_amount.value = course_data.fee_amount;
        minStudentsNumber.value = course_data.minStudentsNumber;
        maxStudentsNumber.value = course_data.maxStudentsNumber;
        space_available.value = course_data.space_available;

        student_list = course_data.student_list;

        fillStudentTable(student_list)

    })

    ci_input.addEventListener('input', (e) => {
        // Obtener el valor actual del input
        const inputValue = e.target.value;

        // Remover caracteres no numéricos
        const numericValue = inputValue.replace(/\D/g, '');

        // Actualizar el valor del input con los caracteres numéricos
        ci_input.value = numericValue;
    })

    ci_button.addEventListener('click', async (e) => {
        const value = ci_input.value;
        if (!value) {
            fillStudentTable(student_list)
        } else {
            const url = `/obtener_alumno_por_ci/${value}/${courseId}`
            const response = await fetch(url)
            const json = await response.json()
            fillStudentTable(json)
        }
    })


    const fillStudentTable = (student_list) => {
        student_table.innerHTML = '';
        const fragment = d.createDocumentFragment()

        student_list.map((item) => {

            const tr = d.createElement('tr')
            const tdName = d.createElement('td')
            const tdLastName = d.createElement('td')
            const tdCI = d.createElement('td')
            const tdCheck = d.createElement('td')
            const checkbox = d.createElement('input')
            checkbox.type = 'checkbox';
            checkbox.name = item.id;
            checkbox.value = item.id;

            checkbox.addEventListener('change', (e) => {
                if (e.target.checked) {
                    student_quantity.value = parseInt(student_quantity.value) + 1;
                } else {
                    student_quantity.value = parseInt(student_quantity.value) - 1;
                }
            })
            tdName.textContent = item.name;
            tdLastName.textContent = item.lastName;
            tdCI.textContent = item.ciNumber;
            tdCheck.append(checkbox)
            tr.append(tdName)
            tr.append(tdLastName)
            tr.append(tdCI)
            tr.append(tdCheck)
            fragment.append(tr)

        })
        student_table.append(fragment)
    }
})
