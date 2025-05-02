class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://flask_user:flaskpass@mysql:3306/desercion_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "super-secret-key"  # puedes cambiar esto por algo más seguro
