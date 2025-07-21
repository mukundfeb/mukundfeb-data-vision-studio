import pandas as pd
import streamlit as st
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor, plot_tree
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns
from fpdf import FPDF
from PIL import Image
from io import BytesIO
st.set_page_config(page_title="prediction", layout="wide")
st.markdown("""
<style>
    .prediction-main {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding-top: 50px;
        font-family: 'Segoe UI', sans-serif;
        color: #0D47A1;
    }

    .prediction-container {
        background-color: #F3F9FF;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        width: 90%;
        max-width: 900px;
        margin: auto;
    }

    .prediction-title {
        text-align: center;
        font-size: 32px;
        margin-bottom: 20px;
        color: #1565C0;
        font-weight: bold;
    }

    .prediction-form {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 10px;
        margin-top: 10px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.06);
    }

    .prediction-form label {
        font-weight: bold;
        color: #0D47A1;
    }

    .stTextInput, .stNumberInput, .stSelectbox, .stSlider {
        background-color: #ffffff;
        border-radius: 8px;
        border: 1px solid #BBDEFB;
        padding: 5px 10px;
    }

    .stButton>button {
        background-color: #0D47A1;
        color: white;
        padding: 10px 18px;
        border: none;
        border-radius: 8px;
        font-size: 16px;
        margin-top: 15px;
        transition: background-color 0.3s ease;
    }

    .stButton>button:hover {
        background-color: #1565C0;
    }

    .prediction-result {
        margin-top: 20px;
        font-size: 20px;
        font-weight: bold;
        color: #2E7D32;
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

<h2>📊 Smart ML Forecast</h2>
<p style='font-size: 18px;'>🔍 Look for patterns in your data!</p>
</div>
""", unsafe_allow_html=True)
#hide sidebar
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
# data uploading sesion state
if 'uploaded_file' not in st.session_state:
    st.warning("Nn data found please upload your data in the dashboard first!")
else:
    df = st.session_state.uploaded_file
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
        df = df.fillna(0)
st.markdown("""
            <div style='
                background-color: #E3F2FD;
                border-left: 6px solid #42A5F5;
                border-radius: 10px;
                padding: 20px;
                font-family: "Segoe UI", sans-serif;
                color: #0D47A1;
                text-align: center;'>
                <h3> 🤖 Select the Target Variable for Prediction</h3>
                </div>
            </div>
        """, unsafe_allow_html=True)
# target variable selection
target = st.selectbox("Select the target variable for prediction", df.columns)
st.markdown("""
            <div style='
                background-color: #E3F2FD;
                border-left: 6px solid #42A5F5;
                border-radius: 10px;
                padding: 20px;
                font-family: "Segoe UI", sans-serif;
                color: #0D47A1;
                text-align: center;'>
                <h3> 🤖 Choose Your Machine Learning Model</h3>
                </div>
            </div>
        """, unsafe_allow_html=True)
# model selection
model_selection = st.selectbox("Choose a Machine Learning Model:",
                                ["Linear Regression", "Random Forest", "Decision Tree", "KNN Regressor", "SVM Regressor"])
# Split the data into features and target variable
x = df.drop(columns=[target])
y = df[target]
# Split the data into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
# feature scaling
scaler = StandardScaler()
x_train_scaled = scaler.fit_transform(x_train)
x_test_scaled = scaler.fit_transform(x_test)

    # Initialize model
