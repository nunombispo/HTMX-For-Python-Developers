# HTMX Todo App - FastAPI Demo

A simple, interactive todo list application demonstrating HTMX with FastAPI, Jinja2 templates, and Bootstrap 5 styling. Perfect for showcasing HTMX's power to Python developers!

> 📚 **Support the Project**: This demo is part of the [HTMX for Python Developers](https://www.kickstarter.com/projects/devasservice/htmx-for-python-developers-book-and-course) book and course on Kickstarter!

## Features

- ✅ Add todos without page refresh
- ✅ Toggle completion status dynamically
- ✅ Delete todos with confirmation
- ✅ Live count of incomplete tasks
- ✅ Beautiful Bootstrap 5 UI

## Quick Start

### Installation

1. Install dependencies:

```bash
pip install -r requirements.txt
```

### Running the App

```bash
python app.py
```

Or using uvicorn directly:

```bash
uvicorn app:app --reload
```

Then open your browser to `http://localhost:8000`

## How It Works

This app showcases HTMX's core features:

- **Dynamic Content Loading**: New todos are added via `hx-post` without full page reloads
- **Partial Updates**: Only the new todo item is swapped into the DOM using `hx-swap="beforeend"`
- **Element Replacement**: Toggling and deleting use `hx-swap="outerHTML"` to update specific elements
- **Event Triggers**: The todo counter automatically updates when todos change using custom events
- **Server-Side Rendering**: All HTML is rendered server-side with Jinja2 templates

## Technology Stack

- **FastAPI**: Modern Python web framework
- **HTMX**: Dynamic HTML via AJAX, WebSockets, and Server-Sent Events
- **Jinja2**: Powerful templating engine
- **Bootstrap 5**: Responsive CSS framework

## Project Structure

```
.
├── app.py                 # FastAPI application
├── templates/
│   ├── index.html        # Main page template
│   └── todo_item.html    # Partial template for todo items
├── requirements.txt      # Python dependencies
└── README.md            # This file
```
