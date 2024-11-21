{
    "name": "Email Template Change",
    "author": "Odoo",
    "website": "https://www.odoo.com",
    "category": "Administration",
    "version": "18.0.1.0.0",
    "depends": ["sale_management"],
    "data": [
        # FIELDS
        "data/ir_model_fields.xml",
        # VIEWS
        "views/email_templates.xml",
        "views/res_company_views.xml",
    ],
}
