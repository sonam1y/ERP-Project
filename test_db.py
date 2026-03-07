from db import connect

try:
    db = connect()
    if db.is_connected():
        print("✅ MySQL Connected Successfully!")
except mysql.connector.Error as err:
    print("❌ Error:", err)

