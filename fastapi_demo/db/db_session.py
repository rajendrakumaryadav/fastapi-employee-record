import os

from dotenv import load_dotenv
from sqlmodel import Session, create_engine

# print(os.environ)
# load_dotenv()


def _get_engine():
    """
    Retrieves the SQLAlchemy engine, creating it if it doesn't exist.
    Raises ValueError if the connection string is invalid.
    """
    if os.environ.get("TEST", None) is not None:
        load_dotenv("test.env")
    else:
        load_dotenv()  # Load environment variables from .env file

    connection_string = os.environ.get("CONNECTION_STRING", None)
    if not connection_string:
        raise ValueError("Invalid connection string, cannot provide session")
    engine = create_engine(connection_string)
    return engine


# @contextmanager
def get_session() -> Session:
    engine = _get_engine()
    return Session(engine)
