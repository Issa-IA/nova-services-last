# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Partner fleet",
    "summary": """
        Helpdesk""",
    'version': '18.0.1.0.0',
    "license": "AGPL-3",
    'category': 'Novatec',
    "author":
    "shayma",
    "website": "",
    "depends": ["mail", "portal", 'base','product', 'sale','contacts', 'fleetADD1'],
    "data": [
        "view/inherit_part_fleet.xml",
        "view/fleet_template.xml",

    ],
    "demo": [""],
    "development_status": "Beta",
    "application": True,
    "installable": True,
}
