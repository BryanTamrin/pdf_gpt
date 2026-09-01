from function import delete_database, pdf_to_page, page_to_embedding, add_database, process_question
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
    extracted_page = pdf_to_page(f"pdfs/{file.filename}")
    page_embedding = page_to_embedding(extracted_page)
    add_database(extracted_page, page_embedding, file.filename)
    return RedirectResponse(url="/", status_code=303)

@app.post("/delete")
async def delete_pdf(pdf_name: str):
    os.remove(f"pdfs/{pdf_name}")
    delete_database(pdf_name)
    return RedirectResponse(url="/", status_code=303)

@app.post("/ask")
async def ask_question(question: str):
    answer = process_question(question)
    return {"answer": answer}