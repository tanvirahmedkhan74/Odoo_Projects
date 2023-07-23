{
    'name': 'Hr_Employee_Ext',
    'description': 'Extention for HR Module',
    'depends': ['base', 'hr', 'hr_recruitment', 'hr_holidays'],
    'data': [
        'security/security_rules.xml',
        'security/ir.model.access.csv',
        'views/hr_leave_ext_view.xml',
        'views/hr_employee_em_view.xml',
        'views/hr_applicant_ext_view.xml',
    ],
}
