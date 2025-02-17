import os
import csv
import matplotlib.pyplot as plt
import numpy as np

# Get the category name (folder name)
category = input("Enter the product category (e.g., laptops, phones): ").strip().replace(" ", "_")
csv_folder = os.path.join("csv", category)
current_csv = os.path.join(csv_folder, "current.csv")
previous_csv = os.path.join(csv_folder, "previous.csv")

# Check if files exist
if not os.path.exists(current_csv):
    print(f"Error: {current_csv} not found!")
    exit()
if not os.path.exists(previous_csv):
    print(f"Warning: {previous_csv} not found! Comparison will not be possible.")
    exit()

# Function to read product data from a CSV file
def read_product_data(file_path):
    data = {}
    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            price_str = row[1].replace(",", "").strip()  # Remove commas & spaces
            if price_str and price_str.replace(".", "").isdigit():  # Check if valid number
                data[row[0]] = float(price_str)
    return data

# Read data from both files
current_data = read_product_data(current_csv)
previous_data = read_product_data(previous_csv)

# Get only common product names
common_products = set(current_data.keys()).intersection(set(previous_data.keys()))

# Extract prices for comparison & filter based on 10% difference
filtered_products = []
filtered_current_prices = []
filtered_previous_prices = []

for product in common_products:
    cur_price = current_data[product]
    prev_price = previous_data[product]
    
    price_diff = abs(cur_price - prev_price) / prev_price * 100  # Percentage difference
    if price_diff > 10:  # Ignore if difference is more than 10%
        print(f"Skipping {product}: Price change {price_diff:.2f}% exceeds 10%")
        continue

    filtered_products.append(product[:20])  # Shorten names for clarity
    filtered_current_prices.append(cur_price)
    filtered_previous_prices.append(prev_price)

# Check if there is data to plot
if not filtered_products:
    print("No valid price data available to plot.")
    exit()

# Plot the comparison bar chart
x = np.arange(len(filtered_products))  # X-axis labels

plt.figure(figsize=(12, 6))
bar_width = 0.4

# Plot bars
plt.bar(x - bar_width/2, filtered_previous_prices, bar_width, label="Previous Price", color="red")
plt.bar(x + bar_width/2, filtered_current_prices, bar_width, label="Current Price", color="green")

# Labels & Formatting
plt.xticks(x, filtered_products, rotation=45, ha="right")
plt.ylabel("Price (INR)")
plt.title(f"Price Comparison for {category.replace('_', ' ')}")
plt.legend()
plt.tight_layout()

# Show plot
plt.show()
