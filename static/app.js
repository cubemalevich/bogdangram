document.addEventListener("DOMContentLoaded", function () {
    const chatBox = document.getElementById("chat-box");
    const messageForm = document.getElementById("message-form");
    const messageInput = document.getElementById("message-input");

    // Получение сообщений с сервера
    function getMessages() {
        fetch("/get_messages")
            .then((response) => response.json())
            .then((data) => {
                data.messages.forEach((message) => {
                    addMessage(message.message_text, message.sender);
                });
            })
            .catch((error) => {
                console.error("Error getting messages:", error);
            });
    }

    function addMessage(message, sender) {
        const messageDiv = document.createElement("div");
        messageDiv.className = "message";
        const messageText = document.createElement("p");
    
        messageText.textContent = `${sender ? sender.trim() : 'You'} - ${message.trim()}`;
    
        messageDiv.appendChild(messageText);
        chatBox.appendChild(messageDiv);
    }
    

    // Обработчик отправки сообщения
    messageForm.addEventListener("submit", function (e) {
        e.preventDefault();
        const message = messageInput.value;

        if (message) {
            // Получаем nickname из локального хранилища
            const nickname = localStorage.getItem('nickname') || 'You';
            
            addMessage(message, nickname);
            messageInput.value = "";

            console.log("Sending message to server. Message:", message);

            const requestBody = { message };
            
            // Отправляем сообщение на сервер
            fetch("/send_message", {
                method: "POST",
                body: new URLSearchParams(requestBody),
                headers: { "Content-Type": "application/x-www-form-urlencoded" },
            })
                .then((response) => {
                    if (!response.ok) {
                        throw new Error("Network response was not ok");
                    }
                    return response.json();
                })
                .then((data) => {
                    console.log("Server response after sending message:", data);
                })
                .catch((error) => {
                    console.error("There was a problem with the fetch operation:", error);
                });
        }
    });

    // Получаем и отображаем сообщения при загрузке страницы
    getMessages();
});
