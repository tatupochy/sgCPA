// document.addEventListener('DOMContentLoaded', () => {
//     const d = document;
//     const year = d.getElementById('year')
//     const revenues_table_body = d.getElementById('revenues-table-body')
//     const total_revenueElement = d.getElementById('total_revenue')
//     const revenues_table = d.getElementById('revenues-table')

//     year.addEventListener('change', async(e) => {
//         const value = e.target.value;

//         const url = `get_revenues_per_year/${value}`

//         const response = await fetch(url)

//         const {monthly_revenues, total_revenue} = await response.json()

//         total_revenueElement.textContent = total_revenue;


//         const fragment = d.createDocumentFragment()


//         monthly_revenues.map(element => {
//             const tr = d.createElement('tr')
//             const tdMonth = d.createElement('td')
//             const tdRevenue = d.createElement('td')

//             tdMonth.textContent = element[0]
//             tdRevenue.textContent = element[1]

//             tr.append(tdMonth)
//             tr.append(tdRevenue)

//             fragment.append(tr)

//         });

//         revenues_table_body.innerHTML = '';

//         revenues_table.innerHTML = '';

//         revenues_table_body.append(fragment)


//     })
// })