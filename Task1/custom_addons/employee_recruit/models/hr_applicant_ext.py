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
        employee.update({
            'parent_id': self.parent_id.id
        })

        employee.write({
            'emergency_ids': [(0, 0, x) for x in self.emergency_ids]
        })

        employee.write({
            'education_ids': [(0, 0, x) for x in self.education_ids]
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
