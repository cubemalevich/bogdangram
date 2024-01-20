document.addEventListener("DOMContentLoaded", function () {
    const chatBox = document.getElementById("chat-box");
    const messageForm = document.getElementById("message-form");
    const messageInput = document.getElementById("message-input");
    const emojiButton = document.getElementById("emoji-button");
    const emojiPicker = document.getElementById("emoji-picker");

    const emojiList = [
        '😁', '😂', '😃', '😄', '😅', '😆', '😇', '😈', '😉', '😊',
        '😋', '😌', '😍', '😎', '😏', '😐', '😒', '😓', '😔', '😖',
        '😘', '😚', '😜', '😝', '😞', '😠', '😡', '😢', '😣', '😤',
        '😥', '😨', '😩', '😪', '😫', '😭', '😰', '😱', '👍', '🎉',
        '❤️', '😸', '😹', '😺', '😻', '😼', '😽', '😾', '😿', '🙀',
        '💩', '👴', '🙅', '🙆', '🙇', '🙈', '🙉', '🙊', '🙋', '🙌',
        '🙍', '🙎', '🙏', '🐌', '🐍', '🐎', '🐑', '🐒', '🐔', '🐗'
    ];

    const emojisPerRow = 10;

    emojiList.forEach((emoji, index) => {
        const emojiSpan = document.createElement('span');
        emojiSpan.innerText = emoji;
        emojiPicker.appendChild(emojiSpan);

        if ((index + 1) % emojisPerRow === 0) {
            const breakElement = document.createElement('br');
            emojiPicker.appendChild(breakElement);
        }
    });

    emojiButton.addEventListener("click", function () {
        emojiPicker.classList.toggle("show");
    });

    emojiPicker.addEventListener("click", function (event) {
        if (event.target.tagName === "SPAN") {
            const emoji = event.target.innerText;
            messageInput.value += emoji;
        }
        emojiPicker.classList.remove("show");
    });

    let lastTimestamp = 0;

    function getMessages() {
        fetch(`/get_messages?timestamp=${lastTimestamp}`)
            .then((response) => response.json())
            .then((data) => {
                console.log("Received data from server:", data);
                if (data && data.messages) {
                    data.messages.forEach((message) => {
                        if (message.message_text && message.sender) {
                            addMessage(message, message.sender);
                        }
                    });
                }
                lastTimestamp = data.timestamp || lastTimestamp;
            })
            .catch((error) => {
                console.error("Error getting messages:", error);
            });
    }

    function addMessage(message, sender) {
        console.log("Adding message:", message, "from sender:", sender);
    
        if (message && message.message_text && sender) {
            const messageDiv = document.createElement("div");
            messageDiv.className = "message";
            const messageText = document.createElement("p");
    
            const displaySender = sender || 'Guest';
            const displayMessage = message.message_text || '';
    
            console.log("Displaying:", displaySender, displayMessage);
    
            const senderDiv = document.createElement("div");
            senderDiv.className = "sender";
            senderDiv.innerText = displaySender;
            messageDiv.appendChild(senderDiv);
    
            messageText.innerText = displayMessage;
            messageDiv.appendChild(messageText);
    
            chatBox.appendChild(messageDiv);
        }
    }
    
    messageForm.addEventListener("submit", function (e) {
        e.preventDefault();
        const message = messageInput.value;

        if (message) {
            const username = sessionStorage.getItem('username');
            addMessage(message, username);
            messageInput.value = "";

            const requestBody = { message, username };
            
            fetch("/send_message", {
                method: "POST",
                body: JSON.stringify({ message, username }), 
                headers: { "Content-Type": "application/json" }, 
            })
            .then((response) => response.json())
            .then((data) => {
                if (data && data.message) {
                    console.log("Server response after sending message:", data.message);
                } else {
                    console.error("Invalid server response:", data);
                }
            })
            .catch((error) => {
                console.error("There was a problem with the fetch operation:", error);
            });
        }
    });

    setInterval(getMessages, 1000);
});
