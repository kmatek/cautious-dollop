from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from app.config import settings
from routes import links, users


app = FastAPI()

# Routes
app.include_router(links.router)
app.include_router(users.router)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Pagination
add_pagination(app)


@app.get("/")
async def root():
    return {"message": "Hello World"}
