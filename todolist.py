from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()


class Table(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True)
    task = Column(String, default="Nothing to do!")
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)


def add_task(task, deadline):
    new_task = Table(task=task, deadline=datetime.strptime(deadline, '%Y-%m-%d'))
    session.add(new_task)
    session.commit()
    print("The task has been added!\n")


def show_today():
    today = datetime.today().strftime("%d %b")
    print(f"Today {today}:")
    rows = session.query(Table).filter(Table.deadline == datetime.today().date()).all()
    if len(rows) == 0:
        print("Nothing to do!\n")
    else:
        for i in range(1, len(rows)+1):
            print(f"{i}. {rows[i-1]}")
        print("\n")

def show_all():
    print("All tasks:")
    rows = session.query(Table).all()
    if len(rows) == 0:
        print("Nothing to do!\n")
    else:
        for i in range(1, len(rows)+1):
            print("{}. {}. {}".format(i, rows[i-1], rows[i-1].deadline.strftime("%d %b")))
        print("\n")

def show_week():
    today = datetime.today().date()
    print("\n")
    for i in range(7):
        day = today + timedelta(days=i)
        print(day.strftime("%A %d %b:"))
        rows = session.query(Table).filter(Table.deadline == day).all()
        if len(rows) == 0:
            print("Nothing to do!")
        for j in range(1,len(rows)+1):
            print(f"{j}. {rows[j-1]}")
        print("\n")
def show_missed():
    print("\nMissed tasks:")
    rows = session.query(Table).filter(Table.deadline < datetime.today().date()).order_by(Table.deadline).all()
    for i in range(1, len(rows)+1):
        print("{}. {}. {}".format(i, rows[i-1], rows[i-1].deadline.strftime("%d %b")))
    print("\n")
def del_task():
    rows = session.query(Table).filter(Table.deadline < datetime.today().date()).order_by(Table.deadline).all()
    if len(rows) == 0:
        print("Nothing is missed!")
    else:
        deleted = ""
        print("Chose the number of the task you want to delete:")
        for i in range(1, len(rows)+1):
             print("{}. {}. {}".format(i, rows[i-1], rows[i-1].deadline.strftime("%d %b")))

        user = int(input())
        for i in range(1, len(rows)+1):
            "{}. {}. {}".format(i, rows[i-1], rows[i-1].deadline.strftime("%d %b"))
            if user == i:
                rows_ = session.query(Table).all()
                delete_this = rows_[i-1]
                session.delete(delete_this)
                session.commit()
                print("The task has been deleted!\n")




def state_machine():
    while True:
        i = input("""1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit
""")
        if i == "1":
            show_today()
        elif i == "2":
            show_week()
        elif i == "3":
            show_all()
        elif i == "4":
            show_missed()
        elif i == "5":
            i = input("Enter task\n")
            j = input("Enter deadline\n")
            add_task(i, j)
        elif i == "6":
            del_task()
        else:
            print("Bye!")
            break


state_machine()
