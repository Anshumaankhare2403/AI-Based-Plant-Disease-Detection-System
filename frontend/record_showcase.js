import { chromium } from '@playwright/test';
import path from 'path';
import fs from 'fs';

async function recordShowcase() {
  console.log('[Showcase] Launching Microsoft Edge browser with Playwright...');
  const screenshotsDir = path.resolve('../docs/screenshots');
  const videosDir = path.resolve('../docs/videos');

  if (!fs.existsSync(screenshotsDir)) fs.mkdirSync(screenshotsDir, { recursive: true });
  if (!fs.existsSync(videosDir)) fs.mkdirSync(videosDir, { recursive: true });

  const browser = await chromium.launch({
    channel: 'msedge',
    headless: true,
  });

  const context = await browser.newContext({
    viewport: { width: 1280, height: 720 },
    recordVideo: {
      dir: videosDir,
      size: { width: 1280, height: 720 },
    },
  });

  const page = await context.newPage();
  const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

  try {
    // 1. Landing Page
    console.log('[Showcase] 1. Visiting Landing Page...');
    await page.goto('http://127.0.0.1:5173/');
    await page.waitForLoadState('networkidle');
    await sleep(1500);
    await page.screenshot({ path: path.join(screenshotsDir, '01_landing_hero.png') });
    console.log('[Showcase] Saved 01_landing_hero.png');

    // Scroll to see supported crops and features
    await page.evaluate(() => window.scrollBy({ top: 500, behavior: 'smooth' }));
    await sleep(1200);
    await page.evaluate(() => window.scrollBy({ top: 600, behavior: 'smooth' }));
    await sleep(1200);
    await page.screenshot({ path: path.join(screenshotsDir, '01_landing_fullpage.png'), fullPage: true });
    console.log('[Showcase] Saved 01_landing_fullpage.png');

    // Scroll back up
    await page.evaluate(() => window.scrollTo({ top: 0, behavior: 'smooth' }));
    await sleep(800);

    // 2. Registration / Authentication
    console.log('[Showcase] 2. Navigating to Register Page...');
    await page.goto('http://127.0.0.1:5173/register');
    await page.waitForLoadState('networkidle');
    const timestamp = Date.now();
    await page.getByPlaceholder(/Dr\. Maya Patel/i).fill('Agronomist Showcase');
    await page.getByPlaceholder(/agronomist@farm\.org/i).fill(`demo_${timestamp}@plantcare.org`);
    await page.getByPlaceholder(/At least 6 characters/i).fill('demoPassword123');
    await page.getByPlaceholder(/Repeat password/i).fill('demoPassword123');
    await sleep(1200);
    await page.screenshot({ path: path.join(screenshotsDir, '02_register_account.png') });
    console.log('[Showcase] Saved 02_register_account.png');

    await page.getByRole('button', { name: /Create Account/i }).click();
    await sleep(2000);

    // 3. Dashboard Analytics
    console.log('[Showcase] 3. Viewing Dashboard Analytics...');
    await page.waitForURL(/.*dashboard/);
    await sleep(2000);
    await page.screenshot({ path: path.join(screenshotsDir, '03_dashboard_analytics.png') });
    console.log('[Showcase] Saved 03_dashboard_analytics.png');

    // 4. Disease Detection Page
    console.log('[Showcase] 4. Navigating to Foliar Disease Detection...');
    await page.getByRole('link', { name: /New Scan/i }).click();
    await page.waitForURL(/.*detect/);
    await sleep(1200);

    // Upload leaf sample
    const testImagePath = path.resolve('./e2e/test_leaf.jpg');
    const fileChooserPromise = page.waitForEvent('filechooser');
    await page.locator('div[class*="border-dashed"]').click();
    const fileChooser = await fileChooserPromise;
    await fileChooser.setFiles(testImagePath);
    await sleep(1500);

    await page.screenshot({ path: path.join(screenshotsDir, '04_disease_detection_upload.png') });
    console.log('[Showcase] Saved 04_disease_detection_upload.png');

    // Run CNN diagnosis
    console.log('[Showcase] 5. Running CNN Diagnosis...');
    await page.getByRole('button', { name: /Run CNN Diagnosis/i }).click();
    await page.locator('text=Diagnosis Report').waitFor({ timeout: 15000 });
    await sleep(2500);

    // Scroll down to view management protocols
    await page.screenshot({ path: path.join(screenshotsDir, '05_diagnosis_result_recommendations.png') });
    console.log('[Showcase] Saved 05_diagnosis_result_recommendations.png');

    await page.evaluate(() => window.scrollBy({ top: 400, behavior: 'smooth' }));
    await sleep(1500);
    await page.screenshot({ path: path.join(screenshotsDir, '05_diagnosis_protocols.png') });
    console.log('[Showcase] Saved 05_diagnosis_protocols.png');

    // 6. Detection History
    console.log('[Showcase] 6. Navigating to Detection History...');
    await page.getByRole('link', { name: /History/i }).first().click();
    await page.waitForURL(/.*history/);
    await sleep(2000);
    await page.screenshot({ path: path.join(screenshotsDir, '06_detection_history.png') });
    console.log('[Showcase] Saved 06_detection_history.png');

    // 7. Model Info / Architecture Page
    console.log('[Showcase] 7. Navigating to Model Architecture Info...');
    await page.getByRole('link', { name: /Model Info/i }).first().click();
    await page.waitForURL(/.*model-info/);
    await sleep(2000);
    await page.screenshot({ path: path.join(screenshotsDir, '07_model_architecture_info.png') });
    console.log('[Showcase] Saved 07_model_architecture_info.png');

    // 8. About Project Page
    console.log('[Showcase] 8. Navigating to About Page...');
    await page.getByRole('link', { name: /About/i }).first().click();
    await page.waitForURL(/.*about/);
    await sleep(2000);
    await page.screenshot({ path: path.join(screenshotsDir, '08_about_project.png') });
    console.log('[Showcase] Saved 08_about_project.png');

    console.log('[Showcase] Workflow completed successfully.');
  } catch (err) {
    console.error('[Showcase] Error during recording:', err);
  } finally {
    // Close context to finish writing the video
    const videoObj = page.video();
    await page.close();
    await context.close();
    await browser.close();

    if (videoObj) {
      const originalVideoPath = await videoObj.path();
      const finalVideoPath = path.join(videosDir, 'plantcare_ai_demo.webm');
      console.log(`[Showcase] Video originally saved to: ${originalVideoPath}`);
      if (fs.existsSync(originalVideoPath)) {
        fs.copyFileSync(originalVideoPath, finalVideoPath);
        console.log(`[Showcase] Final demo video saved to: ${finalVideoPath}`);
      }
    }
  }
}

recordShowcase();

