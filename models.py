from sqlalchemy import Column, Integer, String
from database import Base

class mySchoolClasses(Base):
	__tablename__ = "mySchoolClasses"
	id = Column(Integer, primary_key=True, index=True)
	name = Column(String)
	schoolName = Column(String)
	teacherName = Column(String)
	studentCount = Column(Integer)