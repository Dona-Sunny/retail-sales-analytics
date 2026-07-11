from __future__ import annotations

import json
import random
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
RAW_PATH = DATA_DIR / "raw" / "retail_sales_raw.csv"
CLEANED_PATH = DATA_DIR / "cleaned" / "retail_sales_cleaned.csv"
STAGING_DIR = DATA_DIR / "staging"
SUMMARY_PATH = DATA_DIR / "cleaned" / "project_summary.json"
QUALITY_PATH = DATA_DIR / "cleaned" / "data_quality_report.json"

RNG = random.Random(42)


@dataclass(frozen=True)
class Location:
    city: str
    province: str
    region: str


LOCATIONS = [
    Location("Toronto", "Ontario", "Central"),
    Location("Ottawa", "Ontario", "Central"),
    Location("Mississauga", "Ontario", "Central"),
    Location("Hamilton", "Ontario", "Central"),
    Location("Montreal", "Quebec", "East"),
    Location("Quebec City", "Quebec", "East"),
    Location("Halifax", "Nova Scotia", "Atlantic"),
    Location("St. John's", "Newfoundland and Labrador", "Atlantic"),
    Location("Fredericton", "New Brunswick", "Atlantic"),
    Location("Winnipeg", "Manitoba", "Prairies"),
    Location("Saskatoon", "Saskatchewan", "Prairies"),
    Location("Calgary", "Alberta", "West"),
    Location("Edmonton", "Alberta", "West"),
    Location("Vancouver", "British Columbia", "West"),
    Location("Victoria", "British Columbia", "West"),
]

FIRST_NAMES = [
    "Aiden", "Amelia", "Ava", "Benjamin", "Charlotte", "Chloe", "Daniel",
    "Ella", "Emily", "Ethan", "Grace", "Harper", "Henry", "Isla", "Jack",
    "Jackson", "James", "Layla", "Leah", "Liam", "Lily", "Logan", "Lucas",
    "Mason", "Mia", "Nathan", "Noah", "Olivia", "Owen", "Scarlett", "Sofia",
    "Sophia", "Thomas", "Victoria", "William", "Zoe",
]

LAST_NAMES = [
    "Anderson", "Baker", "Brown", "Campbell", "Carter", "Clark", "Davis",
    "Edwards", "Evans", "Foster", "Garcia", "Green", "Hall", "Harris",
    "Hill", "Jackson", "Johnson", "King", "Lee", "Lewis", "Martin",
    "Mitchell", "Moore", "Nguyen", "Parker", "Patel", "Roberts", "Scott",
    "Singh", "Smith", "Taylor", "Thomas", "Thompson", "Walker", "White",
    "Wilson", "Young",
]

CUSTOMER_SEGMENTS = ["Consumer", "Corporate", "Home Office", "Small Business"]
SEGMENT_WEIGHTS = [0.44, 0.24, 0.18, 0.14]
SALES_CHANNELS = ["Online", "In-Store", "Marketplace", "Phone Order"]
CHANNEL_WEIGHTS = [0.47, 0.28, 0.18, 0.07]
PAYMENT_METHODS = ["Credit Card", "Debit Card", "PayPal", "Cash", "Gift Card"]
PAYMENT_WEIGHTS = [0.49, 0.19, 0.17, 0.11, 0.04]


