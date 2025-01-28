from playwright.async_api import async_playwright

async def crawl_and_save_html(user_input: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Set to True to run in headless mode
        page = await browser.new_page()

        # Navigate to the Florida Secretary of State business search page
        print("Navigating to the page...")
        await page.goto("https://search.sunbiz.org/Inquiry/CorporationSearch/ByName")

        # Type user input into the "Entity Name" text field
        print(f"Filling out the search form with user input: {user_input}")
        await page.fill('input[name="SearchTerm"]', user_input)

        # Click the "Search Now" button
        print("Clicking the 'Search Now' button...")
        await page.click('input[value="Search Now"]')

        # Wait for the new page to load
        print("Waiting for the page to load...")
        await page.wait_for_load_state('networkidle')

        # Extract the links from the table
        print("Extracting links from the table...")
        links = await page.query_selector_all('table tbody a[href]')
        
        if links:
            # Get the first link
            first_link = links[0]
            href = await first_link.get_attribute('href')
            print(f"Opening the first link: {href}")

            # Click the first link
            await first_link.click()

            # Wait for the page to load
            await page.wait_for_load_state('networkidle')

            # Go back to the previous page
            print("Going back to the previous page...")
            await page.go_back()

            # Wait for the page to load again after going back
            await page.wait_for_load_state('networkidle')

            # Re-query the links after going back to ensure they're valid
            print("Re-querying the links after going back...")
            links = await page.query_selector_all('table tbody a[href]')

            # Loop through the remaining links (skip the first one)
            for i in range(1, len(links)):
                link = links[i]
                href = await link.get_attribute('href')
                print(f"Opening link {i+1}: {href}")

                # Click the link
                await link.click()

                # Wait for the page to load
                await page.wait_for_load_state('networkidle')

                # Go back to the previous page
                print(f"Going back to the previous page after opening link {i+1}...")
                await page.go_back()

                # Wait for the page to load again after going back
                await page.wait_for_load_state('networkidle')

                # Re-query the links after going back to ensure they're valid
                print(f"Re-querying the links after going back from link {i+1}...")
                links = await page.query_selector_all('table tbody a[href]')
        else:
            print("No links found on the page.")

        # Close the browser
        await browser.close()
