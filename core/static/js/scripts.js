    
let deleteButton = document.querySelector('.delete-btn')
let searchBtn = document.querySelector('#search-btn')
let searchForm = document.querySelector('#search-form')
let doneTasks = document.querySelector('#done-tasks')

deleteButton.onclick = (e) => {
    e.preventDefault()

    let delLink = deleteButton.getAttribute('href')
    let result = confirm('Quer deletar essa tarefa?')

    if (result){
        window.location.href = delLink
    }
}

searchBtn.onclick = () => {
    searchForm.submit()
}

doneTasks.onclick = () => {
    doneTasks.submit()
}