PRODUCT_BLUEPRINT = {
    "Electronics": {
        "Accessories": ["Wireless Mouse", "Mechanical Keyboard", "USB Hub", "Laptop Stand", "Webcam"],
        "Audio": ["Bluetooth Speaker", "Noise Cancelling Headset", "Studio Earbuds", "Sound Bar", "Conference Mic"],
        "Computing": ["Portable SSD", "27 Inch Monitor", "Mini Projector", "Router", "Graphics Tablet"],
        "Mobile": ["Phone Charger", "Tablet Cover", "Power Bank", "Smart Watch Band", "Wireless Dock"],
    },
    "Furniture": {
        "Office": ["Standing Desk", "Executive Desk", "Bookshelf", "Printer Cabinet", "Meeting Table"],
        "Seating": ["Ergonomic Chair", "Guest Chair", "Stool", "Lounge Chair", "Drafting Chair"],
        "Storage": ["File Cabinet", "Storage Bench", "Drawer Unit", "Shelf Rack", "Closet Organizer"],
        "Decor": ["Desk Lamp", "Wall Clock", "Floor Lamp", "Planter Stand", "Mirror"],
    },
    "Office Supplies": {
        "Paper": ["Notebook Pack", "Copy Paper Box", "Sticky Notes", "Sketch Pad", "Shipping Labels"],
        "Writing": ["Gel Pen Set", "Marker Kit", "Mechanical Pencil", "Highlighter Pack", "Correction Tape"],
        "Organization": ["Binder Set", "Document Tray", "Desk Organizer", "Label Maker", "Planner"],
        "Mailroom": ["Packing Tape", "Bubble Mailer", "Shipping Scale", "Envelope Box", "Stapler"],
    },
    "Home & Kitchen": {
        "Appliances": ["Blender", "Coffee Maker", "Air Fryer", "Electric Kettle", "Rice Cooker"],
        "Dining": ["Dinnerware Set", "Glassware Set", "Cutlery Tray", "Serving Bowl", "Water Pitcher"],
        "Storage": ["Food Container Set", "Pantry Bin", "Spice Rack", "Utility Cart", "Vacuum Canister"],
        "Decor": ["Throw Blanket", "Candle Set", "Wall Art", "Area Rug", "Table Runner"],
    },
    "Sports & Outdoors": {
        "Fitness": ["Yoga Mat", "Resistance Bands", "Dumbbell Set", "Foam Roller", "Jump Rope"],
        "Travel": ["Duffel Bag", "Travel Mug", "Packing Cube Set", "Cooler Bag", "Carry-On Scale"],
        "Outdoor Gear": ["Camping Lantern", "Folding Chair", "Picnic Mat", "Insulated Bottle", "Trail Backpack"],
        "Cycling": ["Bike Helmet", "Water Bottle Cage", "Phone Mount", "Repair Kit", "LED Bike Light"],
    },
    "Apparel": {
        "Athleisure": ["Performance Tee", "Training Hoodie", "Jogger Pants", "Sports Bra", "Zip Jacket"],
        "Accessories": ["Baseball Cap", "Canvas Tote", "Running Socks", "Leather Belt", "Winter Scarf"],
        "Outerwear": ["Rain Jacket", "Puffer Vest", "Fleece Pullover", "Windbreaker", "Softshell Coat"],
        "Footwear": ["Running Shoes", "Walking Sneakers", "Slip-On Shoes", "Trail Shoes", "Indoor Slippers"],
    },
}

PRICE_RANGES = {
    "Electronics": (18, 420),
    "Furniture": (35, 680),
    "Office Supplies": (4, 90),
    "Home & Kitchen": (10, 260),
    "Sports & Outdoors": (8, 240),
    "Apparel": (12, 180),
}

BRANDS = [
    "Atlas", "Northwind", "Summit", "Vista", "Pioneer", "Cedar", "Harbor",
    "Lumen", "Nova", "Apex", "Evergreen", "Aurora",
]


def build_customers(total_customers: int = 620) -> pd.DataFrame:
    seen_names: set[tuple[str, str]] = set()
    rows = []
    start_join = date(2022, 1, 1)
    end_join = date(2025, 12, 31)
    join_span = (end_join - start_join).days

    for index in range(1, total_customers + 1):
        while True:
            first_name = RNG.choice(FIRST_NAMES)
            last_name = RNG.choice(LAST_NAMES)
            name_key = (first_name, last_name)
            if name_key not in seen_names:
                seen_names.add(name_key)
                break

        location = RNG.choice(LOCATIONS)
        join_date = start_join + timedelta(days=RNG.randint(0, join_span))

        rows.append(
            {
                "customer_id": f"CUST-{index:04d}",
                "customer_name": f"{first_name} {last_name}",
                "customer_segment": RNG.choices(CUSTOMER_SEGMENTS, weights=SEGMENT_WEIGHTS, k=1)[0],
                "city": location.city,
                "province": location.province,
                "region": location.region,
                "join_date": join_date.isoformat(),
            }
        )

    return pd.DataFrame(rows)


