from sqlalchemy import Column,Integer,create_engine,text,ForeignKey,String,Float
from sqlalchemy.orm import declarative_base,sessionmaker,relationship

engine=create_engine("sqlite:///mini_project.db")
Base=declarative_base()
Session=sessionmaker(bind=engine)
session=Session()

class Category(Base):
    __tablename__="categories"
    id=Column(Integer,primary_key=True)
    name=Column(String)
    expenses=relationship("Expense",back_populates="category")
class Expense(Base):
    __tablename__ = "expenses"
    id=Column(Integer, primary_key=True)
    title=Column(String)
    amount=Column(Float)
    date=Column(String)
    category_id=Column(Integer, ForeignKey("categories.id"))

    category=relationship("Category", back_populates="expenses")
class Subscription(Base):
    __tablename__="subscriptions"
    id=Column(Integer, primary_key=True)
    name=Column(String)
    amount=Column(Float)
    next_date=Column(String)
class Budget(Base):
    __tablename__="budgets"
    id=Column(Integer,primary_key=True)
    month=Column(String)
    limit=Column(Integer)


Base.metadata.create_all(engine)

#FUNCTIONS
def add_category():
    name=input("Enter category name: ")
    session.add(Category(name=name))
    session.commit()
    print("Successfully added category!!")

def add_expense():
    title=input("Enter Expense title: ")
    amount=float(input("Enter Amount: "))
    date=input("Enter Date in (YYYY-MM-DD) Format: ")
    category_id=int(input("Category ID: "))
    category=session.query(Category).filter(Category.id == category_id).first()
    if not category:
        print("Category not found")
        return

    session.add(Expense(title=title,amount=amount,date=date,category_id=category_id))
    session.commit()
    print("Expense added Successfully!!")

def update_expense():
    new_id = int(input("Expense ID: "))
    exp = session.query(Expense).filter(Expense.id == new_id).first()

    if exp:
        exp.title=input("Enter New title: ")
        exp.amount=float(input("Enter New amount: "))
        exp.date=input("Entr New date: ")
        session.commit()
        print("Expense updated Successfully!")
    else:
        print("Error Expense not found")
def delete_expense():
    del_id=int(input("ENter the id of expense to delete: "))
    exp=session.query(Expense).filter(Expense.id==del_id).first()
    if exp:
        session.delete(exp)
        print("Successfully deleted!!")
    else:
        print("Id not found")
def search_by_date():
    date = input("Enter date (YYYY-MM-DD): ")
    expenses = session.query(Expense).filter(Expense.date == date).all()

    if not expenses:
        print("No records found")
        return

    for e in expenses:
        print(e.title, "₹", e.amount, "-", e.category.name)

def search_by_date():
    date = input("Enter date (YYYY-MM-DD): ")
    expenses = session.query(Expense).filter(Expense.date == date).all()

    if not expenses:
        print("No records found")
        return

    for e in expenses:
        print(e.title, "₹", e.amount, "-", e.category.name)

#REPORT MODULE 

def category_report():
    sql = """
    SELECT c.name, SUM(e.amount)
    FROM categories c
    JOIN expenses e ON c.id = e.category_id
    GROUP BY c.name
    """

    result = session.execute(text(sql))
    print("\n***Category Wise Expense Report***")

    for row in result:
        print(row[0], "→ ₹", row[1])



def set_budget():
    month=input("Month (YYYY-MM): ")
    limit=float(input("Monthly limit: "))

    session.add(Budget(month=month, limit=limit))
    session.commit()
    print("Budget set successfully")


def budget_alert():
    month=input("Month (YYYY-MM): ")

    total=session.execute(
        text("SELECT SUM(amount) FROM expenses WHERE date LIKE :m"),
        {"m": f"{month}%"}
    ).scalar()

    budget = session.query(Budget).filter(Budget.month == month).first()

    if not budget:
        print("No budget set for this month")
    elif total and total > budget.limit:
        print("Budget exceeded! Spent:", total)
    else:
        print("Within the budget")


def add_subscription():
    name = input("Subscription name: ")
    amount = float(input("Amount: "))
    next_date = input("Next payment date: ")

    session.add(Subscription(name=name, amount=amount, next_date=next_date))
    session.commit()
    print("Subscription added")


def view_subscriptions():
    subs = session.query(Subscription).all()
    for s in subs:
        print(s.name, "₹", s.amount, "Next:", s.next_date)

#----********************------------------


while True:
    print("""
===== FINTRACK PRO =====
1. Add Category
2. Add Expense
3. Update Expense
4. Delete Expense
5. Search by Date
6. Category Analytics
7. Set Monthly Budget
8. Budget Alert
9. Add Subscription
10. View Subscriptions
11. Exit
""")

    choice = input("Choose: ")

    if choice == "1":
        add_category()
    elif choice == "2":
        add_expense()
    elif choice == "3":
        update_expense()
    elif choice == "4":
        delete_expense()
    elif choice == "5":
        search_by_date()
    elif choice == "6":
        category_report()
    elif choice == "7":
        set_budget()
    elif choice == "8":
        budget_alert()
    elif choice == "9":
        add_subscription()
    elif choice == "10":
        view_subscriptions()
    elif choice == "11":
        print("Exiting FinTrack Pro created by Hrishikesh")
        break
    else:
        print("Invalid choice ENTERED")



