from odoo import models, fields, api
from datetime import datetime
from odoo13.addons.hr_recruitment.models.hr_recruitment import Applicant


class ApplicantExtension(models.Model):
    _inherit = 'hr.applicant'

    parent_id = fields.Many2one('hr.employee', string="Manager")

    emergency_ids = fields.One2many('hr.applicant.emg', 'emergency_id', string="||")
    education_ids = fields.One2many('hr.applicant.edu', 'education_id', string="||")

    # For test purpose
    def test_button(self):
        print(self.parent_id.user_id.id)
        print(self.env.user.id)

        return self.show_applicant_wizard()

    # def show_applicant_wizard(self):
    #     # action = self.env['ir.actions.act_window'].for_xml_id('hr.applicant.leave.wizard',
    #     #                                                       'hr_applicants_leave_wizard_action')
    #     action = self.env.ref('applicant.wizard.hr_applicants_leave_wizard_action').read()[0]
    #     return action

    def show_applicant_wizard(self):
        # self.env.ref('<module_name>.<action_name>')
        action = self.env.ref('employee_recruit.hr_applicant_wiz_action').read()[0]
        return action

    def create_employee_from_applicant(self):
        # self.show_applicant_wizard()
        curr_act_window = super(ApplicantExtension, self).create_employee_from_applicant()
        leave_action = self.show_applicant_wizard()

        # Retrieving the employee using the emp_id filed of hr.applicant
        employee = self.env['hr.employee'].browse(self.emp_id.id)

        employee.write({
            'parent_id': self.parent_id.id,  # Assigning the manager or the parent_id

            # Mapping Applicant's emergency_ids, education_ids one2many fields data to hr.employee model
            'emergency_ids': [(0, 0, {'emp_name': v1, 'emp_phone': v2, 'emp_address': v3}) for v1, v2, v3 in
                              self.emergency_ids.mapped(lambda rec: (rec.emp_name, rec.emp_phone, rec.emp_address))],
            'education_ids': [(0, 0, {'institute': v1, 'degree': v2, 'passing_year': v3}) for v1, v2, v3 in
                              self.education_ids.mapped(lambda rec: (rec.institute, rec.degree, rec.passing_year))]
        })

        return leave_action


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


class HrLeaveAllocation(models.TransientModel):
    _name = 'applicant.wizard'
    _inherit = 'hr.leave.allocation'

    alloc_rel = fields.Many2one('hr.leave.allocation', string="Applicant_Allocation")

    desc = fields.Char('Description')
    leave_type = fields.Many2one('hr.leave.type', string="Leave Type")
    days = fields.Float('Duration')

    def create_leave(self):
        date_obj = datetime.today()
        today = date_obj.date()
        curr_year = date_obj.year
        current_time = date_obj.time()

        last_date = datetime.strptime("31/12/" + str(curr_year) + " " + current_time.strftime("%H:%M:%S"),
                                      "%d/%m/%Y %H:%M:%S")
        last_date = last_date.replace(microsecond=0)

        self.env['hr.leave.allocation'].create({
            'employee_id': self.env.user.id,
            'allocation_type': 'accrual',
            'number_per_interval': self.days,
            'interval_number': 1,
            'unit_per_interval': 'days',
            'interval_unit': 'years',
            'holiday_type': 'employee',
            'date_to': last_date
        })
