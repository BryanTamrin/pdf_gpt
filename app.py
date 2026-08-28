from function import pdf_to_page, page_to_embedding, add_database, process_question
from fastapi import FastAPI, Request, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
def home(request: Request):
    pdfs = os.listdir("pdfs")
    return templates.TemplateResponse(
        request,
        "index.html",
        {"pdfs": pdfs}
    )
@app.post("/upload")
async def upload_pdf(file: UploadFile):
    content = await file.read()

    with open (f"pdfs/{file.filename}", "wb") as f:
        f.write(content)
    return RedirectResponse(url="/", status_code=303)

@app.post("/delete")
async def delete_pdf(pdf_name: str):
    os.remove(f"pdfs/{pdf_name}")
    return RedirectResponse(url="/", status_code=303)