def build_products() -> pd.DataFrame:
    rows = []
    product_index = 1
    risky_products: set[str] = set()

    for category, subcategories in PRODUCT_BLUEPRINT.items():
        low_price, high_price = PRICE_RANGES[category]
        for subcategory, product_types in subcategories.items():
            for product_type in product_types:
                brand = BRANDS[(product_index - 1) % len(BRANDS)]
                price = round(RNG.uniform(low_price, high_price), 2)

                if category in {"Furniture", "Electronics"} and product_index % 7 == 0:
                    cost_ratio = RNG.uniform(0.84, 0.93)
                    risky_products.add(f"PROD-{product_index:04d}")
                else:
                    cost_ratio = RNG.uniform(0.46, 0.72)

                cost_per_unit = round(price * cost_ratio, 2)

                rows.append(
                    {
                        "product_id": f"PROD-{product_index:04d}",
                        "product_name": f"{brand} {product_type}",
                        "category": category,
                        "subcategory": subcategory,
                        "unit_price": price,
                        "cost_per_unit": cost_per_unit,
                    }
                )
                product_index += 1

    products = pd.DataFrame(rows)
    products["risky_product"] = products["product_id"].isin(risky_products)
    return products


def order_date_range() -> tuple[date, int]:
    start = date(2024, 1, 1)
    end = date(2025, 12, 31)
    return start, (end - start).days


def build_orders(customers: pd.DataFrame, products: pd.DataFrame, total_orders: int = 2600) -> tuple[pd.DataFrame, pd.DataFrame]:
    product_lookup = products.set_index("product_id").to_dict("index")
    product_ids = list(product_lookup.keys())
    risky_ids = set(products.loc[products["risky_product"], "product_id"])
    customer_ids = customers["customer_id"].tolist()

    order_rows = []
    item_rows = []

    start_date, days_span = order_date_range()

    for index in range(1, total_orders + 1):
        order_id = f"ORD-{index + 1000:05d}"
        customer_id = RNG.choice(customer_ids)
        order_date = start_date + timedelta(days=RNG.randint(0, days_span))
        sales_channel = RNG.choices(SALES_CHANNELS, weights=CHANNEL_WEIGHTS, k=1)[0]
        payment_method = RNG.choices(PAYMENT_METHODS, weights=PAYMENT_WEIGHTS, k=1)[0]

        order_rows.append(
            {
                "order_id": order_id,
                "customer_id": customer_id,
                "order_date": order_date.isoformat(),
                "sales_channel": sales_channel,
                "payment_method": payment_method,
            }
        )

        item_count = RNG.choices([1, 2, 3, 4], weights=[0.28, 0.39, 0.23, 0.10], k=1)[0]
        chosen_products = RNG.sample(product_ids, item_count)

        for product_id in chosen_products:
            product = product_lookup[product_id]
            quantity = RNG.choices([1, 2, 3, 4, 5, 6, 7, 8], weights=[0.26, 0.22, 0.18, 0.12, 0.09, 0.06, 0.04, 0.03], k=1)[0]

            if product_id in risky_ids:
                discount = RNG.choices([0.10, 0.15, 0.20, 0.25, 0.30], weights=[0.18, 0.22, 0.28, 0.20, 0.12], k=1)[0]
            else:
                discount = RNG.choices([0.00, 0.05, 0.10, 0.15, 0.20], weights=[0.33, 0.29, 0.22, 0.11, 0.05], k=1)[0]

            item_rows.append(
                {
                    "order_id": order_id,
                    "product_id": product_id,
                    "quantity": quantity,
                    "unit_price": product["unit_price"],
                    "discount": discount,
                }
            )

    return pd.DataFrame(order_rows), pd.DataFrame(item_rows)


def build_clean_dataset(customers: pd.DataFrame, products: pd.DataFrame, orders: pd.DataFrame, order_items: pd.DataFrame) -> pd.DataFrame:
    dataset = (
        order_items
        .merge(orders, on="order_id", how="left")
        .merge(customers.drop(columns=["join_date"]), on="customer_id", how="left")
        .merge(products.drop(columns=["risky_product"]), on="product_id", how="left", suffixes=("_order", "_product"))
    )

    dataset = dataset.rename(
        columns={
            "order_id": "Order_ID",
            "order_date": "Order_Date",
            "customer_id": "Customer_ID",
            "customer_name": "Customer_Name",
            "customer_segment": "Customer_Segment",
            "city": "City",
            "province": "Province",
            "region": "Region",
            "product_id": "Product_ID",
            "product_name": "Product_Name",
            "category": "Category",
            "subcategory": "Subcategory",
            "quantity": "Quantity",
            "unit_price_order": "Unit_Price",
            "cost_per_unit": "Cost_Per_Unit",
            "discount": "Discount",
            "sales_channel": "Sales_Channel",
            "payment_method": "Payment_Method",
        }
    )

    dataset["Gross_Sales"] = (dataset["Quantity"] * dataset["Unit_Price"]).round(2)
    dataset["Discount_Amount"] = (dataset["Gross_Sales"] * dataset["Discount"]).round(2)
    dataset["Net_Sales"] = (dataset["Gross_Sales"] - dataset["Discount_Amount"]).round(2)
    dataset["Total_Cost"] = (dataset["Quantity"] * dataset["Cost_Per_Unit"]).round(2)
    dataset["Profit"] = (dataset["Net_Sales"] - dataset["Total_Cost"]).round(2)
    return dataset


