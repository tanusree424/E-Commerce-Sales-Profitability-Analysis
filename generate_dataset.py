"""
Synthetic retail dataset generator (Bangladesh e-commerce flavour) for Python data-cleaning practice.
Run:  python generate_dataset.py
Output: customers.csv, products.csv, orders.csv, order_items.csv, README.md (in OUT folder)
Seed is fixed -> same files every time.
"""
import os
from datetime import date, timedelta

import numpy as np
import pandas as pd

SEED = 42
rng = np.random.default_rng(SEED)
OUT = os.environ.get("OUT_DIR", "/mnt/user-data/outputs")
os.makedirs(OUT, exist_ok=True)

N_CUST, N_ORD, N_PROD = 1400, 6500, 180
D_START, D_END = date(2022, 7, 1), date(2025, 12, 31)
SIGNUP_END = date(2025, 9, 30)

GEO = {
    "Dhaka": ["Dhaka", "Gazipur", "Narayanganj", "Tangail"],
    "Chattogram": ["Chattogram", "Cox's Bazar", "Cumilla", "Noakhali"],
    "Rajshahi": ["Rajshahi", "Bogura", "Pabna", "Natore"],
    "Khulna": ["Khulna", "Jashore", "Kushtia", "Satkhira"],
    "Sylhet": ["Sylhet", "Moulvibazar", "Habiganj"],
    "Rangpur": ["Rangpur", "Dinajpur", "Kurigram", "Gaibandha"],
    "Barishal": ["Barishal", "Bhola", "Patuakhali"],
    "Mymensingh": ["Mymensingh", "Jamalpur", "Netrokona"],
}
REGIONS = list(GEO)
REGION_P = np.array([.35, .20, .10, .10, .08, .07, .05, .05])

FIRST = ["Rahim", "Karim", "Sadia", "Nusrat", "Tanvir", "Farhan", "Mim", "Rafi", "Tasnim", "Imran", "Shirin", "Arif",
         "Jannat", "Hasan", "Mehedi", "Sumaiya", "Rubel", "Nabila", "Sakib", "Anika", "Fahim", "Lamia", "Zahid",
         "Maliha", "Shuvo", "Rima", "Kamal", "Salma", "Tareq", "Ishrat", "Nayeem", "Sabrina", "Parvez", "Mou",
         "Asif", "Tithi", "Jahid", "Rumana", "Sohel", "Orpita"]
LAST = ["Ahmed", "Hossain", "Rahman", "Islam", "Khan", "Chowdhury", "Akter", "Uddin", "Sarker", "Mia", "Begum",
        "Talukder", "Biswas", "Das", "Roy", "Sikder", "Mondal", "Haque", "Karim", "Siddique", "Bhuiyan", "Sheikh",
        "Alam", "Majumder", "Paul"]

