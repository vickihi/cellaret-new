# Web Project 2 - Cellaret
Cellaret is a bilingual web application that helps users manage their beverage collections and explore the SAQ product catalog through a simple, user-friendly interface.

# TABLE OF CONTENTS
- [Team Members](#team-members)
- [ER Model](https://app.diagrams.net/#G1uI5tPZXW0piwWYsHi4QuV0FyxZVa4p_w#%7B%22pageId%22%3A%22A44Uredbnt4s9DRfil-q%22%7D)
- [Tech Stack](#tech-stack)
- [Installation Guide](#installation-guide)
- [Models API documentation](https://docs.google.com/document/d/1QUqMycmabYId3sL8fyMwKQ5-qFpc2TMJUuoC3NFHl4A/edit?tab=t.0#heading=h.sd0q0penlayf)
- [Continuous Integration](#continuous-integration)
- [Personas]()
- [Color palette & Typography system]()
- [Mockups]()


# TEAM MEMBERS
* Bradley Colbourne
* Jooeun Lee
* Weiwei Gou
* Xia He
* Xin He

# TECH STACK
Cellaret uses a lightweight, server-rendered Django stack to deliver a responsive bilingual web application for managing beverage collections. The architecture supports core features such as catalog browsing, cellar management, and user account functionality within a unified system.
### Backend
* Python + Django — Backend framework with Django Templates for server-side rendering
* SQLite3 — Local development database
### Frontend
* CSS — Basic styling
* Tailwind CSS — Utility-first CSS framework for styling
* Vanilla JavaScript — Lightweight client-side interactions
### External Services
* SAQ GraphQL API — External API used to fetch and synchronize the product catalog
### DevOps & Tooling
* Git + GitHub — Version control and collaboration
* GitHub Actions — Continuous integration (linting, formatting, testing)

  
# INSTALLATION GUIDE
## Prerequisites
Before running the project, make sure you have the following installed:

#### 1.  **Python (3.8+)**
-   **Installation:**
	-   **Windows:** Download and install from [Python.org](https://www.python.org/downloads/windows/)
	-   **Mac:** Recommended to install via Homebrew  ([Homebrew](https://brew.sh/))
        ```bash
	     brew install python
	    ```
-   **Verify installation:**
	-   **Windows:** 
		```bash
		 python --version
		```
	-   **Mac:**
		```bash
		 python3 --version
		```    
#### 2.  **uv** (Python package manager)
-   **Installation:**
    -   **Windows:** `scoop install uv` (requires [Scoop](https://scoop.sh/))  
    -   **Mac:** `brew install uv` (requires [Homebrew](https://brew.sh/)) 
-   **Verify installation:**
	```bash
	 uv --version
	```   
#### 3.  **Git**
-   **Installation:**
	-   **Windows:** Download and install from [Git for Windows](https://git-scm.com/download/win).
	    
	-   **macOS:** Install via Homebrew ([Homebrew](https://brew.sh/))
		   ```bash
			 brew install git
		   ```
-   **Verify installation:** 
	```bash
	 git --version
	```    
## Steps to Set Up the Project
#### 1. Clone the Repository
```bash
 git clone https://github.com/582-41W-VA/web-project-2-cellaret.git
 cd web-project-2-cellaret
```
#### 2. Install Dependencies 
This command installs all necessary packages in the project’s virtual environment.
```bash
 uv sync
```
#### 3. Apply Database Migrations
This will create the necessary database tables. 
```bash
 uv run manage.py migrate
```
> SQLite is Django’s default database, so for this project no extra setup is required.
#### 4. Create a Superuser 
This will create the Admin access.
```bash
 uv run manage.py createsuperuser
```
Follow the prompts to create the admin account:
-   **Username:** (e.g., `admin`) 
-   **Email address:** (e.g., `admin@test.com`)  
-   **Password:** (enter twice, characters will not be visible)
#### 5. Run the Development Server
```bash
 uv run manage.py runserver
```
#### 6. Access in Browser
-   **Main site:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)  
-   **Admin panel:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)  
    > Login using the superuser credentials you just created.
### Summary
1.  Install prerequisites (**Python + uv + Git**)
2.  **Clone** repository
3.  **Sync** dependencies 
4.  **Apply** migrations
5.  **Create** superuser
6.  **Run** server
7.  **Open** in browser
   
# CONTINUOUS INTEGRATION
CI runs automatically on every:
- `push` 
- `pull_request`

CI pipeline steps: 
Formatter check: 
```bash
uv run ruff format --check
```
Linter: 
```bash
uv run ruff check
```
Tests: 
```bash
uv run pytest
``` 
Workflow file:
- `.github/workflows/ci.yml`
