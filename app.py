import pandas as pd
import matplotlib.pyplot
import streamlit as st
import mysql.connector
import seaborn as sn
import io 
import zipfile 
st.set_page_config(
    page_title="Data Analytics & Data Science Automation Tool",
    page_icon="📈",
    layout="wide"
)
st.title("🌐 Smart Data Analytics & Data Science Automation Tool")
st.write('Import, Clean, Analyze, & Forecasting, Generate Report, Business Idea Plan')
st.divider()
st.sidebar.title("Navigation")
page=st.sidebar.selectbox("Choose Service",["Home","Data Import","Data Cleaning","Data Visulization","Forecasting","Reports"])

if page=="Home":
   st.markdown("""
<style>
.dashboard-title {
    font-size: 30px;
    font-weight: 700;
    margin-bottom: 22px;
}

div[data-testid="stHorizontalBlock"] {
    gap: 18px;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 18px;
    padding: 20px;
    min-height: 210px;
}

.logo-box {
    width: 52px;
    height: 52px;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 27px;
    margin-bottom: 15px;
}

.card-label {
    color: #cbd5e1;
    font-size: 15px;
    margin-bottom: 12px;
}

.card-value {
    color: #ffffff;
    font-size: 25px;
    font-weight: 700;
    margin-bottom: 12px;
}

.card-info {
    color: #94a3b8;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)

   st.markdown(
    '<div class="dashboard-title">'
    '📊 Project Dashboard</div>',
    unsafe_allow_html=True
)

   col1, col2, col3 = st.columns(3)

   cards = [
    (col1, "🗄️", "#183B63", "Data Sources",
     "3", "Excel · CSV · MySQL"),
    (col2, "⚙️", "#164332", "Data Processing",
     "Automated", "Clean · Transform"),
    (col3, "📈", "#3B2857", "Visualization",
     "Insights", "Charts · Trends"),
  ]

   for col, logo, color, label, value, info in cards:
    with col:
        with st.container(border=True):
            st.markdown(f"""
            <div class="logo-box" style="background:{color}">
                {logo}
            </div>
            <div class="card-label">{label}</div>
            <div class="card-value">{value}</div>
            <div class="card-info">{info}</div>
            """, unsafe_allow_html=True)
   st.divider()
   st.subheader("Select Your Data Sources")
   source=st.radio("How do you want to Import?",['Excel','csv','MySQL'],horizontal=True)
   st.info(f"Selected Data Sources:{source}")
   st.subheader("Features of Tool")
   st.subheader("✨ Features of Tool")

   features = [
    ("📂", "Data Import",
     "Import data from Excel, CSV, and MySQL."),
    ("🧹", "Data Cleaning",
     "Handle missing values and remove duplicate records."),
    ("📊", "Data Visualization",
     "Create charts using Matplotlib and Seaborn."),
    ("💰", "Sales Analysis",
     "Analyze product sales, revenue, and profitability."),
    ("📈", "Sales Forecasting",
     "Predict future sales using historical data."),
    ("💡", "Business Recommendations",
     "Generate data-driven business insights."),
    ("🎯", "Future Planning",
     "Create future plans based on analytical results.")
    ]   

   for i, (icon, title, description) in enumerate(features, start=1):
    with st.container(border=True):
        col1, col2 = st.columns([1, 10])

        with col1:
            st.markdown(f"### {i:02d}")

        with col2:
            st.markdown(f"**{icon} {title}**")
            st.write(description)
   st.success("Application Started...........,   Data Import Will be implemented in the next step")

elif page=="Data Import":
   st.subheader("Import Data Center")
   source=st.selectbox("Select Data Source",['Excel File','CSV File',"MySQL Database"])
   if source=="Excel File":
      uploaded_file=st.file_uploader("Upload Excel File",type=["xlxs"])
      if uploaded_file is not None:
        try:
            df=pd.read_excel(uploaded_file)
            st.success("Excel File loaded...")
            col1,col2,col3,col4=st.columns(4)
            col1.metric("Total Row",df.shape[0])
            col2.metric("Total Columns",df.shape[1])
            col3.metric('Missing',df.isnull().sum().sum())
            col4.metric('Duplicates',df.duplicated().sum().sum())
            st.subheader("Data Preview")
            st.dataframe(df.head(10),use_container_width=True)
            st.subheader("Columns Information")
            st.write(df.dtypes.astype(str))
            st.session_state["row_data"]=df
        except Exception as e:
           st.error(f"Unable to read excel file:{e}")


   elif source =='CSV File':
         uploaded_file=st.file_uploader("Upload CSV File",type=['CSV'])
         if uploaded_file is not None:
            try:
               df=pd.read_csv(uploaded_file)
               col1,col2,col3,col4=st.columns(4)
               col1.metric("Total Row",df.shape[0])
               col2.metric("Total Columns",df.shape[1])
               col3.metric('Missing',df.isnull().sum().sum())
               col4.metric('Duplicates',df.duplicated().sum().sum())
               st.subheader("Data Preview")
               st.dataframe(df.head(10),use_container_width=True)
               st.subheader("Columns Information")
               st.write(df.dtypes.astype(str))
               st.session_state["row_data"]=df
            except Exception as e:
                st.error(f"Unable to read CSV file:{e}")

   elif source == 'MySQL Database':

    st.subheader("Connect To MySQL")

    host = st.text_input("Host", value="localhost")
    port = st.number_input("Port", min_value=1, max_value=65535, value=3306)
    user = st.text_input("Username", value="root")
    password = st.text_input("Password", type="password")
    database = st.text_input("Database Name")

    # Connect to MySQL
    if st.button("Connect to MySQL"):

        try:
            conn = mysql.connector.connect(
                host=host,
                port=int(port),
                user=user,
                password=password,
                database=database
            )

            cursor = conn.cursor()
            cursor.execute("SHOW TABLES")

            tables = [row[0] for row in cursor.fetchall()]

            cursor.close()
            conn.close()

            # Store connection configuration
            st.session_state["mysql_config"] = {
                "host": host,
                "port": int(port),
                "user": user,
                "password": password,
                "database": database
            }

            # Store available tables
            st.session_state["mysql_tables"] = tables

            st.success("MySQL Connected Successfully!")

        except Exception as e:
            st.error(f"Connection Failed: {e}")

    # Display tables outside the connection button
    if st.session_state.get("mysql_tables"):

        tables = st.session_state["mysql_tables"]

        st.subheader("Available Tables")

        selected_table = st.selectbox(
            "Select Table to Load",
            tables
        )

        # Load selected table
        if st.button("Load Table Data"):

            conn = None

            try:
                config = st.session_state["mysql_config"]

                conn = mysql.connector.connect(
                    host=config["host"],
                    port=config["port"],
                    user=config["user"],
                    password=config["password"],
                    database=config["database"]
                )

                # Safely quote the table name
                safe_table = "`" + selected_table.replace("`", "``") + "`"

                query = f"SELECT * FROM {safe_table}"

                df = pd.read_sql(query, conn)

                # Save data for other modules
                st.session_state["row_data"] = df

                st.success("Table data loaded successfully!")

                # Display loaded data
                st.subheader("Loaded Table Preview")

                st.dataframe(
                    df.head(10),
                    use_container_width=True
                )

                # Display row and column counts
                col1, col2 = st.columns(2)

                with col1:
                    st.metric("Total Rows", len(df))

                with col2:
                    st.metric("Total Columns", len(df.columns))

            except Exception as e:
                st.error(f"Unable to load table data: {e}")

            finally:
                if conn is not None and conn.is_connected():
                    conn.close()

    elif "mysql_tables" in st.session_state:
        st.warning("No tables found in this database.")


elif page == 'Data Cleaning':
    st.subheader("Automated Data Cleaning")
    if "row_data" not in st.session_state:
        st.warning("Please Load Data First From The import module")
    else:
        df=st.session_state["row_data"].copy()
        st.subheader("Orignal Data Priview")
        st.dataframe(df.head(10),use_container_width=True)
        report = pd.DataFrame({
            "Column":df.columns,
            "Data Type":df.dtypes.astype(str).values,
            "Missing Value": df.isna().sum().values,
            "Missin %": (df.isna().mean().values*100).round(2),
            "Unique Value":df.nunique().values
        })
        st.subheader("Data Quality Report")
        st.dataframe(report,use_container_width=True)
        st.metric('Orignal Rows',len(df))
        st.metric("Duplicated Row",int(df.duplicated().sum()))
        st.metric("Total Missing Value:",int(df.isna().sum().sum()))
        st.metric("Total Missing Values in %",(df.isna().sum().sum()/len(df)*100).round(2),"%")
        st.metric("Total Unique Value",df.nunique().sum())
        st.divider()
        st.subheader("Cleaning Opetion")
        remove_deplicates = st.checkbox("Remove duplicate rows",value=True)
        trim_spaces = st.checkbox("Remove Extra Space From text",value=True)
        missing_action=st.selectbox("Handle Missing Values",["Keep Missing Values","Remove rows with missing values","fill numeric with median and text with mode"])
        if st.button('Clean Data'):
            cleaned_df = df.copy()
            orignal_rows=len(cleaned_df)
            if remove_deplicates:
                cleaned_df = cleaned_df.drop_duplicates()
    
            if  trim_spaces :
                text_columns = cleaned_df.select_dtypes(include=['object','string']).columns
                for column in text_columns:
                    cleaned_df[column] = (cleaned_df[column].str.strip())

            if missing_action =="Remove rows with missing values":
                cleaned_df = cleaned_df.dropna()
                st.write(cleaned_df)
                st.session_state["Cleaned_data"] = cleaned_df
                st.success("Data Cleaning")
                col1, col2, col3 = st.columns(3)
                col1.metric("Original Rows", orignal_rows)
                col2.metric("Cleaned Rows", len(cleaned_df))
                col3.metric("Total Rows Removed", orignal_rows - len(cleaned_df))
                st.subheader("Cleaned data Preview")
                st.dataframe(cleaned_df,use_container_width=True)
                st.subheader('Remaining Missing Values')
                st.dataframe(cleaned_df.isna().sum().rename("Missing Values").to_frame())
                                
            elif missing_action == "fill numeric with median and text with mode":
            
                for column in cleaned_df.columns:
                    if cleaned_df[column].isna().any():
                        if pd.api.types.is_numeric_dtype(cleaned_df[column]):
                            median_value = cleaned_df[column].median()
                            if pd.notna(median_value):
                                cleaned_df[column] = cleaned_df[column].fillna(median_value)
                            
                        else:
                               mode_value = cleaned_df[column].mode(dropna=True)
                               if not mode_value.empty:
                                  cleaned_df[column]= cleaned_df[column].fillna(mode_value.iloc[0])
                st.session_state["Cleaned_data"] = cleaned_df
                st.success("Data Cleaning")
                col1, col2, col3 = st.columns(3)
                col1.metric("Original Rows", orignal_rows)
                col2.metric("Cleaned Rows", len(cleaned_df))
                col3.metric("Total Rows Removed", orignal_rows - len(cleaned_df))
                st.subheader("Cleaned data Preview")
                st.dataframe(cleaned_df,use_container_width=True)
                st.subheader('Remaining Missing Values')
                st.dataframe(cleaned_df.isna().sum().rename("Missing Values").to_frame())
            else:
                st.session_state["Cleaned_data"] = cleaned_df
                st.success("Data Cleaning")
                col1, col2, col3 = st.columns(3)
                col1.metric("Original Rows", orignal_rows)
                col2.metric("Cleaned Rows", len(cleaned_df))
                col3.metric("Total Rows Removed", orignal_rows - len(cleaned_df))
                st.subheader("Cleaned data Preview")
                st.dataframe(cleaned_df,use_container_width=True)
                st.subheader('Remaining Missing Values')
                st.dataframe(cleaned_df.isna().sum().rename("Missing Values").to_frame())
                                   
                csv_data = cleaned_df.to_csv(index=True).encode("utf-8-sig")
                st.download_button("Download Cleaned File",data=csv_data,file_name="Cleaned data.csv",mime='text/csv')



elif page=="Data Visulization":
    st.subheader("📊 Dynamic Visulization Charts")
    if "Cleaned_data" in st.session_state:
        df = st.session_state["Cleaned_data"].copy()
        st.success("Using Cleaned Data")

    else:
        df = None
        st.warning("Please clean the data first from Data Cleaning page.")
    if df is not None:
        if df.empty:
            st.warning("The selected dataset is empty")
        elif len(df.columns)==0:
            st.warning("The data set has no columns")
        else:
            st.write("Dataset Preview")
            st.dataframe(df,use_container_width=True)
            chart_type =['Line Chart','Bar Chart','Horizental Bar Chart','Pie Chart','Donut Chart','Scatter Chart','Area Chart','Step Chart'
                         ,'Heatmap',"Stem Chart"]
            chart_type = st.selectbox("Select Chart Type",chart_type)
            columns= df.columns.tolist()
            numeric_columns = df.select_dtypes(include='number').columns.tolist()
            x_column =st.selectbox("Select X-Axis/Category",columns)
            y_option = numeric_columns or columns
            y_column = st.selectbox("Select Y-Axis/Values",y_option)
            color_column = st.selectbox("Option Grouping Column",["None"] + columns )
            aggregation = st.selectbox("Select Calculation",["Normal", "Maximum", "Average", "Minimum"])
            
            df[y_column] = pd.to_numeric(df[y_column], errors="coerce")
            
            if st.button("Generate Chart"):
                try:
                    import matplotlib.pyplot as plt 
                    x=df[x_column]
                    y = pd.to_numeric(df[y_column], errors="coerce")                  
                    valid = x.notna() & y.notna()
                    x = x[valid]
                    y = y[valid]
                    if len(x) == 0:
                        st.error("No Valid Data Availabel for this Chart")
                    elif chart_type in ['Scatter Plot','Hexbin Plot','Bubble Chart'] and not pd.api.types.is_numeric_dtype(df[x_column]):
                        st.error("This Chart Required")
                
                        
                    if aggregation == "Normal":
                        chart_data = df.groupby(x_column)[y_column].sum()
                    elif aggregation == "Maximum":
                        chart_data = df.groupby(x_column)[y_column].max()
                    elif aggregation == "Average":
                        chart_data = df.groupby(x_column)[y_column].mean()
                    elif aggregation == "Minimum":
                        chart_data = df.groupby(x_column)[y_column].min()

        
            

                    if chart_type=='Line Chart':
                        fig, ax = plt.subplots(figsize=(6,4))
                        ax.plot( chart_data.index.astype(str), chart_data.values ,marker='o', linewidth=2)
                        ax.set_title("Data Visualization")
                        ax.set_xlabel(x_column)
                        ax.set_ylabel(y_column)
                        ax.grid(True, alpha=0.3)
                        plt.xticks(rotation=45)
                        fig.tight_layout()
                        st.pyplot(fig)

                    elif chart_type == 'Bar Chart':
                        fig, ax = plt.subplots(figsize=(6,4))

                        bars = ax.bar( chart_data.index.astype(str), chart_data.values )
                        ax.bar_label(bars, fmt="%.2f", padding=3)
                        ax.set_title("Bar Chart")
                        ax.set_xlabel(x_column)
                        ax.set_ylabel(y_column)
                        plt.xticks(rotation=45)
                        fig.tight_layout()

                        st.pyplot(fig)
                    elif chart_type =='Horizental Bar Chart':
                        fig, ax = plt.subplots(figsize=(6,4)) 
                        bars = ax.barh( chart_data.index.astype(str), chart_data.values ) 
                        # Add labels 
                        ax.bar_label(bars, fmt="%.2f", padding=3) 
                        ax.set_title(f"{aggregation} {y_column} by {x_column}") 
                        ax.set_xlabel(y_column) 
                        ax.set_ylabel(x_column) 
                        fig.tight_layout() 
                        st.pyplot(fig) 
                    elif chart_type =='Pie Chart':
                        fig, ax = plt.subplots(figsize=(4,4))
                        ax.pie( chart_data.values, labels=chart_data.index.astype(str), autopct="%1.1f%%", startangle=90, pctdistance=0.7 ) 
                        ax.set_title(f"{aggregation} {y_column} by {x_column}") 
                        ax.axis("equal") 
                        st.pyplot(fig)

                    elif chart_type == 'Donut Chart':
                        fig, ax = plt.subplots(figsize=(4,4))
                        ax.pie( chart_data.values, labels=chart_data.index.astype(str), autopct="%1.1f%%", startangle=90, pctdistance=0.7,wedgeprops={'width':0.5} ) 
                        ax.set_title(f"{aggregation} {y_column} by {x_column}") 
                        ax.axis("equal") 
                        st.pyplot(fig)

                    elif chart_type =="Scatter Chart":
                        fig,ax = plt.subplots(figsize=(6,4))
                        ax.scatter( chart_data.index.astype(str), chart_data.values )
                         
                        ax.set_title(f"{aggregation} {y_column} by {x_column}") 
                        ax.set_xlabel(y_column) 
                        ax.set_ylabel(x_column) 
                        fig.tight_layout() 
                        st.pyplot(fig) 

                    elif chart_type =='Area Chart':
                        
                        fig,ax = plt.subplots(figsize=(6,4))
                        ax.fill_between( range(len(chart_data)), chart_data.values, alpha=0.4 )
                        ax.plot( range(len(chart_data)), chart_data.values, marker="o", linewidth=2 )
                        ax.set_xticks(range(len(chart_data))) 
                        ax.set_xticklabels( chart_data.index.astype(str), rotation=45, ha="right" )
                        ax.set_title(f"{aggregation} {y_column} by {x_column}") 
                        ax.set_xlabel(y_column) 
                        ax.set_ylabel(x_column) 
                        ax.grid(True, alpha=0.3)
                        fig.tight_layout() 
                        st.pyplot(fig) 
                    elif chart_type =='Step Chart':
                        
                        fig, ax = plt.subplots(figsize=(6,4)) 
                        x = range(len(chart_data)) 
                        y = chart_data.values 
                        ax.step(x, y, where="mid", linewidth=2) 
                        ax.plot(x, y, "o", markersize=5) 
                        ax.set_xticks(list(x)) 
                        ax.set_xticklabels( chart_data.index.astype(str), rotation=45, ha="right" ) 
                        ax.set_title(f"{aggregation} {y_column} by {x_column}") 
                        ax.set_xlabel(x_column) 
                        ax.set_ylabel(y_column) 
                        ax.grid(True, alpha=0.3) 
                        fig.tight_layout() 
            
                        st.pyplot(fig)
                
                    elif chart_type =='Stem Chart':
                        
                        fig, ax = plt.subplots(figsize=(6,4)) 
                        x = range(len(chart_data)) 
                        y = chart_data.values 
                        ax.stem(x, y, markerfmt='*',linefmt='--',basefmt='-') 
                        ax.plot(x, y, "o", markersize=5) 
                        ax.set_xticks(list(x)) 
                        ax.set_xticklabels( chart_data.index.astype(str), rotation=45, ha="right" ) 
                        ax.set_title(f"{aggregation} {y_column} by {x_column}") 
                        ax.set_xlabel(x_column) 
                        ax.set_ylabel(y_column) 
                        ax.grid(True, alpha=0.3) 
                        fig.tight_layout() 

                    elif chart_type =='Heatmap':
                        numeric_df = df.select_dtypes(include="number")
                        if numeric_df.empty or len(numeric_df.columns) < 2: 
                            st.error("For Heatmap Minimum Select  Two  Numrics columns") 
                        else: 
                            corr = numeric_df.corr()
                        fig, ax = plt.subplots(figsize=(10, 6)) 
                        sn.heatmap( corr, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax )
                        ax.set_title("Correlation Heatmap") 
                        fig.tight_layout() 
                        st.pyplot(fig)
                    if "fig" in locals():

                        chart_buffer = io.BytesIO()

                        fig.savefig(
                            chart_buffer,
                            format="png",
                            bbox_inches="tight"
                        )

                        st.session_state["visualization_chart_png"] = (
                            chart_buffer.getvalue()
                        )

                        st.session_state["visualization_chart_title"] = (
                            chart_type
                        )

                        # Save chart data if available
                        if "chart_data" in locals():

                            st.session_state["visualization_chart_data_csv"] = (
                                chart_data.rename("value")
                                .to_csv()
                                .encode("utf-8-sig")
                            )

                        plt.close(fig)

 
                except Exception as e:
                    st.error(f"{e}")



elif page == "Forecasting":

    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import io

    st.title("📈 Sales Forecasting")
    st.write("Forecast future values using Moving Average.")

    # Check data availability
    if "Cleaned_data" in st.session_state:
        df = st.session_state["Cleaned_data"].copy()

    elif "row_data" in st.session_state:
        df = st.session_state["row_data"].copy()

    else:
        st.warning("Please import your dataset first.")
        st.stop()

    # Select numeric columns
    numeric_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    if not numeric_columns:
        st.error("No numeric columns available.")
        st.stop()

    # Select target column
    target_column = st.selectbox(
        "Select Sales / Revenue Column",
        numeric_columns
    )

    # Select moving average window
    window = st.number_input(
        "Moving Average Window",
        min_value=2,
        max_value=30,
        value=3,
        step=1
    )

    # Select forecast periods
    periods = st.number_input(
        "Forecast Periods",
        min_value=1,
        max_value=365,
        value=7,
        step=1
    )

    # Select chart type
    chart_type = st.selectbox(
        "Select Chart Type",
        ["Line Chart", "Bar Chart"]
    )

    if st.button("Generate Forecast"):

        # Prepare numeric data
        values = pd.to_numeric(
            df[target_column],
            errors="coerce"
        ).dropna().to_numpy(dtype=float)

        if not np.isfinite(values).all():

            st.error("Data contains invalid numeric values.")

        elif len(values) < int(window):

            st.error(
                f"Please provide at least {int(window)} valid records."
            )

        else:

            # Select only the historical records
            # used as the initial moving average window
            historical_data = values[-int(window):]

            # Create a separate history for forecasting
            history = list(historical_data)

            forecast = []

            # Generate future predictions
            for i in range(int(periods)):

                next_value = round(
                    np.mean(history[-int(window):]), 1
                )

                forecast.append(next_value)

                # Add prediction for the next calculation
                history.append(next_value)

            # Create forecast table
            forecast_df = pd.DataFrame({
                "Future Period": range(
                    int(window) + 1,
                    int(window) + int(periods) + 1
                ),
                "Predicted " + target_column: forecast
            })

            # Save forecast data for Reports
            st.session_state["forecast_report_df"] = (
                forecast_df.copy()
            )

            st.session_state["forecast_column"] = target_column

            st.subheader("Forecast Results")

            st.dataframe(
                forecast_df,
                use_container_width=True
            )

            # Chart periods
            historical_periods = range(
                1, len(historical_data) + 1
            )

            future_periods = range(
                len(historical_data) + 1,
                len(historical_data) + int(periods) + 1
            )

            # Create chart
            fig, ax = plt.subplots(figsize=(10, 5))

            if chart_type == "Line Chart":

                ax.plot(
                    historical_periods,
                    historical_data,
                    marker="o",
                    label="Selected Historical Data"
                )

                ax.plot(
                    future_periods,
                    forecast,
                    marker="o",
                    linestyle="--",
                    label="Forecast"
                )

                # Show historical mean
                mean_value = np.mean(historical_data)

                ax.axhline(
                    mean_value,
                    linestyle=":",
                    label=f"Historical Mean: {mean_value:.2f}"
                )

                ax.set_title(
                    f"{target_column} - Moving Average Forecast"
                )

                ax.set_xlabel("Historical Records + Future Periods")
                ax.set_ylabel(target_column)
                ax.legend()
                ax.grid(axis="y", alpha=0.3)

            elif chart_type == "Bar Chart":

                bars = ax.bar(
                    historical_periods,
                    historical_data,
                    label="Selected Historical Data"
                )

                forecast_bars = ax.bar(
                    future_periods,
                    forecast,
                    label="Forecast"
                )

                ax.bar_label(bars, fontsize=8)
                ax.bar_label(forecast_bars, fontsize=8)

                ax.set_title(
                    f"{target_column} - Moving Average Forecast"
                )

                ax.set_xlabel("Historical Records + Future Periods")
                ax.set_ylabel(target_column)
                ax.legend()
                ax.grid(axis="y", alpha=0.3)

            fig.tight_layout()

            # Display chart
            st.pyplot(fig)

            # Save chart for Reports page
            chart_buffer = io.BytesIO()

            fig.savefig(
                chart_buffer,
                format="png",
                bbox_inches="tight"
            )

            st.session_state["forecast_chart_png"] = (
                chart_buffer.getvalue()
            )

            plt.close(fig)

            # Download forecast CSV
            csv_data = forecast_df.to_csv(
                index=False
            ).encode("utf-8-sig")

            st.download_button(
                "📥 Download Forecast CSV",
                data=csv_data,
                file_name="forecast_results.csv",
                mime="text/csv"
            )

            st.success("Forecast generated successfully!")


elif page == "Reports":

    import matplotlib.pyplot as plt

    st.title("📑 Complete Project Reports")
    st.write("Data Cleaning, Visualization and Forecasting Reports")
    st.divider()

    # GET DATA
    raw_df = st.session_state.get("row_data")
    cleaned_df = st.session_state.get("Cleaned_data")

    if raw_df is None:
        st.warning("Please import your dataset first.")

    else:

        df = cleaned_df if cleaned_df is not None else raw_df

        # =====================================
        # 1. DATASET OVERVIEW
        # =====================================

        st.header("1. 📊 Dataset Overview")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Rows", df.shape[0])
        col2.metric("Total Columns", df.shape[1])
        col3.metric("Missing Values", int(df.isna().sum().sum()))
        col4.metric("Duplicate Rows", int(df.duplicated().sum()))

        st.subheader("Dataset Preview")
        st.dataframe(df.head(10), use_container_width=True)

        # Download current dataset
        st.download_button(
            "⬇️ Download Current Dataset",
            data=df.to_csv(index=False).encode("utf-8-sig"),
            file_name="current_dataset.csv",
            mime="text/csv",
            key="report_current_data"
        )

        # =====================================
        # 2. DATA CLEANING REPORT
        # =====================================

        st.divider()
        st.header("2. 🧹 Data Cleaning Report")

        if cleaned_df is not None:

            original_rows = len(raw_df)
            cleaned_rows = len(cleaned_df)

            original_missing = int(raw_df.isna().sum().sum())
            cleaned_missing = int(cleaned_df.isna().sum().sum())

            original_duplicates = int(raw_df.duplicated().sum())
            cleaned_duplicates = int(cleaned_df.duplicated().sum())

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Original Rows",
                original_rows
            )

            col2.metric(
                "Cleaned Rows",
                cleaned_rows
            )

            col3.metric(
                "Rows Removed",
                original_rows - cleaned_rows
            )

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Missing Before",
                original_missing
            )

            col2.metric(
                "Missing After",
                cleaned_missing
            )

            col3.metric(
                "Duplicates Removed",
                original_duplicates - cleaned_duplicates
            )

            # Column-wise cleaning report
            cleaning_report = pd.DataFrame({
                "Column": cleaned_df.columns.astype(str),
                "Data Type": cleaned_df.dtypes.astype(str).values,
                "Missing Values": cleaned_df.isna().sum().values,
                "Missing Percentage": (
                    cleaned_df.isna().mean().values * 100
                ).round(1),
                "Unique Values": [
                    cleaned_df.iloc[:, i].nunique()
                    for i in range(len(cleaned_df.columns))
                ]
            })

            st.subheader("Cleaned Data Quality Report")

            st.dataframe(
                cleaning_report,
                use_container_width=True
            )

            st.download_button(
                "⬇️ Download Cleaning Report CSV",
                data=cleaning_report.to_csv(
                    index=False
                ).encode("utf-8-sig"),
                file_name="cleaning_report.csv",
                mime="text/csv",
                key="report_cleaning_csv"
            )

            st.download_button(
                "⬇️ Download Cleaned Dataset",
                data=cleaned_df.to_csv(
                    index=False
                ).encode("utf-8-sig"),
                file_name="cleaned_dataset.csv",
                mime="text/csv",
                key="report_cleaned_data"
            )

        else:
            st.info(
                "Please open Data Cleaning and click Clean Data first."
            )

        # =====================================
        # 3. DATA VISUALIZATION REPORT
        # =====================================

        st.divider()
        st.header("3. 📈 Data Visualization Report")

        viz_png = st.session_state.get(
            "visualization_chart_png"
        )

        viz_title = st.session_state.get(
            "visualization_chart_title",
            "Data Visualization"
        )

        viz_csv = st.session_state.get(
            "visualization_chart_data_csv"
        )

        if viz_png is not None:

            st.subheader(viz_title)

            st.image(
                viz_png,
                use_container_width=True
            )

            st.download_button(
                "⬇️ Download Visualization Chart",
                data=viz_png,
                file_name="visualization_chart.png",
                mime="image/png",
                key="report_viz_png"
            )

            if viz_csv is not None:

                st.download_button(
                    "⬇️ Download Visualization Data",
                    data=viz_csv,
                    file_name="visualization_data.csv",
                    mime="text/csv",
                    key="report_viz_csv"
                )

        else:
            st.info(
                "Generate a chart on the Data Visulization page first. "
                "The chart must be saved in session state to appear here."
            )

        # =====================================
        # 4. FORECASTING REPORT
        # =====================================

        st.divider()
        st.header("4. 🔮 Forecasting Report")

        forecast_df = st.session_state.get(
            "forecast_report_df"
        )

        forecast_png = st.session_state.get(
            "forecast_chart_png"
        )

        forecast_column = st.session_state.get(
            "forecast_column",
            "Forecast Column"
        )

        if forecast_df is not None:

            st.write(
                f"Forecast Column: **{forecast_column}**"
            )

            st.subheader("Forecast Results")

            st.dataframe(
                forecast_df,
                use_container_width=True
            )

            st.download_button(
                "⬇️ Download Forecast Results CSV",
                data=forecast_df.to_csv(
                    index=False
                ).encode("utf-8-sig"),
                file_name="forecast_results.csv",
                mime="text/csv",
                key="report_forecast_csv"
            )

            if forecast_png is not None:

                st.subheader("Forecast Chart")

                st.image(
                    forecast_png,
                    use_container_width=True
                )

                st.download_button(
                    "⬇️ Download Forecast Chart",
                    data=forecast_png,
                    file_name="forecast_chart.png",
                    mime="image/png",
                    key="report_forecast_png"
                )

        else:
            st.info(
                "Generate a forecast on the Forecasting page first. "
                "The forecast results must be saved in session state."
            )

        # =====================================
        # 5. NUMERIC SUMMARY
        # =====================================

        st.divider()
        st.header("5. 📋 Numeric Summary")

        numeric_df = df.select_dtypes(include="number")

        if not numeric_df.empty:

            summary = numeric_df.describe().round(2)

            st.dataframe(
                summary,
                use_container_width=True
            )

            st.download_button(
                "⬇️ Download Numeric Summary",
                data=summary.to_csv().encode("utf-8-sig"),
                file_name="numeric_summary.csv",
                mime="text/csv",
                key="report_summary_csv"
            )

        else:
            st.info("No numeric columns available.")

        # =====================================
        # 6. EXCEL REPORT
        # =====================================

        st.divider()
        st.header("6. 📁 Download Complete Excel Report")

        excel_buffer = io.BytesIO()

        try:

            with pd.ExcelWriter(
                excel_buffer,
                engine="openpyxl"
            ) as writer:

                raw_df.to_excel(
                    writer,
                    sheet_name="Original Data",
                    index=False
                )

                df.to_excel(
                    writer,
                    sheet_name="Current Data",
                    index=False
                )

                column_info = pd.DataFrame({
                    "Column": df.columns.astype(str),
                    "Data Type": df.dtypes.astype(str).values,
                    "Missing Values": df.isna().sum().values,
                    "Unique Values": [
                        df.iloc[:, i].nunique()
                        for i in range(len(df.columns))
                    ]
                })

                column_info.to_excel(
                    writer,
                    sheet_name="Column Information",
                    index=False
                )

                if not numeric_df.empty:
                    numeric_df.describe().round(2).to_excel(
                        writer,
                        sheet_name="Numeric Summary"
                    )

                if cleaned_df is not None:
                    cleaning_report.to_excel(
                        writer,
                        sheet_name="Cleaning Report",
                        index=False
                    )

                if forecast_df is not None:
                    forecast_df.to_excel(
                        writer,
                        sheet_name="Forecast",
                        index=False
                    )

            st.download_button(
                "⬇️ Download Complete Excel Report",
                data=excel_buffer.getvalue(),
                file_name="complete_project_report.xlsx",
                mime=(
                    "application/vnd.openxmlformats-officedocument."
                    "spreadsheetml.sheet"
                ),
                key="report_excel"
            )

        except Exception as e:
            st.error(f"Excel Report Error: {e}")

        # =====================================
        # 7. COMPLETE ZIP REPORT
        # =====================================

        st.divider()
        st.header("7. 📦 Download Complete ZIP Report")

        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(
            zip_buffer,
            mode="w",
            compression=zipfile.ZIP_DEFLATED
        ) as archive:

            archive.writestr(
                "original_data.csv",
                raw_df.to_csv(index=False)
            )

            archive.writestr(
                "current_data.csv",
                df.to_csv(index=False)
            )

            if cleaned_df is not None:

                archive.writestr(
                    "cleaned_data.csv",
                    cleaned_df.to_csv(index=False)
                )

                archive.writestr(
                    "cleaning_report.csv",
                    cleaning_report.to_csv(index=False)
                )

            if not numeric_df.empty:

                archive.writestr(
                    "numeric_summary.csv",
                    numeric_df.describe().round(2).to_csv()
                )

            if viz_png is not None:

                archive.writestr(
                    "visualization_chart.png",
                    viz_png
                )

            if viz_csv is not None:

                archive.writestr(
                    "visualization_data.csv",
                    viz_csv
                )

            if forecast_df is not None:

                archive.writestr(
                    "forecast_results.csv",
                    forecast_df.to_csv(index=False)
                )

            if forecast_png is not None:

                archive.writestr(
                    "forecast_chart.png",
                    forecast_png
                )

        st.download_button(
            "⬇️ Download Complete Project ZIP",
            data=zip_buffer.getvalue(),
            file_name="complete_project_report.zip",
            mime="application/zip",
            key="report_zip"
        )

        st.success("Reports are ready!")