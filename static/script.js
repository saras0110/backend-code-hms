let video = document.getElementById('video');
let canvas = document.getElementById('canvas');
let result = document.getElementById('result');

// Use your actual backend URL
const backendURL = "https://backend-code-hms.onrender.com";

navigator.mediaDevices.getUserMedia({ video: true })
  .then(stream => video.srcObject = stream)
  .catch(err => console.error("Camera access denied:", err));

function startAnalysis(type) {
  result.innerText = "Analyzing...";

  canvas.width = 48;
  canvas.height = 48;
  let ctx = canvas.getContext('2d');
  ctx.drawImage(video, 0, 0, 48, 48);

  let imageData = canvas.toDataURL('image/jpeg');

  fetch(`${backendURL}/${type}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ image: imageData })
  })
  .then(res => res.json())
  .then(data => {
    if (type === 'emotion') {
      result.innerHTML = `Emotion: ${data.label} ${data.emoji}`;
    } else if (type === 'structure') {
      result.innerHTML = `Face Shape: ${data.label}`;
    } else if (type === 'skin') {
      result.innerHTML = `Skin Type: ${data.label}`;
    }
  })
  .catch(err => {
    result.innerText = "Error: " + err.message;
    console.error(err);
  });
}
