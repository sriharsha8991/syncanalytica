import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt 
import plotly.express as px
import seaborn as sns
from groq_chat import *

# Apply custom styles for a professional and aesthetic layout
def apply_custom_styles():
    st.markdown("""
    <style>
        /* General app styling */
        body {
            font-family: 'Roboto', sans-serif;
            background-color: #f9fafb;
            color: #333;
        }
        h1, h2, h3, h4 {
            color: #2c3e50;
        }
        .hero-section {
            text-align: center;
            padding: 30px 20px;
            background: linear-gradient(to right, #3498db, #2980b9);
            color: white;
            border-radius: 10px;
            margin-bottom: 30px;
        }
        .hero-section h1 {
            margin-bottom: 10px;
            font-size: 36px;
        }
        .hero-buttons {
            margin-top: 20px;
        }
        .hero-buttons button {
            background-color: #ffffff;
            color: #2980b9;
            font-size: 16px;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
            margin: 5px;
            cursor: pointer;
        }
        .hero-buttons button:hover {
            background-color: #d6eaf8;
        }
        /* DataFrames */
        .stDataFrame {
            border: 1px solid #bdc3c7;
            border-radius: 5px;
        }
        /* Section Headers */
        .custom-header {
            background-color: #3498db;
            color: white;
            padding: 10px;
            border-radius: 5px;
            text-align: center;
            margin-bottom: 20px;
        }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state for navigation
if "page" not in st.session_state:
    st.session_state.page = "Landing Page"

# Main application
def main():
    apply_custom_styles()

    # Render hero section and handle navigation
    render_hero_section()

    # Page routing
    if st.session_state.page == "Landing Page":
        landing_page()
    elif st.session_state.page == "Data Analysis Desk":
        data_analysis_desk()
    elif st.session_state.page == "Generate Report":
        generate_report()

# Render the hero section with navigation buttons
def render_hero_section():
    st.markdown("""
    <div class="hero-section">
        <h1>Data and Text Exploration Tool</h1>
        <p>Analyze, explore, and generate insights from your data with ease.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        if st.button("Landing Page"):
            st.session_state.page = "Landing Page"
    with col2:
        if st.button("Data Analysis Desk"):
            st.session_state.page = "Data Analysis Desk"
    with col3:
        if st.button("Generate Report"):
            st.session_state.page = "Generate Report"

# Landing page
def landing_page():
    st.markdown("<div class='custom-header'><h1>Welcome to the Data Exploration Tool</h1></div>", unsafe_allow_html=True)
    st.write("""
    ### Features:
    - **Upload and Analyze Data**: Upload CSV or Excel files for analysis.
    - **Interactive Insights**: Get comprehensive statistics and correlations.
    - **Generate Reports**: Export insights into a well-formatted HTML report.
    """)

# Data Analysis Desk
def data_analysis_desk():
    st.markdown("<div class='custom-header'><h1>Data Analysis Desk</h1></div>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload your file", type=['csv', 'xlsx'])

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            if df.empty:
                st.error("Uploaded file is empty. Please upload a valid file.")
            else:
                st.write("### Data Preview")
                st.dataframe(df.head())

                # Display slicers for filtering
                display_slicers(df)

                # Perform analysis
                analysis_results = perform_full_analysis(df)
                st.session_state['analysis_results'] = analysis_results
                display_analysis_results(analysis_results)

                # Display visualizations
                display_visualizations(df)
        except Exception as e:
            st.error(f"Error reading file: {e}")

# Perform full analysis
def perform_full_analysis(df):
    try:
        numeric_df = df.select_dtypes(include=['number'])
        results = {
            "Descriptive Statistics": numeric_df.describe(),
            "Correlation Analysis": numeric_df.corr(),
            "Missing Data Analysis": {
                "Counts": df.isnull().sum(),
                "Percentage": df.isnull().sum() / len(df) * 100
            },
            "Categorical Data Analysis": {
                col: df[col].value_counts() for col in df.select_dtypes(include=['object', 'category']).columns
            }
        }
        return results
    except Exception as e:
        st.error(f"Failed to perform analysis due to: {str(e)}")
        return {}

# Display analysis results
def display_slicers(df):
    # Categorical slicers
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns
    if len(categorical_cols) > 0:
        selected_column = st.selectbox("Select categorical column for filtering", categorical_cols)
        unique_values = df[selected_column].unique()
        selected_values = st.multiselect(f"Select values from {selected_column}", unique_values, default=unique_values)
        if selected_values:
            df = df[df[selected_column].isin(selected_values)]
    
    # Numeric slicers
    numeric_cols = df.select_dtypes(include=['number']).columns
    if len(numeric_cols) > 0:
        selected_column = st.selectbox("Select numeric column for range filter", numeric_cols)
        min_val = df[selected_column].min()
        max_val = df[selected_column].max()
        range_values = st.slider(f"Select range for {selected_column}", min_value=int(min_val), max_value=int(max_val), value=(int(min_val), int(max_val)))
        df = df[(df[selected_column] >= range_values[0]) & (df[selected_column] <= range_values[1])]
    
    st.write(f"### Filtered Data Preview (showing first 10 rows)")
    st.dataframe(df.head())
    return df

# Display visualizations
def display_visualizations(df):
    # Plotting a distribution of numeric data
    numeric_df = df.select_dtypes(include=['number'])
    if not numeric_df.empty:
        st.subheader("Distribution of Numeric Data")
        fig = plt.figure(figsize=(10, 6))
        numeric_df.hist(bins=15, edgecolor='black', figsize=(10, 6))
        st.pyplot(fig)

    # Plot correlation heatmap using Seaborn
    if not numeric_df.empty:
        st.subheader("Correlation Heatmap")
        corr = numeric_df.corr()
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
        st.pyplot(fig)

    # Plot interactive scatter plot using Plotly
    if len(numeric_df.columns) >= 2:
        st.subheader("Interactive Scatter Plot")
        fig = px.scatter(df, x=numeric_df.columns[0], y=numeric_df.columns[1], title="Scatter Plot")
        st.plotly_chart(fig)

def display_analysis_results(results):
    for analysis_type, result in results.items():
        st.subheader(analysis_type)
        st.dataframe(result)


# Generate Report
def generate_report():
    st.markdown("<div class='custom-header'><h1>Generate HTML Report</h1></div>", unsafe_allow_html=True)
    if 'analysis_results' in st.session_state and st.button('Save Report to HTML'):
        # Save the report as HTML and return the content as a string
        html_content = save_html_report(st.session_state['analysis_results'])
        st.success("Report saved to 'report.html'")
        
        # Provide a download button for the HTML report
        st.download_button(
            label="Download Report",
            data=html_content,
            file_name="report.html",
            mime="text/html"
        )
        
    api_key = "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"  # Replace with your actual API key
    client = initialize_groq_client(api_key)

    try:
        with open('report.html', 'r', encoding='utf-8') as file:
            html_content = file.read()

        # Define the context for summarization
        context = html_content  # Replace with the actual context

        # Generate the summary and report
        report = generate_summary_report(client, context)
        st.write("Generated Report:\n", report)

    except Exception as e:
        st.error(f"An error occurred while generating the report: {e}")


# Save HTML Report
# Save HTML Report
def save_html_report(analysis_results):
    html_content = ""
    for title, data in analysis_results.items():
        html_content += f"<h1>{title}</h1>\n"
        html_content += pd.DataFrame(data).to_html() + "\n"
    
    # Save the content to a file
    with open('report.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return html_content


if __name__ == "__main__":
    main()
