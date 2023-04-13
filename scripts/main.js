var coll = document.getElementsByClassName("collapsible");
console.log(coll)
var i;

for (i = 0; i < coll.length; i++) {
    coll[i].addEventListener("click", function () {
        this.classList.toggle("active");
        var content = this.nextElementSibling;
        if (content.style.display === "block") {
            content.style.display = "none";
        } else {
            content.style.display = "block";
        }
    });
}

function displayClock() {
    var display = new Date().toLocaleTimeString('en-GB', { timeZone: 'Europe/London', year: 'numeric', month: 'numeric', day: 'numeric', hour: '2-digit', minute: '2-digit' });
    document.querySelector('.date-time').innerHTML = display;
    setTimeout(displayClock, 1000);
}

async function writeArticles(path) {
    // read json file
    let response = await fetch(path, { cache: "reload" });
    let data = await response.json();
    // loop through each story and set headline
    for (let i = 0; i < 7; i++) {
        document.getElementById('button-' + i).textContent = "> " + data[i].title;
        let article = document.createElement('div');
        // loop through summary sentences and add to div
        for (let j = 0; j < 7; j++) {
            let sentence = document.createElement('p');
            sentence.textContent = data[i].summary[j];
            article.append(sentence);
        }
        document.getElementById('article-' + i).prepend(article);
        let bbcLogo = article.nextElementSibling;
        bbcLogo.href = data[i].url;
    }
}

async function writeSportArticles(path) {
    // read json file
    let response = await fetch(path, { cache: "reload" });
    let data = await response.json();
    // loop through each story and set headline
    for (let i = 0; i < 7; i++) {
        document.getElementById('sport-button-' + i).textContent = "> " + data[i].title;
        let article = document.createElement('div');
        // loop through summary sentences and add to div
        for (let j = 0; j < 7; j++) {
            let sentence = document.createElement('p');
            sentence.textContent = data[i].summary[j];
            article.append(sentence);
        }
        document.getElementById('sport-article-' + i).prepend(article);
        let bbcLogo = article.nextElementSibling;
        bbcLogo.href = data[i].url;
    }
}

writeArticles('data/bbc.json');
writeSportArticles('data/bbc-sport.json');

