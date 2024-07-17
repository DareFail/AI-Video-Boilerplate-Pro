if (checkUrlVariableF(window.location.href)) {
    document.getElementById("fullRoom").style.display = "block";
} else if (checkUrlVariableR(window.location.href)) {
    joinRoom("rps");
}

function checkUrlVariableF(url) {
    const parsedUrl = new URL(url);
    const searchParams = new URLSearchParams(parsedUrl.search);
    return searchParams.get('f') === 't';
}

function checkUrlVariableR(url) {
    const parsedUrl = new URL(url);
    const searchParams = new URLSearchParams(parsedUrl.search);
    return searchParams.get('r') === 't';
}

function joinRoom(game) {
    const letters = 'abcdefghijklmnopqrstuvwxyz';
    let randomPath = '';

    for (let i = 0; i < 6; i++) {
        const position = Math.floor(Math.random() * letters.length);
        randomPath += letters[position];
    }

    window.location.href = location.origin + '/' + game + "/" + randomPath + '/';
}



