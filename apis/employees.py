from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Department(Base):
    __tablename__ = 'department'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))


class Employee(Base):
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    hired_on = Column(DateTime, default=func.now())
    department_id = Column(Integer, ForeignKey('department.id'))
    # Use cascade='delete,all' to propagate the deletion of a Department onto its Employees
    department = relationship(
        Department,
        backref=backref('employees',
                        uselist=True,
                        cascade='delete,all'))
    # Dept accesses employees use list


engine = create_engine('mysql://root:@localhost:3306/test', echo=True)

Session = sessionmaker()
Session.configure(bind=engine)
Base.metadata.create_all(engine)
session = Session()

john = Employee(name='john')
it_department = Department(name='IT')
john.department = it_department

session.add(john)
session.commit()

it = session.query(Department) \
    .filter(Department.name == 'IT') \
    .order_by(Department.id.desc()) \
    .first()

print it.employees
print it.employees[0].name

# session.delete(it)
# session.commit()
