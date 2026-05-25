import pandas as pd
import streamlit as st
import pymysql
from sqlalchemy import create_engine, text

# ==========================================
# 1. DATABASE CONNECTION SETUP
# ==========================================

# Step A: Connect to MySQL server generally
conn = pymysql.connect(
    host="localhost", user="root", password="Datascience2025"
)

# Step B: Tell MySQL to open your specific database folder
cursor = conn.cursor()
cursor.execute("USE earthquakes;")

# Step C: Setup the high-speed SQLAlchemy engine lane for Pandas queries
engine = create_engine(
    "mysql+pymysql://root:Datascience2025@localhost/earthquakes"
)


# ==========================================
# 2. SMART AUTOMATED COLUMN VERIFICATION
# ==========================================
def add_column_if_missing(cursor, table_name, column_name, column_type_sql):
    cursor.execute(
        """
        SELECT COUNT(*) FROM information_schema.COLUMNS
        WHERE TABLE_SCHEMA=%s AND TABLE_NAME=%s AND COLUMN_NAME=%s
        """,
        ("earthquakes", table_name, column_name),
    )
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type_sql};"
        )


# Run the smart checks for all 5 custom metrics
add_column_if_missing(cursor, "EQ", "year", "INT")
add_column_if_missing(cursor, "EQ", "month", "INT")
add_column_if_missing(cursor, "EQ", "hour", "INT")
add_column_if_missing(cursor, "EQ", "day_of_week", "VARCHAR(20)")
add_column_if_missing(cursor, "EQ", "depth_category", "VARCHAR(20)")
conn.commit()

# Automatically refresh/fill those columns with calculated time & depth rules
with engine.begin() as db_modifier:
    db_modifier.execute(text("UPDATE EQ SET year = YEAR(time);"))
    db_modifier.execute(text("UPDATE EQ SET month = MONTH(time);"))
    db_modifier.execute(text("UPDATE EQ SET hour = HOUR(time);"))
    db_modifier.execute(text("UPDATE EQ SET day_of_week = DAYNAME(time);"))
    db_modifier.execute(
        text(
            "UPDATE EQ SET depth_category = IF(depth_km < 50, 'Shallow', 'Deep');"
        )
    )


