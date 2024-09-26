import subprocess
import os
import sys

def display_clean():
    os.system('clear')
    print("")

# Function to install required packages
def install_dependencies():
    print("Installing necessary dependencies...")

    # Install psycopg2 dependency for Python
    subprocess.run(["pkg", "install", "-y", "py311-psycopg2"], check=True)

    print("Dependencies installed successfully.")

# Function to install PostgreSQL
def install_postgresql(version):
    # Install the selected PostgreSQL version
    package_name = f"postgresql{version}-server"
    print(f"Installing PostgreSQL {version}...")
    subprocess.run(["pkg", "install", "-y", package_name], check=True)
    
    # Enable PostgreSQL service
    subprocess.run(["sysrc", f"postgresql_enable=YES"], check=True)

    # Initialize the database cluster
    subprocess.run([f"/usr/local/etc/rc.d/postgresql", "initdb"], check=True)

    # Start the PostgreSQL service
    subprocess.run([f"service", "postgresql", "start"], check=True)

    print(f"PostgreSQL {version} successfully installed and started.")

# Function to configure PostgreSQL
def configure_postgresql():
    # Set up PostgreSQL for external connections
    pg_hba_conf = "/usr/local/pgsql/data/pg_hba.conf"
    with open(pg_hba_conf, 'a') as f:
        f.write("host    all             all             127.0.0.1/32            trust\n")
        f.write("host    all             all             ::1/128                 trust\n")
    print("Configured pg_hba.conf for local connections.")

# Function to create a test database and confirm its creation
def create_test_database():
    import psycopg2
    from psycopg2 import sql

    # Create a PostgreSQL user and database
    print("Creating a test user and database...")
    
    # Create a new user and database
    subprocess.run(["su", "-l", "pgsql", "-c", "createuser -s test_user"], check=True)
    subprocess.run(["su", "-l", "pgsql", "-c", "createdb test_db -O test_user"], check=True)
    
    # Connect to the database and create a test table
    conn = psycopg2.connect(dbname="test_db", user="test_user", password="")
    cur = conn.cursor()
    
    cur.execute("""
        CREATE TABLE test_table (
            id SERIAL PRIMARY KEY,
            message TEXT
        );
    """)
    
    cur.execute("INSERT INTO test_table (message) VALUES (%s)", ("All OK",))
    
    # Confirm the test database creation
    cur.execute("SELECT * FROM test_table;")
    result = cur.fetchall()
    
    if result and result[0][1] == "All OK":
        print("Test database successfully created and verified!")
    else:
        print("There was an issue with the test database creation.")
    
    cur.close()
    conn.close()

def main():
    display_clean()
    
    # Install dependencies (PostgreSQL client and psycopg2)
    install_dependencies()

    # User to choose PostgreSQL version
    while True:
        version = input("Choose PostgreSQL version to install (14, 15, 16, 17): ").strip()
        if version in ['14', '15', '16', '17']:
            break
        print("Invalid input. Please enter one of the versions: 14, 15, 16, 17.")
    
    # Install PostgreSQL selected version
    install_postgresql(version)
    
    # Configure PostgreSQL
    configure_postgresql()
    
    # Create and confirm test database
    create_test_database()

# Run the main script
if __name__ == "__main__":
    main()
