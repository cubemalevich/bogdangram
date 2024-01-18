document.addEventListener("DOMContentLoaded", function () {
    const chatBox = document.getElementById("chat-box");
    const messageForm = document.getElementById("message-form");
    const messageInput = document.getElementById("message-input");

    let userId;  // Переменная для хранения user_id

    // Функция для отправки запроса на получение сообщений с сервера
    function getMessages() {
        fetch("/get_messages")
            .then((response) => response.json())
            .then((data) => {
                data.messages.forEach((message) => {
                    addMessage(message.message_text, message.user_id);
                });
            })
            .catch((error) => {
                console.error("Error getting messages:", error);
            });
    }

    // Функция для добавления сообщения в чат
    // Функция для добавления сообщения в чат
    // Функция для добавления сообщения в чат
    function addMessage(message) {
        const messageDiv = document.createElement("div");
        messageDiv.className = "message";
        const messageText = document.createElement("p");

        // Разбираем сообщение на никнейм и текст
        const [nickname, text] = message.split(':');

        messageText.textContent = `${nickname.trim()}: ${text.trim()}`;
        messageDiv.appendChild(messageText);
        chatBox.appendChild(messageDiv);
    }



    // Функция для получения user_id
    // Функция для получения user_id
    // Функция для получения user_id
    async function getUserId() {
        console.log("Before fetching user_id. Current user_id:", userId);

        // Убедитесь, что код загружает user_id из localStorage перед выполнением fetch
        userId = localStorage.getItem('user_id');

        // Проверяем, если user_id не определен или null, устанавливаем в undefined
        if (!userId || userId === 'null') {
            userId = undefined;
        }

        if (userId) {
            // Устанавливаем user_id в скрытое поле
            document.getElementById("user-id").value = userId;
            getMessages();
        } else {
            console.error("User ID is None or null. Cannot fetch messages.");
        }

        console.log("After fetching user_id. Current user_id:", userId);
    }




    

    // Отправка сообщения на сервер
    // Отправка сообщения на сервер
    // Отправка сообщения на сервер
    // Отправка сообщения на сервер
    messageForm.addEventListener("submit", function (e) {
        e.preventDefault();
        const message = messageInput.value;

        // Игнорировать отправку сообщения, если user_id не определен
        if (message && userId !== undefined) {
            addMessage(message, "cube");  // Жестко заданный никнейм "cube" (можете изменить по своему усмотрению)
            messageInput.value = "";

            // Добавим отладочное сообщение
            console.log("Sending message to server. User ID:", userId, "Message:", message);

            // Отправляем сообщение и user_id на сервер
            const requestBody = { message, user_id: userId };
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
                // Обработка успешной отправки сообщения, если нужно
            })
            .catch((error) => {
                console.error("There was a problem with the fetch operation:", error);
            });
        }
    });




    // Запускаем получение user_id при загрузке страницы
    getUserId();
});
