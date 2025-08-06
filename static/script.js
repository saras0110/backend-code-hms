let video = document.getElementById('video');
let canvas = document.getElementById('canvas');
let result = document.getElementById('result');
const backendURL = "https://your-render-backend.onrender.com";

navigator.mediaDevices.getUserMedia({ video: true })
  .then(stream => video.srcObject = stream);

function startAnalysis(type) {
  result.innerText = "Analyzing...";
  canvas.getContext('2d').drawImage(video, 0, 0, 224, 224);
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
  });
}
