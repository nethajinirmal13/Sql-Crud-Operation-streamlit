import streamlit as st
import mysql.connector
from mysql.connector import Error
from tabulate import tabulate

def create_connection():
    connection = None
    try:
       connection = mysql.connector.connect(
            host=st.secrets["mysql"]["host"],
            port=st.secrets["mysql"]["port"],
            user=st.secrets["mysql"]["user"],
            password=st.secrets["mysql"]["password"],
            database=st.secrets["mysql"]["database"],
            ssl_ca=st.secrets["mysql"]["ssl_ca"]
       )     
       if connection.is_connected():
            st.success("Connection to MySQL DB successful")
    except Error as e:
        st.error(f"The error '{e}' occurred")
    return connection


def create_user(connection,user_id, name, age):
    cursor = connection.cursor()
    query = "INSERT INTO users (id,name, age) VALUES (%s,%s, %s)"
    cursor.execute(query, (user_id,name, age))
    connection.commit()
    
    


# Function to read all users from the database
def read_users(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    return rows


def update_user(connection, user_id, name, age):
    cursor = connection.cursor()
    query = "UPDATE users SET name = %s, age = %s WHERE id = %s"
    cursor.execute(query, (name, age, user_id))
    connection.commit()
    

# Function to delete a user from the database
def delete_user(connection, user_id):
    cursor = connection.cursor()
    query = "DELETE FROM users WHERE id = %s"
    cursor.execute(query, (user_id,))
    connection.commit()
    

# Main function to create the Streamlit app interface
def main():
    st.title("MySQL CRUD Operations")

    # Connect to MySQL
    connection = create_connection()

    # Create a new user
    st.subheader("Create User")
    user_id= st.number_input("Id",min_value=0,max_value=1001)
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0)
    if st.button("Create"):
        create_user(connection, user_id,name, age)
        st.success("User created successfully")

    # Read all users
    st.subheader("Read Users")
    if st.button("Read"):
        users = read_users(connection)
        # for user in users:
        #     st.write(f"ID: {user[0]}, Name: {user[1]}, Age: {user[2]}")
        headers = ["ID", "Name", "Age"]
        table = tabulate(users, headers, tablefmt="psql")
        st.text(table)
        
    # Update a user
    st.subheader("Update User")
    user_id = st.number_input("User ID to update", min_value=1)
    new_name = st.text_input("New Name")
    new_age = st.number_input("New Age", min_value=0)
    if st.button("Update"):
        update_user(connection, user_id, new_name, new_age)
        st.success("User updated successfully")

    # Delete a user
    st.subheader("Delete User")
    del_user_id = st.number_input("User ID to delete", min_value=1)
    if st.button("Delete"):
        delete_user(connection, del_user_id)
        st.success("User deleted successfully")






# Entry point of the script
if __name__ == "__main__":
    main()