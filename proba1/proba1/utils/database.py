from .database_connection import DatabaseConnection
from typing import List, Dict, Union

# Global variables
Book = Dict[str, Union[str, int]]
DB_HOST = "data.db"

class Database:
    """A class used to interact with the database of the library.
    ...
    Attributes
    ----------
    DB_HOST : str
        The database host (default "db.host").
    
    """
    DB_HOST = "data.db"

    @classmethod
    def create_book_table(cls) -> None:
        """Creates a book table if it doesn't already exist."""

        with DatabaseConnection(cls.DB_HOST) as connection:
            cursor = connection.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                author_id INTEGER,
                year INTEGER,
                available INTEGER,
                FOREIGN KEY (author_id) REFERENCES author(id)
            )
        """)


    @classmethod
    def add_book(cls, name: str, author: str, year: int) -> None:
        """Adds a book to the books table and the author to the author table if not already present.

        Parameters
        ----------
        name : str
            The name of the book to be added.
        author : str
            The name of the author of the book.
        year : int
            The year of publishing the book.
        """

        with DatabaseConnection(cls.DB_HOST) as connection:
            cursor = connection.cursor()

            # Check if the author already exists in the author table
            cursor.execute("SELECT id FROM author WHERE id = ?", (author,))
            author_row = cursor.fetchone()
            # If the author doesn't exist, insert them into the author table
            if author_row is None:
                cursor.execute("INSERT INTO author (id) VALUES (?)", (author,))
                author_id = cursor.lastrowid
            else:
                author_id = author_row[0]

            # Insert the book into the books table
            cursor.execute("INSERT INTO books (name, author, year, available) VALUES (?, ?, ?, 1)",
                        (name, author_id, year))

    @classmethod
    def get_all_books(cls) -> List[Book]:
        """Gets all the books of the library."""

        with DatabaseConnection(cls.DB_HOST) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM books")
            books = [{"name": row[0], "author": row[1], "year": row[2], "available": row[3]} for row in cursor.fetchall()]

        return books

    @classmethod
    def book_not_available(cls, name: str) -> None:
        """Marks a book as not available in the library.

        Parameters
        ----------
        name : str
            The name of the book which is no longer available in the library.
        """
        with DatabaseConnection(cls.DB_HOST) as connection:
            cursor = connection.cursor()
            cursor.execute("UPDATE books SET available=? WHERE name=?", (0, name))

    @classmethod
    def book_available(cls, name: str) -> None:
        """Marks a book as available in the library.

        Parameters
        ----------
        name : str
            The name of the book which is available in the library.
        """
        with DatabaseConnection(cls.DB_HOST) as connection:
            cursor = connection.cursor()
            cursor.execute("UPDATE books SET available=? WHERE name=?", (1, name))
    @classmethod
    def delete_book(cls, name: str) -> None:
        """Deletes a book.

        Parameters
        ----------
        name : str
            The name of the book to be deleted.
        """
        with DatabaseConnection(cls.DB_HOST) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM books WHERE name=?", (name,))
            book = cursor.fetchone()

            if book:
                cursor.execute("DELETE FROM books WHERE name=?", (name,))
                print(f"The book '{name}' has been deleted.")
            else:
                print(f"The book '{name}' does not exist in the database.")
                
    @classmethod
    def delete_all_books(cls) -> None:
        """
        Deletes all books from the database.

        Parameters:
        - cls: The class representing the database.

        Returns:
        - None
        """

        with DatabaseConnection(cls.DB_HOST) as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM books")
            print("All books have been deleted from the database.")

    @classmethod
    def sort_books(cls) -> None:
        """Sorts books by year of publishing and prints them."""

        with DatabaseConnection(cls.DB_HOST) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT name, author, year FROM books ORDER BY year")

            books = cursor.fetchall()

            sorted_books = [(name, author, year) for name, author, year in books]

        for book in sorted_books:
            name, author, year = book
            print(f"Book: {name}, Author: {author}, Year: {year}")

    @classmethod
    def search_book(cls, name: str) -> None:
        """Search for a book in a library.

        Parameters
        ----------
        name : str
            The name of the book to search for.
        """
        with DatabaseConnection(cls.DB_HOST) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM books WHERE name=?", (name,))
            results = cursor.fetchall()

        if results:
            print("Matching books found:")
            for result in results:
                print(result)  # Adjust this line to print specific book details
        else:
            print("No books found matching the search query.")

    @classmethod
    def create_person_table(cls) -> None:
        """Creates a PERSON table if it doesn't already exist."""
        with DatabaseConnection(cls.DB_HOST) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS person (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    person_type TEXT NOT NULL
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS author (
                    id INTEGER PRIMARY KEY,
                    FOREIGN KEY (id) REFERENCES person(author_id)
                )
            """)
            #cursor.execute(f"DROP TABLE IF EXISTS reader")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reader(
                    id INTEGER PRIMARY KEY,
                    active TEXT,
                    book TEXT,
                    FOREIGN KEY (id) REFERENCES person(reader_id)
                )
            """)

    @classmethod
    def add_author(cls, name: str) -> None:
        """Adds an author to the person and author tables if not already present.

        Parameters
        ----------
        name : str
            The name of the author.

        """

        with DatabaseConnection(cls.DB_HOST) as connection:
            cursor = connection.cursor()

            # Check if the author already exists in the person table
            cursor.execute("SELECT id FROM person WHERE name = ? AND person_type = 'AUTHOR'", (name,))
            author_row = cursor.fetchone()
            # If the author doesn't exist, insert them into the person and author tables
            if author_row is None:
                # Insert the author into the person table
                cursor.execute("INSERT INTO person (name, person_type) VALUES (?, 'AUTHOR')", (name,))

                # Retrieve the author's primary key
                author_id = cursor.lastrowid

                # Insert the author into the author table
                cursor.execute("INSERT INTO author (id) VALUES (?)", (author_id))
            else:
                author_id = author_row[0]

    @classmethod
    def add_reader(cls, name: str, active: str) -> None:
        """Adds a reader to the person and reader tables.

        Parameters
        ----------
        name : str
            The name of the reader.
        active : str
            YES or NO.
        preferred_genre : str
            The preferred genre of the reader.

        """
        with DatabaseConnection(cls.DB_HOST) as connection:
            cursor = connection.cursor()
            
            # Insert the reader into the person table
            cursor.execute("INSERT INTO person (name, person_type) VALUES (?, 'READER')", (name,))

            # Retrieve the reader's primary key
            reader_id = cursor.lastrowid

            # Insert the reader into the reader table
            cursor.execute("INSERT INTO reader (id, active, book_id) VALUES (?, ?,0)", (reader_id, active))


    @classmethod
    def get_all_readers(cls) -> List[Book]:
        """Gets all readers."""

        with DatabaseConnection(cls.DB_HOST) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM reader")
            results = cursor.fetchall()
        for result in results:
                print(result)  # Adjust this line to print specific

    @classmethod
    def get_all_authors(cls) -> List[Book]:
        """Gets all readers."""

        with DatabaseConnection(cls.DB_HOST) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM author")
            results = cursor.fetchall()
        for result in results:
                print(result)  # Adjust this line to print specific

    @classmethod
    def delete_all(cls) -> None:
        """
        Deletes all from the database.

        Parameters:
        - cls: The class representing the database.

        Returns:
        - None
        """

        with DatabaseConnection(cls.DB_HOST) as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM books")
            cursor.execute("DELETE FROM author")
            cursor.execute("DELETE FROM reader")
            cursor.execute("DELETE FROM person")
            print("All data has been deleted from the database.")

    @classmethod
    def loan_book(cls, reader_id: int, book: str) -> None:
        """Associates a book with a reader and marks the book as not available.

        Parameters
        ----------
        reader_id : int
            The ID of the reader.
        book : int
            The name of the book to be loaned.

        """
        with DatabaseConnection(cls.DB_HOST) as connection:
            cursor = connection.cursor()

            # Update the reader's book_id with the loaned book
            cursor.execute("UPDATE reader SET book = ? WHERE id = ?", (book, reader_id))

            # Mark the book as not available
            cursor.execute("UPDATE books SET available=? WHERE name=?", (0, book))
