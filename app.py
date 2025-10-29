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
    # Return the new todo item and update empty state and count via out-of-band swaps
    template_env = templates.env
    todo_html = template_env.get_template("todo_item.html").render(todo=new_todo, request=request)
    empty_state_html = template_env.get_template("empty_state.html").render(
        has_todos=len(todos) > 0, request=request
    )
    count_html = template_env.get_template("todo_count.html").render(
        count=len([t for t in todos if not t["completed"]]), request=request
    )
    return f'{todo_html}<div id="empty-state" class="text-center text-muted py-5" hx-swap-oob="true">{empty_state_html}</div><span id="todo-count" class="badge bg-info" hx-swap-oob="true">{count_html}</span>'


@app.delete("/todos/{todo_id}", response_class=HTMLResponse)
async def delete_todo(request: Request, todo_id: str):
    """Delete a todo item"""
    global todos
    todos = [todo for todo in todos if todo["id"] != todo_id]
    # Return empty string to remove element, plus out-of-band updates for empty state and count
    template_env = templates.env
    empty_state_html = template_env.get_template("empty_state.html").render(
        has_todos=len(todos) > 0, request=request
    )
    count_html = template_env.get_template("todo_count.html").render(
        count=len([t for t in todos if not t["completed"]]), request=request
    )
    return f'<div id="empty-state" class="text-center text-muted py-5" hx-swap-oob="true">{empty_state_html}</div><span id="todo-count" class="badge bg-info" hx-swap-oob="true">{count_html}</span>'


@app.put("/todos/{todo_id}/toggle", response_class=HTMLResponse)
async def toggle_todo(request: Request, todo_id: str):
    """Toggle completion status of a todo"""
    for todo in todos:
        if todo["id"] == todo_id:
            todo["completed"] = not todo["completed"]
            template_env = templates.env
            todo_html = template_env.get_template("todo_item.html").render(todo=todo, request=request)
            count_html = template_env.get_template("todo_count.html").render(
                count=len([t for t in todos if not t["completed"]]), request=request
            )
            return f'{todo_html}<span id="todo-count" class="badge bg-info" hx-swap-oob="true">{count_html}</span>'
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

