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
    id_enrollment_date.value = today;

    curso.addEventListener('change', async (e) => {
        const value = e.target.value;
        const url = `/obtener_curso/${value}`
        const response = await fetch(url)
        const { course_data } = await response.json()
        id_enrollment_amount.value = course_data.enrollment_amount;
        id_fee_amount.value = course_data.fee_amount;
        minStudentsNumber.value = course_data.minStudentsNumber;
        maxStudentsNumber.value = course_data.maxStudentsNumber;
        space_available.value = course_data.space_available;

        const fragment = d.createDocumentFragment()
        student_table.innerHTML = '';
        course_data.student_list.map((item) => {

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


    })
})