document.addEventListener("DOMContentLoaded", function () {
    const registerForm = document.getElementById("register-form");

    registerForm.addEventListener("submit", function (e) {
        e.preventDefault();
        console.log("Form submitted");

        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;
        
        const requestBody = { username, password };
        console.log("Request body:", requestBody); // Проверка содержимого запроса
        
        fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestBody)
        }).then(response => {
            console.log("Server response:", response); // Проверка ответа от сервера

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        }).then(data => {
            console.log(data.message); // Вывод сообщения об успешной регистрации
        }).catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
    });
});
