{
        'name': 'Library Management',
        'description': 'Book Management Catalog and lending',
        'author': 'Tanvir Ahmed Khan',
        'depends': ['base'],
        'application': True,
        'data': [
                    'security/library_security.xml',
                    'security/ir.model.access.csv',
                    'views/library_menu.xml',
                 ],
}
