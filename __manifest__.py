{
    'name': 'GT Empréstimos',
    'version': '1.0',
    'category': 'Financial',
    'summary': 'Gestão de Empréstimos: parcelas, juros, renegociação e inadimplência',
    'author': 'GT Empréstimos',
    'license': 'LGPL-3',
    'depends': ['base', 'mail'],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'data/cron_data.xml',
        'views/loan_views.xml',
        'views/installment_views.xml',
        'views/renegotiation_views.xml',
    ],
    'installable': True,
    'application': False,
}
