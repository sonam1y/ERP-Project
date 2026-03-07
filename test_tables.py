import mysql.connector

# 1️⃣ Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="sonam9355",
    database="erp_system"
)

cur = db.cursor()

# 2️⃣ Check Users Table
print("----Users Table----")
cur.execute("SELECT * FROM users")
for row in cur.fetchall():
    print(row)

# 3️⃣ Check Products Table
print("\n----Products Table----")
cur.execute("SELECT * FROM products")
for row in cur.fetchall():
    print(row)

# 4️⃣ Check Customers Table
print("\n----Customers Table----")
cur.execute("SELECT * FROM customers")
for row in cur.fetchall():
    print(row)
