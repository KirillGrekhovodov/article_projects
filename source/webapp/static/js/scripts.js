async function makeRequest(url, method="GET"){
    let csrfToken = await getCookie('csrftoken')
    let response = await fetch(url,
        {
            "method": method,
            "headers": {'X-CSRFToken': csrfToken},
        }
    );
    if(response.ok){
        return await response.json();
    }
    else{
        let error = new Error(response.text);
        console.log(error);
        throw error;
    }
}

async function onClick(event){
    event.preventDefault();
    let a = event.target;
    let url = a.href;
    let response = await makeRequest(url, "POST");
    console.log(a.parentElement)
    let span = a.parentElement.getElementsByTagName("span")[0]
    span.innerText = response.test
    console.log(response)
}

function onLoad(){
    let links= document.querySelectorAll('[data-js="js"]');
    for (let link of links){
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