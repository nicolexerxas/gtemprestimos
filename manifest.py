{
    'name': 'GT Empréstimos',
    'version': '1.0',
    'category': 'Financial',
    'summary': 'Registro e gestão de operações de empréstimos: cálculo de juros, parcelas, renegociação e status.',
    'author': 'GT Empréstimos',
    'license': 'LGPL-3',
    'depends': ['base', 'mail'],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'data/cron_data.xml',
        'views/loan_views.xml',
        'views/installment_views.xml',
    ],
    'installable': True,
    'application': False,
}