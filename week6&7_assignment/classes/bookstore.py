import pymysql

class Bookstore:
    
    """A class representing a bookstore with methods to manage books in the database.

    Attributes:
        conn (pymysql.connections.Connection): Represents the connection to the database.
        c (pymysql.cursors.Cursor): Represents the cursor object to execute SQL queries"""
     
    def __init__(self):
        """Establishing connection to the database"""
        self.conn = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            database='bookstore',
            cursorclass=pymysql.cursors.DictCursor
        )
        self.c = self.conn.cursor()

    def show_books(self):
        """Retrieving and displaying all books from the database"""
        self.c.execute('SELECT * FROM Books')
        rows = self.c.fetchall()
        if not rows:
            print("No books found.")
        else:
            for row in rows:
                print("Book ID:", row['book_id'])
                print("Book Title:", row['book_title'])
                print("Book Author:", row['book_author'])
                print("Quantity:", row['quantity'])
                print("Signed Edition:", row['signed_edition'])
                print("Promotional Price:", row['promo_price'])
                print("Retail Price:", row['retail_price'])
                print()

    def add_book(self):
        """Adding a new book to the database"""
        while True:
            book_title = input("Enter book title: ")
            if book_title:
                break
            else:
                print("Please enter a valid book title.")
        while True:
            book_author = input("Enter book author: ")
            if book_author:
                break
            else:
                print("Please enter a valid book author.")
        while True:
            try:
                quantity = int(input("Enter quantity on hand: "))
                break
            except ValueError:
                print("Please enter a valid integer for quantity.")
        while True:
            signed_edition = input("Is it a signed edition? (Y/N): ").upper()
            if signed_edition in ('Y', 'N', ''):
                break
            else:
                print("Please enter 'Y', 'N', or leave it blank.")
        promo_price = input("Enter promotional price (optional): ")
        if promo_price:
            promo_price = float(promo_price)
        while True:
            try:
                retail_price = float(input("Enter retail price: "))
                break
            except ValueError:
                print("Please enter a valid floating-point number for retail price.")
        self.c.execute('''INSERT INTO Books (book_title, book_author, quantity, signed_edition, promo_price, retail_price) 
                        VALUES (%s, %s, %s, %s, %s, %s)''', (book_title, book_author, quantity, signed_edition, promo_price, retail_price))
        self.conn.commit()
        print("Book added successfully!")

    def record_sale(self):
        """Recording a sale of a book"""
        while True:
            try:
                book_id = int(input("Enter the ID of the book sold: "))
                break
            except ValueError:
                print("Please enter a valid integer for book ID.")
        while True:
            try:
                quantity_sold = int(input("Enter the quantity sold: "))
                break
            except ValueError:
                print("Please enter a valid integer for quantity sold.")

        self.c.execute('SELECT quantity FROM Books WHERE book_id = %s', (book_id,))
        current_quantity = self.c.fetchone()['quantity']
        if current_quantity >= quantity_sold:
            new_quantity = current_quantity - quantity_sold
            self.c.execute('UPDATE Books SET quantity = %s WHERE book_id = %s', (new_quantity, book_id))
            self.conn.commit()
            print("Sale recorded successfully!")
        else:
            print("Not enough quantity on hand to fulfill the sale.")

    def edit_book(self):
        """Editing details of a book
        Arguments:
            book_id (int): The ID of the book to be edited.
            field (str): The field to be edited. It can be one of 'book_title', 'book_author', 'quantity', 
            'signed_edition', 'promo_price', or 'retail_price'."""
        
        while True:
            try:
                book_id = int(input("Enter the ID of the book you want to edit: "))
                break
            except ValueError:
                print("Please enter a valid integer for book ID.")
        field = input("Enter the field you want to edit (book_title/book_author/quantity/signed_edition/promo_price/retail_price): ").strip()
        if field == "quantity":
            while True:
                try:
                    new_value = int(input("Enter new quantity: "))
                    break
                except ValueError:
                    print("Please enter a valid integer for quantity.")
        elif field == "promo_price" or field == "retail_price":
            while True:
                try:
                    new_value = float(input(f"Enter new {field}: "))
                    break
                except ValueError:
                    print(f"Please enter a valid floating-point number for {field}.")
        elif field == "signed_edition":
            while True:
                new_value = input("Is it a signed edition? (Y/N): ").upper()
                if new_value in ('Y', 'N', ''):
                    break
                else:
                    print("Please enter 'Y', 'N', or leave it blank.")
        else:
            new_value = input(f"Enter new {field}: ")
        self.c.execute(f'UPDATE Books SET {field} = %s WHERE book_id = %s', (new_value, book_id))
        self.conn.commit()
        print("Book details updated successfully!")

    def remove_book(self):
        """Removing a book from the database
         Arguments:
            book_id (int): The ID of the book to be removed."""
        while True:
            try:
                book_id = int(input("Enter the ID of the book you want to remove: "))
                break
            except ValueError:
                print("Please enter a valid integer for book ID.")
        confirm = input("Are you sure you want to delete this book? (Y/N): ").upper()
        if confirm == 'Y':
            self.c.execute('DELETE FROM Books WHERE book_id = %s', (book_id,))
            self.conn.commit()
            print("Book removed successfully!")
        else:
            print("Removal canceled.")

    def exit_program(self):
        """Exiting the program"""
        print("Exiting program.")
        self.conn.close()
        exit()

