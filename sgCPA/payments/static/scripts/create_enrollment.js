document.addEventListener('DOMContentLoaded', () => {
    const d = document;

    const curso = d.getElementById('id_course')
    const id_enrollment_amount = d.getElementById('id_enrollment_amount')
    const id_fee_amount = d.getElementById('id_fee_amount')
    const minStudentsNumber = d.getElementById('minStudentsNumber')
    const maxStudentsNumber = d.getElementById('maxStudentsNumber')
    const id_enrollment_date = d.getElementById('id_enrollment_date')
    const today = new Date().toISOString().split('T')[0];
    id_enrollment_date.value = today;

    curso.addEventListener('change', async(e) => {
        const value = e.target.value;
        const url = `/obtener_curso/${value}`
        const response = await fetch(url)
        const {course_data} = await response.json()
        id_enrollment_amount.value = course_data.enrollment_amount;
        id_fee_amount.value = course_data.fee_amount;
        minStudentsNumber.value = course_data.minStudentsNumber;
        maxStudentsNumber.value = course_data.maxStudentsNumber;

    })
})