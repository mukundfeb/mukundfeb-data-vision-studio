import pandas as pd
import streamlit as st
import duckdb

st.set_page_config(page_title="SQL Query", layout="wide")

# Styles
st.markdown("""
    <style>
        .main {
            font-family: 'Segoe UI', sans-serif;
        }
        h1 {
            color: #4CAF50;
            text-align: center;
            padding-top: 20px;
        }
        .sql-box textarea {
            border-radius: 10px;
            padding: 12px;
            font-size: 16px;
            font-family: monospace;
            border: 1px solid #ccc;
            width: 100%;
            min-height: 150px;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            font-size: 16px;
            border: none;
            border-radius: 10px;
            margin-top: 15px;
        }
        .stFileUploader {
            margin-top: 20px;
        }
        [data-testid="stSidebar"], [data-testid="collapsedControl"], #MainMenu, footer {
            display: none;
            visibility: hidden;
        }
    </style>
""", unsafe_allow_html=True)

# Header 
st.markdown("""
                    <div style='
                        background-color: #e8f5e9;
                        border-left: 7px solid #4CAF50;
                        border-radius: 10px;
                        padding: 20px;
                        font-family: "Segoe UI", sans-serif;
                        color: #333;
                        text-align: center;'>
                    <h1 style='color:#4CAF50;'>	🛠 SQL Workspace</h1>
            <p style='font-size: 18px; margin-top: 10px;'>✨ Let's get started on your SQL queries.</p>
        </div>
    </div>
                """, unsafe_allow_html=True)

# Data Check 
if 'uploaded_file' not in st.session_state:
    st.warning("⚠️ No data found. Please upload your data in the Dashboard first!")
else:
    df = st.session_state.uploaded_file

    if df is not None:
        # Fill missing values
        df = df.fillna(0)
        duckdb.register("dashboard_table", df)

        # Preview 
    st.markdown("""
           <div style='
               background-color: #E8F5E9;
               border-left: 6px solid #388E3C;
               border-radius: 10px;
               padding: 15px;
               margin-top: 20px;
               color: #333; 
           '>
               <h1>🤖 Data Preview</h1>
           </div>
       """, unsafe_allow_html=True)

    st.dataframe(df)
        #  SQL Editor
    st.markdown("""
            <div class="sql-box">
               <h3> 🧠 Write Your SQL Query Below:</h3>
               <textarea id="sql query" placeholder="SELECT * FROM dashboard_table LIMIT 10;"></textarea>
            </div>
        """, unsafe_allow_html=True)
    sql_query = st.text_area("SQL Query", height=200, key="sql_query")

        # Run SQL Button
    if st.button("▶️ Run Query"):
            with st.spinner("✅ Running Your SQL Query..."):
                try:
                    queries = [q.strip() for q in sql_query.split(";") if q.strip()]
                    last_result = None

                    for i, q in enumerate(queries):
                        st.markdown(f"📥 Executing Query {i+1}: `{q}`")
                        result = duckdb.query(q).to_df()
                        last_result = result

                    if last_result is not None:
                        st.success("✅ Last Query Successful!")
                        st.dataframe(last_result)

                        csv = last_result.to_csv(index=False).encode("utf-8")
                        st.download_button("⬇️ Download Result", csv, "query_result.csv", "text/csv")
                except Exception as e:
                    st.error(f"❌ Error: {e}")

        # Go back to Dashboard
    if st.button("🔙 Go back to Dashboard"):
            st.switch_page("pages/dashboard.py")
