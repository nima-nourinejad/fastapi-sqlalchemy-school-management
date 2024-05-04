from fastapi import FastAPI, Depends
from pydantic import BaseModel, Field
from uuid import UUID
import models
from database import sessionlocal, engine
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
	try:
		db = sessionlocal()
		yield db
	finally:
		db.close()

class mySchoolClasses(BaseModel):
	name: str = Field(min_length=1)
	schoolName: str = Field(min_length=1, max_length=100)
	teacherName: str = Field(min_length=1, max_length=100)
	studentCount: int = Field(gt=1, lt=100)

mySchoolClassesList = []

@app.get("/")
def read_school_class(db: Session = Depends(get_db)):
	return(db.query(models.mySchoolClasses).all())

@app.post("/")
def create_school_class(mySchoolClass: mySchoolClasses, db: Session = Depends(get_db)):
	school_class = models.mySchoolClasses()
	school_class.name = mySchoolClass.name
	school_class.schoolName = mySchoolClass.schoolName
	school_class.teacherName = mySchoolClass.teacherName
	school_class.studentCount = mySchoolClass.studentCount
	db.add(school_class)
	db.commit()

@app.put("/{schoolclass_id}")
def schoolClassUpdate(mySchoolClass_id: int, mySchoolClass: mySchoolClasses, db: Session = Depends(get_db)):
	school_class = db.query(models.mySchoolClasses).filter(models.mySchoolClasses.id).filter(models.mySchoolClasses.id == mySchoolClass_id).first()
	if school_class is None:
		print("The school class does not exist")
	school_class.name = mySchoolClass.name
	school_class.schoolName = mySchoolClass.schoolName
	school_class.teacherName = mySchoolClass.teacherName
	school_class.studentCount = mySchoolClass.studentCount
	db.add(school_class)
	db.commit()
	return mySchoolClass

@app.delete("/{schoolclass_id}")
def delete_school_class(mySchoolClass_id: int, db: Session = Depends(get_db)):
	school_class = db.query(models.mySchoolClasses).filter(models.mySchoolClasses.id).filter(models.mySchoolClasses.id == mySchoolClass_id).first()
	if school_class is not None:
		db.query(models.mySchoolClasses).filter(models.mySchoolClasses.id == mySchoolClass_id).delete()
		db.commit()