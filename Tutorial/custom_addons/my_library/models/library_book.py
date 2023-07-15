from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools.translate import _


class LibraryBook(models.Model):
    _name = 'library.book'
    _inherit = ['base.archive']
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
            ('borrowed', 'Borrowed'),
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
    age_days = fields.Float(
        string='Days Since Release',
        compute='_compute_age',
        inverse='_inverse_age',
        search='_search_age',
        store=False,
        compute_sudo=True
    )

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
    publisher_city = fields.Char('Publisher City', related='publisher_id.city', readonly=True)

    ref_doc_id = fields.Reference(selection='_referencable_models', string='Reference Document')

    _sql_constraints = [
        ('name_uniq', 'UNIQUE (name)', 'Book Title Must be unique'),
        ('positive_page', 'CHECK(pages > 0)', 'No of Pages Must be Positive Dude!')]

    "Overriding name_get() for short title"

    def name_get(self):
        result = []
        for record in self:
            rec_name = "%s (%s)" % (record.name, record.date_release)
            result.append((record.id, rec_name))

        return result

    @api.constrains('date_release')
    def _check_release_date(self):
        for record in self:
            if record.date_release and record.date_release > fields.Date.today():
                raise models.ValidationError('Release Date Must be in the past!')

    @api.depends('date_release')
    def _compute_age(self):
        today = fields.Date.today()

        for book in self:
            if book.date_release:
                delta = today - book.date_release
                book.age_days = delta.days
            else:
                book.age_days = 0

    def _inverse_age(self):
        today = fields.Date.today()
        for book in self.filtered('date_release'):
            d = today - timedelta(days=book.age_days)
            book.date_release = d

    @api.model
    def _referencable_models(self):
        models = self.env['ir.model'].search([('field_id.name', '=', 'message_ids')])
        return [(x.model, x.name) for x in models]

    "Not Mandatory if store=True is set"

    def _search_age(self, operator, value):
        today = fields.Date.today()
        value_days = timedelta(days=value)
        value_date = today - value_days

        operator_map = {
            '>': '<', '>=': '<=',
            '<': '>', '<=': '>=',
        }
        new_op = operator_map.get(operator, operator)
        return [('date_release', new_op, value_date)]
    
    "Changing Book States"
    @api.model
    def is_allowed_transition(self, old_state, new_state):
        allowed = [('draft', 'available'),
                    ('available', 'borrowed'),
                    ('borrowed', 'available'),
                    ('available', 'lost'),
                    ('borrowed', 'lost'),
                    ('lost', 'available')]

        return (old_state, new_state) in allowed

    def change_state(self, new_state):
        for bk in self:
            if bk.is_allowed_transition(bk.state, new_state):
                bk.state = new_state
            else:
                err = _("Transitioning from %s to %s is not allowed sorry!") % (bk.state, new_state)
                raise UserError(err)

    def make_available(self):
        self.change_state('available')
    def make_borrowed(self):
        self.change_state('borrowed')
    def make_lost(self):
        self.change_state('lost')

    "Accessing Another Model By attaining Empty Recordset"
    def log_all_library_members(self):

        # Attatining the empty recordset
        library_member_model = self.env['library.member']

        all_members = library_member_model.search([])

        print("All Members: ",all_members)
        return True

    @api.model
    def books_with_multi_authors(self, all_books):
         return all_books.filter(lambda b: len(b.author_ids) > 1)

    def filter_books(self):
        rc_set = self.search([])
        res = books_with_multi_authors(rc_set)

        logger.info("Books : ", res)


    "Class Inheritance"
    class ResPartner(models.Model):
        _inherit = 'res.partner'

        published_book_ids = fields.One2many('library.book', 'publisher_id', string='Published Books')
        authored_book_ids = fields.Many2many('library.book', 'author_ids', string='Authored Books')

        count_books = fields.Integer('Number of Authored Books', compute='_compute_count_books')

        @api.depends('authored_book_ids')
        def _compute_count_books(self):
            for r in self:
                r.count_books = len(r.authored_book_ids)

    "Delegation Inheritance"
    class LibraryMember(models.Model):
        _name = 'library.member'
        _description = 'Inheriting Partner Model using partner_id field'
        _inherits = {'res.partner':'partner_id'}

        partner_id = fields.Many2one('res.partner', ondelete='cascade')

        date_start = fields.Date('Member Since')
        date_end = fields.Date('Termination Date')
        member_number = fields.Char()
        date_of_birth = fields.Date('Date of birth')

        @api.constrains('date_of_birth')
        def _check_birth_date(self):
            today = fields.Date.today()

            for r in self:
                if r.date_of_birth and r.date_of_birth >= today:
                    raise models.ValidationError('You can\'t possibly from the Future! Please check DOBirth')

    class BaseArchive(models.AbstractModel):
        _name = 'base.archive'
        _description='Adding Active Field'
        active = fields.Boolean(default=True)

        def do_archive(self):
            for r in self:
                r.active = not r.active
