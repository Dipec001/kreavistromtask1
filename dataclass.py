from dataclasses import dataclass
import sqlite3


# Define the Employee data class
@dataclass
class Employee:
    employee_id: int
    name: str
    age: str
    department: str
    salary: str


class EmployeeManagementSystem:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

        # Create an employees' table if it doesn't exist
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS employees
                            (employee_id INTEGER PRIMARY KEY,
                             name TEXT,
                             age TEXT,
                             department TEXT,
                             salary TEXT)''')
        self.conn.commit()

        # Initialize next_employee_id
        self.next_employee_id = self.get_next_employee_id()

    def get_next_employee_id(self):
        # Retrieve the maximum employee_id from the database and increment it
        self.cursor.execute("SELECT MAX(employee_id) FROM employees")
        max_id = self.cursor.fetchone()[0]
        if max_id is not None:
            return max_id + 1
        return 1

    def add_employee(self):
        """Function to add employees to the system"""
        while True:
            print("Add Employee")
            name = input("Name: ")

            if not name:
                print("Name cannot be empty. Please enter a name.")
                continue  # Repeat the loop to get a valid name

            age = input("Age: ")
            department = input("Department: ")
            salary = input("Salary: ")

            # Create an Employee object with a unique employee_id
            employee = Employee(self.next_employee_id, name, age, department, salary)
            self.next_employee_id += 1

            # Insert the new employee into the database
            self.cursor.execute(
                "INSERT INTO employees (employee_id, name, age, department, salary) VALUES (?, ?, ?, ?, ?)",
                (employee.employee_id, employee.name, employee.age, employee.department, employee.salary))
            self.conn.commit()

            print(f"Employee {employee.name} added successfully with ID {employee.employee_id}!")
            break  # Exit the loop if a valid name is provided

    def display_all_employees(self):
        self.cursor.execute("SELECT * FROM employees")
        employees = self.cursor.fetchall()
        print("\nEmployee Details")
        if not employees:
            print("No employees")
        else:
            for employee in employees:
                print(f"Employee ID: {employee[0]}")
                print(f"Name: {employee[1]}")
                print(f"Age: {employee[2]}")
                print(f"Department: {employee[3]}")
                print(f"Salary: ${employee[4]}")
                print("-" * 20)

    def update_employee(self):
        name_to_update = input("Enter the name of the employee to update: ")

        # Query the database for employees with the specified name
        self.cursor.execute("SELECT * FROM employees WHERE name = ?", (name_to_update,))
        matching_employees = self.cursor.fetchall()

        if not matching_employees:
            print(f"No employees with the name {name_to_update} found!")
            return

        print("Matching Employees:")
        for emp in matching_employees:
            print(f"Employee ID: {emp[0]}, Name: {emp[1]}")

        try:
            selected_id = int(input("Enter the ID of the employee to update: "))

            # Check if the selected_id exists in the list of matching employees
            if any(emp[0] == selected_id for emp in matching_employees):
                for emp in matching_employees:
                    if emp[0] == selected_id:
                        employee_to_update = emp

                        print(f"Current details for {employee_to_update[1]}:")
                        print(f"Name: {employee_to_update[1]}")
                        print(f"Age: {employee_to_update[2]}")
                        print(f"Department: {employee_to_update[3]}")
                        print(f"Salary: ${employee_to_update[4]}")

                        new_salary = input("Enter the new salary: ")

                        # Update the salary in the database for the selected employee
                        self.cursor.execute("UPDATE employees SET salary = ? WHERE employee_id = ?",
                                            (new_salary, employee_to_update[0]))
                        self.conn.commit()

                        print(f"Salary for {employee_to_update[1]} updated successfully!")
                        return
            else:
                print("Invalid ID. No employee updated.")
        except ValueError:
            print("Invalid input. Please enter a valid employee ID.")

    def remove_employee(self):
        name_to_remove = input("Enter the name of the employee to remove: ").lower()

        # Query the database for employees with the specified name
        self.cursor.execute("SELECT * FROM employees WHERE name = ?", (name_to_remove,))
        matching_employees = self.cursor.fetchall()

        if not matching_employees:
            print(f"No employees with the name {name_to_remove} found!")
            return

        print("Matching Employees:")
        for emp in matching_employees:
            print(f"Employee ID: {emp[0]}, Name: {emp[1]}")

        try:
            selected_id = int(input("Enter the ID of the employee to delete: "))

            # Check if the selected_id exists in the list of matching employees
            if any(emp[0] == selected_id for emp in matching_employees):
                for emp in matching_employees:
                    if emp[0] == selected_id:
                        employee_to_remove = emp

                        # Delete the employee from the database
                        self.cursor.execute("DELETE FROM employees WHERE employee_id = ?", (employee_to_remove[0],))
                        self.conn.commit()

                        print(f"Employee {employee_to_remove[1]} removed from the system.")
                        return
            else:
                print("Invalid ID. No employee removed.")
        except ValueError:
            print("Invalid input. Please enter a valid employee ID.")

    def search_employee(self):
        name_to_search = input('Please enter the name of the employee you are searching for:').lower()

        # Query the database for employees with the specified name
        self.cursor.execute("SELECT * FROM employees WHERE name = ?", (name_to_search,))
        matching_employees = self.cursor.fetchall()

        if not matching_employees:
            print(f"No employees with the name {name_to_search} found!")
            return

        print("Matching Employees:")
        for emp in matching_employees:
            print(f"Employee ID: {emp[0]}, Name: {emp[1]}")

        selected_id = int(input("Enter the ID of the employee to view details: "))

        # Find the employee with the selected ID in the matching employees
        selected_employee = None
        for emp in matching_employees:
            if emp[0] == selected_id:
                selected_employee = emp
                break

        if selected_employee:
            print("\nEmployee Details:")
            print(f"Employee ID: {selected_employee[0]}")
            print(f"Name: {selected_employee[1]}")
            print(f"Age: {selected_employee[2]}")
            print(f"Department: {selected_employee[3]}")
            print(f"Salary: ${selected_employee[4]}")
        else:
            print("Invalid ID. No employee details displayed.")

    def close(self):
        self.conn.close()


# Menu-driven user interface
if __name__ == "__main__":
    db_file = "employee_database.db"
    emp_system = EmployeeManagementSystem(db_file)
    while True:
        print("\nEmployee Management System")
        print("1. Add Employee")
        print("2. Display all Employees")
        print("3. Search Particular Employee")
        print("4. Update Employee Details")
        print("5. Remove Employee")
        print("6. Quit")

        choice = input("Enter your choice: ")

        if choice == '1':
            emp_system.add_employee()
        elif choice == '2':
            emp_system.display_all_employees()
        elif choice == '3':
            emp_system.search_employee()
        elif choice == '4':
            emp_system.update_employee()
        elif choice == '5':
            emp_system.remove_employee()
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")