from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from appwrite.client import Client
from appwrite.services.users import Users
from appwrite.services.databases import Databases
from appwrite.id import ID
from dotenv import load_dotenv
import os
from pydantic import BaseModel
# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (update this in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Appwrite client
client = Client()
client.set_endpoint(os.getenv("APPWRITE_ENDPOINT", "https://cloud.appwrite.io/v1"))
client.set_project(os.getenv("PROJECT_ID"))
client.set_key(os.getenv("API_KEY_SECRET"))

# Initialize Appwrite services
users = Users(client)
databases = Databases(client)

# Database and collection IDs
DATABASE_ID = os.getenv("DATABASE_ID")
COLLECTION_ID = os.getenv("COLLECTION_ID")
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI backend!"}

# Define the Pydantic model for signup data
class SignupRequest(BaseModel):
    email: str
    password: str
    name: str

@app.post("/signup")
async def signup(user: SignupRequest):
    try:
        # Create user in the backend (Appwrite or other service)
        user_data = {
            "email": user.email,
            "password": user.password,
            "name": user.name
        }

        # Simulate saving the user data (you can replace this with actual DB operations)
        # e.g., Create user in database, authenticate with Appwrite, etc.
        
        # Return a success message
        return {"message": "User created successfully", "user": user_data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
# Login endpoint
@app.post("/login")
async def login(email: str, password: str):
    try:
        # Create a session (login) in Appwrite
        session = users.create_session(email, password)
        return {"message": "Login successful", "session": session}
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid credentials")

# Run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)