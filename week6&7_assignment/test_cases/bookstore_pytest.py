import pytest
from classes.bookstore import Bookstore

@pytest.fixture
def bookstore():
    """Fixture to create an instance of Bookstore before each test and close the database connection afterward."""
    my_db = Bookstore()
    yield my_db
    my_db.conn.close()

def test_show_books(bookstore):
    """Test the show_books method."""
    expected_books = [
        {'book_id': 1, 'book_title': 'Book1', 'book_author': 'Author1', 'quantity': 10, 'signed_edition': 'N', 'promo_price': None, 'retail_price': 20.0},
        {'book_id': 2, 'book_title': 'Book2', 'book_author': 'Author2', 'quantity': 5, 'signed_edition': 'Y', 'promo_price': 15.0, 'retail_price': 25.0},
        {'book_id': 3, 'book_title': 'Book3', 'book_author': 'Author3', 'quantity': 3, 'signed_edition': 'N', 'promo_price': None, 'retail_price': 30.0}
    ]
    bookstore.show_books()
    
def test_add_book(bookstore):
    """Test the add_book method."""
    book_data = {
        'book_title': 'NewBook',
        'book_author': 'NewAuthor',
        'quantity': 15,
        'signed_edition': 'Y',
        'promo_price': 10.0,
        'retail_price': 35.0
    }
    #Add the book
    bookstore.add_book(book_data['book_title'], book_data['book_author'], book_data['quantity'], book_data['signed_edition'], book_data['promo_price'], book_data['retail_price'])
    #retrieve the added book from the database and assert its presence
    bookstore.c.execute('SELECT * FROM Books WHERE book_title = %s', (book_data['book_title'],))
    added_book = bookstore.c.fetchone()
    assert added_book is not None
    
def test_record_sale(bookstore):
    """Test the record_sale method."""
    book_id = 1
    quantity_sold = 2
    #Record the sale
    bookstore.record_sale(book_id, quantity_sold)
    #retrieve the updated quantity from the database and assert its correctness
    bookstore.c.execute('SELECT quantity FROM Books WHERE book_id = %s', (book_id,))
    updated_quantity = bookstore.c.fetchone()['quantity']
    expected_quantity = 8  # 10 - 2 = 8
    assert updated_quantity == expected_quantity

def test_edit_book(bookstore):
    """Test the edit_book method."""
    book_id = 1
    field = 'book_title'
    new_value = 'Updated Title'
    bookstore.edit_book(book_id, field, new_value)
    #Retrieve the updated book details and assert the correctness of the updated field
    bookstore.c.execute('SELECT book_title FROM Books WHERE book_id = %s', (book_id,))
    updated_title = bookstore.c.fetchone()['book_title']
    assert updated_title == new_value

def test_remove_book(bookstore):
    """Test the remove_book method."""
    book_id = 1
    bookstore.remove_book(book_id)
    """Check if the book is removed from the database"""
    bookstore.c.execute('SELECT * FROM Books WHERE book_id = %s', (book_id,))
    removed_book = bookstore.c.fetchone()
    assert removed_book is None

def test_exit_program(bookstore):
    """Test the exit_program method."""
    with pytest.raises(SystemExit):
        bookstore.exit_program()

    """Check if the database connection is closed"""
    assert bookstore.conn.closed
