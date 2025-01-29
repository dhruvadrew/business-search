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
                if changed_date_span:
                    # Extract the date part after "Changed: "
                    changed_date = changed_date_span.text.strip().replace("Changed: ", "")
                else:
                    changed_date = ""  # If "Changed: " span is not found, set it as empty

                return mailing_address, changed_date  # Return both mailing address and changed date

    return "", None  # Return empty strings if no matching section is found

def extract_officer_director_details(html):
    soup = BeautifulSoup(html, "html.parser")
    
    # Find all divs with class "detailSection"
    detail_sections = soup.find_all("div", class_="detailSection")
    
    # Initialize a list to store officer/director details
    officer_details = []
    
    # Initialize an array to store names
    names = []
    
    # Loop through each detailSection to find the one with "Officer/Director Detail"
    for detail_section in detail_sections:
        span = detail_section.find("span", string="Officer/Director Detail")
        if not span:
            span = detail_section.find("span", string="Authorized Person(s) Detail")
        if span:            
            # Skip the next span
            next_span = span.find_next("span")
            
            # Find the second span which starts with "Title "
            title_span = next_span.find_next("span", string=lambda text: text and text.startswith("Title"))
            if title_span:
                # Extract the officer title
                officer_title = title_span.text[6:]
                
                # Skip the next two <br> elements to get to the officer name (plain text)
                title_span.find_next("br")  # Skip first <br>
                title_span.find_next("br")  # Skip second <br>
                
                # The officer name is two lines after the title
                officer_name = title_span.find_next("br").find_next("br").find_next(text=True).strip()
                
                # Add the officer name to the names array
                names.append(officer_name)
                
                # The officer address is in the next div after the officer name
                address_div = title_span.find_next("span").find_next("div")
                officer_address = ""
                if address_div:
                    # Combine all the text from the div's children with new lines
                    address_parts = [line.strip() for line in address_div.stripped_strings]
                    officer_address = "\n".join(address_parts)
                
                # Add the officer details to the list
                officer_details.append({
                    "officer_title": officer_title,
                    "officer_name": officer_name,
                    "officer_address": officer_address
                })
                
                # Now look for any subsequent officer/director details
                next_officer_span = title_span.find_next("span", string=lambda text: text and text.startswith("Title"))
                print(next_officer_span)
                while next_officer_span:
                    # Extract the title, name, and address for each officer
                    officer_title = next_officer_span.text[6:]
                    
                    # Extract the officer name (plain text)
                    officer_name = next_officer_span.find_next("br").find_next("br").find_next(text=True).strip()
                    
                    # Extract the address from the next div
                    address_div = next_officer_span.find_next("span").find_next("div")
                    officer_address = ""
                    if address_div:
                        address_parts = [line.strip() for line in address_div.stripped_strings]
                        officer_address = "\n".join(address_parts)
                    
                    # Add the officer details to the list
                    officer_details.append({
                        "officer_title": officer_title,
                        "officer_name": officer_name,
                        "officer_address": officer_address
                    })
                    
                    # Look for the next officer/director title
                    next_officer_span = next_officer_span.find_next("span", string=lambda text: text and text.startswith("Title "))
    
    return officer_details



def extract_registered_agent_details(html):
    soup = BeautifulSoup(html, "html.parser")
    
    # Find all divs with class "detailSection"
    detail_sections = soup.find_all("div", class_="detailSection")
    
    # Initialize variables to store the extracted data
    registered_agent_name = ""
    registered_agent_address = ""
    name_changed = ""
    address_changed = ""
    
    # Loop through each detailSection to find the one with "Registered Agent Name & Address"
    for detail_section in detail_sections:
        span = detail_section.find("span", string="Registered Agent Name & Address")
        if span:
            # Find the next span for the registered agent name
            registered_agent_name_span = span.find_next("span")
            if registered_agent_name_span:
                registered_agent_name = registered_agent_name_span.text.strip()
            
            # Find the next div for the registered agent address
            address_div = registered_agent_name_span.find_next("span").find_next("div")
            if address_div:
                # Combine all the text from the div's children with new lines
                address_parts = [line.strip() for line in address_div.stripped_strings]
                registered_agent_address = "\n".join(address_parts)
            
            # Check for "Name Changed: " span
            name_changed_span = span.find_next("span", string=lambda text: text and text.startswith("Name Changed:"))
            if name_changed_span:
                name_changed = name_changed_span.text.strip().replace("Name Changed: ", "")
            
            # Check for "Address Changed: " span
            address_changed_span = span.find_next("span", string=lambda text: text and text.startswith("Address Changed:"))
            if address_changed_span:
                address_changed = address_changed_span.text.strip().replace("Address Changed: ", "")
            
            return registered_agent_name, registered_agent_address, name_changed, address_changed
    
    # Return empty strings if no matching section is found
    return "", "", "", ""


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

