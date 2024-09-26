const container = document.getElementById('container');
const registerBtn = document.getElementById('register');
const loginBtn = document.getElementById('login');

registerBtn.addEventListener('click', () => {
    container.classList.add("active");
});

loginBtn.addEventListener('click', () => {
    container.classList.remove("active");
});

// Function to handle registration
document.getElementById('signup-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    const User_name = document.querySelector('.sign-up input[name="userName"]').value;
    const PASS_WORD = document.querySelector('.sign-up input[name="password"]').value;

    try {
        const response = await fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ User_name, PASS_WORD })
        });
        const result = await response.text();
        alert(result);
    } catch (error) {
        console.error('Error:', error);
    }
});

// Function to handle login
document.getElementById('login-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    const User_name = document.querySelector('.sign-in input[name="userName"]').value;
    const PASS_WORD = document.querySelector('.sign-in input[name="password"]').value;

    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ User_name, PASS_WORD })
        });
        const data = await response.json();

        if (data.success) {
            localStorage.setItem('username', User_name); // Store the username in local storage
            window.location.href = 'dashboard.html';
        } else {
            document.getElementById('message').textContent = data.message;
        }
    } catch (error) {
        console.error('Error:', error);
    }
});