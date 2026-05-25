# Earthquake-Insights-Project_1

PROJECT SUMMARY 

🌏 Global Earthquake Data Pipeline & Interactive Dashboard
Explore: Use the sidebar to read about the magic of understanding nature on the Home page, then switch to Project Analytics to run any of the 30 queries live!

📝 Project Summary 
As the world adopts more advanced tracking technology, we aren't just getting more raw numbers—we are discovering how to turn massive, chaotic streams of natural events into an organized, highly structured database system.

This project takes raw, messy global earthquake data, cleans it using fundamental data science statistics, stores it securely inside a MySQL relational database, and visualizes live trends through an interactive Streamlit web dashboard.

🛠️ Tools Used & Their Roles
Google Colab & Jupiter & Anaconda navigator
VS Code (Visual Studio Code)
MySQL & MySQL Workbench
GitHub

Skills take away From This Project : Python, SQL, Pandas & Null handling, Streamlit

🧠 Key Technical Learnings & Concepts Mastered

1. Data Scrubbing vs. File Handling
File Handling is the mechanical process of using Python to physically open, read, write, clone, or save data documents (like .csv, .txt, or binary files) on your computer's hard drive.
Data Scrubbing (Cleaning) is the analytical process of repairing the actual content inside those files—such as finding corrupt inputs, correcting data types, and handling missing parameters.

2. Deep Dive into Null Value Cleaning
The Golden Rule: We must never leave raw NULL holes in an analytical dataset. Even if a column contains more than 70% missing values, it points to a problem with the original recording equipment or reporting source.
The Strategy: Instead of leaving rows blank, we systematically clean them by replacing NULL inputs with standard fillers like 0 (for missing numerical sensor readings) or 'Unknown' (for text gaps).
Statistical Imputation: I mastered using Mean (average value for normally distributed numbers), Median (middle value to handle skewed numbers with extreme outliers), and Mode (most frequent entry for categories) to mathematically clean and fill data gaps without losing critical records.

3. VS Code & Package Management Environment
.py vs .ipynb Files: I learned that .ipynb (Jupyter Notebooks) are great for visual, step-by-step data exploration and chart testing, while .py (Python scripts) are required to build production-grade applications like Streamlit dashboards.
Using pip: Mastered using Python's package installer inside the terminal to build isolated environments, install libraries, and export a requirements.txt checklist so other developers can run my project instantly.

4. Advanced SQL & Dashboard Architecture
Dynamic Schema Alterations: Instead of manually editing tables in MySQL Workbench, I wrote automated Python code that inspects the database's hidden blueprints (information_schema.COLUMNS). If custom metrics like year, month, or depth_category are missing, the script heals itself by running ALTER TABLE and UPDATE routines.
Streamlit UI Architecture: Built a left-sidebar navigation menu separating the app into an educational Home space (focusing on Disaster Management themes) and a Project Analytics page that dynamically feeds the database 30 custom data questions on demand.

🚀 Project Features & Real-world Outcomes
Self-Healing Database Operations: The application checks table structures on boot-up, preventing repetitive execution crashes.
Advanced Statistical Insights: Instantly isolates complex patterns like ultra-deep tectonic shifts, high-frequency disaster zones, sensor quality gaps, and tsunami correlation risks.
Interactive Professional UI: Built with an interactive table grid layout allowing users to easily sort, filter, and review results dynamically.
Disaster Management Impact: By converting messy raw date strings and deep kilometer values into clean classifications like Shallow or Deep tremors, the project moves from simple arithmetic to meaningful public safety analysis.

📖 How to Navigate and Approach This Repository
Repository File Checklist
EQ_Project_1.py: use core analytics and sql connection
EQ_Project_2.py: The core backend script queries and frontend Streamlit application code.


How to Run and Test This Project
Prepare the Database: Import EarthQuakes.sql into your local MySQL Workbench and ensure your connection credentials match.
Activate Your Environment: Open your project folder in VS Code and activate your virtual sandbox:
Mac Laptop: source env/bin/activate
Windows Laptop: env\Scripts\activate
Boot Up the Dashboard: Run the following command in your terminal window: Bash  streamlit run EQ_Project_2.py
