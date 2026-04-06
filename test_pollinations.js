const https = require('https');
const fs = require('fs');

const prompt = encodeURIComponent("cybersecurity shield with lock, dark theme, digital protection");
const width = 1024;
const height = 1024;

const url = `https://image.pollinations.ai/prompt/${prompt}?width=${width}&height=${height}&model=flux`;

console.log('Testing Pollinations.ai (free AI images)...');
console.log('URL:', url.substring(0, 100) + '...');

https.get(url, (res) => {
    if (res.headers['content-type']?.includes('image')) {
        const chunks = [];
        res.on('data', (chunk) => chunks.push(chunk));
        res.on('end', () => {
            const body = Buffer.concat(chunks);
            fs.writeFileSync('images/test_pollinations.png', body);
            console.log('SUCCESS: Image saved!');
            console.log('Size:', body.length, 'bytes');
        });
    } else {
        console.log('Status:', res.statusCode);
        console.log('Content-Type:', res.headers['content-type']);
    }
}).on('error', (e) => console.error('Error:', e.message));
