{
    "name": "Spreadsheet Group - quick example",
    "category": "Spreadsheet",
    "author": "Odoo PS",
    "license": "OEEL-1",
    "website": "https://www.odoo.com",
    "version": "18.0.0.0.0",
    "depends": [
        "spreadsheet_edition",
    ],
    "data": [
        "security/res_groups.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "group_spreadsheet/static/src/components/cog_menu_spreadsheet.js",
            "group_spreadsheet/static/src/components/list_controller.js",
        ],
        "web.assets_backend_lazy": [
            "group_spreadsheet/static/src/components/pivot_view.js",
            "group_spreadsheet/static/src/components/graph_view.js",
        ],
    },
}
