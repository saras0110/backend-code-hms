const video = document.getElementById('video');
const emojiImg = document.getElementById('emoji');

const EMOJI_MAP = {
    happy: "emojis/happy.png",
    sad: "emojis/sad.png",
    angry: "emojis/angry.png",
    surprised: "emojis/surprised.png",
    neutral: "emojis/neutral.png"
};

navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => { video.srcObject = stream; })
    .catch(err => console.error("Camera error: ", err));

setInterval(() => {
    captureAndSendFrame();
}, 2000); // every 2 seconds

function captureAndSendFrame() {
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0);
    canvas.toBlob(blob => {
        const formData = new FormData();
        formData.append('image', blob, 'frame.jpg');

        fetch("https://YOUR-RENDER-BACKEND-URL/detect_emotion", {
            method: "POST",
            body: formData
        })
        .then(res => res.json())
        .then(data => {
            if (data.emotion) {
                const emotion = data.emotion.toLowerCase();
                emojiImg.src = EMOJI_MAP[emotion] || "emojis/neutral.png";
            }
        })
        .catch(err => console.error(err));
    }, 'image/jpeg');
}

