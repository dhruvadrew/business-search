import os
from playwright.async_api import async_playwright
from supabase import create_client, Client
from dotenv import load_dotenv
from bs4 import BeautifulSoup


load_dotenv()
url = os.getenv("DATABASE_URL")
key = os.getenv("DATABASE_KEY")

supabase: Client = create_client(url, key)

def extract_document_images(html):
    soup = BeautifulSoup(html, "html.parser")
    
    # Find all divs with class "detailSection"
    detail_sections = soup.find_all("div", class_="detailSection")
    
    # Loop through each detailSection to find the one with "Document Images"
    for detail_section in detail_sections:
        span = detail_section.find("span", string="Document Images")
        if span:
            # Find the next table after this span
            table = span.find_next("table")
            if table:
                # Extract rows from tbody
                rows = table.find("tbody").find_all("tr")
                
                document_data = []
                for row in rows:  # Iterate through all rows without skipping
                    cols = row.find_all("td")
                    if len(cols) >= 2:
                        # Assuming the first column contains the document name or ID
                        document_name = cols[0].text.strip()
                        # Assuming the second column contains the link to the document image
                        document_url = cols[1].find("a")["href"] if cols[1].find("a") else None
                        if document_url:
                            # Prepend the base URL to the document URL
                            full_url = "https://search.sunbiz.org" + document_url
                            document_data.append({"Document Name": document_name, "Document URL": full_url})

                return document_data  # Return the first matching document data

    return []  # Return an empty list if no matching section is found


def extract_principal_address_and_changed_date(html):
    soup = BeautifulSoup(html, "html.parser")
    
    # Find all divs with class "detailSection"
    detail_sections = soup.find_all("div", class_="detailSection")
    
    # Loop through each detailSection to find the one with "Principal Address"
    for detail_section in detail_sections:
        span = detail_section.find("span", string="Principal Address")
        if span:
            # Find the next span element and the div inside it for the principal address
            address_div = span.find_next("span").find_next("div")
            if address_div:
                # Combine all the text from the div's children with new lines
                address_parts = [line.strip() for line in address_div.stripped_strings]
                principal_address = "\n".join(address_parts)
            else:
                principal_address = ""  # If no address div is found, set it to empty string
            
            # Find the next span after the principal address for the "Changed: " text
            changed_date_span = span.find_next("span", string=lambda text: text and text.startswith("Changed:"))
            if changed_date_span:
                # Extract the date part after "Changed: "
                changed_date = changed_date_span.text.strip().replace("Changed: ", "")
            else:
                changed_date = ""  # If "Changed: " span is not found, set it as empty

            return principal_address, changed_date  # Return both principal address and changed date

    return "", ""  # Return empty strings if no matching section is found


def extract_mailing_address_and_changed_date(html):
    soup = BeautifulSoup(html, "html.parser")
    
    # Find all divs with class "detailSection"
    detail_sections = soup.find_all("div", class_="detailSection")
    
    # Loop through each detailSection to find the one with "Mailing Address"
    for detail_section in detail_sections:
        span = detail_section.find("span", string="Mailing Address")
        if span:
            # Find the next span element and the div inside it for the mailing address
            address_div = span.find_next("span").find_next("div")
            if address_div:
                # Combine all the text from the div's children with new lines
                address_parts = [line.strip() for line in address_div.stripped_strings]
                mailing_address = "\n".join(address_parts)
                
                # Find the next span after the mailing address for the "Changed: " text
                changed_date_span = span.find_next("span", string=lambda text: text and text.startswith("Changed:"))
                print(changed_date_span)
                if changed_date_span:
                    # Extract the date part after "Changed: "
                    changed_date = changed_date_span.text.strip().replace("Changed: ", "")
                else:
                    changed_date = ""  # If "Changed: " span is not found, set it as empty

                return mailing_address, changed_date  # Return both mailing address and changed date

    return "", None  # Return empty strings if no matching section is found


