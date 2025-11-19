from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, Response
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
    # Return just the new todo item HTML and trigger refresh of count/empty state via header
    todo_html = templates.TemplateResponse("todo_item.html", {
        "request": request,
        "todo": new_todo
    }).body.decode()
    
    response = HTMLResponse(content=todo_html)
    response.headers["HX-Trigger"] = "todoChanged"
    return response


@app.delete("/todos/{todo_id}", response_class=HTMLResponse)
async def delete_todo(request: Request, todo_id: str):
    """Delete a todo item"""
    global todos
    todos = [todo for todo in todos if todo["id"] != todo_id]
    # Return empty string to remove element and trigger refresh via header
    response = HTMLResponse(content="")
    response.headers["HX-Trigger"] = "todoChanged"
    return response


@app.put("/todos/{todo_id}/toggle", response_class=HTMLResponse)
async def toggle_todo(request: Request, todo_id: str):
    """Toggle completion status of a todo"""
    for todo in todos:
        if todo["id"] == todo_id:
            todo["completed"] = not todo["completed"]
            # Return updated todo item and trigger refresh via header
            todo_html = templates.TemplateResponse("todo_item.html", {
                "request": request,
                "todo": todo
            }).body.decode()
            
            response = HTMLResponse(content=todo_html)
            response.headers["HX-Trigger"] = "todoChanged"
            return response
    return ""


@app.get("/todos/count", response_class=HTMLResponse)
async def get_todo_count(request: Request):
    """Get the count of incomplete todos"""
    count = len([todo for todo in todos if not todo["completed"]])
    return templates.TemplateResponse("todo_count.html", {
        "request": request,
        "count": count
    })


@app.get("/todos/empty-state", response_class=HTMLResponse)
async def get_empty_state(request: Request):
    """Get the empty state HTML"""
    return templates.TemplateResponse("empty_state.html", {
        "request": request,
        "has_todos": len(todos) > 0
    })


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)

