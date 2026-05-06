# Quick Start Guide

This guide provides the necessary commands to run the **FIND THE MATCH** application locally on your Windows machine.

## Prerequisites
Ensure you have **XAMPP** running with both the **Apache** and **MySQL** modules started.
The MySQL database named `find_the_match` should exist.

## 1. Activate the Virtual Environment
Before running any Python or Django commands, you must activate the virtual environment. Open a Command Prompt or PowerShell in the project directory (`c:\find_the_match`) and run:

```powershell
.\venv\Scripts\activate
```
*(You should see `(venv)` appear at the beginning of your command line prompt.)*

## 2. Run the Development Server
With the virtual environment active, start the Django development server:

```powershell
python manage.py runserver
```

You can now access the application in your browser at:
**[http://localhost:8000](http://localhost:8000)**

## 3. Important URLs and Default Accounts

- **Main Application**: `http://localhost:8000/`
- **Admin Panel**: `http://localhost:8000/admin/`

**Default Admin Account** (Use this to approve new students or test the Organizer view):
- **Username:** `admin`
- **Password:** `admin`

---

### Optional: Other Useful Commands

**If you make changes to your database models**, run these commands to update the database:
```powershell
python manage.py makemigrations
python manage.py migrate
```

**If you need to install dependencies on a new machine**, activate the virtual environment and run:
```powershell
pip install -r requirements.txt
```
