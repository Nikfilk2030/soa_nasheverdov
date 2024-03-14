import pytest
from ..database_routes import update_user


@pytest.fixture
def app():
    from .. import create_app
    app = create_app()
    return app

def test_update_user(app):
    client = app.test_client()
    response = client.put('/update')
    assert response.status_code == 200
