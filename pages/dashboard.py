import streamlit as st
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
# Set page title correctly
st.set_page_config(page_title="Dashboard", layout="wide")
st.markdown("""
    <style>
           <style>
    .dashboard-main {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding-top: 60px;
        font-family: 'Segoe UI', sans-serif;
        color: #0D47A1;
    }

    .dashboard-container {
        background-color: #E3F2FD;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        width: 90%;
        max-width: 1000px;
        margin: auto;
    }

    .dashboard-title {
        text-align: center;
        font-size: 30px;
        margin-bottom: 20px;
        color: #1976D2;
        font-weight: bold;
    }

    .dashboard-section {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 10px;
        margin-top: 15px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    }

    .dashboard-section h4 {
        font-size: 20px;
        margin-bottom: 10px;
        color: #1565C0;
    }

    .dashboard-section p {
        font-size: 16px;
        line-height: 1.5;
        color: #333;
    }

    .stButton>button {
        background-color: #1976D2;
        color: white;
        padding: 10px 16px;
        border: none;
        border-radius: 10px;
        font-size: 16px;
        margin-top: 10px;
    }

    .stSelectbox, .stTextInput, .stFileUploader, .stNumberInput {
        border-radius: 8px !important;
    }
</style>
""", unsafe_allow_html=True) 

# Application Header
st.markdown("""
                    <div style='
                        background-color: #e8f5e9;
                        border-left: 7px solid #4CAF50;
                        border-radius: 10px;
                        padding: 20px;
                        font-family: "Segoe UI", sans-serif;
                        color: #333;
                        text-align: center;'>
                    <h1 style='color:#4CAF50;'>	🤖 Welcome to Dashboard...</h1>
            <p style='font-size: 18px; margin-top: 10px;'>✨ Let's get started on your Data Analysis journey..</p>
        </div>
    </div>
                """, unsafe_allow_html=True)


