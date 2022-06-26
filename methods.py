from config import DATABASE_URI
from crud import get_session_engine

def restart_session():
    s, _ = get_session_engine(DATABASE_URI)