def create_raw_dataset(clean_dataset: pd.DataFrame) -> pd.DataFrame:
    raw = clean_dataset.copy()

    duplicate_rows = raw.sample(24, random_state=42)
    raw = pd.concat([raw, duplicate_rows], ignore_index=True)

    category_variants = {
        "Electronics": ["electronics", "Electronic", " ELECTRONICS "],
        "Furniture": [" furniture", "FURNITURE ", "Furnitures"],
        "Office Supplies": ["office supplies", "Office supply", " OFFICE SUPPLIES"],
        "Home & Kitchen": ["home & kitchen", "Home and Kitchen", " HOME & KITCHEN "],
        "Sports & Outdoors": ["sports & outdoors", "Sports and Outdoors", " SPORTS & OUTDOORS "],
        "Apparel": ["apparel", "Apparels", " APPAREL "],
    }
    segment_variants = {
        "Consumer": [" consumer", "CONSUMER ", "Consumer"],
        "Corporate": ["corporate", " CORPORATE", "Corporate "],
        "Home Office": ["home office", "Home office", " HOME OFFICE "],
        "Small Business": ["small business", "Small business", " SMALL BUSINESS "],
    }
    channel_variants = {
        "Online": ["online", " Online ", "ONLINE"],
        "In-Store": ["in-store", "In store", " IN-STORE "],
        "Marketplace": ["marketplace", "Marketplace ", " MARKETPLACE"],
        "Phone Order": ["phone order", "Phone order", " PHONE ORDER "],
    }

    category_indices = raw.sample(96, random_state=7).index
    for index in category_indices:
        category = raw.at[index, "Category"].strip()
        raw.at[index, "Category"] = RNG.choice(category_variants[category])

    segment_indices = raw.sample(72, random_state=8).index
    for index in segment_indices:
        segment = raw.at[index, "Customer_Segment"].strip()
        raw.at[index, "Customer_Segment"] = RNG.choice(segment_variants[segment])

    channel_indices = raw.sample(48, random_state=9).index
    for index in channel_indices:
        channel = raw.at[index, "Sales_Channel"].strip()
        raw.at[index, "Sales_Channel"] = RNG.choice(channel_variants[channel])

    city_indices = raw.sample(60, random_state=10).index
    raw.loc[city_indices, "City"] = raw.loc[city_indices, "City"].apply(lambda value: f" {value.upper()} ")

    negative_qty_indices = raw.sample(12, random_state=11).index
    raw.loc[negative_qty_indices, "Quantity"] = raw.loc[negative_qty_indices, "Quantity"] * -1

    negative_price_indices = raw.sample(8, random_state=12).index
    raw.loc[negative_price_indices, "Unit_Price"] = raw.loc[negative_price_indices, "Unit_Price"] * -1

    invalid_discount_indices = raw.sample(10, random_state=13).index
    raw.loc[invalid_discount_indices, "Discount"] = raw.loc[invalid_discount_indices, "Discount"] * 100

    blank_customer_indices = raw.sample(6, random_state=14).index
    raw.loc[blank_customer_indices, "Customer_ID"] = ""

    blank_product_indices = raw.sample(6, random_state=15).index
    raw.loc[blank_product_indices, "Product_ID"] = ""

    date_swap_indices = raw.sample(24, random_state=16).index
    for position, index in enumerate(date_swap_indices):
        current_value = pd.to_datetime(raw.at[index, "Order_Date"])
        if position < 8:
            raw.at[index, "Order_Date"] = current_value.strftime("%d-%m-%Y")
        elif position < 16:
            raw.at[index, "Order_Date"] = current_value.strftime("%Y/%m/%d")
        else:
            raw.at[index, "Order_Date"] = "2025-13-40"

    return raw


