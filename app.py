import streamlit as st
import pandas as pd
import json
import plotly.express as px

# --- Page Configuration ---
st.set_page_config(
    page_title="Spectrum Auction Analysis",
    page_icon="📡",
    layout="wide",
)

# --- Styling and Palette ---
# Define a professional color palette
COLORS = {
    "primary": "#3366cc", # A rich blue for main elements
    "secondary": "#2e8b57", # A forest green for accents
    "success_bar": "#3cb371", # A medium sea green
    "fail_bar": "#d86464", # A muted red
    "background_light": "#f0f2f6", # A very light gray for background
    "text_dark": "#262730" # A dark charcoal for text
}

# Inject custom CSS for a cleaner, more modern look
st.markdown(f"""
    <style>
    .reportview-container {{
        background-color: {COLORS["background_light"]};
    }}
    .sidebar .sidebar-content {{
        background-color: {COLORS["background_light"]};
    }}
    .stButton>button {{
        background-color: {COLORS["primary"]};
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
    }}
    .stButton>button:hover {{
        background-color: {COLORS["secondary"]};
    }}
    .stTabs .stTabs--activeTab {{
        background-color: {COLORS["primary"]};
        color: white;
    }}
    h1 {{
        color: {COLORS["primary"]};
        text-align: center;
        padding: 20px 0;
        border-bottom: 2px solid {COLORS["primary"]};
    }}
    h2, h3, h4 {{
        color: {COLORS["text_dark"]};
    }}
    .stTabs {{
        background-color: #ffffff;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        padding: 15px;
        margin-bottom: 20px;
    }}
    .stPlotlyChart {{
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        overflow: hidden;
    }}
    </style>
""", unsafe_allow_html=True)


# --- Data Loading ---
@st.cache_data
def load_data():
    """
    Loads all necessary data from local CSV files.
    - band_analysis.csv: Analysis by frequency band.
    - band_analysis_filtered.csv: Filtered analysis by band.
    - service_area_analysis.csv: Analysis by service area.
    - spectrum-auction-report.md: Markdown report with insights.
    """
    data = {}
    files_to_load = {
        'band_data': 'band_analysis.csv',
        'band_data_filtered': 'band_analysis_filtered.csv',
        'area_data': 'service_area_analysis.csv',
        'report_md': 'spectrum-auction-report.md'
    }

    for key, filename in files_to_load.items():
        try:
            if filename.endswith('.csv'):
                # For CSV files, load them into pandas DataFrames
                data[key] = pd.read_csv(filename)
            else:
                # For the markdown file, read its content as a string
                with open(filename, 'r', encoding='utf-8') as f:
                    data[key] = f.read()
        except FileNotFoundError:
            st.error(f"Error: The file '{filename}' was not found. Please make sure it's in the correct directory.")
            return (None,) * 4
        except Exception as e:
            st.error(f"An unexpected error occurred while loading '{filename}': {e}")
            return (None,) * 4
            
    return data.get('band_data'), data.get('band_data_filtered'), data.get('area_data'), data.get('report_md')

# Load the data
band_data, band_data_filtered, area_data, report_md = load_data()

# Halt application if data loading fails
if not all([band_data is not None, band_data_filtered is not None, area_data is not None, report_md]):
    st.warning("One or more data files could not be loaded. Halting the application.")
    st.stop()

# --- Main Application ---
st.title("Spectrum Auction Analysis Dashboard 📡")
st.markdown("An in-depth look at Indian Spectrum Auctions based on provided auction data.")