SUBS = [
    ("Electronics", "Phones", (8000, 90000), ["Smartphone", "Tablet", "Smartwatch"]),
    ("Electronics", "Headphones", (800, 12000), ["Earbuds", "Headset", "Bluetooth Speaker", "Neckband"]),
    ("Electronics", "Accessories", (300, 3500), ["Power Bank", "USB Cable", "Charger", "Mouse", "Keyboard"]),
    ("Furniture", "Chairs", (3000, 25000), ["Office Chair", "Gaming Chair", "Stool", "Armchair"]),
    ("Furniture", "Tables", (5000, 40000), ["Work Desk", "Dining Table", "Coffee Table", "Side Table"]),
    ("Furniture", "Storage", (2500, 30000), ["Bookshelf", "Wardrobe", "Shoe Rack", "Cabinet"]),
    ("Office Supplies", "Paper", (150, 1200), ["A4 Paper Ream", "Notebook", "Sticky Notes", "Notepad"]),
    ("Office Supplies", "Binders", (100, 900), ["Ring Binder", "File Folder", "Clipboard", "Box File"]),
    ("Office Supplies", "Pens", (50, 600), ["Ballpoint Pens", "Gel Pens", "Marker Set", "Highlighters"]),
    ("Clothing", "Men", (600, 5000), ["Cotton Shirt", "Panjabi", "Jeans", "Polo T-Shirt"]),
    ("Clothing", "Women", (700, 7000), ["Saree", "Kurti", "Salwar Kameez", "Scarf"]),
    ("Clothing", "Footwear", (900, 8000), ["Sneakers", "Sandals", "Formal Shoes", "Slippers"]),
    ("Home & Kitchen", "Cookware", (500, 6000), ["Non-stick Pan", "Pressure Cooker", "Knife Set", "Casserole"]),
    ("Home & Kitchen", "Appliances", (2500, 30000), ["Rice Cooker", "Electric Kettle", "Blender", "Air Fryer"]),
    ("Home & Kitchen", "Decor", (300, 6000), ["Wall Clock", "Vase", "Table Lamp", "Photo Frame"]),
]
BRANDS = ["Nova", "Zenith", "Aurora", "Orbit", "Pioneer", "Lumen", "Vertex", "Terra", "Kite", "Meghna", "Padma", "Jamuna"]
SERIES = ["Pro", "Lite", "Plus", "Max", "Air", "Neo", "Prime", "Classic"]
RETURN_REASONS = ["Defective", "Wrong item", "Not as described", "Changed mind", "Late delivery"]


def d2s(d):
    return d.strftime("%Y-%m-%d")


# ───────────────────────── CLEAN DATA ─────────────────────────
# customers
cust_ids = [f"C{i:04d}" for i in range(1, N_CUST + 1)]
c_region = rng.choice(REGIONS, N_CUST, p=REGION_P)
c_city = [str(rng.choice(GEO[r])) for r in c_region]
c_name = [f"{rng.choice(FIRST)} {rng.choice(LAST)}" for _ in range(N_CUST)]
c_email = [f"{n.lower().replace(' ', '.')}{i + 1}@example.com" for i, n in enumerate(c_name)]
c_segment = rng.choice(["Consumer", "Corporate", "Home Office"], N_CUST, p=[.52, .30, .18])
sp = (SIGNUP_END - D_START).days
c_signup = [D_START + timedelta(days=int(x)) for x in rng.integers(0, sp + 1, N_CUST)]
customers = pd.DataFrame({
    "customer_id": cust_ids, "customer_name": c_name, "email": c_email, "segment": c_segment,
    "signup_date": [d2s(d) for d in c_signup], "city": c_city, "region": c_region, "country": "Bangladesh",
})

