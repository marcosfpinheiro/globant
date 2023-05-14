from io import BytesIO
import sys
sys.path.append("..")

from fastapi import APIRouter, Depends, Request, File, Form, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import text
import pandas as pd

from database import engine, SessionLocal

router = APIRouter(
    prefix = "/metrics",
    tags = ["metrics"],
    responses= {404: {"description": "Not Found"}}
)

templates = Jinja2Templates(directory="templates")

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@router.get("/", response_class=HTMLResponse)
async def list_hired_mean(request: Request, db: Session = Depends(get_db)):
    departments = db.execute(text('''select 
	emp.department_id, 
	dep.department, 
	count(*) as hired 
from 
	hired_employees emp
JOIN
	departments dep
ON 
	dep.id = emp.department_id
group by emp.department_id, dep.department
having count(*) > (
	select avg(count)
		from(
			select count(*) 
			from 
				hired_employees 
			where 
				extract(year from DATE(datetime)) = '2021'
			group by department_id ) as count_dep)
order by hired desc'''))
 
    return templates.TemplateResponse("department_average.html", {"request": request, "departments": departments})


@router.get("/empl", response_class=HTMLResponse)
async def list_employees_hired_quarter(request: Request, db: Session = Depends(get_db)):
    employees = db.execute(text('''SELECT ct.department, ct.jobs, coalesce(ct.Q1,0) as Q1, coalesce(ct.Q2,0) as Q2, coalesce(ct.Q3,0) as Q3, coalesce(ct.Q4,0) as Q4
FROM crosstab (
    'select 
		dep.department,
	 	jobs.job,
		extract(quarter from DATE(datetime)),
		count(extract(quarter from DATE(datetime)))
	from 
		hired_employees emp
	JOIN
 		departments dep
 		ON dep.id = emp.department_id
 	JOIN
 		jobs
 		ON jobs.id = emp.job_id
	where datetime is not null
	AND extract(year from DATE(datetime)) = ''2021''
	group by 1,2,3', 
	'select distinct extract(quarter from DATE(datetime)) from hired_employees where datetime is not null'
) AS ct (department text, jobs text, Q1 int, Q2 int, Q3 int, Q4 int) 
order by 
	department, 
	jobs'''))
 
    return templates.TemplateResponse("employees_hired_quarters.html", {"request": request, "employees": employees})