def extract_annual_reports(html):
    soup = BeautifulSoup(html, "html.parser")
    
    # Find all divs with class "detailSection"
    detail_sections = soup.find_all("div", class_="detailSection")
    
    # Loop through each detailSection to find the one with "Annual Reports"
    for detail_section in detail_sections:
        span = detail_section.find("span", string="Annual Reports")
        if span:
            # Find the next table after this span
            table = span.find_next("table")
            if table:
                # Extract rows from tbody
                rows = table.find("tbody").find_all("tr")
                
                # Ignore the first row (header)
                report_data = []
                for row in rows[1:]:  # Skip the first row
                    cols = row.find_all("td")
                    if len(cols) >= 2:
                        report_year = cols[0].text.strip()
                        filed_date = cols[1].text.strip()
                        report_data.append({"Report Year": report_year, "Filed Date": filed_date})

                return report_data  # Return the first matching report data

async def extract_business_details(page):
    """Extract business details from the page."""
    business_data = {
        'name': await page.inner_text('div.corporationName p:nth-child(2)'),
        'document_number': await page.inner_text('label[for="Detail_DocumentId"] + span'),
        'fei_ein_number': await page.inner_text('label[for="Detail_FeiEinNumber"] + span'),
        'date_filed': await page.inner_text('label[for="Detail_FileDate"] + span'),
        'state': await page.inner_text('label[for="Detail_EntityStateCountry"] + span'),
        'status': await page.inner_text('label[for="Detail_Status"] + span'),
        'last_event': await page.inner_text('label[for="Detail_LastEvent"] + span'),
        'event_date_filed': await page.inner_text('label[for="Detail_LastEventFileDate"] + span'),
    }

    html = await page.content()

    # Extract principal address
    principal_address, principal_changed = extract_principal_address_and_changed_date(html)
    business_data["principal_address"] = principal_address
    business_data["principal_changed"] = principal_changed
    

    # Extract mailing address
    mailing_address, changed_date = extract_mailing_address_and_changed_date(html)
    business_data["mailing_address"] = mailing_address
    business_data["mailing_changed"] = changed_date

    # Extract annual reports
    annual_reports = []
    annual_reports = extract_annual_reports(html)

    # Extract document URLs
    document_urls = []
    document_urls = extract_document_images(html)

    business_data["annual_reports"] = annual_reports
    business_data["document_urls"] = document_urls

    print(business_data)

    return business_data



def save_to_database(data):
    """Save extracted data to the database."""

    # Ensure that the changed_date is set to None if it's empty
    if not data.get("mailing_changed"):
        data["mailing_changed"] = None  # Set to None if empty

    if not data.get("principal_changed"):
        data["principal_changed"] = None  # Set to None if empty

    supabase.table("businesses").insert(data).execute()
    print(f"Successfully saved business: {data['name']}")

async def crawl_and_save_html(user_input: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, slow_mo=0)  # Set to True to run in headless mode
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
        #await page.wait_for_load_state('networkidle')

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
            #await page.wait_for_load_state('networkidle')

            # Extract business details
            print("Extracting business details...")
            business_data = await extract_business_details(page)

            # Save business details to the database
            print("Saving business details to the database...")
            save_to_database(business_data)

            # Go back to the previous page
            print("Going back to the previous page...")
            await page.go_back()

            # Wait for the page to load again after going back
            #await page.wait_for_load_state('networkidle')

            # Re-query the links after going back to ensure they're valid
            print("Re-querying the links after going back...")
            links = await page.query_selector_all('table tbody a[href]')

            # Loop through the remaining links (skip the first one)
            j = min(5, len(links))
            for i in range(1, j):
                link = links[i]
                href = await link.get_attribute('href')
                print(f"Opening link {i+1}: {href}")

                # Click the link
                await link.click()

                # Wait for the page to load
                #await page.wait_for_load_state('networkidle')

                # Extract business details
                print("Extracting business details...")
                business_data = await extract_business_details(page)

                # Save business details to the database
                print("Saving business details to the database...")
                save_to_database(business_data)

                # Go back to the previous page
                print(f"Going back to the previous page after opening link {i+1}...")
                await page.go_back()

                # Wait for the page to load again after going back
                #await page.wait_for_load_state('networkidle')

                # Re-query the links after going back to ensure they're valid
                print(f"Re-querying the links after going back from link {i+1}...")
                links = await page.query_selector_all('table tbody a[href]')
        else:
            print("No links found on the page.")

        # Close the browser
        await browser.close()