# Hide sidebar and Streamlit default footer/menu
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        display: none;
    }
    [data-testid="collapsedControl"] {
        display: none;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Bullet points (centered)
st.markdown("""
<div style='
    background-color: #FFFFFF;
    border: 2px dashed #64B5F6;
    border-radius: 8px;
    padding: 20px;
    font-family: "Segoe UI", sans-serif;
    color: #1A237E;
    margin-top: 10px;
    <h2 style='color: #1565C0;'>🌟 Steps To Follow</h2>
    <ul style='text-align: left; font-size: 16px; line-height: 1.8; padding-left: 20px;'>
        <li>📁 Upload CSV files to instantly visualize data</li>
        <li>📊 View dynamic charts like bar, line, pie, heatmaps, and more</li>
        <li>🧠 Use preprocessed data to generate insights and predictions</li>
        <li>📝 Export visualizations as professional reports</li>
        <li>🗃️ Connect to SQL database for interactive dashboard filtering</li>
    </ul>
</div>
""", unsafe_allow_html=True)


# Explore dataset from internet
st.markdown("""
<div style='
    background-color: #f3f1ff;
    border-left: 6px solid #7C4DFF;
    border-radius: 10px;
    padding: 20px;
    font-family: "Segoe UI", sans-serif;
    color: #333;
    text-align: center;'>

<h3 style='color:#7C4DFF;'>🌍 Explore Datasets from the Web</h3>
<p style='font-size: 16px;'>🔎 Discover ready-to-use datasets on platforms like:</p>
<p>
  📦 <a href='https://www.kaggle.com/datasets' target='_blank' style='color:#3F51B5;'>Kaggle</a> &nbsp; | &nbsp;
  🏛️ <a href='https://data.gov.in/' target='_blank' style='color:#3F51B5;'>Data.gov</a> &nbsp; | &nbsp;
  🧠 <a href='https://www.reddit.com/r/datasets/' target='_blank' style='color:#3F51B5;'>Reddit Datasets</a>
</p>
<p style='font-size: 15px;'>Download your favorite dataset and upload it to explore with Data Vision Studio..</p>

</div>
""", unsafe_allow_html=True)

# file uploading session state
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None

# file uploader
st.markdown(""" 
            <style>
            .stfile-uploader {
               background-color: #E3F2FD;
               border: 2px dashed #64B5F6;
               border-radius: 10px;
               padding: 20px;
               font-family: "Segoe UI", sans-serif;
               color: #1A237E;
               text-align: center;
            }
            .stfile-uploader input[type="file"]{
               display: none;
            }
            .stfile-uploader label{
               display: inline-block;
               background-color: #64B5F6;
               color: white;
               padding: 10px 20px;
               border-radius: 10px;
               cursor: pointer;
               font-size: 16px;
            }
            </style>
            """, unsafe_allow_html=True)
st.markdown("""
   <div style='
                        background-color: #e8f5e9;
                        border-left: 7px solid #4CAF50;
                        border-radius: 10px;
                        padding: 20px;
                        font-family: "Segoe UI", sans-serif;
                        color: #333;
                        text-align: center;'>
                    <h3 style='color:#4CAF50;'>	🤖 Upload Your File Here...</h3>
            <p style='font-size: 18px; margin-top: 10px;'>✨ Get Instant Insights From Your data</p>
    </div>
                """, unsafe_allow_html=True)
uploaded_file = st.file_uploader("Upload your CSV file", type=['csv'], key='file_uploader')
if uploaded_file is not None:
    # Read the CSV File
    df = pd.read_csv(uploaded_file)
    st.session_state.uploaded_file = df
    st.success("file uploaded successfully!")

    # Display the DataFrame
    st.markdown("""
                    <div style='
                        background-color: #e8f5e9;
                        border-left: 7px solid #4CAF50;
                        border-radius: 10px;
                        padding: 20px;
                        font-family: "Segoe UI", sans-serif;
                        color: #333;
                        text-align: center;'>
                    <h3 style='color:#4CAF50;'>🤖 Here Is Your Data</h3>
                    </div>
                """, unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True)
    st.markdown("""
   <div style='
                        background-color: #e8f5e9;
                        border-left: 7px solid #4CAF50;
                        border-radius: 10px;
                        padding: 20px;
                        font-family: "Segoe UI", sans-serif;
                        color: #333;
                        text-align: center;'>
                    <h3 style='color:#4CAF50;'>	🤖 Encode Your File Here For Better Insights...</h3>
    </div>
                """, unsafe_allow_html=True)
    # Encoding options
    processing_options=st.selectbox("select processing technique u want",
    ["LabelEncoder",
     "Standard Scaler"])
    if processing_options == "LabelEncoder":
      label = LabelEncoder()
      st.markdown("""
                  <div style='
                      background-color: #E8F5E9;
                      border-left: 6px solid #388E3C;
                      border-radius: 10px;
                      padding: 15px;
                      margin-top: 20px;
                      font-family: "Segoe UI", sans-serif;
                      text-align: center;
                      color: #1B5E20;'>
                      <h4> 📊 Applying LabelEncoder To The Data</h4>
                  </div>
      """, unsafe_allow_html=True)
      for col in df.select_dtypes(include='object').columns.tolist():
        df[col] = label.fit_transform(df[col])
    elif processing_options == "Standard Scaler":
       scaler = StandardScaler()
       st.markdown("""
                   <div style='
                       background-color: #E8F5E9;
                       border-left: 6px solid #388E3C;
                       border-radius: 10px;
                       padding: 15px;
                       margin-top: 20px;
                       font-family: "Segoe UI", sans-serif;
                       text-align: center;
                       color: #1B5E20;'>
                       <h4> 📊 Applying Standard Scaler To The Data</h4>
                   </div>
       """, unsafe_allow_html=True)
       num_cols = df.select_dtypes(include=['int64', 'float64']).columns
       df[num_cols] = scaler.fit_transform(df[num_cols])
    st.dataframe(df, use_container_width=True)
    st.markdown("""
                <div style='
    background-color: #E3F2FD;
    border-left: 6px solid #2196F3;
    border-radius: 10px;
    padding: 20px;
    font-family: "Segoe UI", sans-serif;
    color: #0D47A1;
    text-align: center;'>
                <h2>🤖 Want Sql Query To Update Data<span style="color:#1976D2;">Dashboard</span>!</h2>
<p style='font-size: 18px;'>✨ Let's get started Lets Integrate SQL With your Data</p>

</div>
""", unsafe_allow_html=True)
    if st.button("Generate SQL Query"):
        st.switch_page("pages/sql_query.py")
                

#switch to visualization page
if st.button("Go to Visualization Page"):
    if st.session_state.uploaded_file is not None:
        st.switch_page("pages/visualization.py")
    else:
        st.warning("please upload a csv file to proceed!")