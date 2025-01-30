# Florida Secretary of State Business Search Tool

This project is a web application built with Next.js, FastAPI, Supabase, and Playwright that allows users to search for registered businesses in Florida.  It leverages a backend service to crawl and scrape data from the Florida Secretary of State's website and store it in a Supabase database. The application provides a user-friendly interface for searching and viewing detailed business information.

## Features

* **Search Businesses:** Search for businesses by name.
* **Detailed Business Information:** View comprehensive details for each business, including name, document number, FEI/EIN number, filing date, status, principal address, mailing address, registered agent information, officer details, annual reports, and document URLs.
* **Mock Data Handling:** Gracefully handles cases where the external API is unavailable by displaying mock data and notifying the user.
* **Loading State Indication:** Displays a loading spinner while fetching data.
* **Error Handling:** Provides clear error messages when API requests fail.
* **Responsive Design:** Adapts seamlessly to various screen sizes.
* **Efficient Data Fetching:** Uses React Query for efficient data fetching and caching.
* **Animated UI Elements:**  Includes animations for a smoother user experience.

## Usage

1.  **Run the development server:**
    ```bash
    npm run dev
    # or
    yarn dev
    # or
    pnpm dev
    # or
    bun dev
    ```
2.  Open [http://localhost:3000](http://localhost:3000) in your browser.
3.  Enter a business name in the search bar and press Enter or click the search button.
4.  View the search results with detailed business information.

## Installation

1.  Clone the repository:
    ```bash
    git clone <repository_url>
    ```
2.  Navigate to the project directory:
    ```bash
    cd business-search-tool
    ```
3.  Install dependencies:
    ```bash
    npm install
    # or
    yarn install
    # or
    pnpm install
    # or
    bun install

    #front end dependencies (for clarification)
    npm install @tanstack/react-query lucide-react

    #back end dependencies (make sure to have pip!)
    pip install playwright supabase py-dotenv beautifulsoup4 fastapi databases pydantic
    ```
4.  Start the backend server (located in the `backend` directory). You'll need Python 3, pip, and more as mentioned below.
    ```bash
    #back end dependencies (make sure to have pip!), cd backend, runs on localhost:8000 or note ip address given in console
    pip install playwright supabase py-dotenv beautifulsoup4 fastapi databases pydantic
    uvicorn main:app --reload
    ```
6.  Run the development server using the command provided in the Usage section.

## Technologies Used

* **Next.js:** A React framework for building web applications. Used for the frontend of the application.
* **React:** A JavaScript library for building user interfaces. Used for the frontend components.
* **Tailwind CSS:** A utility-first CSS framework. Used for styling the application.
* **@tanstack/react-query:**  A data fetching library for React.  Handles asynchronous data fetching and caching efficiently.
* **Lucide:**  An icon library providing the icons used in the application.
* **Playwright:**  A Node library used for web automation, particularly in the backend to crawl and scrape data.
* **FastAPI:** A modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.  Used for the backend API.
* **Supabase:** A backend-as-a-service (BaaS) platform, providing database (PostgreSQL) and other functionalities. Used for persistent storage of business data.
* **Python:** Used for the backend server's logic (web scraping and data processing).
* **Beautiful Soup:** Python library for parsing HTML and XML documents. Used for extracting data from web pages.


## API Documentation

The backend API (located in the `backend` directory) exposes the following endpoints:


**POST `/crawl`**

*   **Request Body:**
    ```json
    {
      "user_input": "string"
    }
    ```
*   **Response:**
    ```json
    {
      "message": "Crawl successful",
      "names": ["business_name_1", "business_name_2", ...]
    }
    ```
    or
    ```json
    {
      "message": "Crawl failed",
      "error": "string"
    }
    ```

**POST `/businesses`**

*   **Request Body:**
    ```json
    {
      "names": ["business_name_1", "business_name_2", ...]
    }
    ```
*   **Response:** (Array of business objects or 404 error if not found)


**GET `/business/{business_name}`**

*   **Response:** A JSON object representing the business details.  Or a 404 if not found.


## Dependencies

The project dependencies are listed in the `package.json` file.
