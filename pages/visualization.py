import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from fpdf import FPDF
from PIL import Image
from io import BytesIO
# set page title correctly
st.set_page_config(page_title="visualization", layout="wide")
st.markdown("""
            <style>
    .visual-main {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding-top: 60px;
        font-family: 'Segoe UI', sans-serif;
        color: #1A237E;
    }

    .visual-container {
        background-color: #F3F7FA;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        width: 90%;
        max-width: 1100px;
        margin: auto;
    }

    .visual-title {
        text-align: center;
        font-size: 28px;
        margin-bottom: 20px;
        color: #0D47A1;
        font-weight: bold;
    }

    .visual-section {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        margin-top: 15px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    }

    .visual-section h4 {
        font-size: 20px;
        color: #1565C0;
        margin-bottom: 10px;
    }

    .visual-section p {
        font-size: 16px;
        line-height: 1.6;
        color: #333;
    }

    .stButton>button {
        background-color: #0288D1;
        color: white;
        padding: 10px 16px;
        border: none;
        border-radius: 10px;
        font-size: 16px;
        margin-top: 10px;
    }

    .stSelectbox, .stFileUploader, .stRadio, .stCheckbox {
        border-radius: 8px !important;
    }

    .visual-chart-title {
        font-size: 18px;
        color: #0D47A1;
        margin-top: 20px;
        text-align: center;
    }

</style>
""", unsafe_allow_html=True)
# Title
st.markdown("""
<div style='
    background-color: #F3E5F5;
    border-left: 6px solid #9C27B0;
    border-radius: 10px;
    padding: 20px;
    font-family: "Segoe UI", sans-serif;
    color: #4A148C;
    text-align: center;'>

<h2>📈 Data Explorer</h2>
<p style='font-size: 18px;'>🔍 Look for patterns in your data!</p>
</div>
""", unsafe_allow_html=True)
# Add Steps to Follow
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
        <li>🔍 <strong>Select the columns</strong> you want to analyze or visualize.</li>
        <li>📊 <strong>Choose your chart type</strong> – Bar, Line, Scatter, Pie, Heatmap, and more.</li>
        <li>⚙️ <strong>Customize</strong> the chart: Configure axes, titles, legends, and formatting.</li>
        <li>💾 <strong>Save charts</strong> for report generation if needed.</li>
        <li>📤 <strong>Export or download</strong> the visual as a PDF report.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

#hide the side bar
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
# data uploading session state
if 'uploaded_file' not in st.session_state:
    st.warning("no data found please upload your data in the dashboard first!")
else:
    df= st.session_state.uploaded_file
    if df is not None:
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

