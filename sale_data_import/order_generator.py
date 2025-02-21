import random
import csv
import faker

random.seed(123)

fake = faker.Faker()
fake.seed_instance(123)
# Define the file name for the CSV
csv_file_path = "./sample_orders.csv"

# Define the header (which won't necessarily match Odoo fields directly)
header = [
    "order reference",
    "item",
    "qty",
    "total",
    "customer",
    "customer's email",
    "position",
    "purchase date",
    "region",
    "city",
    "zipcode",
]


regions = ["North", "South", "East", "West", "Central"]
# Adjust the pool sizes for customers and products
num_partners = 30
num_products = 20
total_orders = 200
total_order_lines = 1500

# Generate a pool of 30 unique customers
customers_pool = [(fake.name(), fake.email(), fake.job(), fake.city(), fake.zipcode()) for _ in range(num_partners)]

# Generate a pool of 20 unique products
products_pool = [f"Product {i+1}" for i in range(num_products)]

partner_order_pool = [(f"ORD-{random.randint(1000, 1200)}", random.choice(customers_pool)) for _ in range(total_orders)]

# Reset rows and generate 500 orders with the 30 partners and 20 products
rows = []
for i in range(total_order_lines):
    order_reference, (customer, customer_email, position, city, zipcode) = random.choice(partner_order_pool)
    item = random.choice(products_pool)
    qty = random.randint(1, 10)
    total = round(qty * random.uniform(20.00, 500.00), 2)
    purchase_date = fake.date_this_year()
    region = random.choice(regions)

    rows.append([order_reference, item, qty, total, customer, customer_email, position, purchase_date, region, city, zipcode])

# Write the updated data to the CSV file
with open(csv_file_path, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(header)  # Write the header
    writer.writerows(rows)  # Write the data
