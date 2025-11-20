from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from fastapi.responses import RedirectResponse
from hybrid_model import get_reply
from time import time
import random
import json
import bcrypt
import os

app = FastAPI()

# CORS for Sveltekit
app.add_middleware(
  CORSMiddleware,
  allow_origins = ["http://localhost:5173"],
  allow_credentials = True,
  allow_methods = ["*"],
  allow_headers = ["*"],
)

USER_FILE = "users.json"

def load_users():
  if not os.path.exists(USER_FILE):
    return {"users": []}
  with open(USER_FILE, "r") as f:
    return json.load(f)
  
def save_users(data):
  with open(USER_FILE, "w") as f:
    json.dump(data, f, indent=4)

# Models
class SignupModel(BaseModel):
  name: str
  email: EmailStr
  password: str

class LoginModel(BaseModel):
  email: EmailStr
  password: str

class QueryModel(BaseModel):
  text: str

class ForgotPasswordModel(BaseModel):
  email: EmailStr

class VerifyOtpModel(BaseModel):
  email: EmailStr
  otp: str

class ResetPassModel(BaseModel):
  email: EmailStr
  new_password: str

@app.get("/api/hello")
def hello():
  return {"message": "Hello from FastAPI!"}

@app.get("/api/home")
def go_home():
  return RedirectResponse(url="http://localhost:5173/home")

@app.post("/api/signup")
def signup(user: SignupModel):
  data = load_users()

  # check duplicate email
  for u in data["users"]:
    if u["email"] == user.email:
      raise HTTPException(status_code=400, detail="Email already exists")
    
  # Hash password
  hashed_pw = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt()).decode()

  new_user = {
    "name": user.name,
    "email": user.email,
    "password": hashed_pw
  }

  data["users"].append(new_user)
  save_users(data)

  return {"message": "Signup successful"}

@app.post("/api/login")
def login(user: LoginModel):
  data = load_users()

  for u in data["users"]:
    if u["email"] == user.email:
      # Validate password
      if bcrypt.checkpw(user.password.encode(), u["password"].encode()):
        return {
          "message": "Login successful!",
          "name": u["name"],
          "email": u["email"]
        }
      else:
        raise HTTPException(status_code=401, detail="Invalid password")
      
  raise HTTPException(status_code=404, detail="User not found.")

otp_store = {}

@app.post("/api/forgot-password")
def forgot_password(payload: ForgotPasswordModel):
  data = load_users()
  email = payload.email

  user_exists = False
  for u in data["users"]:
    if u["email"] == email:
      user_exists = True

  if not user_exists:
    raise HTTPException(status_code=404, detail="Email not registered")
  
  #Generate OTP
  otp = str(random.randint(100000, 999999))
  expires = time() + 300 # 5 Min

  otp_store[email] = {"otp": otp, "expires": expires}

  print("OTP for", email, ":", otp)

  return {"message": "OTP sent to email"}

@app.post("/api/verify-otp")
def verify_otp(payload: VerifyOtpModel):
  email = payload.email
  otp = payload.otp

  if email not in otp_store:
    raise HTTPException(status_code=400, detail="OTP not requested")
  
  stored = otp_store[email]

  if time() > stored["expires"]:
    raise HTTPException(status_code=400, detail="OTP expired")
  
  # check
  if otp != stored["otp"]:
    raise HTTPException(status_code=400, detail="Invalid OTP")
  
  return {"message": "OTP verified"}

@app.post("/api/reset-password")
def reset_password(payload: ResetPassModel):
  data = load_users()
  email = payload.email

  for u in data["users"]:
    if u["email"] == email:
      hashed_pw = bcrypt.hashpw(payload.new_password.encode(), bcrypt.gensalt()).decode()

      u["password"] = hashed_pw
      save_users(data)

      if email in otp_store:
        del otp_store[email]

      return {"message": "Password reset successful"}
    
  raise HTTPException(status_code=404, detail="User not found")

@app.post("/api/query")
def query(model: QueryModel):
  response = get_reply(model.text)
  return {"reply": response}