<h1>🤖 Data Preview</h1>
</div>
""", unsafe_allow_html=True)
st.dataframe(df)

# Visualizations options
st.markdown("""
            <div style='
               background-color: #E3F2FD;
               border-left: 6px solid #42A5F5;
               border-radius: 10px;
               padding: 20px;
               font-family: "Segoe UI", sans-serif;
               color: #0D47A1;
               text-align: center;'>
               <h2>🌐 Insight Explorer</h2>
               <p style='font-size: 16px;'>Explore your data with various visualization techniques.</p>
           </div>
       """, unsafe_allow_html=True)
st.markdown("""
            <div style='
                background-color: #E3F2FD;
                border-left: 6px solid #42A5F5;
                border-radius: 10px;
                padding: 20px;
                font-family: "Segoe UI", sans-serif;
                color: #0D47A1;
                text-align: center;'>
                <h3> 🤖 Choose your visualization type</h3>
                </div>
            </div>
        """, unsafe_allow_html=True)
visual_options=st.selectbox("select the type of visualization u want to perform",
            ["Bar Chart",
             "Line Chart",
             "Scatter plot",
             "Heat Map",
             "Box Plot",
             "Histogram",
             "Pair Plot",
             "violin plot",
             "Pie Chart",
             "Bubble Chart"])
numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
filtered_df = df.copy()
if visual_options == "Bar Chart":
    st.markdown("""
                <h3 style='text-align: center; color: #4CAF50; font-size: 20px; font-family: "segoe UI", sans-serif;">
                    1. Bar Chart
                </h3>
                """, unsafe_allow_html=True)
    page = st.number_input("Select Page Number", min_value=1, max_value=100, value=1, step=1)
    items_per_page = st.number_input("Items per page", min_value=1, max_value=100, value=10, step=1)
    start = (page - 1) * items_per_page
    end = start + items_per_page
    x = st.selectbox("Select X-axis", numeric_cols + categorical_cols)
    y = st.selectbox("Select Y-axis", numeric_cols + categorical_cols)
    x_range = st.slider("Select X-axis Range", int(filtered_df[x].min()), int(filtered_df[x].max()), (int(filtered_df[x].min()), int(filtered_df[x].max())))
    y_range = st.slider("Select Y-axis Range", int(filtered_df[y].min()), int(filtered_df[y].max()), (int(filtered_df[y].min()), int(filtered_df[y].max())))
    filtered_df = df[(df[x] >= x_range[0]) & (df[x] <= x_range[1]) & (df[y] >= y_range[0]) & (df[y] <= y_range[1])].dropna().iloc[start:end]
    if st.button("Generate Bar Chart"):
        fig, ax = plt.subplots(figsize=(20, 10))  # adjust height if needed
        sns.barplot(data=filtered_df, x=x, y=y, ax=ax)

        # Rotate X labels if categorical
        if filtered_df[x].dtype == "object" or filtered_df[x].nunique() > 20:
           ax.set_xticklabels(ax.get_xticklabels(), rotation=90)

        # Title and layout
        ax.set_title(f"{y} vs {x} (Page {page})")
        plt.tight_layout()

        # Display in Streamlit
        st.pyplot(fig)

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
                        <h4> 📊 Bar Chart Generated Successfully!</h4>
                    </div>
        """, unsafe_allow_html=True)
        chart_buffer = BytesIO()
        fig.savefig(chart_buffer, format='png')
        chart_buffer.seek(0)
        if "chart_images" not in st.session_state:
           st.session_state.chart_images = []
           st.session_state.chart_images.append(chart_buffer.getvalue())
elif visual_options == "Line Chart":
    st.markdown("""
                <h3 style='text-align: center; color: #4CAF50; font-size: 20px; font-family: "segoe UI", sans-serif;">
                    2. Line Chart
                </h3>
                """, unsafe_allow_html=True)
    page = st.number_input("Select Page Number", min_value=1, max_value=100, value=1, step=1)
    items_per_page = st.number_input("Items per page", min_value=1, max_value=100, value=10, step=1)
    start = (page - 1) * items_per_page
    end = start + items_per_page
    x = st.selectbox("Select X-axis", numeric_cols + categorical_cols)
    y = st.selectbox("Select Y-axis", numeric_cols + categorical_cols)
    x_range = st.slider("Select X-axis Range", int(filtered_df[x].min()), int(filtered_df[x].max()), (int(filtered_df[x].min()), int(filtered_df[x].max())))
    y_range = st.slider("Select Y-axis Range", int(filtered_df[y].min()), int(filtered_df[y].max()), (int(filtered_df[y].min()), int(filtered_df[y].max())))
    filtered_df = df[(df[x] >= x_range[0]) & (df[x] <= x_range[1]) & (df[y] >= y_range[0]) & (df[y] <= y_range[1])].dropna().iloc[start:end]
    if st.button("Generate Line Chart"):
        fig, ax = plt.subplots(figsize=(20, 20))
        sns.lineplot(data=filtered_df, x=x, y=y, ax=ax)
        plt.xticks(rotation=45)
        ax.set_title(f"{y} vs {x} (page {page})")
        st.pyplot(fig)
        chart_buffer = BytesIO()
        fig.savefig(chart_buffer, format='png')
        chart_buffer.seek(0)
        if "chart_images" not in st.session_state:
            st.session_state.chart_images = []
        st.session_state.chart_images.append(chart_buffer.getvalue())
