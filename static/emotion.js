const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const resultDiv = document.getElementById('result');
const context = canvas.getContext('2d');

async function setupCamera() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    video.srcObject = stream;
  } catch (err) {
    resultDiv.textContent = 'Camera access denied or not available.';
    console.error(err);
  }
}

function sendFrame() {
  if (video.readyState === 4) {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0);

    canvas.toBlob(async (blob) => {
      const formData = new FormData();
      formData.append('image', blob, 'frame.jpg');  // Optional filename

      try {
        const response = await fetch('/emotion', {
          method: 'POST',
          body: formData,
        });

        if (!response.ok) {
          throw new Error('Server error');
        }

        const data = await response.json();

        if (data.label && data.emoji) {
          resultDiv.innerHTML = `Emotion: ${data.label} <br> ${data.emoji}`;
        } else {
          resultDiv.innerHTML = 'No emotion detected.';
        }
      } catch (error) {
        resultDiv.textContent = 'Error detecting emotion.';
        console.error(error);
      }
    }, 'image/jpeg');
  }

  setTimeout(sendFrame, 2000); //
