import asyncio
from playwright.async_api import async_playwright



async def barbie(floor, hair_color, skin_color, photo, user_id, email="wed32333@gmail.com"):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        await page.goto("https://www.bairbie.me", timeout=80000)
        
        await page.get_by_text(floor, exact=True).click()
        
        await page.click('//*[@id="react-select-2-input"]')
        await page.get_by_text(hair_color, exact=True).click()
             
        await page.click('//*[@id="react-select-3-input"]')
        await page.get_by_text(skin_color, exact=True).click()
            
        await page.get_by_role("textbox").fill(str(user_id)+email)
        await page.locator('//*[@id="fileInput"]').set_input_files(photo)
        
        await page.get_by_text("Make My BaiRBIE").click()

        async with page.expect_download() as download_info:
    # Perform the action that initiates download
            await page.get_by_text("Download for free").click()
        download = await download_info.value
        # Wait for the download process to complete
        print(await download.path())
        # Save downloaded file somewhere
        await download.save_as(f"photos/{user_id}.jpg")
        
        await browser.close()