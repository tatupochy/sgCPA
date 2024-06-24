document.addEventListener('DOMContentLoaded', () => {
    const d = document;

    // const curso = d.getElementById('id_course')
    const student_table = d.getElementById('student_table').querySelector('tbody')
    const ci_button = d.getElementById('ci_button')
    const ci_input = d.getElementById('ci_input')
    const create_enrollment_button = d.getElementById('create_enrollment_button')
    const enrollment_form = d.getElementById('enrollment_form')
    const student_id = d.getElementById('student_id')
    const notFoundStudent = d.getElementById('notFoundStudent')
    const enrollment_message = d.getElementById('enrollment_message')
    const space_available = d.getElementById('space_available')

    const course_id = d.getElementById('course_id').value;

    ci_input.addEventListener('input', (e) => {
        // Obtener el valor actual del input
        const inputValue = e.target.value;

        // Remover caracteres no numéricos
        const numericValue = inputValue.replace(/\D/g, '');

        // Actualizar el valor del input con los caracteres numéricos
        ci_input.value = numericValue;
    })

    let timeoutId; // Variable para almacenar el ID del timeout
    ci_button.addEventListener('click', async (e) => {
        const value = ci_input.value;

        if (!value) {
            create_enrollment_button.disabled = true;
            return student_table.innerHTML = '';
        }

        const url = `/obtener_alumno_por_ci/${value}/${course_id}`
        try {
            const response = await fetch(url)
            if (!response.ok) {
                const json = await response.json()
                throw new Error(json.message)
            }
            const json = await response.json()
            fillStudentTable(json)
            create_enrollment_button.disabled = false;
            student_id.value = json.id;
            ci_input.value = '';
        } catch (error) {
            notFoundStudent.style.display = 'block';
            console.log(error)
            notFoundStudent.textContent = error;

            // Si hay un timeout activo, cancelarlo antes de iniciar uno nuevo
            if (timeoutId) {
                clearTimeout(timeoutId);
            }

            //Configurar el timeout para ocultar el mensaje después de 2 segundos
            timeoutId = setTimeout(() => {
                notFoundStudent.style.display = 'none';
            }, 2000);
        }
    })


    const fillStudentTable = (student) => {
        student_table.innerHTML = '';

        const tr = d.createElement('tr')
        const tdName = d.createElement('td')
        const tdLastName = d.createElement('td')
        const tdCI = d.createElement('td')
        tdName.textContent = student.name;
        tdLastName.textContent = student.lastName;
        tdCI.textContent = student.ciNumber;
        tr.append(tdName)
        tr.append(tdLastName)
        tr.append(tdCI)
        student_table.append(tr)
    }

    enrollment_form.addEventListener('submit', async (e) => {
        e.preventDefault()

        const formData = new FormData(enrollment_form);

        create_enrollment_button.disabled = true;
        try {
            const response = await fetch(enrollment_form.action, {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                const { message } = await response.json()
                student_table.innerHTML = '';
                enrollment_message.textContent = message;
                space_available.value = Number(space_available.value)-1 < 0 ? 0 : Number(space_available.value)-1;
                setTimeout(() => {
                    enrollment_message.textContent = '';
                }, 1000);
            }

        } catch (error) {
            console.log(error)
        } finally {
            create_enrollment_button.disabled = false;
        }

    })

})
