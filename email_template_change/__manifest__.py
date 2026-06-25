{
    "name": "Email Template Change",
    "author": "Odoo",
    "website": "https://www.odoo.com",
    "category": "Administration",
    "version": "19.0.1.0.0",
    "depends": ["sale_management"],
    "license": "LGPL-3",
    "data": [
        # FIELDS
        "data/ir_model_fields.xml",
        # VIEWS
        "views/res_company_views.xml",
        # TEMPLATES
        "views/email_templates.xml",
    ],
}
