from odoo.tests.common import TransactionCase

class TestBook(TransactionCase):
    def setUp(self, *args, **kwargs):
        result = super().setUp(*args, **kwargs)
        user_admin = self.env.ref('base.user_admin')
        self.env = self.env(user=user_admin)
        self.Book = self.env['library.book']
        self.book_ode = self.Book.create({
                'name': 'Odoo Development Essential',
                'isbn': '879-1-78439'})
        return result

    def test_create(self):
        "Test Books are active By Default"
        self.assertEqual(self.book_ode.active, true)

    def test_check_isbn(self):
        "Check Valid ISBN"
        self.assertTrue(self.book_ode._check_isbn)

