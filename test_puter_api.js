const https = require('https');

const prompt = "cybersecurity shield with lock, dark theme, digital protection";
const data = JSON.stringify({
    model: "stabilityai/stable-diffusion-3-medium",
    prompt: prompt,
    width: 1024,
    height: 1024
});

const options = {
    hostname: 'api.puter.com',
    path: '/txt2img',
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(data)
    }
};

const req = https.request(options, (res) => {
    let body = '';
    res.on('data', (chunk) => body += chunk);
    res.on('end', () => {
        console.log('Status:', res.statusCode);
        console.log('Response:', body.substring(0, 2000));
    });
});

req.on('error', (e) => console.error('Error:', e.message));
req.write(data);
req.end();
