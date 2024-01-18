document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.getElementById("login-form");

    loginForm.addEventListener("submit", function (e) {
        e.preventDefault();

        console.log("Form submitted");

        const usernameInput = document.getElementById("username");
        const passwordInput = document.getElementById("password");

        const username = usernameInput.value;
        const password = passwordInput.value;

        const requestBody = new URLSearchParams({ username, password });
        console.log("Request body:", requestBody);

        // ...

    if (username && password) {
        console.log("Sending login request with username:", username);

        fetch("/login", {
            method: "POST",
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: requestBody
        })
        .then(response => {
            console.log("Received response from server:", response);
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            return response.json();
        })
        .then(data => {
            console.log("Server response:", data);
        
            if (data.redirect) {
                // Используем replace вместо href для обновления страницы и установки куки
                window.location.replace(data.redirect);
            } else if (data.error) {
                console.error(data.error);
                // Изменение здесь: используем null вместо "undefined"
                localStorage.setItem('user_id', null);
            } else {
                // Проверяем, что user_id присутствует в ответе и не пуст
                if (data.user_id && data.user_id !== 'null') {
                    localStorage.setItem('user_id', data.user_id);
                    console.log("Authenticated user_id:", data.user_id);
                } else {
                    console.error("User ID is undefined, empty, or 'null'. Cannot proceed.");
                    // Изменение здесь: используем null вместо "undefined"
                    localStorage.setItem('user_id', null);
                }
            }
        })
        
        
        .catch(error => {
            console.error("There was a problem with the fetch operation:", error);
        });
        
    }

    });
});

    document.getElementById("logout-button").addEventListener("click", function () {
    localStorage.removeItem('user_id');
    console.log("Logged out");
});
