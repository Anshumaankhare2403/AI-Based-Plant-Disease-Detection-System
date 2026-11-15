import { test, expect } from '@playwright/test';
import path from 'path';

test.describe('PlantCare AI - End-to-End User Journey', () => {
  const uniqueId = Date.now();
  const testUser = {
    name: `Agronomist ${uniqueId}`,
    email: `tester_${uniqueId}@agrifarm.org`,
    password: 'password123',
  };

  test('Complete workflow: Register, Navigate, Upload Leaf, Diagnose, View History, Logout', async ({ page }) => {
    // 1. Open the application
    await page.goto('/');
    await expect(page).toHaveTitle(/PlantCare AI/i);
    await expect(page.getByRole('link', { name: /Diagnose Leaf Now/i })).toBeVisible();

    // 2. Register with a test account
    await page.goto('/register');
    await page.getByPlaceholder(/Dr\. Maya Patel/i).fill(testUser.name);
    await page.getByPlaceholder(/agronomist@farm\.org/i).fill(testUser.email);
    await page.getByPlaceholder(/At least 6 characters/i).fill(testUser.password);
    await page.getByPlaceholder(/Repeat password/i).fill(testUser.password);
    await page.getByRole('button', { name: /Create Account/i }).click();

    // Verify redirected to dashboard and user is signed in
    await expect(page).toHaveURL(/.*dashboard/);
    await expect(page.getByText(new RegExp(testUser.name, 'i'))).toBeVisible();

    // 3. Navigate to disease detection
    await page.getByRole('link', { name: /New Scan/i }).click();
    await expect(page).toHaveURL(/.*detect/);

    // 4. Upload a valid test image
    const filePath = path.resolve('./e2e/test_leaf.jpg');
    const fileChooserPromise = page.waitForEvent('filechooser');
    await page.locator('div[class*="border-dashed"]').click();
    const fileChooser = await fileChooserPromise;
    await fileChooser.setFiles(filePath);

    // Verify preview is displayed
    await expect(page.locator('img[alt="Leaf preview"]')).toBeVisible();

    // 5. Submit the image
    await page.getByRole('button', { name: /Run CNN Diagnosis/i }).click();

    // 6. Verify the prediction result
    await expect(page.getByText(/Diagnosis Report/i)).toBeVisible({ timeout: 15000 });
    await expect(page.getByText(/Classification Confidence/i)).toBeVisible();
    await expect(page.getByText(/Recommended Agronomic Management Protocols/i)).toBeVisible();

    // 7. Verify the history record
    await page.getByRole('link', { name: /History/i }).first().click();
    await expect(page).toHaveURL(/.*history/);
    await expect(page.locator('table tbody tr').first()).toBeVisible();

    // 8. Log out
    const logoutBtn = page.locator('button[title="Logout"]');
    await logoutBtn.click();
    await expect(page.getByRole('link', { name: /Log In/i })).toBeVisible();
  });
});