def normalize_title(value: str) -> str:
    return " ".join(part.capitalize() for part in value.replace("&", " & ").split())


def standardize_category(value: str) -> str:
    key = value.strip().lower().replace("and", "&")
    key = " ".join(key.split())
    mapping = {
        "electronics": "Electronics",
        "electronic": "Electronics",
        "furniture": "Furniture",
        "furnitures": "Furniture",
        "office supplies": "Office Supplies",
        "office supply": "Office Supplies",
        "home & kitchen": "Home & Kitchen",
        "sports & outdoors": "Sports & Outdoors",
        "apparel": "Apparel",
        "apparels": "Apparel",
    }
    return mapping.get(key, normalize_title(value))


def standardize_segment(value: str) -> str:
    key = " ".join(value.strip().lower().split())
    mapping = {
        "consumer": "Consumer",
        "corporate": "Corporate",
        "home office": "Home Office",
        "small business": "Small Business",
    }
    return mapping.get(key, normalize_title(value))


def standardize_channel(value: str) -> str:
    key = " ".join(value.strip().lower().replace("-", " ").split())
    mapping = {
        "online": "Online",
        "in store": "In-Store",
        "marketplace": "Marketplace",
        "phone order": "Phone Order",
    }
    return mapping.get(key, normalize_title(value))


def standardize_payment(value: str) -> str:
    key = " ".join(value.strip().lower().split())
    mapping = {
        "credit card": "Credit Card",
        "debit card": "Debit Card",
        "paypal": "PayPal",
        "cash": "Cash",
        "gift card": "Gift Card",
    }
    return mapping.get(key, normalize_title(value))


