from fastapi import FastAPI

from routes import links, users

app = FastAPI()

# Routes
app.include_router(links.router)
app.include_router(users.router)


@app.get("/hello")
async def root():
    return {"message": "Hello World"}
