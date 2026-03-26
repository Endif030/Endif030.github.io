#!/usr/bin/env node

// Parse Tavily search results and format for investment report

const fs = require('fs');

if (process.argv.length < 3) {
    console.error('Usage: node parse-results.js <input_json_file>');
    process.exit(1);
}

const inputFile = process.argv[2];

try {
    const data = JSON.parse(fs.readFileSync(inputFile, 'utf8'));
    
    if (data.results && data.results.length > 0) {
        const results = data.results.slice(0, 2); // Take top 2
        results.forEach((result, idx) => {
            console.log(`### ${result.title}`);
            console.log(`*Source: ${result.source}*`);
            console.log('');
            if (result.content) {
                const content = result.content.length > 300 ? 
                    result.content.substring(0, 300) + '...' : 
                    result.content;
                console.log(content);
                console.log('');
            }
            console.log(`🔗 [Read more](${result.url})`);
            console.log('');
        });
    }
} catch (error) {
    console.error(`Error parsing ${inputFile}:`, error.message);
    process.exit(1);
}