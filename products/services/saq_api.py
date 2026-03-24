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


# GraphQL query to fetch products with their name, sku, description,attributes and price
QUERY = """
query ($phrase: String!, $pageSize: Int!, $currentPage: Int!) {
    productSearch(phrase: $phrase, page_size: $pageSize, current_page: $currentPage) {
        total_count
        items {
            productView {
                name
                sku
                description
                attributes(names: [
                    "identite_produit",    # product identity (used as category)
                    "pastille_gout",       # taste tag
                    "pays_origine",        # country
                    "region_origine",      # region
                    "teneur_alcool",       # alcohol degree
                    "nom_producteur",      # producer
                    "format_contenant_ml", # bottle size
                    "millesime_produit",   # vintage
                    "cepage"               # grape variety
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


def _execute_query(query, variables=None):
    """
    Execute a GraphQL query against the SAQ API.
    """
    response = requests.post(
        URL, json={"query": query, "variables": variables or {}}, headers=HEADERS
    )
    if response.status_code != 200:
        raise Exception(f"GraphQL request failed: {response.text}")
    data = response.json()
    if "errors" in data:
        raise Exception(f"GraphQL errors: {data['errors']}")
    return data["data"]


def fetch_products(page=1, page_size=50):
    """
    Fetch a single page of products from the SAQ API.
    Default: 50 products per page
    """
    variables = {"phrase": " ", "pageSize": page_size, "currentPage": page}
    return _execute_query(QUERY, variables)["productSearch"]


def fetch_products_pages(max_pages=2, page_size=50):
    """
    Fetch multiple pages of products.
    Default: 2 pages with 50 products per page
    """
    all_products = []
    for page in range(1, max_pages + 1):
        print(f"Fetching page {page}...")
        data = fetch_products(page=page, page_size=page_size)
        items = data.get("items", [])
        print(f"  Got {len(items)} items")
        if not items:
            break
        all_products.extend(items)
    return all_products
