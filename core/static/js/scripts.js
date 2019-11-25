    
let searchBtn = document.querySelector('#search-btn')
let searchForm = document.querySelector('#search-form')
let table = document.querySelector('.table')

table.onclick = (e) =>{
    
    if (e.target.getAttribute('class') == ('fas fa-trash')){
        e.preventDefault()
        let delLink = e.target.closest('a').getAttribute('href')
        let result = confirm('Would you really like to delete this record?')
    
        if (result){
            window.location.href = delLink
        }        
    }
}

searchBtn.onclick = () => {
    searchForm.submit()
}
