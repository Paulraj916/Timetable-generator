import streamlit as st
import pandas as pd

# Load faculty data
faculty_data = pd.read_csv("faculty_name.csv")

def main():
    st.title("Combined DataFrame Viewer and Faculty Allocation")

    # Checkbox to select odd or even semesters
    semester_type = st.checkbox("Select odd semester")
    if semester_type:
        file_paths = ['sem3update.csv', 'sem5update.csv', 'sem7update.csv']
    else:
        file_paths = ['sem4update.csv', 'sem6update.csv', 'sem8update.csv']

    # Load combined DataFrame
    dfs = [pd.read_csv(file_path) for file_path in file_paths]
    combined_df = pd.concat(dfs, ignore_index=True)

    # Display the combined DataFrame
    st.write(combined_df)

    # Prompt user to input the number of subjects requiring 4 lab faculty members
    num_subjects = st.number_input("Enter the number of subjects requiring 4 lab faculty members:", min_value=0, max_value=len(combined_df), step=1)

    selected_subjects = []
    for i in range(num_subjects):
        selected_subject = st.selectbox(f"Select Subject {i + 1}:", options=combined_df['course title'].tolist())
        selected_subjects.append(selected_subject)

    # Function to handle adding new faculty
    def add_new_faculty(name):
        last_character = faculty_data['character'].iloc[-1]
        new_character = chr(ord(last_character) + 1)
        faculty_data.loc[len(faculty_data)] = [name, new_character]
        faculty_data.to_csv("faculty_name.csv", index=False)
        return new_character

    # List to store allocation data
    allocation_list = []

    # Iterate over each row in the DataFrame
    for index, row in combined_df.iterrows():
        st.subheader(f"Faculty Allocation for {row['course code']} - {row['course title']}")

        # Unique keys for selectboxes
        key_a = f"faculty_a_{index}"
        key_b = f"faculty_b_{index}"
        key_lab_a = f"lab_a_{index}"
        key_lab_b = f"lab_b_{index}"

        # Dropdown menu for selecting faculty A
        faculty_a_options = faculty_data['faculty_name'].tolist() + ["Other"]
        faculty_a = st.selectbox(f"Select Faculty A:", options=faculty_a_options, key=key_a)
        if faculty_a == "Other":
            new_faculty_name = st.text_input("Enter new faculty name:")
            if new_faculty_name:
                new_character = add_new_faculty(new_faculty_name)
                st.write(f"New faculty '{new_faculty_name}' added with character '{new_character}'")
                faculty_a_options.append(new_faculty_name)
                faculty_a = new_faculty_name
        # Retrieve the corresponding character from faculty_name.csv
        faculty_a = faculty_data.loc[faculty_data['faculty_name'] == faculty_a, 'character'].iloc[0]

        # Dropdown menu for selecting faculty B
        faculty_b_options = faculty_data['faculty_name'].tolist() + ["Other"]
        faculty_b = st.selectbox(f"Select Faculty B:", options=faculty_b_options, key=key_b)
        if faculty_b == "Other":
            new_faculty_name = st.text_input("Enter new faculty name:")
            if new_faculty_name:
                new_character = add_new_faculty(new_faculty_name)
                st.write(f"New faculty '{new_faculty_name}' added with character '{new_character}'")
                faculty_b_options.append(new_faculty_name)
                faculty_b = new_faculty_name
        # Retrieve the corresponding character from faculty_name.csv
        faculty_b = faculty_data.loc[faculty_data['faculty_name'] == faculty_b, 'character'].iloc[0]

        # Check if the subject requires extra lab faculty
        extra_lab = row['course title'] in selected_subjects

        # If practical credit is greater than 0 or the subject requires extra lab faculty, ask for lab allocations
        if row['practical'] > 0 or extra_lab:
            if extra_lab:
                lab_faculty_count = 4
            else:
                lab_faculty_count = 2

            lab_a_faculty = [faculty_data.loc[faculty_data['faculty_name'] == st.selectbox(f"Select Lab A:", options=faculty_data['faculty_name'].tolist(), key=f"{key_lab_a}_{i}"), 'character'].iloc[0] for i in range(lab_faculty_count)]
            lab_b_faculty = [faculty_data.loc[faculty_data['faculty_name'] == st.selectbox(f"Select Lab B:", options=faculty_data['faculty_name'].tolist(), key=f"{key_lab_b}_{i}"), 'character'].iloc[0] for i in range(lab_faculty_count)]

            lab_a = ''.join(lab_a_faculty)
            lab_b = ''.join(lab_b_faculty)
        else:
            lab_a, lab_b = "None", "None"

        # Append allocation data to the list
        allocation_data = {
            'course code': row['course code'],
            'course title': row['course title'],
            'credit': row['credit'],
            'practical': row['practical'],
            'lecture': row['lecture'],
            'A': faculty_a,
            'B': faculty_b,
            'lab_a': lab_a,
            'lab_b': lab_b
        }
        allocation_list.append(allocation_data)

    # Button to store data in faculty_allocate.csv
    if st.button("Save Data to faculty_allocate.csv"):
        with open('faculty_allocate.csv', 'w') as f:
            pd.DataFrame(allocation_list).to_csv(f, header=f.tell()==0, index=False)
        st.write("Data saved successfully.")

if __name__ == "__main__":
    main()
