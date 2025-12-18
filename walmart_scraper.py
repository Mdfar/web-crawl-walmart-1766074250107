import json import os import time import pandas as pd from bs4 import BeautifulSoup from curl_cffi import requests from dotenv import load_dotenv

load_dotenv()

class WalmartStoreScraper: def init(self, store_id, zip_code): self.store_id = store_id self.zip_code = zip_code self.proxy_key = os.getenv("PROXY_API_KEY") self.session = requests.Session(impersonate="chrome110") self.base_headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,/;q=0.8", "Accept-Language": "en-US,en;q=0.5", }

def _get_location_cookies(self):
    """Generates the necessary cookies for store-level pricing/availability."""
    # Simplified location data structure used by Walmart's Next.js frontend
    loc_data = {
        "intent": "PICKUP",
        "pickup": {"nodeId": self.store_id},
        "postalCode": {"base": self.zip_code}
    }
    return {
        "nodeId": self.store_id,
        "postalCode": self.zip_code,
        "locGuestData": json.dumps(loc_data)
    }

def scrape_category(self, category_url, max_pages=1):
    all_products = []
    for page in range(1, max_pages + 1):
        url = f"{category_url}?page={page}"
        print(f"Scraping {url} for Store {self.store_id}...")
        
        try:
            # Use ScraperAPI/Proxy if key exists, else direct (unreliable for Walmart)
            if self.proxy_key:
                proxy_url = f"[http://api.scraperapi.com](http://api.scraperapi.com)?api_key={self.proxy_key}&url={url}&render=false"
                response = self.session.get(proxy_url, headers=self.base_headers, cookies=self._get_location_cookies())
            else:
                response = self.session.get(url, headers=self.base_headers, cookies=self._get_location_cookies())

            if response.status_code != 200:
                print(f"Failed to fetch page {page}: {response.status_code}")
                break

            soup = BeautifulSoup(response.text, "html.parser")
            script_data = soup.find("script", id="__NEXT_DATA__")
            
            if not script_data:
                print("Could not find __NEXT_DATA__ JSON blob.")
                continue

            data = json.loads(script_data.string)
            # Navigate the nested JSON for product items
            items = data.get("props", {}).get("pageProps", {}).get("initialData", {}).get("searchResult", {}).get("itemStacks", [{}])[0].get("items", [])
            
            for item in items:
                if item.get("__typename") == "Product":
                    product = {
                        "store_id": self.store_id,
                        "product_id": item.get("id"),
                        "name": item.get("name"),
                        "price": item.get("priceInfo", {}).get("currentPrice", {}).get("price"),
                        "currency": item.get("priceInfo", {}).get("currentPrice", {}).get("currencyUnit"),
                        "availability": item.get("inventory", {}).get("available"),
                        "url": f"[https://www.walmart.com](https://www.walmart.com){item.get('canonicalUrl')}",
                        "image": item.get("imageInfo", {}).get("thumbnailUrl"),
                        "brand": item.get("brand"),
                        "rating": item.get("rating", {}).get("averageRating")
                    }
                    all_products.append(product)
            
            time.sleep(2) # Politeness delay
        except Exception as e:
            print(f"Error on page {page}: {e}")
            
    return all_products


def run_automation(): with open('config.json', 'r') as f: config = json.load(f)

master_data = []
for store in config['stores']:
    scraper = WalmartStoreScraper(store['id'], store['zip'])
    for cat in config['categories']:
        results = scraper.scrape_category(cat['url'], config['settings']['max_pages_per_category'])
        master_data.extend(results)

# Exporting results
if master_data:
    df = pd.DataFrame(master_data)
    df.to_csv("walmart_store_data.csv", index=False)
    df.to_json("walmart_store_data.json", orient="records", indent=4)
    print(f"Success! Collected {len(master_data)} products.")


if name == "main": run_automation()