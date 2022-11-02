const main = async () => {
    const response = await fetch('/news', {
        method: 'GET',
        })
    console.log(response.status)
    if (response.status === 200) {
        resultJson = await response.json()
        for (el of resultJson) {
            liHtml = document.createElement('li')
            liHtml.className = 'list-group-item'
            liHtml.textContent = `${el.title}. City: ${el.category}. Loaded: ${el.created}. Link: ${el.link}`
            news.appendChild(liHtml)
        }
    }
    if (response.status === 401) {
        window.location = '/'
    }
}

main()