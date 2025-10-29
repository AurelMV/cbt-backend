from fastapi import FastAPI
from api.v1.routes import auth, users

app = FastAPI(title="CBT Backend API", version="1.0.0")


app.include_router(auth.router)
app.include_router(users.router)
