
# 📦 Inventory Management System

An **interactive and responsive Inventory Management System** built using **Python**, **CustomTkinter**, and **MySQL**. This project allows you to manage product data efficiently with full **CRUD operations** and a user-friendly graphical interface.

## 🚀 Features

- Add, edit, and delete product details
- View real-time inventory levels
- Search and filter products by name or ID
- Low stock alerts
- Sales and inventory summary reports
- Responsive and interactive GUI built with CustomTkinter
- Secure login system for admin access

## 🛠️ Tech Stack

- **Frontend:** Python (CustomTkinter)
- **Backend:** Python (SQLite/MySQL)
- **Database:** MySQL
- **Others:** Tkinter message boxes, data validation, exception handling


## 🔐 Login Credentials

> **Default Admin Credentials**
> - **Username:** `admin`
> - **Password:** `admin123`

## 🧑‍💻 How to Run the Project

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/inventory-management-system.git
cd inventory-management-system
2. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
3. Set Up MySQL Database
Create a database in MySQL (e.g. inventory_db)

Update your connection settings in database.py

python
Copy
Edit
mydb = mysql.connector.connect(
    host="localhost",
    user="your_mysql_user",
    password="your_mysql_password",
    database="inventory_db"
)
Run the main.py file to auto-create tables

4. Run the Application
bash
Copy
Edit
python main.py
✅ To-Do / Future Enhancements
Add user roles (Admin, Staff)

Export data to Excel/CSV

Barcode scanner integration

Cloud database support
