import sqlite3
import random

conn = sqlite3.connect('inventory_data.sqlite')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS inventory_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    production_year INTEGER,
    order_number TEXT,       
    product_identifier TEXT, 
    semiproduct_index TEXT,
    material_index TEXT,
    material_name_en TEXT,
    quantity REAL,
    unit TEXT,
    price_per_unit REAL,
    total_value REAL)
''')

def generate_product_name(product_code):
    adjectives = ["Ultra", "Premium", "Deluxe", "Basic", "1255", "Fy7cA", "SRGE53j", "JBCWQ1", "ORWNF881BD", "CQIEFU31q314JG" ]
    materials = ["Steel", "Wood", "Plastic", "Composite", "Aluminum"]
    return f"{random.choice(adjectives)} {random.choice(materials)} {product_code}"

def generate_semiproduct_name(product_code, index):
    return f"{product_code}-{index}"

products = {
    "PRD-001": 78, #semiproducts
    "PRD-002": 85, 
    "PRD-003": 110
}

material_index = {
    "AXR": ["Auxiliary Materials"], 
    "CMT": ["Coatings, Materials and Treatments"],
    "CNS": ["Construction Parts"] 
}

annual_production_plan = {
    "PRD-001": 27, 
    "PRD-002": 40,
    "PRD-003": 55,
}

axr_package_size = [1, 5, 10, 20, 24, 36, 48, 50, 100]
cmt_package_size = [2.5, 15.0, 25.0, 50.0]
cns_package_size = [1]

random.seed(123)
data = []
for year in [2023, 2024]:
    for month in range(1, 13):
        for product, bom_size in products.items():
            num_produced = annual_production_plan[product]
            product_name = generate_product_name(product)
            for product_instance in range(num_produced):
                
                num_materials = random.randint(10, 80)

                axr_count = int(num_materials * 0.7)
                cmt_count = int(num_materials * 0.25)
                cns_count = num_materials - (axr_count + cmt_count)

                materials = []
                materials.extend(["AXR"] * axr_count)
                materials.extend(["CMT"] * cmt_count)
                materials.extend(["CNS"] * cns_count)

                random.shuffle(materials)

                order_number = f"{random.randint(1, 1000)}/{year}"

                for idx, material_type in enumerate(materials, 1):
                    semiproduct_bom_usage = num_produced * random.randint(10, 80)
                    semiproduct_index = f"{product}-{random.randint(1, 75)}"
                    semiproduct_name = generate_semiproduct_name(product, idx) 
                    material_id = f"{material_type}-{random.randint(100000, 999999)}"
                    material_name_en = material_index[material_type][0]  
                    price_per_unit = round(random.uniform(0.5, 1000), 2)

                    if material_type == "AXR":
                        package = random.choice(axr_package_size)
                        quantity = round(random.uniform(0.1, 10), 2)
                        unit = "pcs"
                    elif material_type == "CMT":
                        quantity = round(random.choice(cmt_package_size) * random.uniform(0.1, 5), 2)
                        unit = "unit"
                    elif material_type == "CNS":
                        quantity = round(random.choice(cns_package_size) * random.uniform(0.1, 5), 2)
                        unit = "m2"
                    else:
                        quantity = 1
                        unit = "units"
                    
                    total_value = round(quantity * price_per_unit, 2)

                    data.append((
                        order_number, product, semiproduct_index, material_id, material_name_en,
                        quantity, unit, price_per_unit, total_value, year
                    ))

# Corrected the query by removing the trailing comma
cursor.executemany('''
INSERT INTO inventory_usage (
    order_number, product_identifier, semiproduct_index, material_index,
    material_name_en, quantity, unit, price_per_unit, 
    total_value, production_year
)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', data)

conn.commit()
conn.close()

print('Database successfully populated.')
