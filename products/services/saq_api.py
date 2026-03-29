import requests

URL = "https://catalog-service.adobe.io/graphql"

HEADERS = {
    "Content-Type": "application/json",
    "x-api-key": "7a7d7422bd784f2481a047e03a73feaf",
    "magento-customer-group": "b6589fc6ab0dc82cf12099d1c2d40ab994e8410c",
    "magento-environment-id": "2ce24571-9db9-4786-84a9-5f129257ccbb",
    "magento-store-code": "main_website_store",
    "magento-store-view-code": "fr",
    "magento-website-code": "base",
}


# GraphQL query to fetch products with their name, sku, description, attributes and price
QUERY = """
query ($phrase: String!, $pageSize: Int!, $currentPage: Int!, $filter: [SearchClauseInput!]) {
    productSearch(phrase: $phrase, page_size: $pageSize, current_page: $currentPage, filter: $filter) {
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
    (0, 20),
    (20, 30),
    (30, 60),
    (60, 150),
    (150, 999999),
]


OTHER_CATALOG_TYPES = ["2", "3"]


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
        "sort": [{"attribute": "price", "direction": "ASC"}],
    }

    products = _execute_query(QUERY, variables)["productSearch"]

    return products


def fetch_all_products():
    """
    Fetch all products by querying catalog_type 1 with price ranges and catalog_types 2-3 directly.
    """
    all_products = []

    # catalog_type = 1
    for price_from, price_to in CATALOG_TYPE_1_PRICE_RANGES:
        print(f"\nFetching catalog_type=1, price {price_from}-{price_to}...")
        page = 1
        while True:
            items = fetch_products_by_filter(
                page=page,
                filters=[
                    {"attribute": "catalog_type", "eq": "1"},
                    {"attribute": "price", "range": {"from": price_from, "to": price_to}},
                ]
            ).get("items", [])

            all_products.extend(items)
            if len(items) < 500:
                break
            page += 1

    # catalog_type 2-7
    for catalog_type in OTHER_CATALOG_TYPES:
        print(f"\nFetching catalog_type={catalog_type}...")
        page = 1
        while True:
            items = fetch_products_by_filter(
                page=page,
                filters=[{"attribute": "catalog_type", "eq": catalog_type}]
            ).get("items", [])
            print(f"Found {len(items)} items for catalog_type={catalog_type}")

            all_products.extend(items)
            if len(items) < 500:
                break
            page += 1

    return all_products


