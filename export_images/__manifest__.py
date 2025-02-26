{
    "name": "Export Images",
    "summary": """
        Export images contacts
    """,
    "version": "18.0.0.1.0",
    "depends": ["contacts"],
    "data": [
        # VIEWS
        "data/server_action.xml"
    ],
    "assets": {
        # New bundle that will be lazy loaded
        "export_images.external_libraries": [
            # We use the following external libraries:
            # https://github.com/gildas-lormeau/zip.js/tree/master
            # current version:
            # https://github.com/gildas-lormeau/zip.js/releases/tag/v2.7.57
            "export_images/static/src/lib/zip/zip.min.js",
        ],
        "web.assets_backend": [
            "export_images/static/src/js/download_pictures.js",
        ],
    },
    # Exclude the external libraries from the cloc analysis
    # (it would be counted as 1 loc as it's minified)
    "cloc_exclude": ["static/src/lib/**/*"],
}
