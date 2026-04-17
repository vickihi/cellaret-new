# This file is to fetch products from SAQ API and store them in our database.
import requests


# Part1: Setup connection to SAQ API
URL = "https://catalog-service.adobe.io/graphql"

HEADERS = {
    "Content-Type": "application/json",
    "x-api-key": "7a7d7422bd784f2481a047e03a73feaf",
    "magento-customer-group": "b6589fc6ab0dc82cf12099d1c2d40ab994e8410c",
    "magento-environment-id": "2ce24571-9db9-4786-84a9-5f129257ccbb",
    "magento-store-code": "main_website_store",
    "magento-store-view-code": "en",
    "magento-website-code": "base",
}


# Part2: Define the GraphQL query template to fetch products with their: 
# total count,
# name, sku, image url, description, 
# attributes (used as category, taste tag, country, region, alcohol degree, producer, bottle size, vintage, grape variety), 
# and price
QUERY = """
query ($phrase: String!, $pageSize: Int!, $currentPage: Int!, $filter: [SearchClauseInput!], $sort: [ProductSearchSortInput!]) {
    productSearch(phrase: $phrase, page_size: $pageSize, current_page: $currentPage, filter: $filter, sort: $sort) {
        total_count
        items {
            productView {
                name
                sku
                images {
                    url
                }
                attributes(names: [
                    "argumentaire_vente_externe",       # description
                    "identite_produit",                 # product identity (used as category)
                    "pastille_gout",                    # taste tag
                    "pays_origine",                     # country
                    "region_origine",                   # region
                    "pourcentage_alcool_par_volume",    # alcohol degree
                    "nom_producteur",                   # producer
                    "format_contenant_ml",              # bottle size
                    "millesime_produit",                # vintage
                    "cepage"                            # grape variety
                ]) {
                    name
                    value
                }
            }
            product {
                price_range {
                    minimum_price {
                        regular_price { value }
                    }
                }
            }
        }
    }
}
"""


# Part 3: How to fetch all products: 
# Split catalog_type=1 queries into price ranges to stay below the 10,000-result API limit.
#
# --- Discovery process for two level filters ---
#   1. Why split by catalog_type?
#      catalog_type was identified as a valid filter by exploring the API schema via GraphQL introspection
#      and testing each value.
#   2. Why catalog_type 1 & 2?
#      Tested catalog_type values 1–7; only types 1 and 2 contain actual drink products.
#      Types 3–7 return non-product data (recipes, cocktails, articles, and internal content).
#   3. Why catalog_type=1 further split by price?
#      catalog_type=1 has ~25,000 products, exceeding the 10,000-result pagination limit.
#      Splitting by price range keeps each query within the limit.
#   4. Why these price ranges?
#      To ensure each range stays below 10,000 results,
#      ranges are hardcoded based on manually verified product counts per range,
#      and can be adjusted as needed.


# --- Discovery queries (not used in production) ---

# Query 1: Level 1 filter
# Discover all available filter attributes and their values via facets.
# Run this to find catalog_type values (1–7) and the product count for each.
# Look for the result where "attribute": "catalog_type" to see all values (1–7) and their product counts.
# 
# query {
#   productSearch(phrase: " ", page_size: 1, current_page: 1) {
#     facets {
#       title
#       attribute
#       buckets {
#         title
#         ... on ScalarBucket {
#           id
#           count
#         }
#       }
#     }
#   }
# }

# Query 2: Level 2 filter
# Check product count for a specific catalog_type + price range combination.
# Use this to manually verify that each price range stays below 10,000 results.
# 
# query {
#   productSearch(
#     phrase: " "
#     page_size: 1
#     current_page: 1
#     filter: [
#       { attribute: "catalog_type", eq: "1" }
#       { attribute: "price", range: { from: 0, to: 19.99 } }
#     ]
#   ) {
#     total_count
#   }
# }


# --- Define catalog_type=1 price ranges ---
CATALOG_TYPE_1_PRICE_RANGES = [
    (0, 19.99),   # 3135
    (20, 29.99),  # 4404
    (30, 59.99),  # 5732
    (60, 149.99), # 6071
    (150, 90000), # 6281
]


