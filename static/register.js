document.addEventListener("DOMContentLoaded", function () {
    const registerForm = document.getElementById("register-form");

    registerForm.addEventListener("submit", function (e) {
        e.preventDefault();
        console.log("Form submitted");

        const usernameInput = document.getElementById("username");
        const passwordInput = document.getElementById("password");

        const username = usernameInput.value;
        const password = passwordInput.value;

        const requestBody = new URLSearchParams({ username, password });
        console.log("Request body:", requestBody); // Проверка содержимого запроса

        fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: requestBody
        }).then(response => {
            console.log("Server response:", response); // Проверка ответа от сервера

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            window.location.replace("/login");
            //return response.json();
        }).then(data => {
            console.log(data.message); // Вывод сообщения об успешной регистрации
        }).catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
    });
});
