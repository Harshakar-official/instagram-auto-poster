const https = require('https');
const fs = require('fs');

function generateImage(prompt, outputPath, options = {}) {
    return new Promise((resolve, reject) => {
        const width = options.width || 1024;
        const height = options.height || 1024;
        const model = options.model || 'flux';

        const encodedPrompt = encodeURIComponent(prompt);
        const url = `https://image.pollinations.ai/prompt/${encodedPrompt}?width=${width}&height=${height}&model=${model}&nologo=true`;

        console.log('Generating AI image with Pollinations.ai...');

        https.get(url, (res) => {
            if (!res.headers['content-type']?.includes('image')) {
                reject(new Error(`Unexpected content type: ${res.headers['content-type']}`));
                return;
            }

            const chunks = [];
            res.on('data', (chunk) => chunks.push(chunk));
            res.on('end', () => {
                const body = Buffer.concat(chunks);
                fs.writeFileSync(outputPath, body);
                console.log(`Image saved to: ${outputPath} (${body.length} bytes)`);
                resolve(outputPath);
            });
        }).on('error', (err) => {
            reject(err);
        });
    });
}

const prompt = process.argv[2];
const outputPath = process.argv[3];

if (!prompt || !outputPath) {
    console.error('Usage: node ai_image.js "<prompt>" "<output_path>" [width] [height]');
    process.exit(1);
}

generateImage(prompt, outputPath)
    .then(() => {
        console.log('SUCCESS!');
        process.exit(0);
    })
    .catch((err) => {
        console.error('Failed:', err.message);
        process.exit(1);
    });
