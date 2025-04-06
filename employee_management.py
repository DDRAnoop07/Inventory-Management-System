import customtkinter as ctk
from customtkinter import *
import mysql.connector
from mysql.connector import Error
from tkinter import messagebox, ttk

# Database connection
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  # replace with your MySQL username
            password='DDR@#my28',  # replace with your MySQL password
            database='employee_management'
        )
        return connection
    except Error as e:
        messagebox.showerror("Database Error", f"Error connecting to MySQL: {e}")
        return None

# Login Window
class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Inventory Management System - Login")
        self.geometry("1920x1080")
        self.resizable(False, False)
        
        self.configure(fg_color="#2b2b2b")
        
        # Login Frame
        self.login_frame = ctk.CTkFrame(self, fg_color="#333333")
        self.login_frame.pack(pady=40, padx=20, fill="both", expand=True)
        
        # Title Label
        self.title_label = ctk.CTkLabel(
            self.login_frame, 
            text="Inventory Management System",
            font=("Arial", 20, "bold")
        )
        self.title_label.pack(pady=20)
        
        # Username Entry
        self.username_entry = ctk.CTkEntry(
            self.login_frame, 
            placeholder_text="Username",
            width=200
        )
        self.username_entry.pack(pady=10)
        
        # Password Entry
        self.password_entry = ctk.CTkEntry(
            self.login_frame, 
            placeholder_text="Password",
            show="*",
            width=200
        )
        self.password_entry.pack(pady=10)
        
        # Login Button
        self.login_button = ctk.CTkButton(
            self.login_frame, 
            text="Login",
            command=self.login,
            width=200
        )
        self.login_button.pack(pady=20)
    
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        
        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
                user = cursor.fetchone()
                
                if user:
                    self.destroy()
                    app = EmployeeManagementApp()
                    app.mainloop()
                else:
                    messagebox.showerror("Login Failed", "Invalid username or password")
            except Error as e:
                messagebox.showerror("Database Error", f"Error during login: {e}")
            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()

