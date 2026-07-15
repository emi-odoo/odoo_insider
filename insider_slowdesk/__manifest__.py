{
    "name": "Insider Slowdesk",
    "summary": "A support ticket module with deliberate performance anti-patterns (live demo material)",
    "version": "19.0.1.0.0",
    "category": "Services/Helpdesk",
    "author": "Emanuele - Odoo Insider",
    "license": "LGPL-3",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "data/data.xml",
        "views/insider_ticket_views.xml",
    ],
    "application": True,
    "installable": True,
}
