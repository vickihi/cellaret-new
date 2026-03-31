from dataclasses import dataclass

from django.core.paginator import Paginator
from django.urls import reverse

from products.forms import ProductCatalogSearchForm, ProductSortForm
from products.selectors import get_catalog_products


@dataclass
class CatalogPageData:
    form: ProductCatalogSearchForm
    sort_form: ProductSortForm
    page_obj: object
    products: object
    search_query: str
    sort_key: str
    page_range: list
    breadcrumbs: list[dict[str, str | None]]


def build_catalog_page(*, data, page_number, per_page: int = 24) -> CatalogPageData:
    form = ProductCatalogSearchForm(data)
    sort_form = ProductSortForm(data)
    is_valid = form.is_valid()

    search_query = form.cleaned_data.get("q", "") if is_valid else ""
    sort_key = (
        sort_form.cleaned_data.get("sort", "default")
        if sort_form.is_valid()
        else "default"
    )
    products_qs = get_catalog_products(search_query=search_query, sort_key=sort_key)
    paginator = Paginator(products_qs, per_page)
    page_obj = paginator.get_page(page_number)
    elided_page_range = paginator.get_elided_page_range(
        page_obj.number, on_each_side=1, on_ends=1
    )  # type: ignore
    breadcrumbs = [
        {"label": "Home", "url": reverse("products:catalog")},
    ]
    if search_query:
        breadcrumbs.append(
            {
                "label": f"Search results for: {search_query}",
                "url": None,
            }
        )

    return CatalogPageData(
        form=form,
        sort_form=sort_form,
        page_obj=page_obj,
        products=page_obj.object_list,
        search_query=search_query,
        sort_key=sort_key,
        page_range=elided_page_range,
        breadcrumbs=breadcrumbs,
    )
