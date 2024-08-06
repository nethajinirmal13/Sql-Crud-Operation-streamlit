import streamlit as st
import mysql.connector
from mysql.connector import Error
from tabulate import tabulate

def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
            port=4000,
            user="2NWb96BauSzhCfv.root",
            password="glYD5rr41K6XQFlI",
            database="userdetails",
        )
        if connection.is_connected():
            st.sidebar.success("Connection to MySQL DB successful")
    except Error as e:
        st.sidebar.error(f"The error '{e}' occurred")
    return connection


def create_table(connection, table_name):
    cursor = connection.cursor()
    query = f"CREATE TABLE {table_name} (id INT, name VARCHAR(50), age INT)"
    cursor.execute(query)
    connection.commit()

    
    
def show_tables(connection):
    cursor=connection.cursor()
    query="SHOW TABLES"
    cursor.execute(query)
    tables=cursor.fetchall()
    return tabulate(tables,headers=[i[0] for i in cursor.description],tablefmt='psql')
    
    

def create_user(connection, table_name, user_id, name, age):
    cursor = connection.cursor()
    query = f"INSERT INTO {table_name} (id, name, age) VALUES (%s, %s, %s)"
    cursor.execute(query, (user_id, name, age))
    connection.commit()

def read_users(connection, table_name):
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    return rows

def update_user(connection, table_name, user_id, name, age):
    cursor = connection.cursor()
    query = f"UPDATE {table_name} SET name = %s, age = %s WHERE id = %s"
    cursor.execute(query, (name, age, user_id))
    connection.commit()

def delete_user(connection, table_name, user_id):
    cursor = connection.cursor()
    query = f"DELETE FROM {table_name} WHERE id = %s"
    cursor.execute(query, (user_id,))
    connection.commit()

# Main function to create the Streamlit app interface
def main():
    st.title("MySQL CRUD Operations")

    # Connect to MySQL
    connection = create_connection()

    # Sidebar navigation
    page = st.sidebar.selectbox("Choose an action", ["Select","Create Table", "Create User", "Read Users", "Update User", "Delete User"])



    # Create a new table
    if page == "Create Table":
        st.subheader("Create New Table")
        table_name = st.text_input("Table Name")
        if st.button("Create Table"):
            create_table(connection, table_name)
            st.success(f"New table '{table_name}' created successfully")

    
    
    # Select table for other operations
    
    
    st.sidebar.subheader("Select Table")
    selected_table = st.sidebar.text_input("Enter Table Name")
    
    st.sidebar.subheader("Display Tables")
    if  st.sidebar.button("Show"):
        
        tables = show_tables(connection)
        
        if tables:
            st.sidebar.write(tables)
        else:
            st.sidebar.write("No tables found.")



    if selected_table:
        if page == "Create User":
            st.subheader("Create User")
            user_id = st.number_input("ID", min_value=0, max_value=1001)
            name = st.text_input("Name")
            age = st.number_input("Age", min_value=0)
            if st.button("Create"):
                create_user(connection, selected_table, user_id, name, age)
                st.success("User created successfully")

        elif page == "Read Users":
            st.subheader("Read Users")
            if st.button("Read"):
                users = read_users(connection, selected_table)
                headers = ["ID", "Name", "Age"]
                table = tabulate(users, headers, tablefmt="psql")
                st.text(table)

        elif page == "Update User":
            st.subheader("Update User")
            user_id = st.number_input("User ID to update", min_value=1)
            new_name = st.text_input("New Name")
            new_age = st.number_input("New Age", min_value=0)
            if st.button("Update"):
                update_user(connection, selected_table, user_id, new_name, new_age)
                st.success("User updated successfully")

        elif page == "Delete User":
            st.subheader("Delete User")
            del_user_id = st.number_input("User ID to delete", min_value=1)
            if st.button("Delete"):
                delete_user(connection, selected_table, del_user_id)
                st.success("User deleted successfully")

# Entry point of the script
if __name__ == "__main__":
    main()
