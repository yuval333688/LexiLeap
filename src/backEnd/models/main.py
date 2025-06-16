from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from src.backEnd.models.Lesson import Lesson  # adjust the import if needed
app = FastAPI()
# Create a global lesson instance
lesson = Lesson(sudent_id=123)
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


current_word_index = {"index": 0}

@app.get("/", response_class=HTMLResponse)
async def show_word(request: Request):
    index = current_word_index["index"]
    test_num = 1  # You can change this dynamically later

    words = [w.word for w in lesson.tests[test_num - 1].words]
    
    if index >= len(words):
        return templates.TemplateResponse("done.html", {"request": request})
    
    word = words[index]
    return templates.TemplateResponse("word.html", {
        "request": request,
        "word": word,
        "index": index + 1,
        "total": len(words)
    })
@app.post("/next")
async def next_word():
    current_word_index["index"] += 1
    return RedirectResponse(url="/", status_code=303)

@app.get("/reset")
async def reset_word_index():
    current_word_index["index"] = 0
    return RedirectResponse(url="/", status_code=303)
