from dotenv import load_dotenv
import os
from src.backend import app

if __name__ == "__main__":
    
    app.run(debug=True)
