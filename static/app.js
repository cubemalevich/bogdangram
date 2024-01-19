document.addEventListener("DOMContentLoaded", function () {
    const chatBox = document.getElementById("chat-box");
    const messageForm = document.getElementById("message-form");
    const messageInput = document.getElementById("message-input");
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
    
            messageText.innerText = `${displaySender} - ${displayMessage}`;
    
            messageDiv.appendChild(messageText);
            chatBox.appendChild(messageDiv);
        }
    }
    

    messageForm.addEventListener("submit", function (e) {
        e.preventDefault();
        const message = messageInput.value;

        if (message) {
            const username = localStorage.getItem('username');
            addMessage(message, username);
            messageInput.value = "";

            console.log("Sending message to server. Message:", message);

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
