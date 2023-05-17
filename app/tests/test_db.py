from ..db.database import client


def test_db_connection():
    db_client = client
    assert db_client.server_info() is not None