# products
prod_rows, used_names = [], set()
pid = 1
for cat, sub, (lo, hi), nouns in SUBS:
    for _ in range(N_PROD // len(SUBS)):
        while True:
            nm = f"{rng.choice(BRANDS)} {rng.choice(nouns)} {rng.choice(SERIES)} {int(rng.integers(100, 999))}"
            if nm not in used_names:
                used_names.add(nm)
                break
        price = float(np.exp(rng.uniform(np.log(lo), np.log(hi))))
        step = 10 if lo >= 500 else 5
        price = max(lo, round(price / step) * step)
        cost = round(price * rng.uniform(.55, .85), 2)
        prod_rows.append((f"P{pid:03d}", nm, cat, sub, cost, float(price)))
        pid += 1
products = pd.DataFrame(prod_rows, columns=["product_id", "product_name", "category", "subcategory",
                                            "unit_cost", "list_price"])

# orders
w = rng.gamma(0.9, size=N_CUST)
w /= w.sum()
oc_idx = rng.choice(N_CUST, N_ORD, p=w)
o_dates = []
for ci in oc_idx:
    span = (D_END - c_signup[ci]).days
    o_dates.append(c_signup[ci] + timedelta(days=int(span * rng.beta(1.2, 1.0))))
order_ix = np.argsort(np.array(o_dates, dtype="datetime64[D]"), kind="stable")
oc_idx = oc_idx[order_ix]
o_dates = [o_dates[i] for i in order_ix]

o_rows = []
for k in range(N_ORD):
    od = o_dates[k]
    ci = oc_idx[k]
    left = (D_END - od).days
    if left <= 20:
        status = rng.choice(["Delivered", "Shipped", "Processing", "Cancelled"], p=[.15, .40, .40, .05])
    else:
        status = rng.choice(["Delivered", "Cancelled"], p=[.92, .08])
    mode = rng.choice(["Standard", "Express", "Same Day"], p=[.65, .27, .08])
    days = {"Standard": (3, 5), "Express": (1, 2), "Same Day": (0, 1)}[mode]
    ship = None
    if status in ("Delivered", "Shipped"):
        ship = min(D_END, od + timedelta(days=int(rng.integers(days[0], days[1] + 1))))
    sc = {"Standard": (60, 120), "Express": (120, 250), "Same Day": (200, 350)}[mode]
    region = c_region[ci] if rng.random() < .88 else rng.choice(REGIONS)
    pay = rng.choice(["Cash on Delivery", "bKash", "Nagad", "Credit Card", "Bank Transfer"],
                     p=[.45, .25, .10, .12, .08])
    o_rows.append((f"ORD-{k + 1:06d}", cust_ids[ci], d2s(od), d2s(ship) if ship else None, status, region, mode,
                   float(round(rng.uniform(*sc) / 5) * 5), pay))
orders = pd.DataFrame(o_rows, columns=["order_id", "customer_id", "order_date", "ship_date", "status", "region",
                                       "ship_mode", "shipping_cost", "payment_method"])

# order_items
pw = rng.gamma(1.0, size=N_PROD)
pw /= pw.sum()
n_items = rng.choice([1, 2, 3, 4], N_ORD, p=[.55, .28, .12, .05])
ret_p = {"Clothing": .12, "Electronics": .06, "Furniture": .05, "Home & Kitchen": .07, "Office Supplies": .02}
i_rows = []
oi = 1
for k in range(N_ORD):
    oid, status = o_rows[k][0], o_rows[k][4]
    for pi in rng.choice(N_PROD, n_items[k], replace=False, p=pw):
        p = products.iloc[pi]
        if p.category == "Office Supplies":
            qty = int(rng.choice([1, 2, 3, 5, 10, 12], p=[.30, .25, .15, .15, .10, .05]))
        else:
            qty = int(rng.choice([1, 2, 3, 4, 5], p=[.55, .25, .10, .06, .04]))
        price = round(p.list_price * rng.uniform(.97, 1.05), 2)
        disc = float(rng.choice([0, .05, .10, .15, .20, .30], p=[.50, .15, .15, .10, .07, .03]))
        cost = round(qty * p.unit_cost, 2)
        profit = round(qty * price * (1 - disc) - cost, 2)
        ret = status == "Delivered" and rng.random() < ret_p[p.category]
        reasons = RETURN_REASONS + (["Size issue"] * 3 if p.category == "Clothing" else [])
        i_rows.append((f"OI-{oi:06d}", oid, p.product_id, qty, price, disc, cost, profit,
                       "Y" if ret else "N", str(rng.choice(reasons)) if ret else None))
        oi += 1
items = pd.DataFrame(i_rows, columns=["order_item_id", "order_id", "product_id", "quantity", "unit_price",
                                      "discount", "cost", "profit", "returned", "return_reason"])


# ───────────────────────── INJECT DIRT ─────────────────────────
def take(df, used, n, mask=None):
    pool = df.index[mask] if mask is not None else df.index
    pool = np.array([i for i in pool if i not in used])
    ch = rng.choice(pool, n, replace=False)
    used.update(int(i) for i in ch)
    return ch


def case_variant(s):
    return str(rng.choice([s.lower(), s.upper(), s + " ", " " + s]))


LOG = {"customers": {}, "products": {}, "orders": {}, "order_items": {}}

# ---- customers
u = set()
ix = take(customers, u, 42); customers.loc[ix, "city"] = None; LOG["customers"]["city এর missing value"] = len(ix)
ix = take(customers, u, 28); customers.loc[ix, "signup_date"] = None; LOG["customers"]["signup_date এর missing value"] = len(ix)
ix = take(customers, u, 60)
for i in ix:
    customers.at[i, "segment"] = case_variant(customers.at[i, "segment"])
LOG["customers"]["segment এ case/space এর অমিল (consumer, ' Corporate', HOME OFFICE ...)"] = len(ix)
ix = take(customers, u, 21)
for i in ix:
    e = customers.at[i, "email"]
    customers.at[i, "email"] = e.replace("@", "") if rng.random() < .5 else e.replace(".com", "")
LOG["customers"]["invalid email ('@' বা '.com' নেই)"] = len(ix)
ix = take(customers, u, 6)
for i in ix:
    customers.at[i, "signup_date"] = d2s(date(2027, int(rng.integers(1, 13)), int(rng.integers(1, 28))))
LOG["customers"]["ভবিষ্যতের signup_date (২০২৭)"] = len(ix)
ix = take(customers, u, 40)
for i in ix:
    customers.at[i, "customer_name"] = customers.at[i, "customer_name"].upper() if rng.random() < .5 \
        else "  " + customers.at[i, "customer_name"].lower()
LOG["customers"]["customer_name এ ALL CAPS / lowercase / leading space"] = len(ix)
dup = customers.loc[rng.choice(customers.index, 20, replace=False)]
LOG["customers"]["হুবহু duplicate row"] = len(dup)
near = customers.loc[rng.choice(customers.index[customers.email.str.contains("@", na=False)], 10, replace=False)].copy()
near["customer_id"] = [f"C{N_CUST + j:04d}" for j in range(1, 11)]
near["customer_name"] = near["customer_name"].str.upper()
LOG["customers"]["একই email, ভিন্ন customer_id (near-duplicate)"] = len(near)
customers = pd.concat([customers, dup, near]).sample(frac=1, random_state=SEED).reset_index(drop=True)

# ---- products
u = set()
ix = take(products, u, 8)
for i in ix:
    products.at[i, "category"] = case_variant(products.at[i, "category"])
LOG["products"]["category তে case/space এর অমিল"] = len(ix)
ix = take(products, u, 5); products.loc[ix, "subcategory"] = None; LOG["products"]["subcategory missing"] = len(ix)
ix = take(products, u, 4); products.loc[ix, "unit_cost"] = np.nan; LOG["products"]["unit_cost missing"] = len(ix)
ix = take(products, u, 3)
products.loc[ix, "unit_cost"] = (products.loc[ix, "list_price"] * 1.3).round(2)
LOG["products"]["unit_cost > list_price (logic error)"] = len(ix)
dup = products.loc[rng.choice(products.index, 6, replace=False)]
LOG["products"]["হুবহু duplicate row"] = len(dup)
products = pd.concat([products, dup]).sample(frac=1, random_state=SEED).reset_index(drop=True)

# ---- orders
u = set()
ix = take(orders, u, 150)
for i in ix:
    s = orders.at[i, "status"]
    orders.at[i, "status"] = "Canceled" if (s == "Cancelled" and rng.random() < .5) else case_variant(s)
LOG["orders"]["status এ case/space/spelling এর অমিল (delivered, 'SHIPPED ', Canceled ...)"] = len(ix)
ix = take(orders, u, 130); orders.loc[ix, "region"] = None; LOG["orders"]["region missing"] = len(ix)
ix = take(orders, u, 100)
for i in ix:
    orders.at[i, "region"] = str(rng.choice([orders.at[i, "region"].lower(), orders.at[i, "region"].upper()]))
LOG["orders"]["region এ lowercase/UPPERCASE"] = len(ix)
ix = take(orders, u, 90, orders.status.isin(["Delivered", "Shipped"]).values)
orders.loc[ix, "ship_date"] = None
LOG["orders"]["Delivered/Shipped order এ ship_date missing (Cancelled/Processing এ null স্বাভাবিক)"] = len(ix)
ix = take(orders, u, 40, orders.ship_date.notna().values)
for i in ix:
    od = date.fromisoformat(orders.at[i, "order_date"])
    orders.at[i, "ship_date"] = d2s(od - timedelta(days=int(rng.integers(1, 11))))
LOG["orders"]["ship_date < order_date (logic error)"] = len(ix)
ix = take(orders, u, 195)
for i in ix:
    orders.at[i, "order_date"] = date.fromisoformat(orders.at[i, "order_date"]).strftime("%d/%m/%Y")
LOG["orders"]["order_date DD/MM/YYYY format (বাকিগুলো YYYY-MM-DD)"] = len(ix)
ix = take(orders, u, 130, orders.ship_date.notna().values)
for i in ix:
    orders.at[i, "ship_date"] = date.fromisoformat(orders.at[i, "ship_date"]).strftime("%d/%m/%Y")
LOG["orders"]["ship_date DD/MM/YYYY format"] = len(ix)
ix = take(orders, u, 520)
PAYV = {"bKash": ["bkash", "BKASH", "Bkash"], "Cash on Delivery": ["COD", "cash on delivery", "Cash On Delivery "]}
for i in ix:
    s = orders.at[i, "payment_method"]
    orders.at[i, "payment_method"] = str(rng.choice(PAYV[s])) if s in PAYV else case_variant(s)
LOG["orders"]["payment_method এ বানান/case এর অমিল (COD, bkash ...)"] = len(ix)
ix = take(orders, u, 100); orders.loc[ix, "payment_method"] = None; LOG["orders"]["payment_method missing"] = len(ix)
ix = take(orders, u, 12)
orders.loc[ix, "customer_id"] = [f"C{int(rng.integers(1700, 2999))}" for _ in ix]
LOG["orders"]["orphan customer_id (customers এ নেই)"] = len(ix)
ix = take(orders, u, 5); orders.loc[ix, "customer_id"] = None; LOG["orders"]["customer_id missing"] = len(ix)
ix = take(orders, u, 6); orders.loc[ix, "shipping_cost"] = -orders.loc[ix, "shipping_cost"]
LOG["orders"]["negative shipping_cost"] = len(ix)
dup = orders.loc[rng.choice(orders.index, 85, replace=False)]
LOG["orders"]["হুবহু duplicate row"] = len(dup)
orders = pd.concat([orders, dup]).sample(frac=1, random_state=SEED).reset_index(drop=True)

# ---- order_items
u = set()
items["quantity"] = items["quantity"].astype("Int64")
items["discount"] = items["discount"].astype(object)
ix = take(items, u, 60); items.loc[ix, "quantity"] = pd.NA; LOG["order_items"]["quantity missing"] = len(ix)
ix = take(items, u, 30)
items.loc[ix, "quantity"] = [int(x) for x in rng.choice([0, -1, -2], len(ix))]
LOG["order_items"]["quantity ≤ 0 (invalid)"] = len(ix)
ix = take(items, u, 25)
items.loc[ix, "discount"] = [float(x) for x in rng.choice([-.05, -.10, -.20], len(ix))]
LOG["order_items"]["negative discount"] = len(ix)
ix = take(items, u, 25)
items.loc[ix, "discount"] = [float(x) for x in rng.choice([1.25, 1.5, 2.0], len(ix))]
LOG["order_items"]["discount > 1"] = len(ix)
ix = take(items, u, 40)
items.loc[ix, "discount"] = [float(x) for x in rng.choice([5, 10, 15, 20, 25, 30], len(ix))]
LOG["order_items"]["discount percent আকারে (10 মানে 10%) — fraction এ আনতে হবে"] = len(ix)
ix = take(items, u, 20)
items.loc[ix, "discount"] = [f"{int(x)}%" for x in rng.choice([5, 10, 15, 20], len(ix))]
LOG["order_items"]["discount string '15%' আকারে"] = len(ix)
ix = take(items, u, 40); items.loc[ix, "unit_price"] = np.nan; LOG["order_items"]["unit_price missing"] = len(ix)
ix = take(items, u, 50); items.loc[ix, "profit"] = np.nan; LOG["order_items"]["profit missing (পুনর্গণনা করা যায়)"] = len(ix)
ix = take(items, u, 15); items.loc[ix, "product_id"] = [f"P{int(rng.integers(900, 999))}" for _ in ix]
LOG["order_items"]["orphan product_id (products এ নেই)"] = len(ix)
ix = take(items, u, 10); items.loc[ix, "order_id"] = [f"ORD-{int(rng.integers(990000, 999999))}" for _ in ix]
LOG["order_items"]["orphan order_id (orders এ নেই)"] = len(ix)
ix = take(items, u, 25, (items.returned == "Y").values); items.loc[ix, "return_reason"] = None
LOG["order_items"]["returned = Y কিন্তু return_reason missing"] = len(ix)
ix = take(items, u, 800)
for i in ix:
    items.at[i, "returned"] = str(rng.choice({"Y": ["Yes", "y", "1", "TRUE"], "N": ["No", "n", "0", "FALSE"]}[items.at[i, "returned"]]))
LOG["order_items"]["returned এ Y/N এর বদলে Yes/No/1/0/TRUE/FALSE"] = len(ix)
ix = take(items, u, 40); items.loc[ix, "returned"] = None; LOG["order_items"]["returned missing"] = len(ix)
dup = items.loc[rng.choice(items.index, 120, replace=False)]
LOG["order_items"]["হুবহু duplicate row"] = len(dup)
items = pd.concat([items, dup]).sample(frac=1, random_state=SEED).reset_index(drop=True)

# ───────────────────────── WRITE CSVs ─────────────────────────
tables = {"customers": customers, "products": products, "orders": orders, "order_items": items}
for name, df in tables.items():
    df.to_csv(os.path.join(OUT, f"{name}.csv"), index=False, encoding="utf-8")
    print(name, df.shape)

# ───────────────────────── README ─────────────────────────
def issues_md(tbl):
    return "\n".join(f"| {k} | {v} |" for k, v in LOG[tbl].items())


README = f"""# Retail Practice Dataset (Bangladesh E-commerce) — Python Data Cleaning

এটি একটি **synthetic** (কৃত্রিমভাবে তৈরি) dataset; কোনো আসল ব্যক্তি বা কোম্পানির তথ্য নয়। উদ্দেশ্য: Python (pandas) দিয়ে
data cleaning, SQL join/aggregation এবং business-metric বিশ্লেষণের অনুশীলন। Currency: **BDT (৳)**।
সময়কাল: **{D_START} থেকে {D_END}**। Seed ফিক্সড (`{SEED}`), তাই `generate_dataset.py` চালালে একই ফাইল পাবে।

## ফাইল ও row সংখ্যা (raw, dirty অবস্থায়)

| ফাইল | Rows | বিষয়বস্তু |
|---|---|---|
| `customers.csv` | {len(customers):,} | {N_CUST:,} unique customer + duplicate rows |
| `products.csv` | {len(products):,} | {N_PROD} unique product + duplicate rows |
| `orders.csv` | {len(orders):,} | {N_ORD:,} unique order + duplicate rows |
| `order_items.csv` | {len(items):,} | প্রতি order এ ১–৪টি item |
| `schema_mysql.sql` | — | Clean target schema + staging tables (MySQL 8) |

## Relationships

```
customers (1) ──< orders (1) ──< order_items >── (1) products
 customer_id        order_id        order_id / product_id
```

## Column dictionary

**customers.csv**: `customer_id` (PK, C0001…), `customer_name`, `email`, `segment` (Consumer / Corporate / Home Office),
`signup_date`, `city`, `region` (বিভাগ), `country`

**products.csv**: `product_id` (PK, P001…), `product_name`, `category` (5টি), `subcategory` (15টি),
`unit_cost` (প্রতি unit এর ক্রয়মূল্য), `list_price` (প্রতি unit এর তালিকা মূল্য)

**orders.csv**: `order_id` (PK, ORD-000001…), `customer_id` (FK), `order_date`, `ship_date`,
`status` (Delivered / Shipped / Processing / Cancelled), `region` (delivery বিভাগ), `ship_mode`
(Standard / Express / Same Day), `shipping_cost`, `payment_method` (Cash on Delivery, bKash, Nagad, Credit Card, Bank Transfer)

**order_items.csv**: `order_item_id` (PK), `order_id` (FK), `product_id` (FK), `quantity`, `unit_price` (বিক্রয়ের সময়ের দাম),
`discount` (fraction: 0.10 = 10%), `cost` (= quantity × unit_cost, মোট cost), `profit` (মোট profit, discount এর পরে),
`returned` (Y/N), `return_reason`

## Metric definitions (clean করার পরে প্রযোজ্য)

| Metric | সংজ্ঞা |
|---|---|
| Valid order | `status != 'Cancelled'` (revenue/profit এ শুধু valid order ধরো) |
| Valid discount | `0 ≤ discount ≤ 0.30` (fraction হিসেবে) |
| Gross sales | `quantity × unit_price` |
| Net sales (Revenue) | `quantity × unit_price × (1 − discount)` |
| Profit | `Net sales − cost` (`profit` column এর সাথে মেলানো যাবে) |
| Profit margin | `Profit ÷ Net sales` |
| Discount rate | `(Gross sales − Net sales) ÷ Gross sales` |
| AOV (Average Order Value) | valid order গুলোর Net sales ÷ valid order সংখ্যা |
| Return rate | `returned = Y` item সংখ্যা ÷ Delivered order এর মোট item সংখ্যা |
| Net profit after returns | যেসব item `returned = N`, শুধু তাদের Profit |
| Fulfilment days | `ship_date − order_date` (দিন) |
| Repeat customer | যার ২ বা তার বেশি valid order আছে |
| Customer lifetime value | customer প্রতি Net sales এর যোগফল (returned বাদে) |

## ইচ্ছাকৃতভাবে ঢোকানো সমস্যা (Answer key)

> নিজে আগে খুঁজে বের করার চেষ্টা করো, তারপর এখানে মিলিয়ে নাও। সংখ্যাগুলো আনুমানিক নয়, নির্দিষ্ট।
> প্রতিটি row তে সাধারণত একটি করে সমস্যা বসানো হয়েছে।

### customers.csv
| সমস্যা | Rows |
|---|---|
{issues_md("customers")}

### products.csv
| সমস্যা | Rows |
|---|---|
{issues_md("products")}

### orders.csv
| সমস্যা | Rows |
|---|---|
{issues_md("orders")}

### order_items.csv
| সমস্যা | Rows |
|---|---|
{issues_md("order_items")}

## অনুশীলনের প্রস্তাবিত ধাপ

1. `df.info()`, `df.isna().sum()`, `df.duplicated().sum()` দিয়ে প্রাথমিক অডিট
2. Duplicate সরানো; customers এ email দিয়ে near-duplicate চিহ্নিত করে merge করা
3. Text standardise: `str.strip().str.title()`, status/payment/region/segment এর মান ঠিক করা
4. Date parse (`pd.to_datetime(..., format='mixed', dayfirst=True)` এর ঝুঁকি বুঝে নিজে format ঠিক করো), ship_date < order_date ঠিক করা বা flag করা
5. Discount normalise (`15%` → 0.15, `10` → 0.10, ভুল মান NaN/flag), quantity ≤ 0 হ্যান্ডেল
6. Missing `unit_price` / `profit` পুনর্গণনা (`list_price`, `unit_cost` join করে)
7. Orphan key গুলো যাচাই (`merge(indicator=True)`) এবং সিদ্ধান্ত নেওয়া: drop / flag / quarantine table
8. Clean data MySQL এ লোড করে metric গুলো SQL এ হিসাব করা এবং pandas এর ফলের সাথে মেলানো

## Legitimate null (এগুলো ভুল নয়)

- `ship_date` null: Processing ও Cancelled order এ
- `return_reason` null: যেসব item `returned = N`
"""
with open(os.path.join(OUT, "README.md"), "w", encoding="utf-8") as f:
    f.write(README)
print("README written")
