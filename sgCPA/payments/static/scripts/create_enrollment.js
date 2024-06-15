document.addEventListener('DOMContentLoaded', () => {
    const d = document;

    const curso = d.getElementById('id_course')
    const student_table = d.getElementById('student_table').querySelector('tbody')

    curso.addEventListener('change', async(e) => {
        student_table.innerHTML = '';
        const value = e.target.value
        const url = `/alumnos_por_curso/${value}`
        const response = await fetch(url)
        const json = await response.json()
        const fragment = d.createDocumentFragment()
        json.map((item) => {

            const tr = d.createElement('tr')
            const tdName = d.createElement('td')
            const tdLastName = d.createElement('td')
            const tdCI = d.createElement('td')
            const tdCheck = d.createElement('td')
            const checkbox = d.createElement('input')
            checkbox.type = 'checkbox';


            tdName.textContent = item.nombre;
            tdLastName.textContent = item.apellido;
            tdCI.textContent = item.ci;

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