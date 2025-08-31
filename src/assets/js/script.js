function triggerImageUpload() {
  document.getElementById('imageUpload').click();
}

function getResponse() {
  const input = document.getElementById('userInput').value;
  const imageUpload = document.getElementById('imageUpload');
  const chatMessages = document.getElementById('chat-messages');
  const userMessage = document.createElement('div');
  userMessage.className = 'message user-message';
  userMessage.textContent = input || 'Image uploaded!';
  chatMessages.appendChild(userMessage);
  chatMessages.scrollTop = chatMessages.scrollHeight;

  // Dummy response logic
  let reply = "";
  if (imageUpload.files.length > 0) {
    reply = "Bhai, yeh image dekhi—lagta hai haircut ka idea hai! Try a sharp fade, tu toh rockstar ban jayega!";
  } else if (input.toLowerCase().includes("hair")) {
    reply = "Arre bhai, yeh cut karwa le—tera look toh fire ho jayega! Fade with gel lagao!";
  } else if (input.toLowerCase().includes("workout")) {
    reply = "Chal, 15 squats aur 10 curls kar le—tu toh iron man ban jayega! Protein shake mat bhoolna!";
  } else {
    reply = "Bhai, thodi si masti kar—puch hairstyle ya gym wala sawal, main tera boss ban ke bata dunga!";
  }

  setTimeout(() => {
    const aiMessage = document.createElement('div');
    aiMessage.className = 'message ai-message';
    aiMessage.textContent = reply;
    chatMessages.appendChild(aiMessage);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }, 1000);

  document.getElementById('userInput').value = '';
  imageUpload.value = '';
}