def clean_dataset(raw: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, int]]:
    cleaned = raw.copy()
    initial_rows = len(cleaned)

    string_columns = [
        "Order_ID", "Order_Date", "Customer_ID", "Customer_Name", "Customer_Segment",
        "City", "Province", "Region", "Product_ID", "Product_Name", "Category",
        "Subcategory", "Sales_Channel", "Payment_Method",
    ]
    for column in string_columns:
        cleaned[column] = cleaned[column].astype(str).str.strip()

    cleaned["Customer_Name"] = cleaned["Customer_Name"].str.replace(r"\s+", " ", regex=True).apply(normalize_title)
    cleaned["Customer_Segment"] = cleaned["Customer_Segment"].apply(standardize_segment)
    cleaned["City"] = cleaned["City"].apply(normalize_title)
    cleaned["Province"] = cleaned["Province"].apply(normalize_title)
    cleaned["Region"] = cleaned["Region"].apply(normalize_title)
    cleaned["Category"] = cleaned["Category"].apply(standardize_category)
    cleaned["Subcategory"] = cleaned["Subcategory"].apply(normalize_title)
    cleaned["Sales_Channel"] = cleaned["Sales_Channel"].apply(standardize_channel)
    cleaned["Payment_Method"] = cleaned["Payment_Method"].apply(standardize_payment)

    cleaned["Quantity"] = pd.to_numeric(cleaned["Quantity"], errors="coerce").abs()
    cleaned["Unit_Price"] = pd.to_numeric(cleaned["Unit_Price"], errors="coerce").abs().round(2)
    cleaned["Cost_Per_Unit"] = pd.to_numeric(cleaned["Cost_Per_Unit"], errors="coerce").abs().round(2)
    cleaned["Discount"] = pd.to_numeric(cleaned["Discount"], errors="coerce")
    cleaned.loc[cleaned["Discount"] > 1, "Discount"] = cleaned.loc[cleaned["Discount"] > 1, "Discount"] / 100
    cleaned["Discount"] = cleaned["Discount"].clip(lower=0, upper=1).round(4)

    cleaned["Order_Date"] = pd.to_datetime(cleaned["Order_Date"], errors="coerce", format="mixed")

    missing_key_mask = (
        cleaned["Customer_ID"].eq("")
        | cleaned["Product_ID"].eq("")
        | cleaned["Order_ID"].eq("")
        | cleaned["Order_Date"].isna()
    )
    missing_key_rows = int(missing_key_mask.sum())
    cleaned = cleaned.loc[~missing_key_mask].copy()

    duplicate_count = int(cleaned.duplicated(subset=["Order_ID", "Product_ID"]).sum())
    cleaned = cleaned.drop_duplicates(subset=["Order_ID", "Product_ID"], keep="first").copy()

    positive_value_mask = (
        (cleaned["Quantity"] > 0)
        & (cleaned["Unit_Price"] > 0)
        & (cleaned["Cost_Per_Unit"] > 0)
    )
    non_positive_rows = int((~positive_value_mask).sum())
    cleaned = cleaned.loc[positive_value_mask].copy()

    order_level_fields = ["Customer_ID", "Order_Date", "Sales_Channel", "Payment_Method"]
    for column in order_level_fields:
        canonical_values = cleaned.groupby("Order_ID")[column].agg(
            lambda values: values.mode().iloc[0] if not values.mode().empty else values.iloc[0]
        )
        cleaned[column] = cleaned["Order_ID"].map(canonical_values)

    customer_level_fields = ["Customer_Name", "Customer_Segment", "City", "Province", "Region"]
    for column in customer_level_fields:
        canonical_values = cleaned.groupby("Customer_ID")[column].agg(
            lambda values: values.mode().iloc[0] if not values.mode().empty else values.iloc[0]
        )
        cleaned[column] = cleaned["Customer_ID"].map(canonical_values)

    product_level_fields = ["Product_Name", "Category", "Subcategory", "Cost_Per_Unit"]
    for column in product_level_fields:
        canonical_values = cleaned.groupby("Product_ID")[column].agg(
            lambda values: values.mode().iloc[0] if not values.mode().empty else values.iloc[0]
        )
        cleaned[column] = cleaned["Product_ID"].map(canonical_values)

    cleaned["Order_Date"] = cleaned["Order_Date"].dt.strftime("%Y-%m-%d")
    cleaned["Gross_Sales"] = (cleaned["Quantity"] * cleaned["Unit_Price"]).round(2)
    cleaned["Discount_Amount"] = (cleaned["Gross_Sales"] * cleaned["Discount"]).round(2)
    cleaned["Net_Sales"] = (cleaned["Gross_Sales"] - cleaned["Discount_Amount"]).round(2)
    cleaned["Total_Cost"] = (cleaned["Quantity"] * cleaned["Cost_Per_Unit"]).round(2)
    cleaned["Profit"] = (cleaned["Net_Sales"] - cleaned["Total_Cost"]).round(2)
    cleaned = cleaned.sort_values(["Order_Date", "Order_ID", "Product_ID"]).reset_index(drop=True)

    issues = {
        "initial_rows": initial_rows,
        "rows_removed_missing_keys_or_invalid_dates": missing_key_rows,
        "duplicate_order_product_rows_removed": duplicate_count,
        "rows_removed_non_positive_values": non_positive_rows,
        "final_rows": len(cleaned),
    }
    return cleaned, issues


def export_staging_files(cleaned: pd.DataFrame) -> None:
    customers = (
        cleaned[
            ["Customer_ID", "Customer_Name", "Customer_Segment", "City", "Province", "Region"]
        ]
        .drop_duplicates()
        .rename(
            columns={
                "Customer_ID": "customer_id",
                "Customer_Name": "customer_name",
                "Customer_Segment": "customer_segment",
                "City": "city",
                "Province": "province",
                "Region": "region",
            }
        )
        .sort_values("customer_id")
    )

    products = (
        cleaned[
            ["Product_ID", "Product_Name", "Category", "Subcategory", "Unit_Price", "Cost_Per_Unit"]
        ]
        .drop_duplicates()
        .rename(
            columns={
                "Product_ID": "product_id",
                "Product_Name": "product_name",
                "Category": "category",
                "Subcategory": "subcategory",
                "Unit_Price": "unit_price",
                "Cost_Per_Unit": "cost_per_unit",
            }
        )
        .sort_values("product_id")
    )

    orders = (
        cleaned[
            ["Order_ID", "Customer_ID", "Order_Date", "Sales_Channel", "Payment_Method"]
        ]
        .drop_duplicates()
        .rename(
            columns={
                "Order_ID": "order_id",
                "Customer_ID": "customer_id",
                "Order_Date": "order_date",
                "Sales_Channel": "sales_channel",
                "Payment_Method": "payment_method",
            }
        )
        .sort_values("order_id")
    )

    order_items = (
        cleaned[
            ["Order_ID", "Product_ID", "Quantity", "Unit_Price", "Discount"]
        ]
        .rename(
            columns={
                "Order_ID": "order_id",
                "Product_ID": "product_id",
                "Quantity": "quantity",
                "Unit_Price": "unit_price",
                "Discount": "discount",
            }
        )
        .sort_values(["order_id", "product_id"])
    )

    STAGING_DIR.mkdir(parents=True, exist_ok=True)
    customers.to_csv(STAGING_DIR / "customers.csv", index=False)
    products.to_csv(STAGING_DIR / "products.csv", index=False)
    orders.to_csv(STAGING_DIR / "orders.csv", index=False)
    order_items.to_csv(STAGING_DIR / "order_items.csv", index=False)


