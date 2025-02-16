import time
import os
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from amazoncaptcha import AmazonCaptcha

driver = webdriver.Chrome()
driver.get("https://amazon.in")
time.sleep(5)

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

search_bar = driver.find_element(By.ID, "twotabsearchtextbox")
search_product = input("Enter the product name: ").strip().replace(" ", "_")
search_bar.send_keys(search_product)
search_bar.send_keys(Keys.RETURN)
time.sleep(2)

csv_folder = os.path.join("csv", search_product)
current_csv = os.path.join(csv_folder, "current.csv")
previous_csv = os.path.join(csv_folder, "previous.csv")

os.makedirs(csv_folder, exist_ok=True)

if os.path.exists(current_csv):
    if os.path.exists(previous_csv):
        os.remove(previous_csv)
    os.rename(current_csv, previous_csv)


product_names = driver.find_elements(By.CSS_SELECTOR, ".a-size-medium.a-spacing-none.a-color-base.a-text-normal")
product_prices = driver.find_elements(By.CSS_SELECTOR, ".a-price-whole")

with open(current_csv, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Product Name", "Price"])

    for name, price in zip(product_names, product_prices):
        writer.writerow([name.text, price.text if price else "Price not available"])
        print("Product Name:", name.text)
        print("Price:", price.text if price else "Price not available")
        print("=" * 30)

if input("Press Enter to exit...") == "exit":
    driver.quit()
