document.addEventListener('DOMContentLoaded', () => {

    const d = document;

    const url = window.location.href;
    const parts = url.split('/');
    const enrollmentId = parts[5]
    const submit_button = d.getElementById('submit_button')
    console.log(enrollmentId)


    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }


    const form = d.getElementById('form')

    const csrftoken = getCookie('csrftoken');
    const headers = {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken
    }



    form.addEventListener('submit', async(e) => {
        e.preventDefault()

        const course_name = submit_button.dataset.course;
        // console.log

        const fetchUrl = `/enrollments/details/${enrollmentId}/`

        const response = await fetch(fetchUrl, {method: 'POST', headers})

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `matriculados_${course_name}.pdf`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    })


})