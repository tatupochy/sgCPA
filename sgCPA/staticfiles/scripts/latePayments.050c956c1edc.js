document.addEventListener('DOMContentLoaded', () => {
    const d = document;

    const filterButton = d.getElementById('filterButton');

    const clearfilterButton = d.getElementById('clearfilterButton');

    const yearSelector = d.getElementById('yearSelector');

    const monthSelector = d.getElementById('monthSelector');

    filterButton.addEventListener('click', (e) => {
        e.preventDefault()
        const year = yearSelector.value;
        const month = monthSelector.value;

         let url = '/reports/latePayments/';

        if (year) {
            url += `${year}/`;
            if (month) {
                url += `${month}/`;
            }
        }

        if(year && month) window.location.href = url;

        
        
    })

    clearfilterButton.addEventListener('click', (e) => {
        e.preventDefault()

        const url = '/reports/latePayments/';

        window.location.href = url;
    })

})