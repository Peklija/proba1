import sqlite3

class DatabaseConnection:
    """Database connection context manager"""

    def __init__(self, host):
        """
        Parameters
        ----------
        connection : Connection
        host : str
            The database host name.
        """

        self.connection = None
        self.host = host

    def __enter__(self) -> sqlite3.Connection:
        """Opens context resources."""

        self.connection = sqlite3.connect(self.host)
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Closes context resources."""
        if exc_type or exc_val or exc_tb:
            self.connection.close()
        else:
            self.connection.commit()
            self.connection.close()