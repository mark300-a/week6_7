import unittest
from classes.bookstore import Bookstore

class TestBookstore(unittest.TestCase):
    
    def setUp(self):
        self.my_db = Bookstore()

    def tearDown(self):
        self.my_db.conn.close()

    def test_show_books(self):
        """Adding test books"""
        expected_books = [
            {'book_id': 1, 'book_title': 'Book1', 'book_author': 'Author1', 'quantity': 10, 'signed_edition': 'N', 'promo_price': None, 'retail_price': 20.0},
            {'book_id': 2, 'book_title': 'Book2', 'book_author': 'Author2', 'quantity': 5, 'signed_edition': 'Y', 'promo_price': 15.0, 'retail_price': 25.0},
            {'book_id': 3, 'book_title': 'Book3', 'book_author': 'Author3', 'quantity': 3, 'signed_edition': 'N', 'promo_price': None, 'retail_price': 30.0}
        ]
        self.my_db.show_books()

    def test_add_book(self):
        """Test add_book method"""
        book_data = {
            'book_title': 'NewBook',
            'book_author': 'NewAuthor',
            'quantity': 15,
            'signed_edition': 'Y',
            'promo_price': 10.0,
            'retail_price': 35.0
        }
        """Add the book"""
        self.my_db.add_book(
        book_data['book_title'],
        book_data['book_author'],
        book_data['quantity'],
        book_data['signed_edition'],
        book_data['promo_price'],
        book_data['retail_price']
        )

    def test_record_sale(self):
        """Test record_sale method"""
        book_id = 1
        quantity_sold = 2
        #Record the sale
        self.my_db.record_sale(book_id, quantity_sold)
        #Retrieve the updated quantity from the database and assert its correctness
        self.my_db.c.execute('SELECT quantity FROM Books WHERE book_id = %s', (book_id,))
        updated_quantity = self.my_db.c.fetchone()['quantity']
        expected_quantity = 8  # Assuming 10 - 2 = 8
        self.assertEqual(updated_quantity, expected_quantity)

    def test_edit_book(self):
        """Test edit_book method"""
        book_id = 1
        field = 'book_title'
        new_value = 'Updated Title'
        self.my_db.edit_book(book_id, field, new_value)
        #Retrieve the updated book details and assert the correctness of the updated field
        self.my_db.c.execute('SELECT book_title FROM Books WHERE book_id = %s', (book_id,))
        updated_title = self.my_db.c.fetchone()['book_title']
        self.assertEqual(updated_title, new_value)

    def test_remove_book(self):
        """Test remove_book method"""
        book_id = 1
        self.my_db.remove_book(book_id)
        #Check if the book is removed from the database
        self.my_db.c.execute('SELECT * FROM Books WHERE book_id = %s', (book_id,))
        removed_book = self.my_db.c.fetchone()
        self.assertIsNone(removed_book)

    def test_exit_program(self):
        """Test exit_program method"""
        with self.assertRaises(SystemExit):
            self.my_db.exit_program()

        """Check if the database connection is closed"""
        self.assertTrue(self.my_db.conn.closed)


