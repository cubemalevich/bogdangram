document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.getElementById("login-form");

    loginForm.addEventListener("submit", function (e) {
        e.preventDefault();

        console.log("Form submitted");

        const usernameInput = document.getElementById("username");
        const passwordInput = document.getElementById("password");

        const username = usernameInput.value;
        const password = passwordInput.value;

        console.log("Username input (login.html):", username);
        console.log("Password input (login.html):", password);

        const requestBody = new URLSearchParams({ username, password });
        console.log("Request body:", requestBody);

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
                sessionStorage.setItem('username', username);

                if (data.redirect) {
                    console.log("Redirecting to:", data.redirect);
                    window.location.replace(data.redirect);
                } else if (data.error) {
                    sessionStorage.setItem('username', username);
                    console.log("Username saved to sessionStorage:", username);
                    console.log("Current sessionStorage:", sessionStorage);

                } else {
                    if (data.user_id && data.user_id !== 'null') {
                        sessionStorage.setItem('username', username);
                        getUserId(username);
                    } else {
                        console.error("User ID is undefined, empty, or 'null'. Cannot proceed.");
                        sessionStorage.setItem('username', username);
                    }
                }
            })
            
            .catch(error => {
                console.error("There was a problem with the fetch operation:", error);
            });
        }
    });

    function getUserId(username) {
        fetch('/get_user_id')
            .then(response => response.json())
            .then(data => {
                sessionStorage.setItem('username', username);
            })
            .catch(error => {
                console.error("Error fetching user_id:", error);
            });
    }
    
    
});