async def get_inner_text_or_none(page, selector):
    element = await page.query_selector(selector)
    return await element.inner_text() if element else None  # Return None if element not found


async def extract_business_details(page):
    """Extract business details from the page."""
    business_data = {
    'name': await get_inner_text_or_none(page, 'div.corporationName p:nth-child(2)'),
    'document_number': await get_inner_text_or_none(page, 'label[for="Detail_DocumentId"] + span'),
    'fei_ein_number': await get_inner_text_or_none(page, 'label[for="Detail_FeiEinNumber"] + span'),
    'date_filed': await get_inner_text_or_none(page, 'label[for="Detail_FileDate"] + span'),
    'state': await get_inner_text_or_none(page, 'label[for="Detail_EntityStateCountry"] + span'),
    'status': await get_inner_text_or_none(page, 'label[for="Detail_Status"] + span'),
    'last_event': await get_inner_text_or_none(page, 'label[for="Detail_LastEvent"] + span'),
    'event_date_filed': await get_inner_text_or_none(page, 'label[for="Detail_LastEventFileDate"] + span'),
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

    # Extract registered agent details
    registered_agent_name, registered_agent_address, name_changed, address_changed = extract_registered_agent_details(html)
    business_data["registered_agent_name"] = registered_agent_name
    business_data["registered_agent_address"] = registered_agent_address
    business_data["name_changed"] = name_changed
    business_data["address_changed"] = address_changed

    # Extract officer/director details
    officer_details = extract_officer_director_details(html)
    print(officer_details)
    business_data["officer_details"] = officer_details

    business_data["annual_reports"] = annual_reports
    business_data["document_urls"] = document_urls

    print(business_data)

    return business_data



def save_to_database(data):
    """Save extracted data to the database."""

    # Ensure that empty strings are treated as None so Date Crashing doesn't break program
    for key, value in data.items():
        if value == "":
            data[key] = None  # Set empty strings to None for database

    supabase.table("businesses").insert(data).execute()
    print(f"Successfully saved business: {data['name']}")

async def crawl_and_save_html(user_input: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, slow_mo=0)  # Set to True to run in headless mode
        page = await browser.new_page()
        names = []

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
            name = await first_link.text_content()
            print(f"Opening the first link")

            if supabase.table("businesses").select("*").eq("name", name).execute().data:
                print(f"Business already exists in database: {name}")
                names.append(name)
            else:

                # Click the first link
                await first_link.click()
                name = await get_inner_text_or_none(page, 'div.corporationName p:nth-child(2)')
                if supabase.table("businesses").select("*").eq("name", name).execute().data:
                    print(f"Business already exists in database: {name}")
                    await page.go_back()
                    links = await page.query_selector_all('table tbody a[href]')
                    names.append(name)
                else:

                    # Wait for the page to load
                    #await page.wait_for_load_state('networkidle')

                    # Extract business details
                    print("Extracting business details...")
                    business_data = await extract_business_details(page)

                    # Save business details to the database
                    print("Saving business details to the database...")
                    save_to_database(business_data)
                    names.append(business_data["name"])

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
                name = await link.text_content()
                print(name)

                if supabase.table("businesses").select("*").eq("name", name).execute().data:
                    print(f"Business already exists in database: {name}")
                    names.append(name)
                    continue
                print(f"Opening link {i+1}")

                # Click the link
                await link.click()

                name = await page.inner_text('div.corporationName p:nth-child(2)')

                if supabase.table("businesses").select("*").eq("name", name).execute().data:
                    print(f"Business already exists in database: {name}")
                    await page.go_back()
                    links = await page.query_selector_all('table tbody a[href]')
                    continue

                # Wait for the page to load
                #await page.wait_for_load_state('networkidle')

                # Extract business details
                print("Extracting business details...")
                business_data = await extract_business_details(page)

                # Save business details to the database
                print("Saving business details to the database...")
                save_to_database(business_data)
                names.append(business_data["name"])

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

        return names
