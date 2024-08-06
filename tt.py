# tt.py
import pandas as pd
import streamlit as st
import numpy as np

def main():
    st.title("Timetable Generator")
    fix_hr = pd.read_csv("semester_data.csv")
    # Ask the user to select the semester type
    sem = st.radio("Select Semester Type", ('EVEN', 'ODD'))

    # Load the necessary CSV files based on the selected semester type
    if sem == "EVEN":
        year2 = pd.read_csv("sem4update.csv")
        year3 = pd.read_csv("sem6update.csv")
        year4 = pd.read_csv("sem8update.csv")
    else:
        year2 = pd.read_csv("sem3update.csv")
        year3 = pd.read_csv("sem5update.csv")
        year4 = pd.read_csv("sem7update.csv")

    # Retrieve the values based on the year and column names
    try:
        SST = fix_hr.loc[fix_hr["Year"] == 1, "SST"].values[0]
    except IndexError:
        SST = ""

    try:
        APT = fix_hr.loc[fix_hr['Year'] == 2, 'APT'].values[0]
    except IndexError:
        APT = ""

    try:
        LIB2 = fix_hr.loc[fix_hr['Year'] == 1, 'LIB2'].values[0]
    except IndexError:
        LIB2 = ""

    try:
        LIB3 = fix_hr.loc[fix_hr['Year'] == 2, 'LIB3'].values[0]
    except IndexError:
        LIB3 = ""

    try:
        LIB4 = fix_hr.loc[fix_hr['Year'] == 3, 'LIB4'].values[0]
    except IndexError:
        LIB4 = ""

    faculty_allocate_df = pd.read_csv("faculty_allocate.csv")

    # Read the necessary CSV files
    faculty_df = pd.read_csv("faculty_name.csv")

    # Extract the character column as a list
    characters = faculty_df['character'].tolist()

    # Create the DataFrame with "NM" only for Wednesday
    data = {
        "Day": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
        **{str(i): ["NM" if d == "Friday" else "".join(characters) for d in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]] for i in range(1, 9)}
    }

    # Create the DataFrame with "NM" only for Wednesday
    datanull = {
        "Day": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
        **{str(i): ["👍" if d == "Friday" else "NULL" for d in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]] for i in range(1, 9)}
    }
    data2 = {
        "Day": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
        **{str(i): ["NM" if d == "Thursday" else "".join(characters) for d in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]] for i in range(1, 9)}
    }

    # Create the DataFrame with "NM" only for Wednesday
    datanull2 = {
        "Day": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
        **{str(i): ["👍" if d == "Thursday" else "NULL" for d in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]] for i in range(1, 9)}
    }
    data3 = {
        "Day": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
        **{str(i): ["NM" if d == "Wednesday" else "".join(characters) for d in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]] for i in range(1, 9)}
    }

    # Create the DataFrame with "NM" only for Wednesday
    datanull3 = {
        "Day": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
        **{str(i): ["👍" if d == "Wednesday" else "NULL" for d in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]] for i in range(1, 9)}
    }

    IIA = pd.DataFrame(data).set_index("Day")
    IIB = pd.DataFrame(data).set_index("Day")
    IIIA = pd.DataFrame(data2).set_index("Day")
    IIIB = pd.DataFrame(data2).set_index("Day")
    IVA = pd.DataFrame(data3).set_index("Day")
    IVB = pd.DataFrame(data3).set_index("Day")

    IIAF = pd.DataFrame(datanull).set_index("Day")
    IIBF = pd.DataFrame(datanull).set_index("Day")
    IIIAF = pd.DataFrame(datanull2).set_index("Day")
    IIIBF = pd.DataFrame(datanull2).set_index("Day")
    IVAF = pd.DataFrame(datanull3).set_index("Day")
    IVBF = pd.DataFrame(datanull3).set_index("Day")

    # Function to parse input and update timetable
    def update_timetable(df, df1, input_str, value):
        if input_str:
            for entry in input_str.split(","):
                day, hour = map(int, entry.split("-"))
                if day in range(1, 7) and hour in range(1, 9):
                    df.loc[df.index[day - 1], str(hour)] = value
                    df1.loc[df1.index[day - 1], str(hour)] = "👍"

    # Update timetables with input variables
    update_timetable(IIA, IIAF, SST, "SST")
    update_timetable(IIB, IIBF, SST, "SST")
    update_timetable(IIIA, IIIAF, APT, "APT")
    update_timetable(IIIB, IIIBF, APT, "APT")
    update_timetable(IIA, IIAF, LIB2, "LIB2")
    update_timetable(IIB, IIBF, LIB2, "LIB2")
    update_timetable(IIIA, IIIAF, LIB3, "LIB3")
    update_timetable(IIIB, IIIBF, LIB3, "LIB3")
    update_timetable(IVA, IVAF, LIB4, "LIB4")
    update_timetable(IVB, IVBF, LIB4, "LIB4")

    # Define the valid period ranges for practicals
    valid_periods = {
        2: [(1, 2), (3, 4), (5, 6), (7, 8)],
        3: [(1, 2, 3), (2, 3, 4), (5, 6, 7), (6, 7, 8)],
        4: [(1, 2, 3, 4), (5, 6, 7, 8)]
    }

    # Function to check if a period is available for allocation
    def is_available(day, periods, df_alloc):
        return all(df_alloc.loc[day, str(period)] != '👍' for period in periods)

    # Function to update df_alloc after allocation
    def update_df_alloc(day, periods, df_alloc):
        for period in periods:
            df_alloc.at[day, str(period)] = '👍'

    # Function to block out allocated periods in other sections
    def block_faculty(faculties, day, periods, all_class, *timetables):
        for faculty in faculties:
            for i in range(len(timetables)):
                for period in periods:
                    if timetables[i].loc[day, str(period)] == "NULL":
                        all_class[i].loc[day, str(period)] = ''.join(char for char in all_class[i].loc[day, str(period)] if char not in faculty)

    def vacancy(faculties, day, periods, all_class, *timetables):
        for faculty in faculties:
            for i in range(len(timetables)):
                for period in periods:
                    if timetables[i].loc[day, str(period)] == "NULL":
                        if not all(char in all_class[i].loc[day, str(period)] for char in faculty):
                            return 1
        return 0
    
    # Create a DataFrame to track lab availability
    lab_availability = pd.DataFrame(index=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], 
                                    columns=range(1, 9), 
                                    data=2)  # Initialize with 2 available labs for each period

    def update_lab_availability(day, periods):
        for period in periods:
            if lab_availability.loc[day, period] > 0:
                lab_availability.loc[day, period] -= 1
                return True
        return False

    def check_lab_availability(day, periods):
        return all(lab_availability.loc[day, period] > 0 for period in periods)

    def allocate_practicals(year, df, df_alloc, lab_key, all_allocations):
        all_class = [IIA, IIB, IIIA, IIIB, IVA, IVB]
        pending_courses = year.to_dict('records')
        max_attempts = 10
        attempts = {course['course code']: 0 for course in pending_courses}

        while pending_courses:
            course = pending_courses.pop(0)
            allocated = False

            print(f"Trying to allocate: {course['course title']} with practical periods: {course['practical']}")
            
            if course['practical'] not in valid_periods:
                print(f"Error: No valid periods found for practical length {course['practical']}")
                continue

            for index_IIA, row in df.iterrows():
                for periods in valid_periods[course['practical']]:
                    if is_available(row.name, periods, df_alloc) and check_lab_availability(row.name, periods):
                        faculties = faculty_allocate_df[faculty_allocate_df['course code'] == course['course code']][lab_key].values[0]
                        faculties = faculties.split(',')
                        if vacancy(faculties, row.name, periods, all_class, *all_allocations) == 1:
                            continue

                        update_df_alloc(row.name, periods, df_alloc)
                        block_faculty(faculties, row.name, periods, all_class, *all_allocations)
                        update_lab_availability(row.name, periods)

                        for period in periods:
                            df.at[row.name, str(period)] = course['course title']+"❤️"

                        allocated = True
                        break
                if allocated:
                    break

            if not allocated:
                attempts[course['course code']] += 1
                if attempts[course['course code']] >= max_attempts:
                    print(f"Failed to allocate: {course['course title']} after {max_attempts} attempts")
                    continue
                pending_courses.append(course)

            for other_course in list(pending_courses):
                other_allocated = False

                if other_course['practical'] not in valid_periods:
                    print(f"Error: No valid periods found for practical length {other_course['practical']}")
                    continue

                for index_IIA, row in df.iterrows():
                    for periods in valid_periods[other_course['practical']]:
                        if is_available(row.name, periods, df_alloc) and check_lab_availability(row.name, periods):
                            faculties = faculty_allocate_df[faculty_allocate_df['course code'] == other_course['course code']][lab_key].values[0]
                            faculties = faculties.split(',')
                            if vacancy(faculties, row.name, periods, all_class, *all_allocations) == 1:
                                continue

                            update_df_alloc(row.name, periods, df_alloc)
                            block_faculty(faculties, row.name, periods, all_class, *all_allocations)
                            update_lab_availability(row.name, periods)

                            for period in periods:
                                df.at[row.name, str(period)] = other_course['course title']+"❤️"

                            other_allocated = True
                            break
                    if other_allocated:
                        break

                if other_allocated:
                    pending_courses.remove(other_course)

    def allocate_lectures(year, df, df_alloc, class_key, all_allocations):
        all_class = [IIA, IIB, IIIA, IIIB, IVA, IVB]
        pending_courses = year.to_dict('records')
        print("\n\n-------------",pending_courses,"--------------\n\n")
        max_attempts = 10
        attempts = {course['course code']: 0 for course in pending_courses}
        total_lectures = sum(course['lecture'] for course in pending_courses)

        while total_lectures > 0:
            for course in pending_courses:
                if course['lecture'] == 0:
                    continue
                
                print("$$$$$$$$$$$$$$$$$$$$",course,"&&&&&&&&&&&&&&&&&&&&")
                allocated_periods = 0
                print(f"Trying to allocate 1 lecture for: {course['course title']}")

                faculties = faculty_allocate_df[faculty_allocate_df['course code'] == course['course code']][class_key].values[0]
                faculties = faculties.split(',')

                for index_IIA, row in df.iterrows():
                    if course['lecture'] == 0:
                        break
                    for period in range(1, 9):
                        if df_alloc.loc[row.name, str(period)] != '👍' and vacancy(faculties, row.name, [period], all_class, *all_allocations) == 0:
                            df.at[row.name, str(period)] = course['course title']
                            df_alloc.at[row.name, str(period)] = '👍'
                            block_faculty(faculties, row.name, [period], all_class, *all_allocations)
                            allocated_periods += 1
                            course['lecture'] -= 1
                            total_lectures -= 1
                            if allocated_periods >= 1 or course['lecture'] == 0:
                                break
                    if allocated_periods >= 1 or course['lecture'] == 0:
                        break
                attempts[course['course code']] += 1

                if course['lecture'] > 0:
                    print(f"Failed to allocate 1 lecture for: {course['course title']} after {max_attempts} attempts")

    def display_faculty_allocation(sem_update_df):
        # Load the data from CSV files
        faculty_allocate_df = pd.read_csv('faculty_allocate.csv')
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

        practical_table = pd.DataFrame(practical_data, columns=['Course Title', 'A', 'B'])

        # Display the tables using Streamlit
        st.title('Faculty Allocation for Semester Subjects')
        combined_table = pd.concat([lecture_table, practical_table], ignore_index=True)
        # st.table(combined_table)
        st.write(combined_table)

        # st.header('Lecture Subjects')
        # st.table(lecture_table)

        # st.header('Practical Subjects')
        # st.table(practical_table)
    
    # Allocate practicals for all years and sections

    def display_lab_hours(dataframes):
        # Create a dictionary mapping names to DataFrames
        df_dict = {
            "II A": IIA,
            "II B": IIB,
            "III A": IIIA,
            "III B": IIIB,
            "IV A": IVA,
            "IV B": IVB
        }
        
        # Create a dropdown to select the DataFrame
        selected_df_name = st.selectbox("Select a class:", list(df_dict.keys()))
        
        # Get the selected DataFrame
        selected_df = df_dict[selected_df_name]
        
        # Function to filter and format the DataFrame
        def filter_lab_hours(df):
            # Create a copy of the DataFrame to avoid modifying the original
            filtered_df = df.copy()
            
            # Function to process each cell
            def process_cell(x):
                if isinstance(x, str) and '❤️' in x:
                    return x.replace('❤️', '')
                return ''
            
            # Apply the processing function to each cell
            filtered_df = filtered_df.map(process_cell)
            
            return filtered_df
        
        # Filter and display the selected DataFrame
        filtered_df = filter_lab_hours(selected_df)
        st.write(f"Lab Hours for {selected_df_name}:")
        st.table(filtered_df)
        st.write(filtered_df)

    def display_faculty_timetable(timetables):
        # Load faculty data
        faculty_df = pd.read_csv("faculty_name.csv")
        faculty_allocate_df = pd.read_csv("faculty_allocate.csv")
        
        # Create a dropdown to select the faculty
        selected_faculty = st.selectbox("Select a faculty:", faculty_df['faculty_name'].tolist())
        
        # Get the character for the selected faculty
        faculty_char = faculty_df[faculty_df['faculty_name'] == selected_faculty]['character'].values[0]
        
        # Function to get course details for a faculty
        def get_course_details(faculty_char):
            courses = []
            for _, row in faculty_allocate_df.iterrows():
                if (faculty_char in str(row['A']) or 
                    faculty_char in str(row['B']) or 
                    (isinstance(row['lab_a'], str) and faculty_char in row['lab_a']) or 
                    (isinstance(row['lab_b'], str) and faculty_char in row['lab_b'])):
                    courses.append({
                        'code': row['course code'],
                        'title': row['course title'],
                        'is_lab': row['practical'] > 0
                    })
            return courses
        
        faculty_courses = get_course_details(faculty_char)
        
        # Function to create faculty timetable
        def create_faculty_timetable(timetables, faculty_courses):
            days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
            periods = range(1, 9)
            
            faculty_timetable = pd.DataFrame(index=days, columns=periods)
            
            for day in days:
                for period in periods:
                    for i, timetable in enumerate(timetables):
                        cell_value = timetable.loc[day, str(period)]
                        if isinstance(cell_value, str):
                            for course in faculty_courses:
                                if course['title'] in cell_value:
                                    class_name = ["II A", "II B", "III A", "III B", "IV A", "IV B"][i]
                                    faculty_timetable.loc[day, period] = f"{course['title']}{'❤️' if course['is_lab'] else ''} ({class_name})"
            
            # Replace NaN values with empty strings
            faculty_timetable = faculty_timetable.fillna('')
            
            return faculty_timetable
        
        # Create and display the faculty timetable
        faculty_timetable = create_faculty_timetable(timetables, faculty_courses)
        st.write(f"Timetable for {selected_faculty}:")
        st.table(faculty_timetable)
        st.write(faculty_timetable)


    all_allocations = [IIAF, IIBF, IIIAF, IIIBF, IVAF, IVBF]
    allocate_practicals(year2, IIA, IIAF, 'lab_a', all_allocations)
    allocate_practicals(year2, IIB, IIBF, 'lab_b', all_allocations)
    allocate_practicals(year3, IIIA, IIIAF, 'lab_a', all_allocations)
    allocate_practicals(year3, IIIB, IIIBF, 'lab_b', all_allocations)
    allocate_practicals(year4, IVA, IVAF, 'lab_a', all_allocations)
    allocate_practicals(year4, IVB, IVBF, 'lab_b', all_allocations)

    # Allocate lectures for all years and sections
    allocate_lectures(year2, IIA, IIAF, 'A', all_allocations)
    allocate_lectures(year2, IIB, IIBF, 'B', all_allocations)
    allocate_lectures(year3, IIIA, IIIAF, 'A', all_allocations)
    allocate_lectures(year3, IIIB, IIIBF, 'B', all_allocations)
    allocate_lectures(year4, IVA, IVAF, 'A', all_allocations)
    allocate_lectures(year4, IVB, IVBF, 'B', all_allocations)

    # Convert DataFrame to HTML without index
    IIA_html = IIA.to_html(index=False)
    IIB_html = IIB.to_html(index=False)
    IIIA_html = IIIA.to_html(index=False)
    IIIB_html = IIIB.to_html(index=False)
    IVA_html = IVA.to_html(index=False)
    IVB_html = IVB.to_html(index=False)

    # Display the DataFrames using st.markdown
    st.title("2ND-A")
    st.markdown(IIA_html, unsafe_allow_html=True)

 
    st.title("2ND-B")
    st.markdown(IIB_html, unsafe_allow_html=True)

    display_faculty_allocation(year2)

    st.title("3RD-A")
    st.markdown(IIIA_html, unsafe_allow_html=True)

    st.title("3RD-B")
    st.markdown(IIIB_html, unsafe_allow_html=True)

    display_faculty_allocation(year3)

    st.title("4TH-A")
    st.markdown(IVA_html, unsafe_allow_html=True)

    st.title("4TH-B")
    st.markdown(IVB_html, unsafe_allow_html=True)

    display_faculty_allocation(year4)
    

    def display_info(title, content, content_f):
        st.markdown(f"### {title}")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"{title}:")
            st.write(content)
        with col2:
            st.write(f"{title}F:")
            st.write(content_f)

    display_info("IIA", IIA, IIAF)
    display_info("IIB", IIB, IIBF)
    display_info("IIIA", IIIA, IIIAF)
    display_info("IIIB", IIIB, IIIBF)
    display_info("IVA", IVA, IVAF)
    display_info("IVB", IVB, IVBF)

    display_lab_hours([IIA, IIB, IIIA, IIIB, IVA, IVB])

    display_faculty_timetable([IIA, IIB, IIIA, IIIB, IVA, IVB])

    # Adding some additional styling for better visualization
    st.markdown(
        """
        <style>
        .reportview-container {
            background: #f0f2f6;
            padding: 20px;
        }
        .markdown-text-container {
            font-family: 'Arial';
            background: white;
            padding: 15px;
            border-radius: 5px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        }
        </style>
        """, unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
