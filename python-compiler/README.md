# Python Online Compiler

A web-based Python compiler similar to Programiz.

## Quick Start (Use Online API)

The frontend already connects to a public API. Just open `index.html` in your browser!

## Run Your Own Backend

```bash
# Install Flask
pip install flask

# Run backend
cd backend
python3 app.py
```

Then open `index.html` in your browser.

## Files

- `index.html` - Frontend (editor + output)
- `backend/app.py` - Flask API (executes Python code)

## Deploy

### Vercel/Netlify (Frontend only)
Upload `index.html` — uses public compiler API.

### Render/Railway (Full)
Deploy `backend/app.py` as a Python service.