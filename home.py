import os
import csv
import matplotlib.pyplot as plt
import numpy as np

category = input("Enter the product category (e.g., laptops, phones): ").strip().replace(" ", "_")
csv_folder = os.path.join("csv", category)
current_csv = os.path.join(csv_folder, "current.csv")
previous_csv = os.path.join(csv_folder, "previous.csv")

if not os.path.exists(current_csv):
    print(f"Error: {current_csv} not found!")
    exit()
if not os.path.exists(previous_csv):
    print(f"Warning: {previous_csv} not found! Comparison will not be possible.")
    exit()

def read_product_data(file_path):
    data = {}
    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            price_str = row[1].replace(",", "").strip()
            if price_str and price_str.replace(".", "").isdigit():
                data[row[0]] = float(price_str)
    return data

current_data = read_product_data(current_csv)
previous_data = read_product_data(previous_csv)

common_products = set(current_data.keys()).intersection(set(previous_data.keys()))

filtered_products = []
filtered_current_prices = []
filtered_previous_prices = []

for product in common_products:
    cur_price = current_data[product]
    prev_price = previous_data[product]
    
    price_diff = abs(cur_price - prev_price) / prev_price * 100
    if price_diff > 10:
        print(f"Skipping {product}: Price change {price_diff:.2f}% exceeds 10%")
        continue

    filtered_products.append(product[:20])
    filtered_current_prices.append(cur_price)
    filtered_previous_prices.append(prev_price)

if not filtered_products:
    print("No valid price data available to plot.")
    exit()

x = np.arange(len(filtered_products))
plt.figure(figsize=(12, 6))
bar_width = 0.4

plt.bar(x - bar_width/2, filtered_previous_prices, bar_width, label="Previous Price", color="red")
plt.bar(x + bar_width/2, filtered_current_prices, bar_width, label="Current Price", color="green")

plt.xticks(x, filtered_products, rotation=45, ha="right")
plt.ylabel("Price (INR)")
plt.title(f"Price Comparison for {category.replace('_', ' ')}")
plt.legend()
plt.tight_layout()

plt.show()
