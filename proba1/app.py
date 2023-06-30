from utils.database import Database

class Library:
    """A class that creates a console User Interface for interacting with a library."""
    
    USER_CHOICE = """
    Enter:
    -  1 to add a new book
    -  1.1 to add a new author
    -  1.2 to add a new reader
    -  2 to list all books in the library
    -  2.1 to list all authors
    -  2.2 to list all readers
    -  3 to mark a book as not available
    -  3.1 to mark a book as available
    -  4 to delete a book
    -  4.1 to delete all data
    -  5 to sort books by year
    -  6 to search a book
    -  7 to loan a book
    -  0 to quit
    ----------------------------------------
    Your choice: """

    @classmethod
    def menu(cls):
        """Function that allows users to interact with the library through the console."""
        while True:
            user_input = input(cls.USER_CHOICE)
            if user_input == '1.1':
                cls.add_author()
            elif user_input== '1.2':
                cls.add_reader()
            elif user_input == '1':
                cls.add_book()
            elif user_input == '2':
                cls.list_books()
            elif user_input == '2.1':
                cls.show_author()
            elif user_input == '2.2':
                cls.show_reader()
            elif user_input == '3':
                cls.mark_not_available()
            elif user_input == '3.1':
                cls.mark_available()
            elif user_input == '4':
                cls.delete_book()
            elif user_input == '4.1':
                cls.delete_all()
            elif user_input == '5':
                cls.sort_books()
            elif user_input == '6':
                cls.search_books()
            elif user_input == '7':
                cls.loan_book()
            elif user_input == '0':
                break
            else:
                print("Unknown command. Please try again.")

    @classmethod
    def add_book(cls):
        """
        This function allows users to add a new book to the library.

        Parameters:
        - cls: The class representing the library.

        Returns:
        - None
        """
        name = input("Please enter the name of the new book: ")
        author = input("Please enter the name of the author: ")
        year = input("Please enter the year of publication: ")
        try:
            year=int(year)  # Check if year can be converted to an integer
        except ValueError:
            # Exception handling code for invalid year input
            print("Invalid input for the year of publication. Please enter a valid integer.")
            return
        
        Database.add_book(name, author, year)


    @classmethod
    def list_books(cls):
        """
        This function displays all the books currently available in the library.

        Parameters:
        - cls: The class representing the library.

        Returns:
        - None
        """
        # Retrieve all books from the database
        books = Database.get_all_books()
        # Iterate over each book and display its details
        for book in books:
            availability = "Available" if book["available"] else "Not Available"
            print(f"Title: {book['name']}")
            print(f"Author: {book['author']}")
            print(f"Year: {book['year']}")
            print(f"Availability: {availability}")
            print("------------------------")

    @classmethod
    def mark_available(cls):
        """
        This function allows the user to mark a book as available in the library.

        Parameters:
        - cls: The class representing the library.

        Returns:
        - None
        """
        name = input("Enter the name of the book to mark as available: ")
        # Mark the book as not available in the database
        Database.book_available(name)

    @classmethod
    def mark_not_available(cls):
        """
        This function allows the user to mark a book as not available in the library.

        Parameters:
        - cls: The class representing the library.

        Returns:
        - None
        """
        name = input("Enter the name of the book to mark as not available: ")
        # Mark the book as not available in the database
        Database.book_not_available(name)

    @classmethod
    def delete_book(cls):
        """
        This function allows the user to delete a book from the library.

        Parameters:
        - cls: The class representing the library.

        Returns:
        - None
        """
        name = input("Enter the name of the book to delete: ")
        Database.delete_book(name)

    @classmethod
    def sort_books(cls) -> None:
        """
        This function sorts the books in the library by their year of publishing and prints them.

        Parameters:
        - cls: The class representing the library.

        Returns:
        - None
        """
        Database.sort_books()

    @classmethod
    def search_books(cls):
        """This function allows users to search for books in the library by their name.

        Parameters:
        - cls: The class representing the library.

        Returns:
        - None
        """
        name = input("Enter the name of the book to search for: ")
        Database.search_book(name)

    @classmethod
    def delete_all(cls):
        """This function deletes all 
        from library.

        Parameters:
        - cls: The class representing the library.

        Returns:
        - None
        """
        Database.delete_all()

    @classmethod
    def add_reader(cls):
        """
        This function allows users to add a new reader to the library.

        Parameters:
        - cls: The class representing the library.

        Returns:
        - None
        """
        name = input("Please enter the name of the reader: ")
        active = input("Please enter YES or NO (active or not): ")
        try:
            Database.add_reader(name, active)
        except Exception as e:
            # Exception handling code for other exceptions
            print("An exception occurred while inserting the book:", str(e))

    @classmethod
    def show_reader(cls):
        """
        This function allows users to show all readers.

        Parameters:
        - cls: The class representing the library.

        Returns:
        - None
        """        
        Database.get_all_readers()
   
    @classmethod
    def add_author(cls):
        """
        This function allows users to add a new author to the library.

        Parameters:
        - cls: The class representing the library.

        Returns:
        - None
        """
        name = input("Please enter the name of the author: ")
        try:
            Database.add_author(name)
        except Exception as e:
            # Exception handling code for other exceptions
            print("An exception occurred while inserting the book:", str(e))

    @classmethod
    def show_author(cls):
        """
        This function allows users to show all authors.

        Parameters:
        - cls: The class representing the library.

        Returns:
        - None
        """        
        Database.get_all_authors()

    @classmethod
    def loan_book(cls):
        """This function allows users to loan book to specific reader.

        Parameters:
        - cls: The class representing the library.

        Returns:
        - None
        """
        reader_id = input("Enter the number of reader's card: ")   
        book_id = input("Enter the ID of book to loan: ")   
           
        Database.loan_book(reader_id,book_id)  
    
if __name__ == "__main__":
    # Create the book table in the database
    Database.create_person_table()
    Database.create_book_table()

    # Display the library menu
    Library.menu()
