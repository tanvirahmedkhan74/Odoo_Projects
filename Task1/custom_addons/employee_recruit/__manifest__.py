{
    'name': 'Hr_Employee_Ext',
    'description': 'Extention for HR Module',
    'depends': ['base', 'hr', 'hr_recruitment'],
    'data' : [
        'security/ir.model.access.csv',
        # 'views/hr_employee_em_view.xml'
        'views/hr_applicant_ext_view.xml',
    ],
}