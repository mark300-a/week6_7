from classes.bookstore import Bookstore

my_db = Bookstore()

"""Main loop to display options and handle user input"""
while True:
    """Display options to the user"""
    print("\nOptions:")
    print("1. Show all books")
    print("2. Add a Book")
    print("3. Record a book sale")
    print("4. Edit book details")
    print("5. Remove a book")
    print("6. Exit program")
    
    """Prompt the user to enter their choice"""
    choice = input("Enter your choice (1-6): ")
    
    """Execute corresponding method based on user choice"""
    if choice == '1':
        my_db.show_books()
    elif choice == '2':
        my_db.add_book()
    elif choice == '3':
        my_db.record_sale()
    elif choice == '4':
        my_db.edit_book()
    elif choice == '5':
        my_db.remove_book()
    elif choice == '6':
        my_db.exit_program()
    else:
        print("Invalid choice. Please enter a number from 1 to 6.")
