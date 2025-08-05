from dotenv import load_dotenv
import os
load_dotenv()

class Config:
    SECRET_KEY=os.environ.get('SECRET_KEY')
    JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY')
    MONGO_URI="mongodb://localhost:27017/auth_system"
