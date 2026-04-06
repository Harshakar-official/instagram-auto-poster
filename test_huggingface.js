const https = require('https');
const fs = require('fs');

const HF_TOKEN = process.env.HF_TOKEN || '';

const prompt = "cybersecurity shield with lock, dark theme, digital protection, professional infographic style";
const model = "stabilityai/stable-diffusion-xl-base-1.0";

const postData = JSON.stringify({
    inputs: prompt,
    parameters: {
        guidance_scale: 7.5,
        num_inference_steps: 30
    }
});

const options = {
    hostname: 'api-inference.huggingface.co',
    path: `/models/${model}`,
    method: 'POST',
    headers: {
        'Authorization': `Bearer ${HF_TOKEN}`,
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(postData)
    }
};

console.log('Testing HuggingFace Inference API...');
console.log('Model:', model);

const req = https.request(options, (res) => {
    const chunks = [];
    res.on('data', (chunk) => chunks.push(chunk));
    res.on('end', () => {
        const body = Buffer.concat(chunks);
        if (res.headers['content-type']?.includes('image')) {
            fs.writeFileSync('images/test_hf.png', body);
            console.log('SUCCESS: Image saved to images/test_hf.png');
            console.log('Size:', body.length, 'bytes');
        } else {
            console.log('Status:', res.statusCode);
            console.log('Response:', body.toString().substring(0, 1000));
        }
    });
});

req.on('error', (e) => console.error('Error:', e.message));
req.write(postData);
req.end();
