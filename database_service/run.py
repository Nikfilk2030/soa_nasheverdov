from app import create_app
from app.database_utils import initialize_db

app = create_app()
initialize_db(app)

if __name__ == "__main__":
    app.run(debug=True)
