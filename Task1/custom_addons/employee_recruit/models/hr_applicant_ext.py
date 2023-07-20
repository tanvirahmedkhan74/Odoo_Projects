from odoo import models, fields, api

from odoo13.addons.hr_recruitment.models.hr_recruitment import Applicant


class ApplicantExtension(models.Model):
    _inherit = 'hr.applicant'

    parent_id = fields.Many2one('hr.employee', string="Manager")

    emergency_ids = fields.One2many('hr.applicant.emg', 'emergency_id', string="||")
    education_ids = fields.One2many('hr.applicant.edu', 'education_id', string="||")

    def create_employee_from_applicant(self):
        curr_act_window = super(ApplicantExtension, self).create_employee_from_applicant()

        # Retrieving the employee using the emp_id filed of hr.applicant
        employee = self.env['hr.employee'].browse(self.emp_id.id)

        # Assigning the manager or the parent_id

        employee.write({
            'parent_id': self.parent_id.id,
            'emergency_ids': [(0, 0, {'emp_name': v1, 'emp_phone': v2, 'emp_address': v3}) for v1, v2, v3 in
                              self.emergency_ids.mapped(lambda rec: (rec.emp_name, rec.emp_phone, rec.emp_address))],
            'education_ids': [(0, 0, {'institute': v1, 'degree': v2, 'passing_year': v3}) for v1, v2, v3 in
                              self.education_ids.mapped(lambda rec: (rec.institute, rec.degree, rec.passing_year))]
        })

        return curr_act_window


class ApplicantEmployeeEmergency(models.Model):
    _name = 'hr.applicant.emg'

    emergency_id = fields.Many2one('hr.applicant', string="Emergency")

    emp_name = fields.Char('Name')
    emp_phone = fields.Char('Phone')
    emp_address = fields.Char('Address')


class ApplicationEmployeeEducation(models.Model):
    _name = 'hr.applicant.edu'

    education_id = fields.Many2one('hr.applicant', string="Education")
    # employee_edu = fields.Many2one('hr.employee', string="Education")

    institute = fields.Char('Institute')
    degree = fields.Char('Degree')
    passing_year = fields.Char('Passing Year')


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    emergency_ids = fields.One2many('hr.applicant.emg', 'emergency_id', string="||")
    education_ids = fields.One2many('hr.applicant.edu', 'education_id', string="||")