elif visual_options == "Scatter plot":
    st.markdown("""
                <h3 style='text-align: center; color: #4CAF50; font-size: 20px; font-family: "segoe UI", sans-serif;">
                    3. Scatter plot
                </h3>
                """, unsafe_allow_html=True)
    page = st.number_input("Select Page Number", min_value=1, max_value=100, value=1, step=1)
    items_per_page = st.number_input("Items per page", min_value=1, max_value=100, value=10, step=1)
    start = (page - 1) * items_per_page
    end = start + items_per_page
    x = st.selectbox("Select X-axis column", numeric_cols + categorical_cols)
    y = st.selectbox("Select Y-axis column", numeric_cols + categorical_cols)
    x_range = st.slider("Select X-axis Range", int(filtered_df[x].min()), int(filtered_df[x].max()), (int(filtered_df[x].min()), int(filtered_df[x].max())))
    y_range = st.slider("Select Y-axis Range", int(filtered_df[y].min()), int(filtered_df[y].max()), (int(filtered_df[y].min()), int(filtered_df[y].max())))
    filtered_df = df[(df[x] >= x_range[0]) & (df[x] <= x_range[1]) & (df[y] >= y_range[0]) & (df[y] <= y_range[1])].dropna().iloc[start:end]
    if st.button("Generate Scatter plot"):
        fig, ax = plt.subplots(figsize=(20, 20))
        sns.scatterplot(data=filtered_df, x=x, y=y, ax=ax)
        plt.xticks(rotation=45)
        ax.set_title(f"{y} vs {x} (page {page})")
        st.pyplot(fig)
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
                        <h4> 📊 Scatter Plot Generated Successfully!</h4>
                    </div>
        """, unsafe_allow_html=True)
        chart_buffer = BytesIO()
        fig.savefig(chart_buffer, format='png')
        chart_buffer.seek(0)
        if "chart_images" not in st.session_state:
            st.session_state.chart_images = []
        st.session_state.chart_images.append(chart_buffer.getvalue())
elif visual_options == "Heat Map":
    st.markdown("""
                <h3 style='text-align: center; color: #4CAF50; font-size: 20px; font-family: "segoe UI", sans-serif;">
                    4. Heat Map
                </h3>
                """, unsafe_allow_html=True)
    page = st.number_input("Select Page Number", min_value=1, max_value=100, value=1, step=1)
    items_per_page = st.number_input("Items per page", min_value=1, max_value=100, value=10, step=1)
    start = (page - 1) * items_per_page
    end = start + items_per_page
    x = st.selectbox("Select X-axis column", numeric_cols + categorical_cols)
    y = st.selectbox("Select Y-axis column", numeric_cols + categorical_cols)
    x_range = st.slider("Select X-axis Range", int(filtered_df[x].min()), int(filtered_df[x].max()), (int(filtered_df[x].min()), int(filtered_df[x].max())))
    y_range = st.slider("Select Y-axis Range", int(filtered_df[y].min()), int(filtered_df[y].max()), (int(filtered_df[y].min()), int(filtered_df[y].max())))
    filtered_df = df[(df[x] >= x_range[0]) & (df[x] <= x_range[1]) & (df[y] >= y_range[0]) & (df[y] <= y_range[1])].dropna().iloc[start:end]
    if st.button("Generate Heat Map"):
        fig, ax = plt.subplots(figsize=(20, 20))
        sns.heatmap(filtered_df.corr(), annot=True , cmap='coolwarm', ax=ax)
        plt.title(f"Heat Map of {x} vs {y} (page {page})")
        plt.tight_layout()
        plt.xticks(rotation=45)
        st.pyplot(fig)
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
                        <h4> 📊 Heat Map Generated Successfully!</h4>
                    </div>
        """, unsafe_allow_html=True)
        chart_buffer = BytesIO()
        fig.savefig(chart_buffer, format='png')
        chart_buffer.seek(0)
        if "chart_images" not in st.session_state:
            st.session_state.chart_images = []
        st.session_state.chart_images.append(chart_buffer.getvalue())
