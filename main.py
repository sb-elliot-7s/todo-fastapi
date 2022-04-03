from fastapi import FastAPI

from user.controllers import user_router
from todo.controllers import todo_router

app = FastAPI(title='Todo app')

app.include_router(user_router)
app.include_router(todo_router)