# Main Application
class EmployeeManagementApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Inventory Management System")
        self.geometry("1000x600")
        self.resizable(True, True)
        
        self.configure(fg_color="#2b2b2b")
        
        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Main Frame
        self.main_frame = ctk.CTkFrame(self, fg_color="#333333")
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        
        # Title Label
        self.title_label = ctk.CTkLabel(
            self.main_frame, 
            text="Inventory Management System",
            font=("Arial", 24, "bold")
        )
        self.title_label.grid(row=0, column=0, pady=20, sticky="n")
        
        # Search Frame
        self.search_frame = ctk.CTkFrame(self.main_frame, fg_color="#444444")
        self.search_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.search_frame.grid_columnconfigure(0, weight=1)
        
        # Search By Label
        self.search_by_label = ctk.CTkLabel(
            self.search_frame, 
            text="Search By:",
            font=("Arial", 12)
        )
        self.search_by_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        # Search Options
        self.search_var = ctk.StringVar(value="id")
        self.search_options = ["id", "name", "phone", "role", "gender", "salary"]
        
        for i, option in enumerate(self.search_options):
            ctk.CTkRadioButton(
                self.search_frame,
                text=option.capitalize(),
                variable=self.search_var,
                value=option,
                command=self.search_employees
            ).grid(row=0, column=i+1, padx=5, pady=5)
        
        # Search Entry
        self.search_entry = ctk.CTkEntry(
            self.search_frame,
            placeholder_text="Search...",
            width=300
        )
        self.search_entry.grid(row=1, column=0, columnspan=len(self.search_options)+1, padx=10, pady=10, sticky="ew")
        self.search_entry.bind("<KeyRelease>", lambda event: self.search_employees())
        
        # Treeview Frame
        self.tree_frame = ctk.CTkFrame(self.main_frame, fg_color="#444444")
        self.tree_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        self.tree_frame.grid_columnconfigure(0, weight=1)
        self.tree_frame.grid_rowconfigure(0, weight=1)
        
        # Treeview
        self.tree = ttk.Treeview(
            self.tree_frame,
            columns=("id", "name", "phone", "role", "gender", "salary"),
            show="headings",
            selectmode="browse"
        )
        
        # Configure Treeview columns
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("phone", text="Phone")
        self.tree.heading("role", text="Role")
        self.tree.heading("gender", text="Gender")
        self.tree.heading("salary", text="Salary")
        
        self.tree.column("id", width=50, anchor="center")
        self.tree.column("name", width=150, anchor="w")
        self.tree.column("phone", width=120, anchor="w")
        self.tree.column("role", width=150, anchor="w")
        self.tree.column("gender", width=80, anchor="center")
        self.tree.column("salary", width=100, anchor="e")
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)
        
        # Button Frame
        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="#444444")
        self.button_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=10)
        
        # Buttons
        self.new_employee_button = ctk.CTkButton(
            self.button_frame,
            text="New Employee",
            command=self.new_employee
        )
        self.new_employee_button.pack(side="left", padx=5, pady=5)
        
        self.add_employee_button = ctk.CTkButton(
            self.button_frame,
            text="Add Employee",
            command=self.add_employee
        )
        self.add_employee_button.pack(side="left", padx=5, pady=5)
        
        self.update_employee_button = ctk.CTkButton(
            self.button_frame,
            text="Update Employee",
            command=self.update_employee
        )
        self.update_employee_button.pack(side="left", padx=5, pady=5)
        
        self.delete_employee_button = ctk.CTkButton(
            self.button_frame,
            text="Delete Employee",
            command=self.delete_employee,
            fg_color="#d9534f",
            hover_color="#c9302c"
        )
        self.delete_employee_button.pack(side="left", padx=5, pady=5)
        
        self.delete_all_button = ctk.CTkButton(
            self.button_frame,
            text="Delete All",
            command=self.delete_all_employees,
            fg_color="#d9534f",
            hover_color="#c9302c"
        )
        self.delete_all_button.pack(side="left", padx=5, pady=5)
        
        # Form Frame (hidden by default)
        self.form_frame = ctk.CTkFrame(self.main_frame, fg_color="#444444")
        
        # Form Labels and Entries
        self.form_labels = {}
        self.form_entries = {}
        
        form_fields = ["name", "phone", "role", "gender", "salary"]
        
        for i, field in enumerate(form_fields):
            self.form_labels[field] = ctk.CTkLabel(
                self.form_frame,
                text=field.capitalize() + ":",
                font=("Arial", 12)
            )
            self.form_labels[field].grid(row=i, column=0, padx=10, pady=5, sticky="e")
            
            self.form_entries[field] = ctk.CTkEntry(
                self.form_frame,
                width=200
            )
            self.form_entries[field].grid(row=i, column=1, padx=10, pady=5, sticky="w")
        
        # Gender options
        self.gender_var = ctk.StringVar(value="Male")
        ctk.CTkRadioButton(
            self.form_frame,
            text="Male",
            variable=self.gender_var,
            value="Male"
        ).grid(row=3, column=1, padx=5, pady=5, sticky="w")
        
        ctk.CTkRadioButton(
            self.form_frame,
            text="Female",
            variable=self.gender_var,
            value="Female"
        ).grid(row=3, column=1, padx=80, pady=5, sticky="w")
        
        # Form Buttons
        self.save_button = ctk.CTkButton(
            self.form_frame,
            text="Save",
            command=self.save_employee
        )
        self.save_button.grid(row=len(form_fields), column=0, padx=10, pady=10, sticky="e")
        
        self.cancel_button = ctk.CTkButton(
            self.form_frame,
            text="Cancel",
            command=self.cancel_form,
            fg_color="#6c757d",
            hover_color="#5a6268"
        )
        self.cancel_button.grid(row=len(form_fields), column=1, padx=10, pady=10, sticky="w")
        
        # Load initial data
        self.load_employees()
    
    def load_employees(self):
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM employees")
                employees = cursor.fetchall()
                
                for employee in employees:
                    self.tree.insert("", "end", values=employee)
                
            except Error as e:
                messagebox.showerror("Database Error", f"Error loading employees: {e}")
            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()
    
    def search_employees(self):
        search_term = self.search_entry.get()
        search_by = self.search_var.get()
        
        if not search_term:
            self.load_employees()
            return
        
        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                
                if search_by == "id":
                    cursor.execute("SELECT * FROM employees WHERE id = %s", (search_term,))
                elif search_by == "salary":
                    cursor.execute("SELECT * FROM employees WHERE salary = %s", (search_term,))
                else:
                    cursor.execute(f"SELECT * FROM employees WHERE {search_by} LIKE %s", (f"%{search_term}%",))
                
                employees = cursor.fetchall()
                
                # Clear existing data
                for item in self.tree.get_children():
                    self.tree.delete(item)
                
                for employee in employees:
                    self.tree.insert("", "end", values=employee)
                
            except Error as e:
                messagebox.showerror("Database Error", f"Error searching employees: {e}")
            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()
    
    def new_employee(self):
        # Clear form entries
        for entry in self.form_entries.values():
            entry.delete(0, "end")
        
        # Set default gender
        self.gender_var.set("Male")
        
        # Show form frame
        self.form_frame.grid(row=4, column=0, sticky="ew", padx=10, pady=10)
        self.current_action = "add"
    
    def add_employee(self):
        self.new_employee()
    
    def update_employee(self):
        selected_item = self.tree.selection()
        
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an employee to update")
            return
        
        # Get selected employee data
        employee_data = self.tree.item(selected_item, "values")
        
        # Fill form with employee data
        self.form_entries["name"].insert(0, employee_data[1])
        self.form_entries["phone"].insert(0, employee_data[2])
        self.form_entries["role"].insert(0, employee_data[3])
        self.gender_var.set(employee_data[4])
        self.form_entries["salary"].insert(0, employee_data[5])
        
        # Store the employee ID for update
        self.selected_employee_id = employee_data[0]
        
        # Show form frame
        self.form_frame.grid(row=4, column=0, sticky="ew", padx=10, pady=10)
        self.current_action = "update"
    
    def save_employee(self):
        # Get form data
        name = self.form_entries["name"].get()
        phone = self.form_entries["phone"].get()
        role = self.form_entries["role"].get()
        gender = self.gender_var.get()
        salary = self.form_entries["salary"].get()
        
        # Validate data
        if not all([name, phone, role, gender, salary]):
            messagebox.showerror("Error", "Please fill all fields")
            return
        
        try:
            salary = float(salary)
        except ValueError:
            messagebox.showerror("Error", "Salary must be a number")
            return
        
        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                
                if self.current_action == "add":
                    cursor.execute(
                        "INSERT INTO employees (name, phone, role, gender, salary) VALUES (%s, %s, %s, %s, %s)",
                        (name, phone, role, gender, salary)
                    )
                    messagebox.showinfo("Success", "Employee added successfully")
                elif self.current_action == "update":
                    cursor.execute(
                        "UPDATE employees SET name = %s, phone = %s, role = %s, gender = %s, salary = %s WHERE id = %s",
                        (name, phone, role, gender, salary, self.selected_employee_id)
                    )
                    messagebox.showinfo("Success", "Employee updated successfully")
                
                connection.commit()
                self.cancel_form()
                self.load_employees()
                
            except Error as e:
                connection.rollback()
                messagebox.showerror("Database Error", f"Error saving employee: {e}")
            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()
    
    def cancel_form(self):
        self.form_frame.grid_forget()
    
    def delete_employee(self):
        selected_item = self.tree.selection()
        
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an employee to delete")
            return
        
        employee_id = self.tree.item(selected_item, "values")[0]
        employee_name = self.tree.item(selected_item, "values")[1]
        
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete {employee_name} (ID: {employee_id})?"
        )
        
        if confirm:
            connection = create_connection()
            if connection:
                try:
                    cursor = connection.cursor()
                    cursor.execute("DELETE FROM employees WHERE id = %s", (employee_id,))
                    connection.commit()
                    messagebox.showinfo("Success", "Employee deleted successfully")
                    self.load_employees()
                except Error as e:
                    connection.rollback()
                    messagebox.showerror("Database Error", f"Error deleting employee: {e}")
                finally:
                    if connection.is_connected():
                        cursor.close()
                        connection.close()
    
    def delete_all_employees(self):
        confirm = messagebox.askyesno(
            "Confirm Delete All",
            "Are you sure you want to delete ALL employees? This cannot be undone."
        )
        
        if confirm:
            connection = create_connection()
            if connection:
                try:
                    cursor = connection.cursor()
                    cursor.execute("DELETE FROM employees")
                    connection.commit()
                    messagebox.showinfo("Success", "All employees deleted successfully")
                    self.load_employees()
                except Error as e:
                    connection.rollback()
                    messagebox.showerror("Database Error", f"Error deleting employees: {e}")
                finally:
                    if connection.is_connected():
                        cursor.close()
                        connection.close()

# Run the application
if __name__ == "__main__":
    login_app = LoginWindow()
    login_app.mainloop()