# ==========================================
# 3. THE 30 QUERIES DICTIONARY
# ==========================================
QUERIES = {
    "1. Top 10 Strongest Earthquakes": """
        SELECT id, time, place, mag 
        FROM EQ 
        ORDER BY mag DESC 
        LIMIT 10;
    """,
    "2. Top 10 Deepest Earthquakes": """
        SELECT id, time, place, depth_km 
        FROM EQ 
        ORDER BY depth_km DESC 
        LIMIT 10;
    """,
    "3. Severe Shallow Earthquakes": """
        SELECT id, time, place, mag, depth_km 
        FROM EQ 
        WHERE depth_km < 50 AND mag > 7.5;
    """,
    "4. Average Depth per Location Area": """
        SELECT place, AVG(depth_km) AS avg_depth
        FROM EQ 
        GROUP BY place 
        LIMIT 10;
    """,
    "5. Average Magnitude per Calculation Method": """
        SELECT magType, AVG(mag) AS avg_magnitude
        FROM EQ 
        GROUP BY magType;
    """,
    "6. Year with the Most Total Earthquakes": """
        SELECT year, COUNT(*) AS total_earthquakes
        FROM EQ 
        GROUP BY year 
        ORDER BY total_earthquakes DESC 
        LIMIT 1;
    """,
    "7. Month with the Highest Number of Earthquakes": """
        SELECT month, COUNT(*) AS total_earthquakes
        FROM EQ 
        GROUP BY month 
        ORDER BY total_earthquakes DESC;
    """,
    "8. Day of the Week with Most Earthquakes": """
        SELECT day_of_week, COUNT(*) AS total_earthquakes
        FROM EQ 
        GROUP BY day_of_week 
        ORDER BY total_earthquakes DESC;
    """,
    "9. Count of Earthquakes per Hour of the Day": """
        SELECT hour, COUNT(*) AS total_earthquakes
        FROM EQ 
        GROUP BY hour 
        ORDER BY hour ASC;
    """,
    "10. Most Active Reporting Network Agency": """
        SELECT net, COUNT(*) AS total_reports
        FROM EQ 
        GROUP BY net 
        ORDER BY total_reports DESC 
        LIMIT 5;
    """,
    "11. Top 5 Places with the Highest Single Significance Score": """
        SELECT place, MAX(sig) AS max_significance
        FROM EQ 
        GROUP BY place 
        ORDER BY max_significance DESC 
        LIMIT 5;
    """,
    "12. Total Accumulated Significance per Location": """
        SELECT place, SUM(sig) AS total_significance
        FROM EQ 
        GROUP BY place 
        ORDER BY total_significance DESC 
        LIMIT 10;
    """,
    "13. Average Impact Significance across Alert Levels": """
        SELECT alert, AVG(sig) AS avg_significance
        FROM EQ 
        GROUP BY alert;
    """,
    "14. Count of Reviewed Records vs Automated Records": """
        SELECT status, COUNT(*) AS total_records
        FROM EQ 
        GROUP BY status;
    """,
    "15. Breakdown Count by Activity Phenomenon Type": """
        SELECT type, COUNT(*) AS total_events
        FROM EQ 
        GROUP BY type;
    """,
    "16. Most Common Groupings of Associated Data Streams": """
        SELECT types, COUNT(*) AS streaming_frequency
        FROM EQ 
        GROUP BY types 
        ORDER BY streaming_frequency DESC 
        LIMIT 5;
    """,
    "17. Average Machine Recording Errors per Location": """
        SELECT place, AVG(rms) AS avg_rms, AVG(gap) AS avg_gap
        FROM EQ 
        GROUP BY place 
        LIMIT 10;
    """,
    "18. Events Backed by Strong Machine Station Coverage": """
        SELECT id, place, nst 
        FROM EQ 
        WHERE nst > 100 
        ORDER BY nst DESC 
        LIMIT 10;
    """,
    "19. Number of Tsunamis Triggered per Calendar Year": """
        SELECT year, SUM(tsunami) AS total_tsunamis
        FROM EQ 
        GROUP BY year 
        ORDER BY year ASC;
    """,
    "20. Distribution Count across Official Warning Alerts": """
        SELECT alert, COUNT(*) AS total_alerts
        FROM EQ 
        GROUP BY alert 
        ORDER BY total_alerts DESC;
    """,
    "21. Top 5 Highest Average Magnitude Places": """
        SELECT place, AVG(mag) AS avg_magnitude
        FROM EQ 
        GROUP BY place 
        ORDER BY avg_magnitude DESC 
        LIMIT 5;
    """,
    "22. Identification of Ultra-Deep Tectonic Earthquakes": """
        SELECT id, place, depth_km, year 
        FROM EQ 
        WHERE depth_km > 300 
        LIMIT 10;
    """,
    "23. Total Earthquake Activity Counts per Year": """
        SELECT year, COUNT(*) AS incident_count
        FROM EQ 
        GROUP BY year 
        ORDER BY year ASC;
    """,
    "24. Top 5 Locations Sorted by Frequency and Size": """
        SELECT place, COUNT(*) AS incident_count, AVG(mag) AS avg_magnitude
        FROM EQ 
        GROUP BY place 
        ORDER BY incident_count DESC, avg_magnitude DESC 
        LIMIT 5;
    """,
    "25. Average Depth of Earthquakes near the Equator Line": """
        SELECT place, AVG(depth_km) AS avg_depth
        FROM EQ 
        WHERE latitude BETWEEN -5.0 AND 5.0 
        GROUP BY place 
        LIMIT 10;
    """,
    "26. Count of Shallow Focus versus Deep Focus Earthquakes": """
        SELECT depth_category, COUNT(*) AS total_count
        FROM EQ 
        GROUP BY depth_category;
    """,
    "27. Average Magnitude Difference between Tsunamis vs Normal": """
        SELECT tsunami, AVG(mag) AS avg_magnitude
        FROM EQ 
        GROUP BY tsunami;
    """,
    "28. Identify Low Quality Records with Large Sensor Gaps": """
        SELECT id, place, gap, rms 
        FROM EQ 
        WHERE gap > 180 
        ORDER BY rms DESC 
        LIMIT 10;
    """,
    "29. Earliest Recorded Seismic Records Order List": """
        SELECT id, place, time, year, month 
        FROM EQ 
        ORDER BY time ASC 
        LIMIT 10;
    """,
    "30. Locations with Highest Frequency of Deep Focus Tremors": """
        SELECT place, COUNT(*) AS deep_tremor_count
        FROM EQ 
        WHERE depth_km > 300 
        GROUP BY place 
        ORDER BY deep_tremor_count DESC 
        LIMIT 5;
    """,
}

