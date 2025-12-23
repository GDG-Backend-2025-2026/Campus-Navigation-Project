let token = '';

function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    fetch('/auth/login', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({username, password})
    })
    .then(res => res.json())
    .then(data => {
        if (data.token) {
            token = data.token;
            document.getElementById('login-section').style.display = 'none';
            document.getElementById('main-section').style.display = 'block';
            fetchBuildings();
        } else {
            document.getElementById('login-message').innerText = data.message || 'Login failed';
        }
    });
}
function signup() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    fetch('/auth/login', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({username, password})
    })
    .then(res => res.json())
    .then(data => {
        if (data.token) {
            token = data.token;
            
            fetchBuildings();
        } else {
            document.getElementById('login-message').innerText = data.message || 'Login failed';
        }
    });
}

function fetchBuildings() {
    fetch('/buildings/')
        .then(res => res.json())
        .then(data => {
            const list = document.getElementById('building-list');
            list.innerHTML = '';
            data.forEach(b => {
                const li = document.createElement('li');
                li.innerText = b.name;
                list.appendChild(li);
            });
        });
}


