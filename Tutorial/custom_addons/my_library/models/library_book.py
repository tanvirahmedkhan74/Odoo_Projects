from odoo import models, fields


class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'
    _rec_name = 'short_name'
    _order = 'date_release desc, name'

    name = fields.Char('Title', required=True)
    short_name = fields.Char('Short Title', translate=True, index=True,
                             help='Short Representation of the book')

    notes = fields.Text('Internal Notes')
    state = fields.Selection(
        [
            ('draft', 'Not Available'),
            ('available', 'Available'),
            ('lost', 'Lost')
        ],
        'State', default='draft'
    )
    description = fields.Html('Description', sanitize=True, strip_style=False)
    cover = fields.Binary('Book Cover')

    cost_price = fields.Float('Book Cost', digits='Book Price')
    currency_id = fields.Many2one('res.currency', string='Currency')
    retail_price = fields.Monetary('Retail Price', currency_field='currency_id')

    out_of_print = fields.Boolean('Out of Print?')
    date_release = fields.Date('Release Date')
    date_updated = fields.Datetime('Last Updated')

    pages = fields.Integer('Number of Pages',
                           states={'lost': [('readonly', True)]},
                           help='Total Book Page Count', company_dependent=False
                           )

    reader_rating = fields.Float(
        'Reader Average Rating',
        digits=(14, 4)
    )

    category_id = fields.Many2one('library.book.category', string='Category')
    publisher_id = fields.Many2one('res.partner', string='Publisher', ondelete='set null')
    author_ids = fields.Many2many('res.partner', string='Authors')

    "Overriding name_get() for short title"

    def name_get(self):
        result = []
        for record in self:
            rec_name = "%s (%s)" % (record.name, record.date_release)
            result.append((record.id, rec_name))

        return result

    class ResPartner(models.Model):
        _inherit = 'res.partner'

        published_book_ids = fields.One2many('library.book', 'publisher_id', string='Published Books')
        authored_book_ids = fields.Many2many('library.book', 'author_ids', string='Authored Books')
