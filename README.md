Walmart Store-Level Web Scraper

I have scraped Walmart by retail stores using Python and specialized request handling. My approach centers on extracting the __NEXT_DATA__ JSON blob from the page source, which is significantly more stable than CSS selectors and contains high-fidelity product data including store-specific pricing.

Features

Store-Level Precision: Injects locGuestData and nodeId cookies to simulate a specific retail location.

Anti-Bot Bypass: Utilizes curl-cffi to mimic Chrome TLS fingerprints, reducing the risk of Akamai/PerimeterX blocks.

Optimized Performance: Extracts data from embedded JSON rather than parsing the entire DOM.

Scalable Exports: Generates both CSV and JSON structured data.

Setup & Run

Install Dependencies:

Bash
pip install -r requirements.txt


Configure API:

Walmart has aggressive bot detection. It is highly recommended to add a SCRAPERAPI_KEY to the .env file for high-volume tasks.

Configure Targets:

Edit config.json to add the store_id and zip_code for the stores you wish to crawl.

Execution:

Bash
python walmart_scraper.py

Automation Logic

To set up an automatic run (Task 4 in scope), use a Cron job (Linux) or Task Scheduler (Windows) to trigger python walmart_scraper.py at your desired interval. The script is designed to be idempotent and will overwrite/append based on your business logic.