from dotenv import load_dotenv
import os

def Load_Environment_Variables(dotenv_path=".env"):
    load_dotenv(dotenv_path)
    return dict(os.environ)
