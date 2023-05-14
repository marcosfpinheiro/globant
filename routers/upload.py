from io import BytesIO
import sys

sys.path.append("..")
from fastapi import APIRouter, Request, File, Form, UploadFile
from fastapi.templating import Jinja2Templates
import pandas as pd

from database import engine, SessionLocal

router = APIRouter(
    prefix = "/upload",
    tags = ["upload"],
    responses= {404: {"description": "Not Found"}}
)

templates = Jinja2Templates(directory="templates")

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.get("/upload_csv")
async def upload_file(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

@router.post("/upload_csv")
async def load_file(request: Request, 
                    upload_file: UploadFile = File(...), 
                    type_file: str = Form(...),
                    type_load: str = Form(...)):


    content =  upload_file.file.read()
    with BytesIO(content) as data:
        df = pd.read_csv(data, delimiter=',', header=None, index_col=False)
    
    dict_columns = {
        "jobs" : ['id','job'],
        "departments": ['id','department'],
        "hired_employees" : ['id','name','datetime','department_id','job_id'] 
    }

    df.columns = dict_columns[type_file]
    df.to_sql(type_file, con=engine,  index=False, if_exists=type_load)
    

    return templates.TemplateResponse("uploaded.html", {"request": request})   


