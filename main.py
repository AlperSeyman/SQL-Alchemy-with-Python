# Imports
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.exc import IntegrityError


# Create Database
engine = create_engine("sqlite:///missions.db", echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


# Define Models (User and Tasks)
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    tasks = relationship("Tasks", back_populates="user", cascade="all, delete-orphan")

   
                
    
class Tasks(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    title = Column(String(59), nullable=True)
    description = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User",back_populates="tasks")

    
Base.metadata.create_all(engine)

# Utlity Functions
def get_user_by_email(email):
    user_mail =  session.query(User).filter_by(email=email).first()
    return user_mail

def confirm_action(prompt:str) -> bool:
    return input(f"{prompt} (yes/no): ").strip().lower() =='yes'


# CRUD Operations
def add_user():
    name = input("Enter user name: ")
    email = input("Enter email address: ")

    if not name or not email:
        print(f"Error: Name and Email can not be empty")
        return

    if get_user_by_email(email):
        print(f"User already exisits: {email}")
        return

    try:
        session.add(User(name=name, email=email))
        session.commit()
        print(f"User: {name} added")
    except IntegrityError:
        session.rollback()
        print("Error: This email is already in use. Please use a different one.")

def add_task():
    email = input("Enter email of the user to add tasks: ")
    user = get_user_by_email(email)
    if not user:
        print(f"No user found with that email")
        return

    title = input("Enter the title: ")
    description = input("Enter the description: ")
    
    if not title or not description:
        print("Error: Title and Description cannot be empty.")
        return
    
    
    session.add(Tasks(title=title, description=description, user=user))
    session.commit()
    print(f"Added to Databse --> {title} : {description}")


# Query
def query_users():
    for user in session.query(User).all():
        print(f"ID : {user.id}\nName: {user.name}\nEmail: {user.email}")

def query_tasks():
    email = input("Enter email of the user for tasks: ")
    user = get_user_by_email(email)

    if not user:
        print(f"No user found with that email")
        return

    for task in user.tasks:
        print(f"Task Title:  {task.title}\nTask Description : {task.description}")


def update_user():
    email= input("Enter the email of the user for update.")
    user = get_user_by_email(email)

    if not user:
        print(f"No user found with that email")
        return
    
    user.name = input("Enter a new name for the user : ")
    user.email = input("Enter a new email (leave blank to stay the same) : ")
    session.commit()
    print("User was updated")

def delete_user():
    email= input("Enter the email of the user for delete user : ")
    user = get_user_by_email(email)

    if not user:
        print(f"No user found with that email")
        return
    
    if confirm_action(f"Are you sure you want to delete : {user.name} ?"):
        session.delete(user)
        session.commit()
        print("User was deleted....")

def  delete_task():
    email= input("Enter the email to show linked tasks: ")
    user = get_user_by_email(email)

    for task in user.tasks:
        print(f"Task ID: {task.id}\nTitle: {task.title}")

    task_id = input("Enter the ID of the task to delete: ")
    task = session.query(Tasks).get(task_id)

    if not task:
        print(f"There is no task there")
        return
    
    if confirm_action(f"Are you sure you want to delete : {task.id} ?"):
        session.delete(task)
        session.commit()
        print("Task was deleted....")
    

# Main Operations
def main() -> None:
    actions = {
        "1" : add_user,
        "2" : add_task,
        "3" : query_users,
        "4" : query_tasks,
        "5" : update_user,
        "6" : delete_user,
        "7" : delete_task,

    }

    while True:
        print("\nOptions:\n1. Add User\n2. Add Task\n3. Query Users\n4. Query Tasks\n5. Update User\n6. Delete User\n7. Delete Task\n8. Exit")

        transaction = input("Enter an options: ")
        if transaction == "8":
            print("Bis Bald")
            break
        
        action = actions.get(transaction)
        if action:
            action()
        else:
            print("Please select 'Valid Options' ")

if __name__ == "__main__":
    main()