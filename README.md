# Web Project 2 - Cellaret
## TABLE OF CONTENTS

- [Team Members](#team-members)
- [Installation Guide](#installation-guide)
  - [Prerequisites](#prerequisites)
  - [Steps to Set Up the Project](#steps-to-set-up-the-project)
  - [Summary](#summary)

## TEAM MEMBERS
* Bradley Colbourne
* Jooeun Lee
* Weiwei Gou
* Xia He
* Xin He
  
 
## INSTALLATION GUIDE

### Prerequisites
Before running the project, make sure you have the following installed:

#### 1.  **Python (3.8+)**

-   **Installation:**
  
	-   **Windows:** Download and install from [Python.org](https://www.python.org/downloads/)
	   
	-   **Mac:** Recommended to install via Homebrew  ([Homebrew](https://brew.sh/)):  `brew install python`
	
-   **Verify installation:**
        
    ```bash
      # Windows
      python --version
      
      # Mac
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
	    
	-   **macOS:** Install via Homebrew: `brew install git` or run `git --version` to trigger the auto-installer.
    
-   **Verify installation:** 
	```bash
	 git --version
	```    
### Steps to Set Up the Project
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

> SQLite is used by Django by default, so no extra setup is required.

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
