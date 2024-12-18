{
    "name": "prooooooduct Brand",
    "author": "Odoo",
    "website": "https://www.odoo.com",
    "category": "Administration",
    "version": "18.0.1.0.1",
    "depends": ["sale"],
    "data": [
        "data/product_brand.xml",
        # SECURITY
        "security/ir.model.access.csv",
        # VIEWS
        "views/product_brand_views.xml",
        "views/product_template_views.xml",
    ],
}
