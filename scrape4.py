from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.parse import urlparse
import csv

# List of URLs to scrape
urls = [
    "https://www.notino.co.uk/foundation/",
    "https://www.notino.co.uk/concealer/",
    "https://www.notino.co.uk/face-powder/",
    "https://www.notino.co.uk/blusher/",
    "https://www.notino.co.uk/mascara/",
    "https://www.notino.co.uk/eyeshadow/",
    "https://www.notino.co.uk/eyeliner/",
    "https://www.notino.co.uk/lipstick/",
    "https://www.notino.co.uk/lip-gloss/",
    "https://www.notino.co.uk/nail-varnish/",
    "https://www.notino.co.uk/shampoo/",
    "https://www.notino.co.uk/hairspray/",
    "https://www.notino.co.uk/body-butter-cream/",
    "https://www.notino.co.uk/bar-soap/",
    "https://www.notino.co.uk/unisex-fragrances/eaux-de-parfum/"
]

# Set up Selenium
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run Chrome in headless mode (no UI)
driver = webdriver.Chrome(options=options)

# Open the CSV file in write mode
csv_file = open("products.csv", "w", newline="", encoding="utf-8")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["Brand", "Product Name", "Product URL", "Image URL", "Description", "Price", "Category"])

for url in urls:
    category = urlparse(url).path.strip('/').split('/')[-1] if url != "N/A" else "N/A"
    driver.get(url)

    def click_show_more_button():
        try:
            show_more_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Show more')]"))
            )
            show_more_button.click()
            time.sleep(3)  # Wait for the new content to load
            return True
        except:
            return False

    # Scroll down and click "Show more" to load additional content
    while click_show_more_button():
        pass

    # Scroll gradually to ensure all content is loaded
    scroll_height = 0
    scroll_step = 300

    while scroll_height < driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );"):
        driver.execute_script(f"window.scrollTo(0, {scroll_height});")
        time.sleep(2)  # Adjust the wait time as needed
        scroll_height += scroll_step

    soup = BeautifulSoup(driver.page_source, "html.parser")
    product_containers = soup.find_all("div", attrs={"data-testid": "product-container"})

    for container in product_containers:
        product_url_rel = container.find("a", class_="sc-iOeugr iiaXZj")
        if product_url_rel:
            product_url_rel = product_url_rel["href"]
            product_url = urljoin(url, product_url_rel)
        else:
            product_url = "N/A"

        image_container = container.find("div", width="160", attrs={"data-testid": "img-placeholder"})
        if image_container:
            image_url = image_container.find("img")['src']
        else:
            image_url = "N/A"

        brand_name = container.find("h2", class_="sc-gswNZR sc-dwnOUR kaqwLk jIQpuX")
        brand_name = brand_name.text if brand_name else "N/A"

        product_name = container.find("h3", class_="sc-dkrFOg sc-UpCWa dvjKkW isHfcC")
        product_name = product_name.text if product_name else "N/A"

        product_description = container.find("p", class_="sc-ZqFbI dacIKO")
        product_description = product_description.text if product_description else "N/A"

        price_element = container.find("span",
                                       {"data-testid": "price-component"})
        product_price = price_element.text.strip() if price_element else "N/A"

        csv_writer.writerow([brand_name, product_name, product_url, image_url, product_description, product_price, category])

# Clean up
csv_file.close()
driver.quit()
