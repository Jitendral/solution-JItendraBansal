from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from database import get_db_connection
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from psycopg2 import sql
from passlib.context import CryptContext

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to specific frontend domains for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# User model
class User(BaseModel):
    username: str
    password: str

# Root route for testing
@app.get("/")
def read_root():
    return {"message": "Backend is running successfully!"}

# Hash password function
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Verify password function
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Create User
@app.post("/create_user")
async def create_user(user: User):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        hashed_password = hash_password(user.password)
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (user.username, hashed_password))
        conn.commit()
        return {"message": "User created successfully!"}
    except psycopg2.Error as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Database error: {e.pgerror}")
    finally:
        cur.close()
        conn.close()

# Login User
@app.post("/login")
async def login(user: User):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT password FROM users WHERE username = %s", (user.username,))
        result = cur.fetchone()

        if result and verify_password(user.password, result[0]):
            return {"message": "Login successful!"}
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")
    except psycopg2.Error as e:
        raise HTTPException(status_code=400, detail=f"Database error: {e.pgerror}")
    finally:
        cur.close()
        conn.close()

# Database Initialization
@app.on_event("startup")
async def startup_event():
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)
        conn.commit()
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=f"Database initialization failed: {e.pgerror}")
    finally:
        cur.close()
        conn.close()
