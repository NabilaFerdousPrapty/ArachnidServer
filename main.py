from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from appwrite.client import Client
from appwrite.services.users import Users
from appwrite.services.databases import Databases
from appwrite.id import ID
from dotenv import load_dotenv
import os
from pydantic import BaseModel
import logging
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

logging.basicConfig(level=logging.INFO)

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

# Define the Pydantic model for login data

class LoginRequest(BaseModel):
    email: str
    password: str


# Signup endpoint
@app.post("/signup")
async def signup(user: SignupRequest):
    try:
        # Save user data to Appwrite database
        document = databases.create_document(
            DATABASE_ID,
            COLLECTION_ID,
            ID.unique(),  # Auto-generate a unique document ID
            {
                "email": user.email,
                "password": user.password,  # Note: Never store plain-text passwords in production!
                "name": user.name,
            }
        )
         
        # Return a success message with the created document
        return {"message": "User created successfully", "user": document}
    
    except Exception as e:
        print("Error creating document:", str(e))  # Log the error
        raise HTTPException(status_code=400, detail=str(e))
    

# @app.post("/login")
# async def login(request: LoginRequest):
#     logging.info(f"Login attempt with email: {request.email}")

#     try:
#         # Simulating Appwrite session creation (Replace with actual Appwrite code)
#         session = users.create_session(request.email, request.password)
#         logging.info(f"Session created: {session}")

#         return {"message": "Login successful", "session": session}

#     except Exception as e:
#         logging.error(f"Login failed: {e}")
#         raise HTTPException(status_code=401, detail="Invalid credentials")
@app.post("/login")
async def login(email: str, password: str):
    try:
        # Create a session (login) in Appwrite
        session = users.create_session(email=email, password=password)
        return {"message": "Login successful", "session": session}
    except Exception as e:
        print("Login failed:", str(e))  # Log the error for debugging
        raise HTTPException(status_code=401, detail="Invalid credentials")
    

# Check if a user exists
       
@app.get("/check-user/{email}")
async def check_user(email: str):
    user = users.get(email)  # Fetch user from database
    if user:
        return {"message": "User exists", "stored_password": user["password"]}
    return {"message": "User not found"}

# Get all users from the database
@app.get("/users")
async def get_users():
    try:
        # Fetch all documents from the database
        documents = databases.list_documents(DATABASE_ID, COLLECTION_ID)
        return {"users": documents["documents"]}
    except Exception as e:
        print("Error fetching documents:", str(e))  # Log the error for debugging
        raise HTTPException(status_code=400, detail=str(e))
    
# Get a user by ID
@app.get("/user/{document_id}")
async def get_user(document_id: str):
    try:
        # Fetch a document by ID
        document = databases.get_document(DATABASE_ID, COLLECTION_ID, document_id)
        return {"user": document}
    except Exception as e:
        print("Error fetching document:", str(e))

        # Check if the document was not found
        if "not found" in str(e):
            raise HTTPException(status_code=404, detail="Document not found")
        raise HTTPException(status_code=400, detail=str(e))
    
# Update a user by ID
@app.put("/user/{document_id}")
async def update_user(document_id: str, name: str):
    try:
        # Update the document
        document = databases.update_document(
            DATABASE_ID,
            COLLECTION_ID,
            document_id,
            {"name": name}
        )
        return {"message": "User updated successfully", "user": document}
    except Exception as e:
        print("Error updating document:", str(e))
        raise HTTPException(status_code=400, detail=str(e))
    
    
# Delete a user by ID
@app.delete("/user/{document_id}")
async def delete_user(document_id: str):
    try:
        # Delete the document
        databases.delete_document(DATABASE_ID, COLLECTION_ID, document_id)
        return {"message": "User deleted successfully"}
    except Exception as e:
        print("Error deleting document:", str(e))
        raise HTTPException(status_code=400, detail=str(e))
    

# update user by ID
@app.put("/user/{document_id}")
async def update_user(document_id: str, name: str):
    try:
        # Update the document
        document = databases.update_document(
            DATABASE_ID,
            COLLECTION_ID,
            document_id,
            {"name": name}
        )
        return {"message": "User updated successfully", "user": document}
    except Exception as e:
        print("Error updating document:", str(e))
        raise HTTPException(status_code=400, detail=str(e))
    


# Run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)