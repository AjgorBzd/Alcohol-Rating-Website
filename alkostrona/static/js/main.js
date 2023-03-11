const data = document.currentScript.dataset;
const reviewers = data.reviewers;
const currentRate = JSON.parse(data.ratings);
const currentUser = data.currentuser;
const currentPhoto = data.photo;
console.log(currentUser)
const one = document.getElementById('first')
const two = document.getElementById('second')
const three = document.getElementById('third')
const four = document.getElementById('fourth')
const five = document.getElementById('fifth')
const arr = [one, two, three, four, five]
const opinion = document.getElementById('opinion')
const opinionTextBox = document.getElementById('op')
const submitButton = document.getElementById('send_review')
const alcoholReviews = document.getElementById('alcohol_reviews')
let rate = 0





function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

let csrf = getCookie('csrftoken')

let stop_stars = false


const childrenList = document.getElementById('stars').children

const handleRateOpt = (size) => {
    for (let i = 0; i < childrenList.length; i++) {
        if (i < size) {
            childrenList[i].classList.add('checked')
        }
        else {
            childrenList[i].classList.remove('checked')
        }
    }
}

const handleRate = (target) => {

    if (stop_stars === false) {
        console.log("widze czego nie ma")
        switch (target) {
            case 'first': {
                handleRateOpt(1)
                return
            }
            case 'second': {
                handleRateOpt(2)
                return
            }
            case 'third': {
                handleRateOpt(3)
                return
            }
            case 'fourth': {
                handleRateOpt(4)
                return
            }
            case 'fifth': {
                handleRateOpt(5)
                return
            }
        }
    }
}

const appendReview = () => {
    let div = document.createElement('div')

    div.innerHTML = "<div  class='opinion-card'>" + "<div class='top-card'>" + "<div class='card-jpg'><img alt='Profile picture' src=" + currentPhoto +
        "width='100px' height='100px'></div>" +
        "<div class='card-rating'>" + currentUser + "rated " + rate + "/5</div></div>" +
        "<div class='bottom-card'><div class='card_dsc'>" + opinionTextBox.value + "</div></div>"

    alcoholReviews.appendChild(div)
}

const submitReview = (ev) => {
    let opinion = opinionTextBox.value
    let url = window.location.pathname + 'review'
    fetch(url, {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({
            payload: {
                opinion,
                rate
            }
        })
    }).then(data => {
        if (data.status === 200) {
            appendReview()
            opinionTextBox.value = ''

            stop_stars = true
        }
    })
}

submitButton.addEventListener('click', ev => {
    submitReview(ev)
})

const openOpinion = (target) => {
    opinion.style.display = 'block'
    stop_stars = true
    switch (target) {
        case 'first': {
            rate = 1
            return
        }
        case 'second': {
            rate = 2
            return
        }
        case 'third': {
            rate = 3
            return
        }
        case 'fourth': {
            rate = 4
            return
        }
        case 'fifth': {
            rate = 5
            return
        }
    }
}

arr.forEach(item => item.addEventListener("mouseover", ev => {
    handleRate(ev.target.id)
}))

arr.forEach(item => item.addEventListener("click", ev => {
    openOpinion(ev.target.id)
}))

function preloadFunc() {
    console.log(currentRate)
    console.log(currentUser)
    if (currentUser in currentRate) {
        handleRateOpt(currentRate[currentUser] + 1)
        stop_stars = true
        console.log("Podano opinie juz")
    }


}
window.onload = preloadFunc();