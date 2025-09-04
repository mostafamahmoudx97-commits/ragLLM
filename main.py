from fastapi import FastAPI
app = FastAPI()

@app.get("/welcome")
def start():
    return {
    "message": "Hello, World!"
}