import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode

# Function to load CSV
def load_csv(file_path):
    return pd.read_csv(file_path)

# Function to save CSV
def save_csv(data, file_path):
    with open(file_path, 'w') as f:
        f.write(data)

# Function to save unique records based on course code
def save_unique_csv(df, file_path):
    df.drop_duplicates(subset=['course code'], keep='first', inplace=True)
    df.to_csv(file_path, index=False)

def main():
    # Define CSV file paths
    csv_files = {
        "Faculty Name": 'faculty_name.csv',
        "Management Electives": 'management_elect.csv',
        "Mandatory Courses": 'mandatory_course.csv',
        "Open Electives": 'open_elect.csv',
        "Semester 3": 'sem3.csv',
        "Semester 4": 'sem4.csv',
        "Semester 5": 'sem5.csv',
        "Semester 6": 'sem6.csv',
        "Semester 7": 'sem7.csv',
        "Semester 8": 'sem8.csv',
        "Professional Electives": 'prof_elect.csv'
    }

    # Title of the Streamlit app
    st.title("Edit CSV Files")

    # Sidebar dropdown for selecting CSV file
    selected_csv = st.sidebar.selectbox("Select CSV File", list(csv_files.keys()))

    # Load initial CSV data
    df = load_csv(csv_files[selected_csv])
    csv_content = df.to_csv(index=False)

    # Sub-tabs for different editing methods
    sub_tab = st.sidebar.radio("Select Editing Method", ("Excel-like Editor", "Text Editor"))

    # Text Editor tab
    if sub_tab == "Text Editor":
        st.header("Edit CSV content in Text Area")
        edited_csv = st.text_area(f"Edit CSV content below ({selected_csv}):", csv_content, height=400)

        # Save button for text area
        if st.button(f'Save Changes from Text Editor ({selected_csv})'):
            save_csv(edited_csv, csv_files[selected_csv])
            st.success("Changes saved successfully!")
            df = load_csv(csv_files[selected_csv])  # Reload the DataFrame to reflect changes
            csv_content = df.to_csv(index=False)
            if selected_csv == "Professional Electives":
                save_unique_csv(df, 'prof_elect_unique.csv')

    # Excel-like Editor tab
    elif sub_tab == "Excel-like Editor":
        st.header("Edit CSV content in Excel-like Grid")

        # Create a GridOptionsBuilder object
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_pagination(paginationAutoPageSize=True)  # Add pagination
        gb.configure_default_column(editable=True, resizable=True)  # Make columns editable
        gb.configure_grid_options(domLayout='normal')  # Normal layout for better scrolling
        grid_options = gb.build()

        # Display the grid
        grid_response = AgGrid(
            df,
            gridOptions=grid_options,
            update_mode=GridUpdateMode.MODEL_CHANGED,  # Update mode for live editing
            data_return_mode=DataReturnMode.FILTERED_AND_SORTED,  # Return filtered and sorted data
            fit_columns_on_grid_load=True,  # Fit columns on grid load
            enable_enterprise_modules=False,  # Disable enterprise modules for simplicity
            height=600,
            width='100%',
            reload_data=False
        )

        # Get the updated dataframe
        updated_df = grid_response['data']
        updated_df = pd.DataFrame(updated_df)  # Convert to DataFrame

        # Save button for grid editor
        if st.button(f'Save Changes from Grid Editor ({selected_csv})'):
            updated_df.to_csv(csv_files[selected_csv], index=False)
            st.success("Changes saved successfully!")
            df = load_csv(csv_files[selected_csv])  # Reload the DataFrame to reflect changes
            if selected_csv == "Professional Electives":
                save_unique_csv(df, 'prof_elect_unique.csv')

        # Display the updated dataframe
        st.write(f"Updated Data ({selected_csv})")
        st.dataframe(df)

if __name__ == "__main__":
    main()
