from odoo import models, fields, api
from odoo.exceptions import ValidationError


class BookCategory(models.Model):
    _name = 'library.book.category'
    _description = 'Book Categories'
    _parent_store = True
    _parent_name = "parent_id"
    parent_path = fields.Char(index=True)

    name = fields.Char('Category')

    parent_id = fields.Many2one('library.book.category', string='Parent Category', ondelete='restrict',
                                index=True)
    child_ids = fields.One2many('library.book.category', 'parent_id', string='Child Categories')

    @api.constrains('parent_id')
    def _check_hierarchy(self):
        if not self._check_recursion():
            raise models.ValidationError('Error! You can not create recursive categories')