# ==========================================
# 4. STREAMLIT USER INTERFACE (UI) WITH SIDEBAR NAVIGATION
# ==========================================

# 1. Create the Left Sidebar Radio Menu Navigation
with st.sidebar:
    st.header("🧭 Navigation")
    page = st.radio(
        "Go to:",
        ["🏠 Intro", "📊 Project Analytics"]
    )
    st.markdown("---")
    st.caption("Developed for GUVI Earthquake Data Science Project 2026")

# ---------------------------------------------------------
# PAGE 1: HOME PAGE (Earthquake Theme & Disaster Management)
# ---------------------------------------------------------
if page == "🏠 Intro":
    st.title("🌏 Global Earthquake Insights")
    st.subheader("Understanding our dynamic planet to build a safer tomorrow.")
    
    # Theme Banner & Imagery
    st.info(
        "💡 *'Understanding Nature is always MAGIC.'* This project tracks live tectonic "
        "movements across our globe to turn chaotic natural events into structured data patterns."
    )
    
    # Educational Content Sections
    st.markdown("### 🌋 Track Earthquakes?")
    st.write(
        "This project was designed to help us look beneath the Earth's crust and understand "
        "what is happening around the world. By analyzing 5 years of datasets "
        "severely seismic events occur, we can identify high-risk fault zones."
    )
    
    st.markdown("### 🛡️ All Learn Disaster Management to Protect Communities")
    st.write(
        "Disaster Management isn't just about responding after an emergency happens—it starts with **Data and Prevention**. "
        "Through data analysis, we learn 30 key insights about earthquake patterns, magnitudes, locations,"
        "and track & alert systems to build systems that protect communities, secure regional infrastructure, "
        "and ultimately **save human lives**."
    )

    # Simple Visual Metric Cards for the Home Theme
    st.markdown("---")

    st.markdown("### 🛡️ Intro")
    st.write(
        "Hi I am Madhivanan R R, Worked as a Senior UI UX Designer, over all 10+ years of experience in the IT industry."
        " and now transitioning into Data Science and AI ML. "
        "I am excited to apply my skills and knowledge in the field of Data Science and AI ML to contribute to innovative projects and drive impactful results."
    )
    st.image("Madhivanan.jpeg", width=200)


# ---------------------------------------------------------
# PAGE 2: PROJECT PAGE (The 30 Live SQL Queries)
# ---------------------------------------------------------
elif page == "📊 Project Analytics":
    st.title("📊 Earthquake Data Analysis Dashboard")
    st.write(
        "Select any analytical problem statement from the dropdown menu to fetch data live from your MySQL database."
    )

    st.markdown("---")

    # Render the interactive Dropdown Selection Menu
    task = st.selectbox("Choose Task Statement", list(QUERIES.keys()))

    # Render the Run Action Button
    if st.button("Run Analytics Query"):
        with st.spinner("Querying the database server..."):
            try:
                # Pick the specific SQL statement based on selected key string
                sql_code = QUERIES[task]

                # Execute the query using Pandas and text wrappers
                result_df = pd.read_sql(text(sql_code), con=engine)

                # Display the interactive results grid layout on the web screen
                st.subheader(f"📋 Results for: {task}")
                st.dataframe(result_df, use_container_width=True)

                st.success("✨ Data query executed successfully!")
            except Exception as e:
                st.error(f"❌ An error occurred while retrieving data: {e}")