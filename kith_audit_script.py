# Kith E-Commerce Inventory & Supply Chain Audit
# Author: Business Analyst Portfolio Project
# Description: Automated extraction and analysis of live variant telemetry from Kith's Shopify JSON endpoint.

import pandas as pd
import requests

# 1. Fetch live product JSON data from Kith's infrastructure
url = "https://kith.com/products.json?limit=250"
response = requests.get(url)
data = response.json()

print(f"Successfully connected! Total products fetched in first batch: {len(data.get('products', []))}")

# 2. Extract variant records into a structured dataset
variants_list = []
for product in data.get('products', []):
    title = product.get('title')
    vendor = product.get('vendor')
    product_type = product.get('product_type')

    for variant in product.get('variants', []):
        variants_list.append({
            'Product_Title': title,
            'Vendor': vendor,
            'Category': product_type,
            'Variant_Title': variant.get('title'),
            'Price_USD': float(variant.get('price', 0)),
            'Compare_At_Price': float(variant.get('compare_at_price', 0)) if variant.get('compare_at_price') else None,
            'SKU': variant.get('sku'),
            'In_Stock': variant.get('available')
        })

df = pd.DataFrame(variants_list)

# 3. Analyze stockout metrics
total_skus = len(df)
sold_out_skus = (df['In_Stock'] == False).sum()
stockout_rate = (sold_out_skus / total_skus) * 100

print(f"Total Variants Audited: {total_skus}")
print(f"Catalog-Wide Stockout Rate: {stockout_rate:.2f}%")

# 4. Save to CSV for Excel Pivot Table verification
df.to_csv('kith_raw_inventory_audit.csv', index=False)
print("Audit dataset successfully exported to 'kith_raw_inventory_audit.csv'")
