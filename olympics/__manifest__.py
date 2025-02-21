{
    "name": "Olympics",
    "author": "Odoo",
    "website": "https://www.odoo.com",
    "category": "Administration",
    "version": "18.0.1.0.0",
    "depends": ["bus"],
    "data": [
        # SECURITY
        "security/ir.model.access.csv",
        # DATA
        "views/olympic_views.xml",
        "views/menuitems.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "olympics/static/src/**/*",
        ],
    },
}
