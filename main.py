from fastapi import FastAPI, Query, Body
from app.routes import product_routes
from app.routes import user_routes
from app.agents.supervisor import SupervisorLLM



app = FastAPI()

# Initialize supervisor
supervisor = SupervisorLLM()

@app.post("/chat")
async def chat_with_bot_post(payload: dict = Body(...)):
    """
    Example POST body:
    {
        "query": "show all products"
    }
    """
    query = payload.get("query", "")
    result = supervisor.handle_query(query)
    return {"result": result}

app.include_router(product_routes.router)
app.include_router(user_routes.router)

# app.include_router(user_routes.router)

# @app.get("/")
# async def root():
#     return {"message": "Welcome to the E-commerce API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
