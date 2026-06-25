{
    "name": "Print Directly",
    "category": "Uncategorized",
    "author": "Odoo PS",
    "license": "OEEL-1",
    "website": "https://www.odoo.com",
    "version": "18.0.0.0.0",
    "depends": [
        "web",
    ],
    "assets": {
        "web.assets_backend": [
            "print_directly/static/src/components/**/*",
        ],
    },
    # usage of this module has to be checked again,
    # might not work as expected
    "installable": False,
}
