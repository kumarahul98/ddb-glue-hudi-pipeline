import boto3
from datetime import datetime
import names
import random


#! config - Update these variable
table_name = "dynamodb-glue-hudi-pipeline-DynamoDBTable"
record_count = 1


# Initialize a DynamoDB client
dynamodb = boto3.client("dynamodb")

# List of dictionaries with product name, price, and description
products_list = [
    {
        "productName": "Gaming Laptop",
        "price": 1200,
        "description": "High-performance gaming laptop with advanced graphics and fast processing.",
    },
    {
        "productName": "Wireless Headphones",
        "price": 150,
        "description": "Comfortable wireless headphones with noise-cancelling technology.",
    },
    {
        "productName": "Smartphone",
        "price": 800,
        "description": "Latest smartphone with high-resolution display, powerful processor, and long battery life.",
    },
    {
        "productName": "Electric Scooter",
        "price": 300,
        "description": "Foldable electric scooter with adjustable speed settings and LED lights.",
    },
    {
        "productName": "Fitness Tracker",
        "price": 100,
        "description": "Compact fitness tracker with heart rate monitor, sleep tracking, and waterproof design.",
    },
    {
        "productName": "Coffee Maker",
        "price": 250,
        "description": "Automatic coffee maker with programmable timer, stainless steel carafe, and reusable filter.",
    },
    {
        "productName": "Digital Camera",
        "price": 450,
        "description": "High-quality digital camera with full HD video recording, optical zoom lens, and manual mode.",
    },
    {
        "productName": "Portable Charger",
        "price": 75,
        "description": "Powerful portable charger with USB-C and micro-USB ports, supporting quick charge technology.",
    },
    {
        "productName": "Bluetooth Speaker",
        "price": 200,
        "description": "Portable Bluetooth speaker with rich sound quality, long battery life, and water-resistant design.",
    },
    {
        "productName": "Smart TV",
        "price": 600,
        "description": "Smart TV with 4K resolution, voice control, and built-in Wi-Fi connectivity.",
    },
    {
        "productName": "Wearable Smartwatch",
        "price": 180,
        "description": "Stylish wearable smartwatch with health tracking features, GPS, and customizable watch faces.",
    },
    {
        "productName": "Home Security System",
        "price": 400,
        "description": "Complete home security system with motion sensors, indoor and outdoor cameras, and mobile app control.",
    },
    {
        "productName": "Virtual Reality Headset",
        "price": 350,
        "description": "VR headset with immersive display, comfortable head strap, and intuitive controls for virtual reality experiences.",
    },
    {
        "productName": "Solar Power Bank",
        "price": 85,
        "description": "Portable solar power bank with dual USB ports, capable of charging smartphones and tablets.",
    },
    {
        "productName": "Wi-Fi Router",
        "price": 150,
        "description": "Advanced Wi-Fi router with MU-MIMO technology, beamforming antennas, and support for mesh networking.",
    },
]


# Function to generate sample data
def generate_sample_data(entity_type, start_id, count):
    data = []
    product = random.choice(products_list)
    print(product)
    for i in range(start_id, start_id + count):
        if entity_type == "product":
            data.append(
                {
                    "PutRequest": {
                        "Item": {
                            "PK": {"S": f"PRODUCT#{i}"},
                            "SK": {"S": f"PRODUCT#{i}"},
                            "ProductName": {"S": product["productName"]},
                            "Price": {"N": str(product["price"])},
                            "Description": {"S": product["description"]},
                        }
                    }
                }
            )
        elif entity_type == "customer":
            full_name = names.get_full_name()
            first_name = full_name.split(" ")[0]
            data.append(
                {
                    "PutRequest": {
                        "Item": {
                            "PK": {"S": f"CUSTOMER#{i}"},
                            "SK": {"S": f"CUSTOMER#{i}"},
                            "Name": {"S": f"{full_name}"},
                            "Email": {"S": f"{first_name}@example.com"},
                        }
                    }
                }
            )
        elif entity_type == "transaction":
            data.append(
                {
                    "PutRequest": {
                        "Item": {
                            "PK": {"S": f"CUSTOMER#{i}"},
                            "SK": {"S": f"TRANSACTION#{i}"},
                            "TransactionDate": {"S": datetime.now().isoformat()},
                            "TotalAmount": {"N": str(200 * i)},
                            "ProductsPurchased": {
                                "SS": [f"PRODUCT#{j}" for j in range(i, i + 5)]
                            },
                        }
                    }
                }
            )
    return data


# Function to insert data in batches
def insert_data_in_batches(data, table_name):
    batch_size = 25
    for i in range(0, len(data), batch_size):
        batch = data[i : i + batch_size]
        dynamodb.batch_write_item(RequestItems={table_name: batch})


products_data = generate_sample_data("product", 1, record_count)
customers_data = generate_sample_data("customer", 1, record_count)
transactions_data = generate_sample_data("transaction", 1, record_count)

insert_data_in_batches(products_data, table_name)
insert_data_in_batches(customers_data, table_name)
insert_data_in_batches(transactions_data, table_name)

print("Batch insert completed.")
