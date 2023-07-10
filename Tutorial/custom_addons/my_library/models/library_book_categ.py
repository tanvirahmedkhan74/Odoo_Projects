from odoo import models, fields, api
from odoo.exceptions import ValidationError


class BookCategory(models.Model):
    _name = 'library.book.category'
    _description = 'Book Categories'
    _parent_store = True
    _parent_name = "parent_id"
    parent_path = fields.Char(index=True)

    name = fields.Char('Category')
    description = fields.Text('Description')

    # Child category can inheirt many parent category and both resides in this model
    parent_id = fields.Many2one('library.book.category', string='Parent Category', ondelete='restrict',
                                index=True)
    child_ids = fields.One2many('library.book.category', 'parent_id', string='Child Categories')

    @api.constrains('parent_id')
    def _check_hierarchy(self):
        if not self._check_recursion():
            raise models.ValidationError('Error! You can not create recursive categories')

    def create_categories(self):
        categ1 = {'name': 'Computer Science', 'description': 'Computer Science and Programming'}
        categ2 = {'name': 'High Performance Computing', 'description': 'HPC Programming and Architecture'}

        parent_category_val = {'name':'Science', 'description':'Science Related Book Category', 'child_ids': [(0,0, categ1),(0,0, categ2)]}
        record = self.env['library.book.category'].create(parent_category_val)
