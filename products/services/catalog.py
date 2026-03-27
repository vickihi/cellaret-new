from dataclasses import dataclass

from django.core.paginator import Paginator

from products.forms import ProductCatalogSearchForm
from products.selectors import get_catalog_products


@dataclass
class CatalogPageData:
    form: ProductCatalogSearchForm
    page_obj: object
    products: object
    search_query: str


def build_catalog_page(*, data, page_number, per_page: int = 20) -> CatalogPageData:
    form = ProductCatalogSearchForm(data)
    is_valid = form.is_valid()

    search_query = form.cleaned_data.get("q", "") if is_valid else ""
    products_qs = get_catalog_products(search_query=search_query)
    paginator = Paginator(products_qs, per_page)
    page_obj = paginator.get_page(page_number)

    return CatalogPageData(
        form=form,
        page_obj=page_obj,
        products=page_obj.object_list,
        search_query=search_query,
    )