if model_selection == "Linear Regression":
    st.markdown("""
            <div style='
                background-color: #E3F2FD;
                border-left: 6px solid #42A5F5;
                border-radius: 10px;
                padding: 20px;
                font-family: "Segoe UI", sans-serif;
                color: #0D47A1;
                text-align: center;'>
                <h3> 🤖 Processing With Linear Regression Model</h3>
                </div>
            </div>
        """, unsafe_allow_html=True)
    model =  LinearRegression()
    if model:
        model.fit(x_train_scaled, y_train)
        y_pred = model.predict(x_test_scaled)

        st.success("Model trained successfully!")

        # Evaluation
        st.markdown("### Model Evaluation")
        st.write("R² Score:", round(r2_score(y_test, y_pred), 3))
        st.write("Mean Squared Error:", round(mean_squared_error(y_test, y_pred), 3))

        # Visualize Actual vs Predicted
        st.markdown("""
            <div style='
                background-color: #E3F2FD;
                border-left: 6px solid #42A5F5;
                border-radius: 10px;
                padding: 20px;
                font-family: "Segoe UI", sans-serif;
                color: #0D47A1;
                text-align: center;'>
                <h3> 🤖 Visualization With Linear Regression Using Scatter Plot</h3>
                </div>
            </div>
        """, unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.scatterplot(x=y_test, y=y_pred, ax=ax, color="dodgerblue")
        ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
        ax.set_xlabel("Actual Values")
        ax.set_ylabel("Predicted Values")
        ax.set_title("Actual vs Predicted Values")
        st.pyplot(fig)
        chart_buffer = BytesIO()
        fig.savefig(chart_buffer, format='png')
        chart_buffer.seek(0)
        if "chart_images" not in st.session_state:
           st.session_state.chart_images = []
        st.session_state.chart_images.append(chart_buffer.getvalue())
        # Visualize coefficients of the data using matplot
        coef_df = pd.DataFrame({
                'Feature': x.columns,
                'Coefficient': model.coef_
        }).sort_values(by='Coefficient', ascending=False)
        st.markdown("""
            <div style='
                background-color: #E3F2FD;
                border-left: 6px solid #42A5F5;
                border-radius: 10px;
                padding: 20px;
                font-family: "Segoe UI", sans-serif;
                color: #0D47A1;
                text-align: center;'>
                <h3> 🤖 Visualization With Linear Regression Using Bar Plot</h3>
                </div>
            </div>
        """, unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=coef_df, x='Coefficient', y='Feature', palette='viridis', ax=ax)
        ax.set_title("Linear Regression Coefficients")
        st.pyplot(fig)

        # Save the visualized images in pdf
        chart_buffer = BytesIO()
        fig.savefig(chart_buffer, format='png')
        chart_buffer.seek(0)
        if "chart_images" not in st.session_state:
           st.session_state.chart_images = []
        st.session_state.chart_images.append(chart_buffer.getvalue())
        st.markdown("""
            <div style='
                background-color: #E3F2FD;
                border-left: 6px solid #42A5F5;
                border-radius: 10px;
                padding: 20px;
                font-family: "Segoe UI", sans-serif;
                color: #0D47A1;
                text-align: center;'>
                <h3> 🤖 Save Predictions In CSV</h3>
                </div>
            </div>
        """, unsafe_allow_html=True)
        # Download predictions
        result_df = x_test.copy()
        result_df['Actual'] = y_test.values
        result_df['Predicted'] = y_pred
        st.download_button("Download Predictions", result_df.to_csv(index=False), file_name="predictions.csv")
elif model_selection == 'Random Forest':
    n_estimators = st.slider("Number of Trees (n_estimators)", min_value=10, max_value=500, value=100, step=10)
    st.markdown("""
            <div style='
                background-color: #E3F2FD;
                border-left: 6px solid #42A5F5;
                border-radius: 10px;
                padding: 20px;
                font-family: "Segoe UI", sans-serif;
                color: #0D47A1;
                text-align: center;'>
                <h3> 🤖 Processing With Random Forest Model</h3>
                </div>
            </div>
        """, unsafe_allow_html=True)
    model = RandomForestRegressor(n_estimators=n_estimators, random_state=42)
    if model is not None:
        model.fit(x_train_scaled, y_train)
        y_pred = model.predict(x_test_scaled)

        st.success("Model trained successfully!")

        # Evaluation
        st.markdown("### Model Evaluation")
        st.write("R² Score:", round(r2_score(y_test, y_pred), 3))
        st.write("Mean Squared Error:", round(mean_squared_error(y_test, y_pred), 3))

        # Visualize Actual vs Predicted
        st.markdown("""
            <div style='
                background-color: #E3F2FD;
                border-left: 6px solid #42A5F5;
                border-radius: 10px;
                padding: 20px;
                font-family: "Segoe UI", sans-serif;
                color: #0D47A1;
                text-align: center;'>
                <h3> 🤖 Visualization With Random Forest Using Scatter Plot</h3>
                </div>
            </div>
        """, unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.scatterplot(x=y_test, y=y_pred, ax=ax, color="dodgerblue")
        ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
        ax.set_xlabel("Actual Values")
        ax.set_ylabel("Predicted Values")
        ax.set_title("Actual vs Predicted Values")
        st.pyplot(fig)
        chart_buffer = BytesIO()
        fig.savefig(chart_buffer, format='png')
        chart_buffer.seek(0)
        if "chart_images" not in st.session_state:
           st.session_state.chart_images = []
        st.session_state.chart_images.append(chart_buffer.getvalue())
        # Visualize coefficients using matplot
        importance_df = pd.DataFrame({
                'Feature': x.columns,
                'Importance': model.feature_importances_
        }).sort_values(by='Importance', ascending=False)
        st.markdown("""
            <div style='
                background-color: #E3F2FD;
                border-left: 6px solid #42A5F5;
                border-radius: 10px;
                padding: 20px;
                font-family: "Segoe UI", sans-serif;
                color: #0D47A1;
                text-align: center;'>
                <h3> 🤖 Visualization With Random Forest Using Bar Plot</h3>
                </div>
            </div>
        """, unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=importance_df, x='Importance', y='Feature', palette='coolwarm', ax=ax)
        ax.set_title("Random Forest Feature Importance")
        st.pyplot(fig)
        chart_buffer = BytesIO()
        fig.savefig(chart_buffer, format='png')
        chart_buffer.seek(0)
        if "chart_images" not in st.session_state:
           st.session_state.chart_images = []
        st.session_state.chart_images.append(chart_buffer.getvalue())
        # Download predictions
        result_df = x_test.copy()
        result_df['Actual'] = y_test.values
        result_df['Predicted'] = y_pred
        st.download_button("Download Predictions", result_df.to_csv(index=False), file_name="predictions.csv")
elif model_selection == 'Decision Tree':
    st.markdown("""
            <div style='
                background-color: #E3F2FD;
                border-left: 6px solid #42A5F5;
                border-radius: 10px;
                padding: 20px;
                font-family: "Segoe UI", sans-serif;
                color: #0D47A1;
                text-align: center;'>
                <h3> 🤖 Processing With Decision Tree Model</h3>
                </div>
            </div>
        """, unsafe_allow_html=True)
    model = DecisionTreeClassifier()
    if model:
        model.fit(x_train_scaled, y_train)
        y_pred = model.predict(x_test_scaled)

        st.success("Model trained successfully!")

        # Evaluation
        st.markdown("### Model Evaluation")
        st.write("R² Score:", round(r2_score(y_test, y_pred), 3))
        st.write("Mean Squared Error:", round(mean_squared_error(y_test, y_pred), 3))

        # Visualize Actual vs Predicted
        st.markdown("""
            <div style='
                background-color: #E3F2FD;
                border-left: 6px solid #42A5F5;
                border-radius: 10px;
                padding: 20px;
                font-family: "Segoe UI", sans-serif;
                color: #0D47A1;
                text-align: center;'>
                <h3> 🤖 Visualization With Decision Tree Using Scatter Plot</h3>
                </div>
            </div>
        """, unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.scatterplot(x=y_test, y=y_pred, ax=ax, color="dodgerblue")
        ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
        ax.set_xlabel("Actual Values")
        ax.set_ylabel("Predicted Values")
        ax.set_title("Actual vs Predicted Values")
        st.pyplot(fig)
        chart_buffer = BytesIO()
        fig.savefig(chart_buffer, format='png')
        chart_buffer.seek(0)
        if "chart_images" not in st.session_state:
           st.session_state.chart_images = []
        st.session_state.chart_images.append(chart_buffer.getvalue())

        # If Decision Tree model, visualize the tree
        if model_selection == "Decision Tree":
            st.markdown("""
            <div style='
                background-color: #E3F2FD;
                border-left: 6px solid #42A5F5;
                border-radius: 10px;
                padding: 20px;
                font-family: "Segoe UI", sans-serif;
                color: #0D47A1;
                text-align: center;'>
                <h3> 🤖 Let’s visualize the Decision Tree</h3>
                </div>
            </div>
        """, unsafe_allow_html=True)
            st.markdown("### Decision Tree Visualization")
            max_depth_vis = st.slider("Max Depth for Visualization", 1, 10, 3)
            fig, ax = plt.subplots(figsize=(20, 10))
            plot_tree(model, feature_names=x.columns, filled=True, fontsize=10, max_depth=max_depth_vis, ax=ax)
            st.pyplot(fig)
            chart_buffer = BytesIO()
            fig.savefig(chart_buffer, format='png')
            chart_buffer.seek(0)
            if "chart_images" not in st.session_state:
              st.session_state.chart_images = []
            st.session_state.chart_images.append(chart_buffer.getvalue())

        # Download predictions
        result_df = x_test.copy()
        result_df['Actual'] = y_test.values
        result_df['Predicted'] = y_pred
        st.download_button("Download Predictions", result_df.to_csv(index=False), file_name="predictions.csv")
elif model_selection == 'KNN Regressor':
    st.markdown("""
            <div style='
                background-color: #E3F2FD;
                border-left: 6px solid #42A5F5;
                border-radius: 10px;
                padding: 20px;
                font-family: "Segoe UI", sans-serif;
                color: #0D47A1;
                text-align: center;'>
                <h3> 🤖 Processing With KNN Regressor</h3>
                </div>
            </div>
        """, unsafe_allow_html=True)
    model = KNeighborsRegressor()
    if model:
        model.fit(x_train_scaled, y_train)
        y_pred = model.predict(x_test_scaled)

        st.success("Model trained successfully!")

        # Evaluation
        st.markdown("### Model Evaluation")
        st.write("R² Score:", round(r2_score(y_test, y_pred), 3))
        st.write("Mean Squared Error:", round(mean_squared_error(y_test, y_pred), 3))

        # Visualize Actual vs Predicted
        st.markdown("""
            <div style='
                background-color: #E3F2FD;
                border-left: 6px solid #42A5F5;
                border-radius: 10px;
                padding: 20px;
                font-family: "Segoe UI", sans-serif;
                color: #0D47A1;
                text-align: center;'>
                <h3> 🤖 Visualization With KNN Regressor Using Scatter Plot</h3>
                </div>
            </div>
        """, unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.scatterplot(x=y_test, y=y_pred, ax=ax, color="dodgerblue")
        ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
        ax.set_xlabel("Actual Values")
        ax.set_ylabel("Predicted Values")
        ax.set_title("Actual vs Predicted Values")
        st.pyplot(fig)
        chart_buffer = BytesIO()
        fig.savefig(chart_buffer, format='png')
        chart_buffer.seek(0)
        if "chart_images" not in st.session_state:
           st.session_state.chart_images = []
        st.session_state.chart_images.append(chart_buffer.getvalue())

        # If KNN model, visualize neighbors (distance heatmap)
        if model_selection == "KNN Regressor":
            st.markdown("""
            <div style='
                background-color: #E3F2FD;
                border-left: 6px solid #42A5F5;
                border-radius: 10px;
                padding: 20px;
                font-family: "Segoe UI", sans-serif;
                color: #0D47A1;
                text-align: center;'>
                <h3> 🤖 Visualization With KNN Regressor Using Heatmap</h3>
                </div>
            </div>
        """, unsafe_allow_html=True)
            st.markdown("### KNN Neighbor Visualization")
            from sklearn.metrics import pairwise_distances
            dist_matrix = pairwise_distances(x_test_scaled)
            fig, ax = plt.subplots(figsize=(10, 8))
            sns.heatmap(dist_matrix, cmap="viridis", ax=ax)
            ax.set_title("Pairwise Distance Heatmap of Test Samples")
            st.pyplot(fig)
            chart_buffer = BytesIO()
        fig.savefig(chart_buffer, format='png')
        chart_buffer.seek(0)
        if "chart_images" not in st.session_state:
           st.session_state.chart_images = []
        st.session_state.chart_images.append(chart_buffer.getvalue())

        # Download predictions
        result_df = x_test.copy()
        result_df['Actual'] = y_test.values
        result_df['Predicted'] = y_pred
        st.download_button("Download Predictions", result_df.to_csv(index=False), file_name="predictions.csv")
elif model_selection == 'SVM Regressor':
    st.markdown("""
            <div style='
                background-color: #E3F2FD;
                border-left: 6px solid #42A5F5;
                border-radius: 10px;
                padding: 20px;
                font-family: "Segoe UI", sans-serif;
                color: #0D47A1;
                text-align: center;'>
                <h3> 🤖 Processing With SVM Regressor</h3>
                </div>
            </div>
        """, unsafe_allow_html=True)
    model = SVR()
    if model:
        model.fit(x_train_scaled, y_train)
        y_pred = model.predict(x_test_scaled)

        st.success("Model trained successfully!")

        # Evaluation
        st.markdown("### Model Evaluation")
        st.write("R² Score:", round(r2_score(y_test, y_pred), 3))
        st.write("Mean Squared Error:", round(mean_squared_error(y_test, y_pred), 3))

        # Visualize Actual vs Predicted
        st.markdown("""
            <div style='
                background-color: #E3F2FD;
                border-left: 6px solid #42A5F5;
                border-radius: 10px;
                padding: 20px;
                font-family: "Segoe UI", sans-serif;
                color: #0D47A1;
                text-align: center;'>
                <h3> 🤖 Visualization With SVR Regressor Using Scatter Plot</h3>
                </div>
            </div>
        """, unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.scatterplot(x=y_test, y=y_pred, ax=ax, color="dodgerblue")
        ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
        ax.set_xlabel("Actual Values")
        ax.set_ylabel("Predicted Values")
        ax.set_title("Actual vs Predicted Values")
        st.pyplot(fig)
        chart_buffer = BytesIO()
        fig.savefig(chart_buffer, format='png')
        chart_buffer.seek(0)
        if "chart_images" not in st.session_state:
           st.session_state.chart_images = []
        st.session_state.chart_images.append(chart_buffer.getvalue())

        # If SVR model, visualize support vectors influence
        if model_selection == "SVM Regressor":
            st.markdown("""
            <div style='
                background-color: #E3F2FD;
                border-left: 6px solid #42A5F5;
                border-radius: 10px;
                padding: 20px;
                font-family: "Segoe UI", sans-serif;
                color: #0D47A1;
                text-align: center;'>
                <h3> 🤖 Using SVR model, visualize support vectors influence</h3>
                </div>
            </div>
        """, unsafe_allow_html=True)
            st.markdown("### SVR Margin Visualization (2D PCA Projection)")
            from sklearn.decomposition import PCA
            pca = PCA(n_components=2)
            X_test_2d = pca.fit_transform(x_test_scaled)
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.scatterplot(x=X_test_2d[:, 0], y=X_test_2d[:, 1], hue=y_pred, palette="viridis", ax=ax)
            ax.set_title("SVR Predictions in 2D PCA Projection")
            st.pyplot(fig)
            chart_buffer = BytesIO()
        fig.savefig(chart_buffer, format='png')
        chart_buffer.seek(0)
        if "chart_images" not in st.session_state:
           st.session_state.chart_images = []
        st.session_state.chart_images.append(chart_buffer.getvalue())

        # Download predictions
        result_df = x_test.copy()
        result_df['Actual'] = y_test.values
        result_df['Predicted'] = y_pred
        st.download_button("Download Predictions", result_df.to_csv(index=False), file_name="predictions.csv")
else:
    st.warning("Please select the valid model to predict and visualize")
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
if st.button("Go Back To Dashboard"):
    st.switch_page("pages/dashboard.py")