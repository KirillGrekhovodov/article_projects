async function makeRequest(url, method = "GET") {
    let csrfToken = await getCookie('csrftoken')
    let headers = {}
    if (method !== "GET") {
        headers['X-CSRFToken'] = csrfToken
    }
    let response = await fetch(url,
        {
            "method": method,
            "headers": headers,
        }
    );
    if (response.ok) {
        return await response.json();
    } else {
        let error = new Error(response.text);
        console.log(error);
        throw error;
    }
}

async function onClick(event) {
    event.preventDefault();
    let a = event.target;
    let url = a.href;
    let button_text = a.innerText;
    let method = "POST";
    if (button_text === "Дизлайк") {
        method = "DELETE"
    }
    let response = await makeRequest(url, method);
    let span = a.parentElement.getElementsByTagName("span")[0]
    span.innerText = response.likes_count
    a.innerText = button_text === "Дизлайк" ? "Лайк" : "Дизлайк"
}

function onLoad() {
    let links = document.querySelectorAll('[data-like="like"]');
    for (let link of links) {
        link.addEventListener("click", onClick);
    }
}

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

window.addEventListener("load", onLoad);