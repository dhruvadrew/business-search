from playwright.sync_api import sync_playwright

def crawl_and_save_html(user_input):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Set to True to run in headless mode
        page = browser.new_page()

        # Navigate to the Florida Secretary of State business search page
        print("Navigating to the page...")
        page.goto("https://search.sunbiz.org/Inquiry/CorporationSearch/ByName")

        # Type user input into the "Entity Name" text field
        print(f"Filling out the search form with user input: {user_input}")
        page.fill('input[name="SearchTerm"]', user_input)

        # Click the "Search Now" button
        print("Clicking the 'Search Now' button...")
        page.click('input[value="Search Now"]')

        # Wait for the new page to load
        print("Waiting for the page to load...")
        page.wait_for_load_state('networkidle')

        # Extract the links from the table
        print("Extracting links from the table...")
        links = page.query_selector_all('table tbody a[href]')
        
        if links:
            # Get the first link
            first_link = links[0]
            href = first_link.get_attribute('href')
            print(f"Opening the first link: {href}")

            # Click the first link
            first_link.click()

            # Wait for the page to load
            page.wait_for_load_state('networkidle')

            # Go back to the previous page
            print("Going back to the previous page...")
            page.go_back()

            # Wait for the page to load again after going back
            page.wait_for_load_state('networkidle')

            # Re-query the links after going back to ensure they're valid
            print("Re-querying the links after going back...")
            links = page.query_selector_all('table tbody a[href]')

            # Loop through the remaining links (skip the first one)
            for i in range(1, len(links)):
                link = links[i]
                href = link.get_attribute('href')
                print(f"Opening link {i+1}: {href}")

                # Click the link
                link.click()

                # Wait for the page to load
                page.wait_for_load_state('networkidle')

                # Go back to the previous page
                print(f"Going back to the previous page after opening link {i+1}...")
                page.go_back()

                # Wait for the page to load again after going back
                page.wait_for_load_state('networkidle')

                # Re-query the links after going back to ensure they're valid
                print(f"Re-querying the links after going back from link {i+1}...")
                links = page.query_selector_all('table tbody a[href]')
        else:
            print("No links found on the page.")

        # Close the browser
        browser.close()

# Example usage
user_input = "ACME COMEDY"
crawl_and_save_html(user_input)
