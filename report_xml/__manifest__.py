
{
    "name": "XML Reports",
    "version": "15.0.1.0.1",
    "category": "Reporting",
    "website": "",
    "development_status": "Production/Stable",
    "author": "",
    "license": "AGPL-3",
    "installable": True,
    "application": False,
    "summary": "Allow to generate XML reports",
    "depends": ["web"],
    "data": [
        "views/ir_actions_report_view.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "report_xml/static/src/js/report/action_manager_report.esm.js",
        ],
    },
    "demo": [
        "demo/report.xml",  # register report in the system
        "demo/demo_report.xml",  # report body definition
    ],
    "external_dependencies": {
        "python": [  # Python third party libraries required for module
            "lxml"  # XML and HTML with Python
        ]
    },
    "post_init_hook": "post_init_hook",
}
