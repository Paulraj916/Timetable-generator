import streamlit as st
import pandas as pd

def display_faculty_allocation(sem_update_df):
    # Load the data from CSV files
    faculty_allocate_df = pd.read_csv('kadupu-2.csv')
    faculty_name_df = pd.read_csv('faculty_name.csv')

    # Function to get faculty name based on character
    def get_faculty_name(char):
        faculty = faculty_name_df[faculty_name_df['character'] == char]
        if not faculty.empty:
            return faculty.iloc[0]['faculty_name']
        return None

    # Filter subjects with lecture value greater than 0
    lecture_subjects = sem_update_df[sem_update_df['lecture'] > 0]

    # Create a table for subjects with lectures
    lecture_data = []
    for _, row in lecture_subjects.iterrows():
        course_code = row['course code']
        course_title = row['course title']
        allocation = faculty_allocate_df[faculty_allocate_df['course code'] == course_code]
        if not allocation.empty:
            A_char = allocation.iloc[0]['A']
            B_char = allocation.iloc[0]['B']
            A_name = get_faculty_name(A_char)
            B_name = get_faculty_name(B_char)
            lecture_data.append([course_title, A_name, B_name])

    lecture_table = pd.DataFrame(lecture_data, columns=['Course Title', 'A', 'B'])

    # Filter subjects with practical value greater than 0
    practical_subjects = sem_update_df[sem_update_df['practical'] > 0]

    # Create a table for subjects with practicals
    practical_data = []
    for _, row in practical_subjects.iterrows():
        course_code = row['course code']
        course_title = row['course title'] + ' (Lab)'
        allocation = faculty_allocate_df[faculty_allocate_df['course code'] == course_code]
        if not allocation.empty:
            lab_a_chars = allocation.iloc[0]['lab_a'][:2]
            lab_b_chars = allocation.iloc[0]['lab_b'][:2]
            lab_a_names = [get_faculty_name(char) for char in lab_a_chars]
            lab_b_names = [get_faculty_name(char) for char in lab_b_chars]
            practical_data.append([course_title, ', '.join(filter(None, lab_a_names)), ', '.join(filter(None, lab_b_names))])

    practical_table = pd.DataFrame(practical_data, columns=['Course Title (Lab)', 'Lab A', 'Lab B'])

    # Display the tables using Streamlit
    st.title('Faculty Allocation for Semester Subjects')

    # Create two columns for the tables
    col1, col2 = st.columns(2)

    with col1:
        st.header('Lecture Subjects')
        st.table(lecture_table)

    with col2:
        st.header('Practical Subjects')
        st.table(practical_table)

# Example usage
sem5update_df = pd.read_csv('sem3update.csv')
display_faculty_allocation(sem5update_df)
