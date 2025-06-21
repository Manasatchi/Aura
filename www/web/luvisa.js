let memoryMode = "long_term";

// List of Luvisa bg images (place these images in the same directory as your HTML)
const bgImages = ['bg1.jpg', 'bg2.jpg', 'bg3.jpg', 'bg4.jpg'];

// Set a random background image for the page
function setRandomBackground() {
  const randomImage = bgImages[Math.floor(Math.random() * bgImages.length)];
  document.body.style.backgroundImage = `url('${randomImage}')`;
  document.body.style.backgroundSize = "cover";
  document.body.style.backgroundPosition = "center";
  document.body.style.backgroundAttachment = "fixed";
}

// Set Luvisa's profile image (once)
function setProfileImage() {
  const img = document.querySelector(".profile-pic");
  img.src = "luvisa.png";
}

// Append message to the chatbox with dynamic background color based on text length
function appendMessage(sender, text, className = "") {
  const chatbox = document.getElementById("chatbox");
  const div = document.createElement("div");

  div.className = `message ${className}`;

  // Calculate color based on message length
  const length = text.length;
  let bgColor = "";

  if (className === "user-message") {
    const blue = Math.max(50, 209 - length * 2); // Darkens with length
    bgColor = `rgba(6, ${blue}, 209, 0.7)`;
  } else if (className === "bot-message" || className.includes("bot-message")) {
    const pink = Math.max(50, 239 - length * 2);
    bgColor = `rgba(${pink}, 28, 98, 0.7)`;
  }

  div.style.backgroundColor = bgColor;
  div.innerHTML = `<strong>${sender}:</strong> ${text}`;
  chatbox.appendChild(div);
  chatbox.scrollTop = chatbox.scrollHeight;
}

// Display typing indicator
function showTyping() {
  appendMessage("Luvisa❤️", "is typing...", "typing bot-message");
}

// Remove typing indicator
function removeTyping() {
  const typing = document.querySelector(".typing");
  if (typing) typing.remove();
}

// Send user message
function sendMessage() {
  const input = document.getElementById("userInput");
  const message = input.value.trim();
  if (message === "") return;

  appendMessage("You", message, "user-message");
  input.value = "";

  showTyping();

  eel.handle_user_input(message, memoryMode)((response) => {
    removeTyping();

    if (response.startsWith("MODE:")) {
      const parts = response.split("|");
      memoryMode = parts[0].split(":")[1];
      appendMessage("Luvisa❤️", parts[1].split(":")[1], "bot-message");
    } else {
      appendMessage("Luvisa❤️", response, "bot-message");
    }
  });
}

// DOM ready
document.addEventListener("DOMContentLoaded", () => {
  setRandomBackground();

  document.getElementById("userInput").addEventListener("keydown", (e) => {
    if (e.key === "Enter") sendMessage();
  });
});