def build_summary(cleaned: pd.DataFrame, issues: dict[str, int]) -> dict[str, object]:
    monthly = (
        cleaned.assign(order_month=pd.to_datetime(cleaned["Order_Date"]).dt.to_period("M").astype(str))
        .groupby("order_month", as_index=False)[["Net_Sales", "Profit"]]
        .sum()
    )
    category_summary = (
        cleaned.groupby("Category", as_index=False)[["Net_Sales", "Profit"]]
        .sum()
        .sort_values("Net_Sales", ascending=False)
    )
    region_summary = (
        cleaned.groupby("Region", as_index=False)[["Net_Sales", "Profit"]]
        .sum()
        .sort_values("Net_Sales", ascending=False)
    )
    customer_summary = (
        cleaned.groupby(["Customer_ID", "Customer_Name"], as_index=False)[["Net_Sales", "Profit"]]
        .sum()
        .sort_values("Net_Sales", ascending=False)
    )
    product_summary = (
        cleaned.groupby(["Product_ID", "Product_Name"], as_index=False)[["Profit", "Net_Sales"]]
        .sum()
        .sort_values("Profit")
    )

    total_revenue = round(float(cleaned["Net_Sales"].sum()), 2)
    total_profit = round(float(cleaned["Profit"].sum()), 2)
    total_orders = int(cleaned["Order_ID"].nunique())
    average_order_value = round(total_revenue / total_orders, 2)

    summary = {
        "row_counts": {
            "raw_transactions": issues["initial_rows"],
            "cleaned_transactions": len(cleaned),
            "customers": int(cleaned["Customer_ID"].nunique()),
            "products": int(cleaned["Product_ID"].nunique()),
            "orders": total_orders,
        },
        "date_range": {
            "start": cleaned["Order_Date"].min(),
            "end": cleaned["Order_Date"].max(),
        },
        "kpis": {
            "total_revenue": total_revenue,
            "total_profit": total_profit,
            "profit_margin_percentage": round((total_profit / total_revenue) * 100, 2),
            "average_order_value": average_order_value,
            "units_sold": int(cleaned["Quantity"].sum()),
        },
        "highlights": {
            "top_category": category_summary.iloc[0]["Category"],
            "top_region": region_summary.iloc[0]["Region"],
            "top_customer": customer_summary.iloc[0]["Customer_Name"],
            "monthly_peak": monthly.sort_values("Net_Sales", ascending=False).iloc[0]["order_month"],
            "loss_making_products": int((product_summary["Profit"] < 0).sum()),
        },
        "data_quality": issues,
    }
    return summary


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "raw").mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "cleaned").mkdir(parents=True, exist_ok=True)
    STAGING_DIR.mkdir(parents=True, exist_ok=True)

    customers = build_customers()
    products = build_products()
    orders, order_items = build_orders(customers, products)
    clean_seed_dataset = build_clean_dataset(customers, products, orders, order_items)
    raw_dataset = create_raw_dataset(clean_seed_dataset)
    cleaned_dataset, issues = clean_dataset(raw_dataset)

    raw_dataset.to_csv(RAW_PATH, index=False)
    cleaned_dataset.to_csv(CLEANED_PATH, index=False)
    export_staging_files(cleaned_dataset)

    summary = build_summary(cleaned_dataset, issues)
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    QUALITY_PATH.write_text(json.dumps(issues, indent=2), encoding="utf-8")

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()


