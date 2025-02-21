from csv import writer as csv_writer
from itertools import product
import random

# Generate semi-random results for some Olympics events
HEADERS = ["olympics", "event", "athlete", "position", "country"]

MANUALLY_CREATED_RESULTS = [
    ["2020", "100m", "Usain Bolt", "1", "JM"],
    ["2090", "100m", "Usain Bolt", "3", "JM"],
    ["2006", "curling", "Anette Norberg", "1", "SE"],
    ["2006", "curling", "Binia Feltscher", "2", "CH"],
]
FINAL_RESULTS = []

sports = [
    "100m",
    "200m",
    "400m",
    "5000m",
    "marathon",
    "110m hurdles",
    "400m hurdles",
    "high jump",
    "long jump",
    "javelin throw",
    "decathlon",
    "100m freestyle",
    "400m freestyle",
    "200m backstroke",
    "skiing",
    "snowboarding",
    "soccer",
    "table tennis",
    "tennis",
    "triathlon",
    "weightlifting",
    "wrestling",
    "volleyball",
]
pool_of_names = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Hannah", "Ivan", "Jenny", "Emanuele", "Karl"]
pool_of_surnames = [
    "Smith",
    "Johnson",
    "Williams",
    "Jones",
    "Brown",
    "Davis",
    "Miller",
    "Wilson",
    "Moore",
    "Taylor",
    "Maruzzi",
    "Schmidt",
]
pool_of_countries = ["US", "GB", "DE", "FR", "IT", "JP", "RU", "CN"]
names = list(product(pool_of_names, pool_of_surnames))
for year in range(2012, 2024, 2):
    for sport in sports:
        for position in range(1, 32):
            athlete = random.choice(names)
            FINAL_RESULTS.append(
                [str(year), sport, f"{athlete[0]} {athlete[1]}", str(position), random.choice(pool_of_countries)]
            )

with open("starting_data_results.csv", "w") as f:
    writer = csv_writer(f, delimiter=";")
    writer.writerow(HEADERS)
    writer.writerows(MANUALLY_CREATED_RESULTS)
    writer.writerows(FINAL_RESULTS)
