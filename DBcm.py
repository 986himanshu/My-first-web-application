import psycopg2 as psql  # Implemented third party module on present DB API of python

class SQLDatabase:  # This class will be context manager with start and exit defined. It will implement Setup, Do, Teardown pattern
    def __init__(self, config: dict) -> None:  # For connection to PostgreSQL
        self.configuration = config

    def __enter__(self) -> 'cursor':  # Do part: Creating cursor object that will constitute DB API
        try:
            self.conn = psql.connect(**self.configuration)
            self.cursor = self.conn.cursor()
            return self.cursor
        except mysql.connector.errors.InterfaceError as err:
            raise ConnectionError(err)
        except mysql.connector.errors.ProgrammingError as err:
            raise CredentialsError(err)
        return "error"

    def __exit__(self, exc_type, exc_value,
                 exc_trace) -> None:  # Teardown part: It will close connection and release resources safely
        self.conn.commit()
        self.cursor.close()
        self.conn.close()