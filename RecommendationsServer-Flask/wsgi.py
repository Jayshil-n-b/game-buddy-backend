from src.app import app
from dotenv import load_dotenv
import os
import datetime
from flask_jwt_extended import JWTManager

load_dotenv()

jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False


if __name__ == "__main__":
    app.run(debug=True)
