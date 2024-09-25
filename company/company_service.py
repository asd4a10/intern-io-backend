from fastapi import FastAPI, APIRouter, Depends, HTTPException
from pydantic import BaseModel

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import get_db, User, Base, Company

company_router = APIRouter()


class CompanySchema(BaseModel):
    id: int
    name: str
    link: str
    img: str
    category: str
    description: str


# Endpoint to create a new company
@company_router.post("/")
def create_company(company: CompanySchema, companies_db: Session = Depends(get_db)):
    new_company = Company(**company.model_dump())
    companies_db.add(new_company)
    companies_db.commit()
    return {"message": "Company created successfully"}


# Endpoint to get all companies
@company_router.get("/")
def get_companies(companies_db: Session = Depends(get_db)) -> list[CompanySchema]:
    return companies_db.query(Company).all()


# Endpoint to get a specific company by ID
@company_router.get("/{company_id}")
def get_company(
    company_id: int, companies_db: Session = Depends(get_db)
) -> CompanySchema:
    company = companies_db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company


# Endpoint to update a company by ID
@company_router.put("/{company_id}")
def update_company(
    company_id: int,
    updated_company: CompanySchema,
    companies_db: Session = Depends(get_db),
):
    company = companies_db.query(Company).filter(Company.id == company_id)
    company.first()
    if company.first() is None:
        raise HTTPException(status_code=404, detail="Company not found")
    company.update(updated_company.model_dump())
    companies_db.commit()
    return {"message": "Company updated successfully"}


# Endpoint to delete a company by ID
@company_router.delete("/{company_id}")
def delete_company(company_id: int, companies_db: Session = Depends(get_db)):
    company = companies_db.query(Company).filter(Company.id == company_id)
    company.first()
    if not company.first():
        raise HTTPException(status_code=404, detail="Company not found")
    company.delete()
    companies_db.commit()
    return {"message": "Company deleted successfully"}


# Endpoint to create a new company
@company_router.post("/populate")
def populate_db(companies_db: Session = Depends(get_db)):
    companies_db.query(Company).delete()
    import json

    with open("population_scripts/companies.json") as file:
        json_data = json.load(file)
        companies_data = json_data.get("companies")

    for company_data in companies_data:
        # print(company_data)
        company_data["category"] = company_data["categories"][0]
        del company_data["categories"]
        new_company = Company(**company_data)
        companies_db.add(new_company)

    companies_db.commit()
    return {"message": "db is populated with companies"}
