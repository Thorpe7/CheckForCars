""" Script for scraping data from sites of interest. """

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WebScraper:
    def __init__(
        self,
        site_queries: list,
    ):
        self.site_queries = site_queries

    def submit_requests_and_parse(
        self,
    ):
        parsed_text_data = []
        for query in self.site_queries:
            response = requests.get(query)
            if response.status_code == 200:
                html_content = response.text
                soup = BeautifulSoup(html_content, "html.parser")
                parsed_text_data.append(soup)
            else:
                print(f"Failed to retrieve content: {response.status_code}")

        self.parsed_text_data = parsed_text_data

        return parsed_text_data

    def extract_car_data(
        self,
    ):
        for soup in self.parsed_text_data:
            vehicles = soup.find_all("div", class_="vehicle-card")

            for vehicle in vehicles:
                model = vehicle.find("span", class_="model-name").text.strip()
                trim = vehicle.find("span", class_="trim-level").text.strip()
                color = vehicle.find("span", class_="exterior-color").text.strip()
                year = vehicle.find("span", class_="model-year").text.strip()
                price = vehicle.find("span", class_="price").text.strip()
                print(
                    f"Model: {model}, Trim: {trim}, Color: {color}, Year: {year}, Price: {price}"
                )

    def selenium_request_and_parse(
        self,
    ):
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.binary_location = "/usr/local/bin/google-chrome"
        # chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--disable-dev-shm-usage")
        # chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
        # chrome_options.add_argument(
        #     "--remote-debugging-port=9222"
        # )  # Enable remote debugging

        # Set up the WebDriver (ensure you have the appropriate driver installed)
        service = Service("/usr/local/bin/chromedriver")
        driver = webdriver.Chrome(service=service, options=chrome_options)

        parsed_text_data = []
        for query in self.site_queries:
            driver.get(query)

            try:
                # Wait for the vehicle listings to load
                WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "vehicle-card"))
                )
                page_source = driver.page_source
                soup = BeautifulSoup(page_source, "html.parser")
                parsed_text_data.append(soup)

            finally:
                driver.quit()

        self.parsed_text_data = parsed_text_data
        return parsed_text_data


if __name__ == "__main__":
    site_queries = [
        "https://inventory.landroverusa.com/used-certified/search/#/?isFranchiseApproved=true&saleLocationDistance%5Bdistance%5D=0&saleLocationDistance%5Bunit%5D=miles&saleLocationDistance%5Blat%5D=44.90532&saleLocationDistance%5Blon%5D=-93.3387&saleLocationDistance%5Blocation%5D=55424&model%5B0%5D=defender&modelVariant%5B0%5D=defender_x-dynamic%20hse&modelVariant%5B1%5D=defender_x-dynamic%20se&modelVariant%5B2%5D=defender_x%20dynamic%20hse&modelVariant%5B3%5D=defender_defender%20110&modelVariant%5B4%5D=defender_x%20dynamic%20se&productionYear%5Bfrom%5D=2021&productionYear%5Bto%5D=2021&genericColour%5B0%5D=black",
        "https://inventory.landroverusa.com/used-certified/search/#/?isFranchiseApproved=true&saleLocationDistance%5Bdistance%5D=0&saleLocationDistance%5Bunit%5D=miles&saleLocationDistance%5Blat%5D=44.90532&saleLocationDistance%5Blon%5D=-93.3387&saleLocationDistance%5Blocation%5D=55424&model%5B0%5D=defender&modelVariant%5B0%5D=defender_x-dynamic%20hse&modelVariant%5B1%5D=defender_x-dynamic%20se&modelVariant%5B2%5D=defender_x%20dynamic%20hse&modelVariant%5B3%5D=defender_defender%20110&modelVariant%5B4%5D=defender_x%20dynamic%20se&productionYear%5Bfrom%5D=2022&productionYear%5Bto%5D=2022&genericColour%5B0%5D=black",
    ]

    MyWebScraper = WebScraper(site_queries=site_queries)
    # MyWebScraper.submit_requests_and_parse()
    # MyWebScraper.extract_car_data()
    MyWebScraper.selenium_request_and_parse()
    MyWebScraper.extract_car_data()