elif visual_options == "Box Plot":
    st.markdown("""
                <h3 style='text-align: center; color: #4CAF50; font-size: 20px; font-family: "segoe UI", sans-serif;">
                    5. Box Plot
                </h3>)
                """, unsafe_allow_html=True)
    page = st.number_input("Select Page Number", min_value=1, max_value=100, value=1, step=1)
    items_per_page = st.number_input("Items per page", min_value=1, max_value=100, value=10, step=1)
    start = (page - 1) * items_per_page
    end = start + items_per_page
    x = st.selectbox("Select X-axis (Categorical)", numeric_cols + categorical_cols)
    y = st.selectbox("Select Y-axis (Numerical)", numeric_cols + categorical_cols)
    x_range = st.slider("Select X-axis Range", int(filtered_df[x].min()), int(filtered_df[x].max()), (int(filtered_df[x].min()), int(filtered_df[x].max())))
    y_range = st.slider("Select Y-axis Range", int(filtered_df[y].min()), int(filtered_df[y].max()), (int(filtered_df[y].min()), int(filtered_df[y].max())))
    filtered_df = df[(df[x] >= x_range[0]) & (df[x] <= x_range[1]) & (df[y] >= y_range[0]) & (df[y] <= y_range[1])].dropna().iloc[start:end]
    if st.button("Generate Box Plot"):
        fig, ax = plt.subplots(figsize=(20, 20))
        sns.boxplot(x=x, y=y, data=filtered_df, ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)
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
                        <h4> 📊 Box Plot Generated Successfully!</h4>
                    </div>
        """, unsafe_allow_html=True)
        chart_buffer = BytesIO()
        fig.savefig(chart_buffer, format='png')
        chart_buffer.seek(0)
        if "chart_images" not in st.session_state:
            st.session_state.chart_images = []
        st.session_state.chart_images.append(chart_buffer.getvalue())
elif visual_options == "Histogram":
    st.markdown("""
                <h3 style='text-align: center; color: #4CAF50; font-size: 20px; font-family: "segoe UI", sans-serif;">
                    6. Histogram
                </h3>)
                """, unsafe_allow_html=True)
    page = st.number_input("Select Page Number", min_value=1, max_value=100, value=1, step=1)
    items_per_page = st.number_input("Items per page", min_value=1, max_value=100, value=10, step=1)
    start = (page - 1) * items_per_page
    end = start + items_per_page
    x = st.selectbox("Select x-axis", numeric_cols + categorical_cols)
    y = st.selectbox("Select y-axis (optional)", numeric_cols + categorical_cols, index=0)
    x_range = st.slider("Select X-axis Range", int(filtered_df[x].min()), int(filtered_df[x].max()), (int(filtered_df[x].min()), int(filtered_df[x].max())))
    y_range = st.slider("Select Y-axis Range", int(filtered_df[y].min()), int(filtered_df[y].max()), (int(filtered_df[y].min()), int(filtered_df[y].max())))
    top_n = st.slider("Select Top N Categories", min_value=1, max_value=len(df), value=5, step=1)
    filtered_df = df[(df[x] >= x_range[0]) & (df[x] <= x_range[1]) & (df[y] >= y_range[0]) & (df[y] <= y_range[1])].dropna().iloc[start:end]
    if st.button("Generate Histogram"):
        fig, ax = plt.subplots(figsize=(20, 20))
        sns.histplot(data=filtered_df, x=x, y=y, ax=ax, bins=30, kde=True)
        plt.xticks(rotation=45)
        plt.yticks(rotation=45)
        plt.title(f"Histogram of {x} (page {page})")
        plt.tight_layout()
        st.pyplot(fig)
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
                        <h4> 📊 Histogram Generated Successfully!</h4>
                    </div>
        """, unsafe_allow_html=True)
        chart_buffer = BytesIO()
        fig.savefig(chart_buffer, format='png')
        chart_buffer.seek(0)
        if "chart_images" not in st.session_state:
            st.session_state.chart_images = []
        st.session_state.chart_images.append(chart_buffer.getvalue())
