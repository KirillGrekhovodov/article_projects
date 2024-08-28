async function makeRequest(url, method = "GET", body) {
    let token = await getCookie('token')
    console.log(token)
    let headers = {}
    headers['Authorization'] = `Token ${token}`
    headers['Content-Type'] = "application/json"

    let response = await fetch(url,
        {
            "method": method,
            "headers": headers,
            "body": JSON.stringify(body)
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
    let body = {"title": "11111111", "content": "dscdsacsacas"};
    let response = await makeRequest("http://localhost:8000/api/v3/articles/", "POST", body);
    console.log(response);
    // let a = event.target;
    // let url = a.href;
    // let button_text = a.innerText;
    // let method = "POST";
    // if (button_text === "Дизлайк") {
    //     method = "DELETE"
    // }
    // let response = await makeRequest(url, method);
    // let span = a.parentElement.getElementsByTagName("span")[0]
    // span.innerText = response.likes_count
    // a.innerText = button_text === "Дизлайк" ? "Лайк" : "Дизлайк"
}

function onLoad() {
    let button = document.getElementById("api_test");
    button.addEventListener("click", onClick);

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