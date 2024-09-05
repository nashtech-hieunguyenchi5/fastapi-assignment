from fastapi import FastAPI
from routers import task, company, user, auth


app = FastAPI()

app.include_router(company.router)
app.include_router(task.router)
app.include_router(user.router)

if auth.router:
    app.include_router(auth.router)

@app.get("/", tags=["Health Check"])
async def health_check():
    return "API Service is up and running!"
