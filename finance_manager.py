import csv
from flask import Flask, request, render_template, redirect, url_for



class Transaction:
   def __init__(self , amount , date , category , description=''):
      self.amount = amount 
      self.date = date 
      self.category = category 
      self.description = description 

class Income (Transaction):
   def __init__(self , amount , date , category , description=''):
      super().__init__(amount , date , category , description)


class Expense (Transaction):
   def __init__(self , amount , date , category , description=''):
      super().__init__(amount , date , category , description)



transactions = []

def add_income(amount , date , category , description=''):
   income = Income(amount , date , category , description)
   Transaction.append(income)

def add_expense(amount , date , category , description=''):
   expense = Expense(amount , date , category , description)
   Transaction.append(expense)

def remove_transactions(index):
   if 0 <= index <len(transactions):
      del transactions[index]

def list_transactions():
   for index , transaction in enumerate(transactions):
      print(f"{index}: {transaction.category} - {transaction.amount} on {transaction.date} ({transaction.description})")

def filter_transaction_by_category(category):
   return [t for t in transactions if t.category == category]

def calculate_total_income():
   return sum(t.amount for t in transactions if isinstance(t , Income))


def calculate_total_expense():
   return sum(t.amount for t in transactions if isinstance(t , Expense))


def calculate_net_balance():
   return  calculate_total_income() - calculate_total_expense()


def summarize_transaction_by_categoty():
   summary = {}
   for transaction in transactions:
      if transaction.category not in summary:
         summary[transaction.category] = 0
      summary[transaction.category] += transaction.amount

   return summary

def display_summary():
   summary = summarize_transaction_by_categoty()
   for category , total in summary.items():
      print(f"Category : {category} , Total : {total}")


budgets = {}


def set_budget(category , amount ):
   budgets[category] = amount

def analyze_budget():
   summary = summarize_transaction_by_categoty()
   for category , total in summary.items():
      budget = budgets.get(category, 0)
      if total > budget :
         print(f"Over budget in {category} by {total - budget}")
      else:
            print(f"Under budget in {category} by {budget - total}")



def add_income(amount, date, category, description=""):
   try:
      amount = float(amount)
      if amount <= 0 :
         raise ValueError("Amount must be positive.")
      income = Income(amount, date, category, description)
      transactions.append(income)
      print("Income added successfully.")
   except ValueError as ve:
        print(f"Error: {ve}")

def add_expense(amount, date, category, description=""):
    try:
        amount = float(amount)
        if amount <= 0:
            raise ValueError("Amount must be positive.")
        expense = Expense(amount, date, category, description)
        transactions.append(expense)
        print("Expense added successfully.")
    except ValueError as ve:
        print(f"Error: {ve}")


def remove_transaction(index):
    try:
        index = int(index)
        if 0 <= index < len(transactions):
            del transactions[index]
            print("Transaction removed successfully.")
        else:
            raise IndexError("Invalid index. Please enter a valid transaction number.")
    except (ValueError, IndexError) as e:
        print(f"Error: {e}")

def set_budget(category, amount):
    try:
        amount = float(amount)
        if amount < 0:
            raise ValueError("Budget amount must be non-negative.")
        budgets[category] = amount
        print(f"Budget set for {category}: {amount}")
    except ValueError as ve:
        print(f"Error: {ve}")


def main_menu():
   while True:
      print("\nPersonal Finance Manager")
      print("1: Add Income")
      print("2: Add Expense")
      print("3: Remove Transaction")
      print("4: List Transactions")
      print("5: Set Budget")
      print("6: Analyze Budget")
      print("7: Display Summary")
      print("8: Calculate Totals")
      print("9: Exit")

      choice = input("Enter your choice: ")

      if choice == "1":
            amount = input("Enter income amount: ")
            date = input("Enter income date (YYYY-MM-DD): ")
            category = input("Enter income category: ")
            description = input("Enter income description: ")
            add_income(amount, date, category, description)
        
      elif choice == "2":
            amount = input("Enter expense amount: ")
            date = input("Enter expense date (YYYY-MM-DD): ")
            category = input("Enter expense category: ")
            description = input("Enter expense description: ")
            add_expense(amount, date, category, description)
        
      elif choice == "3":
            index = input("Enter transaction number to remove: ")
            remove_transaction(index)
        
      elif choice == "4":
            list_transactions()
        
      elif choice == "5":
            category = input("Enter category to set budget for: ")
            amount = input("Enter budget amount: ")
            set_budget(category, amount)
        
      elif choice == "6":
            analyze_budget()
        
      elif choice == "7":
            display_summary()
        
      elif choice == "8":
            print(f"Total Income: {calculate_total_income()}")
            print(f"Total Expenses: {calculate_total_expenses()}")
            print(f"Net Balance: {calculate_net_balance()}")
        
      elif choice == "9":
            print("Exiting the program.")
            break
        
      else:
            print("Invalid choice. Please try again.")

# Start the program
if __name__ == "__main__":
    main_menu()






app = Flask(__name__)

# Initialize transactions and budgets here or load from persistent storage

@app.route('/')
def home():
    return render_template('index.html', transactions=transactions)

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    amount = float(request.form['amount'])
    date = request.form['date']
    category = request.form['category']
    description = request.form['description']
    t_type = request.form['type']
    
    if t_type == 'Income':
        add_income(amount, date, category, description)
    else:
        add_expense(amount, date, category, description)
    
    return redirect(url_for('home'))

# Additional routes and functions for removing transactions, setting budgets, etc.

if __name__ == '__main__':
    app.run(debug=True)
    
   
