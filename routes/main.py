from fastapi import APIRouter

router = APIRouter(prefix="/v1")

@router.get("/greet/{name}")
async def hello(name: str):
    return {"name": name, "message": "hello, world!"}