from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import List, Optional
from datetime import datetime
import uuid

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# In-memory storage for todos
todos: List[dict] = []


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Main page displaying the todo list"""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "todos": todos
    })


@app.post("/todos", response_class=HTMLResponse)
async def add_todo(request: Request, task: str = Form(...)):
    """Add a new todo item"""
    new_todo = {
        "id": str(uuid.uuid4()),
        "task": task,
        "completed": False,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    todos.append(new_todo)
    # Return just the new todo item HTML to swap in
    return templates.TemplateResponse("todo_item.html", {
        "request": request,
        "todo": new_todo
    })


@app.delete("/todos/{todo_id}", response_class=HTMLResponse)
async def delete_todo(request: Request, todo_id: str):
    """Delete a todo item"""
    global todos
    todos = [todo for todo in todos if todo["id"] != todo_id]
    return ""  # Empty response removes the element


@app.put("/todos/{todo_id}/toggle", response_class=HTMLResponse)
async def toggle_todo(request: Request, todo_id: str):
    """Toggle completion status of a todo"""
    for todo in todos:
        if todo["id"] == todo_id:
            todo["completed"] = not todo["completed"]
            return templates.TemplateResponse("todo_item.html", {
                "request": request,
                "todo": todo
            })
    return ""


@app.get("/todos/count", response_class=HTMLResponse)
async def get_todo_count(request: Request):
    """Get the count of incomplete todos"""
    count = len([todo for todo in todos if not todo["completed"]])
    return templates.TemplateResponse("todo_count.html", {
        "request": request,
        "count": count
    })


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

