# syncanalytica




# Data and Text Exploration Tool  

An interactive web-based tool to upload datasets, analyze data, generate visual insights, and create professional reports effortlessly.  

## Features  
- **Upload Data**: Supports CSV and Excel file formats.  
- **Data Analysis**: Provides descriptive statistics, correlation analysis, and missing data summaries.  
- **Visualizations**: Dynamic plots, heatmaps, and scatter plots.  
- **Report Generation**: Generates HTML reports for easy sharing and documentation.  



## Getting Started  

### Installation  
1. Clone the repository:  
   ```bash
   git clone https://github.com/your-repo/data-exploration-tool.git
   cd data-exploration-tool
   ```  
2. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```  
3. Run the application:  
   ```bash
   streamlit run app.py
   ```  

=

## Usage  

### **Sample Input**  
1. Upload a CSV or Excel file:  
   Example CSV data:  
   ```csv
   Name, Age, Salary, Department
   John, 30, 55000, IT
   Alice, 28, 65000, HR
   Bob, 35, 70000, IT
   ```

2. Select filters or slicers to customize analysis.  

---

### **Sample Output**  
#### Data Preview:  
| Name  | Age | Salary | Department |  
|-------|-----|--------|------------|  
| John  | 30  | 55000  | IT         |  
| Alice | 28  | 65000  | HR         |  

#### Analysis Results:  
1. **Descriptive Statistics**:  
   | Metric  | Age  | Salary |  
   |---------|------|--------|  
   | Mean    | 31.0 | 63333  |  
   | Median  | 30.0 | 65000  |  

2. **Correlation Heatmap**:  
   Visual representation of correlations between numeric features.  

3. **Interactive Scatter Plot**:  
   A plot of Age vs. Salary with department-based color coding.  

#### Generated Report:  
An HTML file summarizing all analysis and insights, downloadable directly.  

---

## Contributions  
Feel free to fork the repository and submit pull requests. Suggestions and bug reports are welcome!  
