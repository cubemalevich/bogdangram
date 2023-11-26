document.addEventListener("DOMContentLoaded", function () {
    const chatBox = document.getElementById("chat-box");
    const messageForm = document.getElementById("message-form");
    const messageInput = document.getElementById("message-input");

    // Функция для добавления сообщения на страницу
    function addMessage(message) {
        const messageDiv = document.createElement("div");
        messageDiv.className = "message";
        messageDiv.textContent = message;
        chatBox.appendChild(messageDiv);
    }

    // Запрос на получение сообщений с сервера
    function getMessages() {
        fetch("/get_messages")
            .then((response) => response.json())
            .then((data) => {
                data.messages.forEach((message) => {
                    addMessage(message);
                });
            });
    }

    // Отправка сообщения на сервер
    messageForm.addEventListener("submit", function (e) {
        e.preventDefault();
        const message = messageInput.value;
        if (message) {
            addMessage(message);
            messageInput.value = "";
            fetch("/send_message", {
                method: "POST",
                body: new URLSearchParams({ message }), 
                headers: { "Content-Type": "application/x-www-form-urlencoded" },
            })
            .then((response) => {
                if (!response.ok) {
                    throw new Error("Network response was not ok");
                }
                return response.json();
            })
            .then((data) => {
                
            })
            .catch((error) => {
                console.error("There was a problem with the fetch operation:", error);
        
            });
        }
    });

    // Получение сообщений при загрузке страницы
    getMessages();
});