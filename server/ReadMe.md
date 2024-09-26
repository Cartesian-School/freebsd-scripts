# Cartesian FreeBSD Automatic Installation Scripts

## Databases

### PostgreSQL

1. **PostgreSQL 17** - Installation script: [postgresql17_auto_installer.py](postgresql17_auto_installer.py)
2. **PostgreSQL 15, 16, or 17** - Multi-version installation script: [postgresql_multi_installer.py](postgresql_multi_installer.py)

### MySQL

1. **MySQL 8.4** - Installation script: [mysql84_auto_installer.py](mysql84_auto_installer.py)

### Description
These scripts provide an automated way to install and configure databases on FreeBSD.

- **PostgreSQL scripts**: The first script is dedicated to PostgreSQL 17, while the second supports installing versions 15, 16, or 17 based on user selection. Both scripts handle the entire installation process, configuration of `pg_hba.conf`, creation of a test database, and verification.
  
- **MySQL script**: The MySQL 8.4 installation script automates the process of setting up MySQL 8.4, configuring the charset to `utf8mb4`, securing the installation with `mysql_secure_installation`, and creating a test database. The script also provides a step-by-step guide to creating a new user and a new database from the command line after installation.

