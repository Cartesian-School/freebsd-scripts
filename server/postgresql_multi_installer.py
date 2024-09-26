import subprocess
import os
import psycopg2

# Function to display and clean the screen
def display_clean():
    os.system('clear')
    print("")

# Function to install necessary dependencies and PostgreSQL (for any version)
def install_postgresql(version):
    print(f"Installing PostgreSQL {version} and necessary dependencies...")
    
    # Install PostgreSQL server, client, and psycopg2 dependencies for the selected version
    package_name = f"postgresql{version}-server"
    client_package = f"postgresql{version}-client"
    psycopg2_packages = ["py311-psycopg2", "py311-psycopg2cffi", "py311-types-psycopg2"]
    
    subprocess.run(["pkg", "install", "-y", package_name, client_package] + psycopg2_packages, check=True)
    
    # Enable PostgreSQL service
    subprocess.run(["sysrc", "postgresql_enable=YES"], check=True)

    # Initialize the PostgreSQL database cluster
    print("Initializing PostgreSQL database...")
    subprocess.run([f"/usr/local/etc/rc.d/postgresql", "initdb"], check=True)

    # Start PostgreSQL service
    subprocess.run(["service", "postgresql", "start"], check=True)

    # Check PostgreSQL service status
    subprocess.run(["service", "postgresql", "status"], check=True)

# Function to configure PostgreSQL (pg_hba.conf)
def configure_postgresql(version):
    # Print the current listen_addresses setting from postgresql.conf
    conf_path = f"/var/db/postgres/data{version}/postgresql.conf"
    subprocess.run(["grep", "listen_addresses", conf_path], check=True)

    # Backup the original pg_hba.conf
    pg_hba_conf_path = f"/var/db/postgres/data{version}/pg_hba.conf"
    subprocess.run(["cp", "-p", pg_hba_conf_path, f"{pg_hba_conf_path}.org"], check=True)
    
    # Update pg_hba.conf with new settings
    print("Configuring pg_hba.conf...")
    pg_hba_content = '''
    local   all             all                                     peer
    host    all             all             127.0.0.1/32            ident
    host    all             all             ::1/128                 ident
    local   replication     all                                     peer
    host    replication     all             127.0.0.1/32            ident
    host    replication     all             ::1/128                 ident
    '''
    
    with open(pg_hba_conf_path, 'w') as f:
        f.write(pg_hba_content)
    
    print("pg_hba.conf configured successfully.")

    # Restart PostgreSQL service to apply the changes
    subprocess.run(["service", "postgresql", "restart"], check=True)

# Function to create and delete a test database
def create_and_delete_test_db():
    print("Creating test database 'test_db'...")

    # Connect to PostgreSQL as the default superuser
    conn = psycopg2.connect(dbname="postgres", user="postgres")
    conn.autocommit = True
    cur = conn.cursor()

    # Create test database and test user
    cur.execute("CREATE DATABASE test_db;")
    cur.execute("CREATE USER test_user WITH PASSWORD 'password';")
    cur.execute("GRANT ALL PRIVILEGES ON DATABASE test_db TO test_user;")

    print("Test database 'test_db' created successfully.")
    
    # Connect to the new test database
    conn_test_db = psycopg2.connect(dbname="test_db", user="test_user", password="password")
    cur_test_db = conn_test_db.cursor()

    # Create a test table and insert a value
    cur_test_db.execute("CREATE TABLE test_table (id SERIAL PRIMARY KEY, message TEXT);")
    cur_test_db.execute("INSERT INTO test_table (message) VALUES ('All OK');")
    
    # Check the inserted value
    cur_test_db.execute("SELECT message FROM test_table;")
    result = cur_test_db.fetchone()
    if result and result[0] == "All OK":
        print("Test data inserted and verified in 'test_table'.")

    # Clean up: close the connection to the test database
    cur_test_db.close()
    conn_test_db.close()

    # Delete test database
    cur.execute("DROP DATABASE test_db;")
    cur.execute("DROP USER test_user;")

    print("Test database 'test_db' and user 'test_user' were successfully deleted.")

    # Close the connection
    cur.close()
    conn.close()

# Function to display instructions for creating a new user and database
def display_instructions():
    print("""
    ===========================================
    Steps to create a new PostgreSQL user and database:
    1. Log in to the PostgreSQL shell as the superuser:
       $ sudo -u postgres psql
    2. Create a new user:
       postgres=# CREATE USER your_username WITH PASSWORD 'your_password';
    3. Create a new database:
       postgres=# CREATE DATABASE your_database;
    4. Grant privileges to the new user on the new database:
       postgres=# GRANT ALL PRIVILEGES ON DATABASE your_database TO your_username;
    5. Exit the PostgreSQL shell:
       postgres=# \\q
    ===========================================
    """)

# Main script flow
def main():
    display_clean()

    # Confirm PostgreSQL installation
    while True:
        version = input("Choose PostgreSQL version to install (15, 16, 17): ").strip()
        if version in ['15', '16', '17']:
            break
        print("Invalid input. Please enter one of the versions: 15, 16, 17.")
    
    # Confirm installation
    while True:
        choice = input(f"Do you want to install PostgreSQL {version} and configure it? (y/n): ").strip().lower()
        if choice in ['y', 'n']:
            break
        print("Invalid input. Please enter 'y' for yes or 'n' for no.")

    if choice == 'y':
        # Install PostgreSQL for the selected version
        install_postgresql(version)
        
        # Configure PostgreSQL with pg_hba.conf
        configure_postgresql(version)

        # Create and delete a test database
        create_and_delete_test_db()
        
        print(f"PostgreSQL {version} installation and configuration completed successfully.")
        
        # Display instructions for creating a new user and database
        display_instructions()
    else:
        print(f"PostgreSQL {version} installation skipped.")

# Run the main script
if __name__ == "__main__":
    main()
