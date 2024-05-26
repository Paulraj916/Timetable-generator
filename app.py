import streamlit as st
import all_data_alteration
import faculty_sub
import hour_calculation
import tt

def main():
    st.title("University Timetable Management System")

    # Initialize session state if not already set
    if 'all_data_alteration' not in st.session_state:
        st.session_state.all_data_alteration = False
    if 'hour_calculation' not in st.session_state:
        st.session_state.hour_calculation = False
    if 'faculty_sub' not in st.session_state:
        st.session_state.faculty_sub = False

    # Step 1: Create sidebar navigation
    page = st.sidebar.radio("Navigate", [ "Data Alteration", "Hour Calculation", "Faculty Subjects Management", "Timetable Generation"])

    # Step 2: Display content based on the selected page
    if page == "Data Alteration":
        st.subheader("Data Alteration")
        # Call the main function of all_data_alteration.py or its functionality
        all_data_alteration.main()
        st.session_state.all_data_alteration = True

    elif page == "Hour Calculation":
        st.subheader("Hour Calculation")
        # Call the main function of hour_calculation.py or its functionality
        hour_calculation.main()
        st.session_state.hour_calculation = True

    elif page == "Faculty Subjects Management":
        st.subheader("Faculty Subjects Management")
        # Call the main function of faculty_sub.py or its functionality
        faculty_sub.main()
        st.session_state.faculty_sub = True

    elif page == "Timetable Generation":
        # Enable timetable generation only if all other pages have been visited
        if all([st.session_state.all_data_alteration, st.session_state.hour_calculation, st.session_state.faculty_sub]):
            st.subheader("Timetable Generation")
            # Call the main function of tt.py or its functionality
            tt.main()
        else:
            st.warning("Please visit all the other sections before generating the timetable.")

if __name__ == "__main__":
    main()
