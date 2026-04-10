import requests

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


# GraphQL query to fetch products with their name, sku, description, attributes and price
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
                    "argumentaire_vente_externe",  # description
                    "identite_produit",            # product identity (used as category)
                    "pastille_gout",               # taste tag
                    "pays_origine",                # country
                    "region_origine",              # region
                    "teneur_alcool",               # alcohol degree
                    "nom_producteur",              # producer
                    "format_contenant_ml",         # bottle size
                    "millesime_produit",           # vintage
                    "cepage"                       # grape variety
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

CATALOG_TYPE_1_PRICE_RANGES = [
    (0, 19.99),
    (20, 29.99),
    (30, 59.99),
    (60, 149.99),
    (150, 90000),
]

CATEGORY_PATHS = [
    "products/wine",
    "products/spirit",
    "products/champagne-and-sparkling-wine",
    "products/beer",
    "products/cider",
    "products/cooler-or-premixed-cocktail",
    "products/port-and-fortified-wine",
]

def _execute_query(query, variables=None):
    """
    Execute a GraphQL query against the SAQ API.
    """
    response = requests.post(
        URL,
        json={"query": query, "variables": variables or {}},
        headers=HEADERS,
        timeout=20,
    )
    response.raise_for_status()

    data = response.json()

    if "errors" in data:
        raise Exception(f"GraphQL errors: {data['errors']}")
    return data["data"]


def fetch_products_by_filter(page=1, page_size=500, filters=None):
    """
    Fetch products by filter.
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


def fetch_all_products():
    """
    Fetch all products by querying catalog_type 1 with price ranges and catalog_type 2 directly.
    """
    all_products = []

    # catalog_type = 1
    for price_from, price_to in CATALOG_TYPE_1_PRICE_RANGES:
        print(f"\nFetching catalog_type=1, price {price_from}-{price_to}...")
        page = 1
        range_total = 0
        while True:
            result = fetch_products_by_filter(
                page=page,
                filters=[
                    {"attribute": "catalog_type", "eq": "1"},
                    {
                        "attribute": "price",
                        "range": {"from": price_from, "to": price_to},
                    },
                ],
            )
            items = result.get("items", [])
            range_total += len(items)
            all_products.extend(items)

            if len(items) < 500:
                break
            page += 1

        print(
            f"Found {range_total} items for catalog_type=1 price range {price_from}-{price_to}"
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
                        {"attribute": "price", "range": {"from": price_from, "to": price_to}},
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