# Use st.container to create a visually distinct main content area
with st.container():
    # --- Sidebar Navigation ---
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Band Analysis", "Service Area Analysis", "Auction Insights", "Data Export"])

    # --- Band Analysis Page ---
    if page == "Band Analysis":
        st.header("Analysis by Frequency Band")
        
        # Add a selector for filtered/unfiltered data
        analysis_type = st.radio(
            "Select Band Analysis View",
            ('All Bands', 'Without 26000 MHz Band'),
            help="Choose to view data for all bands or exclude the 26000 MHz band."
        )

        if analysis_type == 'All Bands':
            band_df = band_data
            st.subheader("Performance Metrics for All Bands")
            # Bar chart for Success Rate
            st.markdown("#### Success Rate by Band")
            fig1 = px.bar(
                band_df, 
                x='Band', 
                y='Success_Rate', 
                title='Success Rate by Frequency Band',
                color_discrete_sequence=[COLORS["success_bar"]],
                template="plotly_white"
            )
            fig1.update_layout(yaxis_title="Success Rate (%)", xaxis_title="Frequency Band (MHz)")
            st.plotly_chart(fig1, use_container_width=True)

            # Bar chart for WP/RP Ratio
            st.markdown("#### Winning Price vs. Reserve Price Ratio")
            fig2 = px.bar(
                band_df, 
                x='Band', 
                y='WP_RP_Ratio', 
                title='WP/RP Ratio by Frequency Band',
                color_discrete_sequence=[COLORS["primary"]],
                template="plotly_white"
            )
            fig2.update_layout(yaxis_title="WP/RP Ratio", xaxis_title="Frequency Band (MHz)")
            st.plotly_chart(fig2, use_container_width=True)

        else: # analysis_type == 'Without 26000 MHz Band'
            band_df = band_data_filtered
            st.subheader("Performance Metrics (26000 MHz Band Excluded)")

            # Bar chart for Success Rate without the 26000 MHz band
            st.markdown("#### Success Rate by Band (26000 MHz Band Excluded)")
            fig1_filtered = px.bar(
                band_df, 
                x='Band', 
                y='Success_Rate', 
                title='Success Rate by Frequency Band (Filtered)',
                color_discrete_sequence=[COLORS["success_bar"]],
                template="plotly_white"
            )
            fig1_filtered.update_layout(yaxis_title="Success Rate (%)", xaxis_title="Frequency Band (MHz)")
            st.plotly_chart(fig1_filtered, use_container_width=True)

            # Bar chart for WP/RP Ratio without the 26000 MHz band
            st.markdown("#### Winning Price vs. Reserve Price Ratio (26000 MHz Band Excluded)")
            fig2_filtered = px.bar(
                band_df, 
                x='Band', 
                y='WP_RP_Ratio', 
                title='WP/RP Ratio by Frequency Band (Filtered)',
                color_discrete_sequence=[COLORS["primary"]],
                template="plotly_white"
            )
            fig2_filtered.update_layout(yaxis_title="WP/RP Ratio", xaxis_title="Frequency Band (MHz)")
            st.plotly_chart(fig2_filtered, use_container_width=True)


    # --- Service Area Analysis Page ---
    elif page == "Service Area Analysis":
        st.header("Analysis by Service Area")
        area_df = area_data

        # Bar charts for performance metrics by service area
        st.subheader("Performance Metrics by Service Area")
        
        st.markdown("#### Success Rate by Service Area")
        # Apply the custom color palette and a clean theme to the plot
        fig1 = px.bar(
            area_df, 
            x='Service_Area', 
            y='Success_Rate', 
            title='Success Rate by Service Area',
            color_discrete_sequence=[COLORS["success_bar"]],
            template="plotly_white"
        )
        fig1.update_layout(yaxis_title="Success Rate (%)", xaxis_title="Service Area")
        st.plotly_chart(fig1, use_container_width=True)

        st.markdown("#### Winning Price vs. Reserve Price Ratio")
        # Apply the custom color palette and a clean theme to the plot
        fig2 = px.bar(
            area_df, 
            x='Service_Area', 
            y='WP_RP_Ratio', 
            title='WP/RP Ratio by Service Area',
            color_discrete_sequence=[COLORS["primary"]],
            template="plotly_white"
        )
        fig2.update_layout(yaxis_title="WP/RP Ratio", xaxis_title="Service Area")
        st.plotly_chart(fig2, use_container_width=True)

    # --- Auction Insights Page ---
    elif page == "Auction Insights":
        st.header("Key Insights and Report")
        st.markdown(report_md, unsafe_allow_html=True)

    # --- Data Export Page ---
    elif page == "Data Export":
        st.header("Export Data")
        st.markdown("Select a dataset to download in CSV or JSON format.")

        # Update export options to reflect new data sources
        export_option = st.selectbox(
            "Choose a dataset to export:", 
            ["Band Analysis (All)", "Band Analysis (Filtered)", "Service Area Analysis"]
        )

        if export_option == "Band Analysis (All)":
            df_export = band_data
            file_prefix = "band_analysis_all"
        elif export_option == "Band Analysis (Filtered)":
            df_export = band_data_filtered
            file_prefix = "band_analysis_filtered"
        else: # Service Area Analysis
            df_export = area_data
            file_prefix = "service_area_analysis"

        st.dataframe(df_export, use_container_width=True)

        # Download buttons
        col1, col2 = st.columns(2)
        
        # CSV Download
        csv = df_export.to_csv(index=False).encode('utf-8')
        col1.download_button(
            label="Download as CSV",
            data=csv,
            file_name=f"{file_prefix}.csv",
            mime='text/csv',
        )

        # JSON Download
        json_string = df_export.to_json(orient='records', indent=4)
        col2.download_button(
            label="Download as JSON",
            data=json_string,
            file_name=f"{file_prefix}.json",
            mime='application/json',
        )