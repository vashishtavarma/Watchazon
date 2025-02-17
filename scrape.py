import time
import os
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from amazoncaptcha import AmazonCaptcha
from bs4 import BeautifulSoup

# Initialize WebDriver
driver = webdriver.Chrome()
driver.get("https://www.amazon.in")
time.sleep(5)

# Handle CAPTCHA if present
try:
    captcha_img = driver.find_element(By.TAG_NAME, "img").get_attribute("src")
    if "captcha" in captcha_img:
        print("CAPTCHA detected. Solving...")
        captcha = AmazonCaptcha.fromlink(captcha_img)
        solution = captcha.solve()
        input_box = driver.find_element(By.ID, "captchacharacters")
        input_box.send_keys(solution)
        input_box.send_keys(Keys.RETURN)
        time.sleep(5)
except Exception:
    print("No CAPTCHA detected.")

# User Input for Product Search
search_product = input("Enter the product name: ").strip().replace(" ", "_")
search_bar = driver.find_element(By.ID, "twotabsearchtextbox")
search_bar.send_keys(search_product)
search_bar.send_keys(Keys.RETURN)
time.sleep(5)

# Set up CSV folder and file paths
csv_folder = os.path.join("csv", search_product)
current_csv = os.path.join(csv_folder, "current.csv")
previous_csv = os.path.join(csv_folder, "previous.csv")
os.makedirs(csv_folder, exist_ok=True)

# Manage previous CSV file
if os.path.exists(current_csv):
    if os.path.exists(previous_csv):
        os.remove(previous_csv)
    os.rename(current_csv, previous_csv)

# Extract page source for parsing
page_source = driver.page_source
soup = BeautifulSoup(page_source, "html.parser")

# Find product containers
products = soup.find_all("div", class_="puis-card-container")

# Write product data to CSV
with open(current_csv, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Product Name", "Price (INR)"])

    for product in products:
        # Skip Sponsored Products
        if product.find("span", class_="s-sponsored-label-info-icon"):
            print("Skipping Sponsored Product.")
            continue

        # Extract product name
        name_tag = product.find("h2")
        product_name = name_tag.get_text(strip=True) if name_tag else "Unknown Product"

        # Extract product price
        price_tag = product.find("span", class_="a-price-whole")
        price_str = price_tag.get_text(strip=True).replace(",", "") if price_tag else "0"

        try:
            price_float = float(price_str)
            writer.writerow([product_name, price_float])
            print(f"Product: {product_name}\nPrice: ₹{price_float}\n{'=' * 40}")
        except ValueError:
            print(f"Skipping {product_name}: Invalid price '{price_str}'")

# Exit and Clean Up
input("Scraping complete. Press Enter to exit...")
driver.quit()
