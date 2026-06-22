import puppeteer from 'puppeteer';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));

const browser = await puppeteer.launch({
  headless: true,
  args: ['--no-sandbox', '--disable-setuid-sandbox']
});

const page = await browser.newPage();
await page.setViewport({ width: 1200, height: 630, deviceScaleFactor: 2 });
await page.goto('file://' + resolve(__dirname, 'og-template.html'), { waitUntil: 'networkidle0' });
await new Promise(r => setTimeout(r, 800));

await page.screenshot({
  path: resolve(__dirname, 'og-image.png'),
  clip: { x: 0, y: 0, width: 1200, height: 630 }
});

await browser.close();
console.log('Saved → og-image.png (1200×630 @2x)');
