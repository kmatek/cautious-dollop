from fastapi import FastAPI
from routes import links

app = FastAPI()
# Routes
app.include_router(links.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}
