import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

def get_driver():
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless")  # Optional: run without opening browser window
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def scrape_olx_car_covers(pages=2):
    base_url = "https://www.olx.in/items/q-car-cover?page="
    scraped_data = []

    driver = get_driver()

    for page in range(1, pages + 1):
        url = base_url + str(page)
        print(f"Scraping: {url}")
        try:
            driver.get(url)
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.EIR5N"))
            )

            # Optional: save HTML for debugging
            with open(f"debug_page_{page}.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            print(f"Saved page source for page {page}")

            listings = driver.find_elements(By.CSS_SELECTOR, "li.EIR5N")

            for item in listings:
                try:
                    title = item.find_element(By.CSS_SELECTOR, "span._2tW1I").text
                    price = item.find_element(By.CSS_SELECTOR, "span._89yzn").text
                    location = item.find_element(By.CSS_SELECTOR, "span._2FcKD").text
                    link = item.find_element(By.TAG_NAME, "a").get_attribute("href")
                    scraped_data.append({
                        "title": title,
                        "price": price,
                        "location": location,
                        "link": link
                    })
                except Exception as e:
                    print("Error extracting item:", e)

        except TimeoutException:
            print(f"Timeout: Content not loaded on page {page}")
            with open(f"debug_page_{page}.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
        except Exception as e:
            print(f"Failed to scrape page {page}: {e}")
            with open(f"debug_page_{page}.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)

        time.sleep(2)

    driver.quit()
    return scraped_data

def save_to_csv(data, filename="car_cover_olx_results.csv"):
    if not data:
        print("No data scraped.")
        return
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "price", "location", "link"])
        writer.writeheader()
        for row in data:
            writer.writerow(row)
    print(f"Saved {len(data)} results to {filename}")

if __name__ == "__main__":
    scraped_data = scrape_olx_car_covers(pages=2)
    save_to_csv(scraped_data)