# --- Low-level HTTP wrapper — handles sending requests and error checking. ---
def _execute_query(query, variables=None):
    """
    Send a GraphQL query to the SAQ API and return the response data.
    """
    response = requests.post(
        URL,
        json={"query": query, "variables": variables or {}},
        headers=HEADERS,
        timeout=20,
    )
    response.raise_for_status()  # raise an exception if the request was not successful for external api

    data = response.json()

    if "errors" in data:
        raise Exception(f"GraphQL errors: {data['errors']}")
    return data["data"]


# --- Assemble query variables and calls _execute_query. ---
def fetch_products_by_filter(page=1, page_size=500, filters=None):
    """
    Assemble query variables (pagination, filters, sort) and call _execute_query.
    Returns the productSearch result directly.
    """
    variables = {
        "phrase": " ",
        "pageSize": page_size,
        "currentPage": page,
        "filter": filters or [],
        "sort": [
            {"attribute": "price", "direction": "ASC"},
            {"attribute": "sku", "direction": "ASC"},
        ],
    }

    products = _execute_query(QUERY, variables)["productSearch"]

    return products


# --- Fetch all products. ---
def fetch_all_products():
    """
    Fetch all products by querying catalog_type 1 with price ranges 
    and catalog_type 2 directly.
    """
    all_products = []

    # catalog_type = 1
    for price_from, price_to in CATALOG_TYPE_1_PRICE_RANGES:
        print(f"\nFetching catalog_type=1, price {price_from}-{price_to}...")
        page = 1
        fetched_count = 0
        while True:
            result = fetch_products_by_filter(
                page=page,
                filters=[
                    {
                        "attribute": "catalog_type", "eq": "1"
                    },
                    {
                        "attribute": "price",
                        "range": {"from": price_from, "to": price_to},
                    },
                ],
            )
            items = result.get("items", [])
            fetched_count += len(items)
            all_products.extend(items)

            if len(items) < 500:
                break
            page += 1

        print(
            f"Found {fetched_count} items for catalog_type=1 price range {price_from}-{price_to}"
        )

    # catalog_type = 2
    print("\nFetching catalog_type=2...")
    page = 1
    type_total = 0
    while True:
        result = fetch_products_by_filter(
            page=page, filters=[{"attribute": "catalog_type", "eq": "2"}]
        )
        items = result.get("items", [])
        type_total += len(items)
        all_products.extend(items)

        if len(items) < 500:
            break
        page += 1

    print(f"Found {type_total} items for catalog_type=2")

    print(f"\n=== Total products fetched: {len(all_products)} ===")
    return all_products



# Part 4: How to map SKUs to categories:
CATEGORY_PATHS = [
    "products/wine",
    "products/spirit",
    "products/champagne-and-sparkling-wine",
    "products/beer",
    "products/cider",
    "products/cooler-or-premixed-cocktail",
    "products/port-and-fortified-wine",
]

def fetch_sku_category_map():
    """
    Return a {sku: category_path} mapping by querying each category path.
    """
    sku_map = {}
    for path in CATEGORY_PATHS:
        print(f"  Fetching category: {path}...")
        for price_from, price_to in CATALOG_TYPE_1_PRICE_RANGES:
            page = 1
            while True:
                result = fetch_products_by_filter(
                    page=page,
                    page_size=500,
                    filters=[
                        {"attribute": "categories", "eq": path},
                        {"attribute": "catalog_type", "eq": "1"},
                        {
                            "attribute": "price",
                            "range": {"from": price_from, "to": price_to},
                        },
                    ],
                )
                items = result.get("items", [])
                for item in items:
                    sku = (item.get("productView") or {}).get("sku")
                    if sku and sku not in sku_map:
                        sku_map[sku] = path
                if len(items) < 500:
                    break
                page += 1
        page = 1
        while True:
            result = fetch_products_by_filter(
                page=page,
                page_size=500,
                filters=[
                    {"attribute": "categories", "eq": path},
                    {"attribute": "catalog_type", "eq": "2"},
                ],
            )
            items = result.get("items", [])
            for item in items:
                sku = (item.get("productView") or {}).get("sku")
                if sku and sku not in sku_map:
                    sku_map[sku] = path
            if len(items) < 500:
                break
            page += 1
    return sku_map