elif visual_options == "Pair Plot":
    st.markdown("""
                <h3 style='text-align: center; color: #4CAF50; font-size: 20px; font-family: "segoe UI", sans-serif;">
                    7. Pair Plot
                </h3>)
                """, unsafe_allow_html=True)
    page = st.number_input("Select Page Number", min_value=1, max_value=100, value=1, step=1)
    items_per_page = st.number_input("Items per page", min_value=1, max_value=100, value=10, step=1)
    start = (page - 1) * items_per_page
    end = start + items_per_page
    x = st.selectbox("Select X-axis (categorical)", numeric_cols + categorical_cols)
    y = st.selectbox("Select Y-axis (numerical)", numeric_cols + categorical_cols)
    x_range = st.slider("Select X-axis Range", int(filtered_df[x].min()), int(filtered_df[x].max()), (int(filtered_df[x].min()), int(filtered_df[x].max())))
    y_range = st.slider("Select Y-axis Range", int(filtered_df[y].min()), int(filtered_df[y].max()), (int(filtered_df[y].min()), int(filtered_df[y].max())))
    filtered_df = df[(df[x] >= x_range[0]) & (df[x] <= x_range[1]) & (df[y] >= y_range[0]) & (df[y] <= y_range[1])].dropna().iloc[start:end]
    if st.button("Generate Pair Plot"):
        fig = sns.pairplot(filtered_df)
        plt.suptitle(f"Pair Plot of {x} vs {y}")
        plt.tight_layout()
        st.pyplot(fig)
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
                        <h4> 📊 Pair Plot Generated Successfully!</h4>
                    </div>
        """, unsafe_allow_html=True)
        chart_buffer = BytesIO()
        fig.savefig(chart_buffer, format='png')
        chart_buffer.seek(0)
        if "chart_images" not in st.session_state:
            st.session_state.chart_images = []
        st.session_state.chart_images.append(chart_buffer.getvalue())
elif visual_options == "violin plot":
    st. markdown("""
                 <h3 style='text-align: center; color: #4CAF50; font-size: 20px; font-family: "segoe UI", sans-serif;">
                    8. Violin Plot
                </h3>
                 """, unsafe_allow_html=True)
    page = st.number_input("Select Page Number", min_value=1, max_value=100, value=1, step=1)
    items_per_page = st.number_input("Items per page", min_value=1, max_value=100, value=10, step=1)
    start = (page - 1) * items_per_page
    end = start + items_per_page
    x = st.selectbox("Select X-axis (Categorical)", categorical_cols + numeric_cols)
    y = st.selectbox("Select Y-axis (Numerical)", numeric_cols + categorical_cols)
    x_range = st.slider("Select X-axis Range", int(filtered_df[x].min()), int(filtered_df[x].max()), (int(filtered_df[x].min()), int(filtered_df[x].max())))
    y_range = st.slider("Select Y-axis Range", int(filtered_df[y].min()), int(filtered_df[y].max()), (int(filtered_df[y].min()), int(filtered_df[y].max())))
    filtered_df = df[(df[x] >= x_range[0]) & (df[x] <= x_range[1]) & (df[y] >= y_range[0]) & (df[y] <= y_range[1])].dropna().iloc[start:end]
    if st.button("Generate Violin Plot"):
        fig, ax = plt.subplots(figsize=(20, 20))
        sns.violinplot(x=x, y=y, data=filtered_df, ax=ax)
        plt.xticks(rotation=45)
        ax.set_title(f"{y} vs {x} (page {page})")
        plt.tight_layout()
        st.pyplot(fig)
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
                        <h4> 📊 Violin Plot Generated Successfully!</h4>
                    </div>
        """, unsafe_allow_html=True)
        chart_buffer = BytesIO()
        fig.savefig(chart_buffer, format='png')
        chart_buffer.seek(0)
        if "chart_images" not in st.session_state:
            st.session_state.chart_images = []
        st.session_state.chart_images.append(chart_buffer.getvalue())
