const { init } = require('@heyputer/puter.js/src/init.cjs');

async function generateImage(prompt, outputPath) {
    try {
        const puter = await init();
        
        console.log('Generating image with Puter AI...');
        
        const result = await puter.ai.txt2img(prompt, {
            model: 'stabilityai/stable-diffusion-3-medium',
            width: 1024,
            height: 1024,
            response_format: 'url'
        });
        
        // Download the image
        const https = require('https');
        const fs = require('fs');
        const file = fs.createWriteStream(outputPath);
        
        return new Promise((resolve, reject) => {
            https.get(result.src, (response) => {
                response.pipe(file);
                file.on('finish', () => {
                    file.close();
                    console.log('Image saved to:', outputPath);
                    resolve(outputPath);
                });
            }).on('error', (err) => {
                fs.unlink(outputPath);
                reject(err);
            });
        });
    } catch (error) {
        console.error('Error generating image:', error);
        throw error;
    }
}

const prompt = process.argv[2];
const outputPath = process.argv[3];

if (!prompt || !outputPath) {
    console.error('Usage: node puter_image.js "<prompt>" "<output_path>"');
    process.exit(1);
}

generateImage(prompt, outputPath)
    .then(() => {
        console.log('Success!');
        process.exit(0);
    })
    .catch((err) => {
        console.error('Failed:', err);
        process.exit(1);
    });
