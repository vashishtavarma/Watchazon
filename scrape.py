import time
import os
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from amazoncaptcha import AmazonCaptcha

# Initialize WebDriver
driver = webdriver.Chrome()
driver.get("https://amazon.in")
time.sleep(5)

# Handle CAPTCHA
try:
    captcha_img = driver.find_element(By.TAG_NAME, "img").get_attribute("src")
    captcha = AmazonCaptcha.fromlink(captcha_img)
    solution = captcha.solve()
    input_box = driver.find_element(By.ID, "captchacharacters")
    input_box.send_keys(solution)
    input_box.send_keys(Keys.RETURN)
    time.sleep(2)
except:
    print("No CAPTCHA detected")

# User Input
search_bar = driver.find_element(By.ID, "twotabsearchtextbox")
search_product = input("Enter the product name: ").strip().replace(" ", "_")
search_bar.send_keys(search_product)
search_bar.send_keys(Keys.RETURN)
time.sleep(2)

# Set up CSV file paths
csv_folder = os.path.join("csv", search_product)
current_csv = os.path.join(csv_folder, "current.csv")
previous_csv = os.path.join(csv_folder, "previous.csv")
os.makedirs(csv_folder, exist_ok=True)

# Manage previous CSV file
if os.path.exists(current_csv):
    if os.path.exists(previous_csv):
        os.remove(previous_csv)
    os.rename(current_csv, previous_csv)

# Scrape product names and prices
product_names = driver.find_elements(By.CSS_SELECTOR, ".a-size-medium.a-spacing-none.a-color-base.a-text-normal")
product_prices = driver.find_elements(By.CSS_SELECTOR, ".a-price-whole")
sponsored_labels = driver.find_elements(By.CSS_SELECTOR, ".a-size-mini.a-color-secondary")

# Identify sponsored product indices
sponsored_indices = {i for i, label in enumerate(sponsored_labels) if "Sponsored" in label.text}

# Write data to CSV
with open(current_csv, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Product Name", "Price"])

    for i, (name, price) in enumerate(zip(product_names, product_prices)):
        if i in sponsored_indices:  # Skip if sponsored
            print(f"Skipping Sponsored Product: {name.text}")
            continue

        price_str = price.text if price else ""
        try:
            price_float = float(price_str.replace(",", ""))  # Convert to float
            writer.writerow([name.text, price_float])  # Only add valid prices
            print("Product Name:", name.text)
            print("Price:", price_float)
            print("=" * 30)
        except ValueError:
            print(f"Skipping {name.text}: Invalid price '{price_str}'")

# Exit condition
if input("Press Enter to exit...") == "exit":
    driver.quit()