elif visual_options == "Pie Chart":
    st.markdown("""
                <h3 style='text-align: center; color: #4CAF50; font-size: 20px; font-family: "segoe UI", sans-serif;">
                    9. Pie Chart
                </h3>
                """, unsafe_allow_html=True)
    page = st.number_input("Select Page Number", min_value=1, max_value=100, value=1, step=1)
    items_per_page = st.number_input("Items per page", min_value=1, max_value=100, value=10, step=1)
    start = (page - 1) * items_per_page
    end = start + items_per_page
    x = st.selectbox("Select Column for Pie Chart", categorical_cols + numeric_cols)
    x_range = st.slider("Select X-axis Range", int(filtered_df[x].min()), int(filtered_df[x].max()), (int(filtered_df[x].min()), int(filtered_df[x].max())))
    filtered_df = df[(df[x] >= x_range[0]) & (df[x] <= x_range[1])].dropna().iloc[start:end]
    if st.button("Generate Pie Chart"):
        fig, ax = plt.subplots(figsize=(10, 10))
        filtered_df[x].value_counts().plot.pie(autopct='%1.1f%%', startangle=90, ax=ax)
        ax.set_ylabel('')
        plt.tight_layout()
        st.pyplot(fig)
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
                        <h4> 📊 Pie Chart Generated Successfully!</h4>
                    </div>
        """, unsafe_allow_html=True)
        chart_buffer = BytesIO()
        fig.savefig(chart_buffer, format='png')
        chart_buffer.seek(0)
        if "chart_images" not in st.session_state:
            st.session_state.chart_images = []
        st.session_state.chart_images.append(chart_buffer.getvalue())
elif visual_options == "Bubble Chart":
    st.markdown("""
                <h3 style='text-align: center; color: #4CAF50; font-size: 20px; font-family: "segoe UI", sans-serif;">
                    10. Bubble Chart
                </h3>
                """, unsafe_allow_html=True)
    page = st.number_input("Select Page Number", min_value=1, max_value=100, value=1, step=1)
    items_per_page = st.number_input("Items per page", min_value=1, max_value=100, value=10, step=1)
    start = (page - 1) * items_per_page
    end = start + items_per_page
    x = st.selectbox("Select X-axis", numeric_cols + categorical_cols)
    y = st.selectbox("Select Y-axis", numeric_cols + categorical_cols)
    size = st.selectbox("Select Size Column", numeric_cols + categorical_cols)
    x_range = st.slider("Select X-axis Range", int(filtered_df[x].min()), int(filtered_df[x].max()), (int(filtered_df[x].min()), int(filtered_df[x].max())))
    y_range = st.slider("Select Y-axis Range", int(filtered_df[y].min()), int(filtered_df[y].max()), (int(filtered_df[y].min()), int(filtered_df[y].max())))
    filtered_df = df[(df[x] >= x_range[0]) & (df[x] <= x_range[1]) & (df[y] >= y_range[0]) & (df[y] <= y_range[1])].dropna().iloc[start:end]
    if st.button("Generate Bubble Chart"):
        fig, ax = plt.subplots(figsize=(10, 10))
        sns.scatterplot(x=x, y=y, size=size, data=filtered_df, sizes=(20, 200), ax=ax)
        ax.set_title(f"{y} vs {x} (page {page})")
        plt.tight_layout()
        plt.xticks(rotation=45)
        st.pyplot(fig)
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
                        <h4> 📊 Bubble Chart Generated Successfully!</h4>
                    </div>
        """, unsafe_allow_html=True)
        chart_buffer = BytesIO()
        fig.savefig(chart_buffer, format='png')
        chart_buffer.seek(0)
        if "chart_images" not in st.session_state:
            st.session_state.chart_images = []
        st.session_state.chart_images.append(chart_buffer.getvalue())
else:
    st.error("Please Select a valid visualization option.")
# Generate PDF Report
st.markdown("""
    <div style='
        background-color: #E8F5E9;
        border-left: 6px solid #4CAF50;
        border-radius: 10px;
        padding: 20px;
        font-family: "Segoe UI", sans-serif;
        color: #1B5E20;
        text-align: center;'>
        <h2> 🤖 Generate PDF Report</h2>
        <p style='font-size: 18px;'>🌟 Generate a comprehensive PDF report of your visualizations.</p>
    </div>
""", unsafe_allow_html=True)
if st.button("🤖 Generate PDF Report"):
    
    if "chart_images" in st.session_state and st.session_state["chart_images"]:
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)

        for i, img_data in enumerate(st.session_state["chart_images"], 1):
            img_path = f"chart_{i}.png"
            with open(img_path, "wb") as f:
                f.write(img_data)
            image = Image.open(img_path)
            image.save(img_path, format='PNG')
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=f"Chart {i}", ln=True, align="C")
            pdf.image(img_path, x=10, y=30, w=180)

        report_path = "visual_report.pdf"
        pdf.output(report_path)

        with open(report_path, "rb") as f:
            st.download_button("⬇️ Download PDF Report", f, file_name="visual_report.pdf", mime="application/pdf")
    else:
        st.warning("❌ No charts available. Please generate some charts first.")
if st.button("Back to Dashboard"):
    st.switch_page("pages/dashboard.py")
if st.button("Go to prediction page"):
    if st.session_state.uploaded_file is not None:
        st.switch_page("pages/prediction.py")
