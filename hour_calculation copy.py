import streamlit as st
import pandas as pd

# Dummy Data
SST = ""
APT = ""
LIB2 = ''
LIB3 = ''
LIB4 = ''

def sem(sem_data,sem_data1,semfixedhr,count,check):
        print(semfixedhr)
        print("----------------")
        print(sem_data)
        
        if(check == 0):
            # Perform calculation part 1
            sem_data,dummy= update_min_lecture(sem_data)

        # Perform calculation part 2
        print(sem_data)
        total_lecture, total_practical = calculate_total_hours(sem_data)
        semfixedhr += total_lecture + total_practical
    
        # Perform calculation part 3
        semdif = 40 - semfixedhr
        print(total_lecture + total_practical)
        print(semfixedhr)

        semdifdiv = semdif // (sem_data.shape[0] - count)

        semdifmod = semdif % (sem_data.shape[0] - count)
        print(semdif,"\t semdif")
        print(semdifdiv,"\t semdifdiv")
        print(semdifmod,"\t semdifmod")
        print((sem_data.shape[0] - count),"\t (sem_data.shape[0] - 1)")
        j=0
        while(j<semdifdiv):
            for i in range((sem_data.shape[0] - count)):
                if sem_data.loc[i, 'lecture'] == 0 :
                    # sem_data.loc[i, 'lecture'] += 0 or just do pass
                    pass
                    # min_credit_subject = sem_data[sem_data['credit'] == sem_data['credit'].min()] 
                    # if min_credit_subject['lecture'].values[0] > 2 and min_credit_subject['credit'].values[0] < 3:
                    #     semdifdiv+=1
                    # else:
                    #     sem_data.loc[i, 'lecture'] += 1
                else:
                    sem_data.loc[i, 'lecture'] += 1
            j+=1
        sem_data,semdifmod= perform_remaining_hours(sem_data, semdifmod)

        for i in range(int(semdifmod)):
            remaining_subjects = sem_data.loc[sem_data['credit'] != sem_data['credit'].min()]
            selected_subject = st.selectbox(f"Select Subject {i+1} for Remaining Hours:", remaining_subjects['course code'], key=f"selectbox_{i}")
            sem_data.loc[sem_data['course code'] == selected_subject, 'lecture'] += 1

        return sem_data

# Function to calculate total lecture and practical hours for a given dataframe
def calculate_total_hours(df):
    total_lecture = df['lecture'].sum()
    total_practical = df['practical'].sum()
    return total_lecture, total_practical

# Function to update the dataframe with the minimum lecture requirement
def update_min_lecture(df):
    min_credit_subject = df[df['credit'] == df['credit'].min()]
    count_condition = len(min_credit_subject[(min_credit_subject['lecture'] > 2) & (min_credit_subject['credit'] < 3)])
    
    if min_credit_subject['lecture'].values[0] > 2 and min_credit_subject['credit'].values[0] < 3:
        df.loc[df['credit'] == df['credit'].min(), 'lecture'] = 2
        
    return df, count_condition

# Function to perform calculations based on remaining hours
def perform_remaining_hours(df, remaining_hours):
    max_credit_subject = df[df['credit'] == df['credit'].max()]
    for index, row in max_credit_subject.iterrows():
        if(remaining_hours==0):
            df.loc[index, 'lecture'] += 1
            remaining_hours-=1
    return df,remaining_hours

def crt_cal(sem_data):
    num_courses = st.number_input("Enter the number of courses:", min_value=1, max_value=10, step=1)
    # Assuming sem_data is your DataFrame containing the course data
    # Define sem_data_copy to make changes on a copy
    sem_data_copy = sem_data.copy()

    # Create a DataFrame to store selected courses with default hours
    selected_courses_df = pd.DataFrame(columns=sem_data.columns)

    # Iterate through the selected courses
    for i in range(num_courses):
        course_title = st.selectbox(f"Select Course Title {i+1}:", options=sem_data_copy['course title'].unique())
        default_hours = st.number_input(f"Enter Default Hours for {course_title}:", min_value=0, step=1)
        
        # Update lecture hours in the original DataFrame
        sem_data_copy.loc[sem_data_copy['course title'] == course_title, 'lecture'] = default_hours
        
        # Add the selected course to the DataFrame for selected courses with default hours
        selected_courses_df = pd.concat([selected_courses_df, sem_data_copy[sem_data_copy['course title'] == course_title]])
        
        # Drop the selected course from the copy to avoid repetition
        sem_data_copy = sem_data_copy.drop(sem_data_copy[sem_data_copy['course title'] == course_title].index)

    # Concatenate the original DataFrame without selected courses and the DataFrame for selected courses
    sem_data_updated = pd.concat([sem_data_copy, selected_courses_df])

    # Reset index to ensure the DataFrame has a consistent index
    sem_data_updated.reset_index(drop=True, inplace=True)

    # Display the updated DataFrame
    print(sem_data_updated)
    sem_data
    sem_data_updated
    return sem_data_updated,num_courses

def main():
    global sem3, sem4, sem5, sem6, sem7, sem8  # Declare global dictionaries

    # Streamlit code starts here
    st.title('Semester Timetable Generator')

    sem_type = st.radio("Select Semester Type", ('Even Semester', 'Odd Semester'))

    if sem_type == 'Even Semester':
        sem_num = st.radio("Select Semester", ('sem4', 'sem6' , 'sem8'))
        if sem_num == 'sem4':
            sem_data = pd.read_csv('sem4.csv')

            st.header('Semester 4 Data')
            st.write(sem_data)

            sem4fixedhr = 0

            # Ask if any course title needs default hours
            default_hours_option = st.radio("Do any course titles need default hours?", ('Yes', 'No'))

            if default_hours_option == 'Yes':
                sem_data_updated,num_courses = crt_cal(sem_data)
            print(sem_data)

            SST = st.text_input('Enter SST Allocated Hour (e.g.1-1,1-2,4-5,4-6):')

            sem4fixedhr += 0 if not SST else len(SST.split(','))

            LIB2 = st.text_input('Enter LIB2 Allocated Hour (e.g.1-1,1-2,4-5,4-6):')
            sem4fixedhr += 0 if not LIB2 else len(LIB2.split(',')) 

            # sem_data_updated.to_csv('sem4update.csv', index=False)

            if default_hours_option == 'Yes':
                #calculation part
                sem_data = sem(sem_data_updated,sem_data,sem4fixedhr,num_courses,1)
            if default_hours_option == 'No':
                sem_data = sem(sem_data,sem_data,sem4fixedhr,0,0)

            st.header('Updated Semester 4 Data')
            st.write(sem_data)
            if st.button('Save sem_data to CSV'):
                sem_data.to_csv('sem4update.csv', index=False)
                st.success('sem_data saved to sem4update.csv')
                sem4['SST']=SST
                sem4['LIB2']=LIB2
        if sem_num == 'sem6':
            sem_data = pd.read_csv('sem6.csv')

            st.header('Semester 6 Data')
            st.write(sem_data)

            sem6fixedhr = 0

            APT = st.text_input('Enter APT Allocated Hour (e.g.1-1,1-2,4-5,4-6):')


            LIB3 = st.text_input('Enter LIB3 Allocated Hour (e.g.1-1,1-2,4-5,4-6):')
            sem6fixedhr += 0 if not APT else len(APT.split(','))
            sem6fixedhr += 0 if not APT else len(LIB3.split(','))
            print("-----------",sem6fixedhr,'-----------')
            # Ask for open elective course code or title
            open_elective_options = pd.read_csv('open_elect.csv')
            open_elective_courses = list(open_elective_options.apply(lambda x: f"{x['course code']} - {x['course title']}", axis=1))
            open_elective_course = st.selectbox("Select Open Elective Course:", options=[''] + open_elective_courses)

            if open_elective_course:
                selected_open_elective = open_elective_options[(open_elective_options['course code'] == open_elective_course.split(" - ")[0]) | (open_elective_options['course title'] == open_elective_course.split(" - ")[1])]
                sem_data = pd.concat([sem_data, selected_open_elective], ignore_index=True)

            # Ask for professional electives
            prof_elective_options = pd.read_csv('prof_elect_unique.csv')
            prof_elective_courses = list(prof_elective_options.apply(lambda x: f"{x['course code']} - {x['course title']}", axis=1))
            prof_electives = []
            for i in range(3):
                prof_elective_course = st.selectbox(f"Select Professional Elective Course {i+1}:", options=[''] + prof_elective_courses)
                if prof_elective_course:
                    selected_prof_elective = prof_elective_options[prof_elective_options['course code'] == prof_elective_course.split(" - ")[0]]
                    prof_electives.append(selected_prof_elective)
            sem_data = pd.concat([sem_data] + prof_electives, ignore_index=True)

            # Ask for mandatory course
            mandatory_options = pd.read_csv('mandatory_course.csv')
            mandatory_courses = list(mandatory_options.apply(lambda x: f"{x['course code']} - {x['course title']}", axis=1))
            mandatory_course = st.selectbox("Select Mandatory Course:", options=[''] + mandatory_courses)
            if mandatory_course:
                selected_mandatory_course = mandatory_options[mandatory_options['course code'] == mandatory_course.split(" - ")[0]]
                sem_data = pd.concat([sem_data, selected_mandatory_course], ignore_index=True)
            sem_data
            sem_data.to_csv('sem6update.csv', index=False)

            # Ask if any course title needs default hours
            default_hours_option = st.radio("Do any course titles need default hours?", ('Yes', 'No'))

            if default_hours_option == 'Yes':
                sem_data_updated,num_courses = crt_cal(sem_data)
            print(sem_data)

            if default_hours_option == 'Yes':
                #calculation part
                sem_data = sem(sem_data_updated,sem_data,sem6fixedhr,num_courses,1)
            else:
                sem_data = sem(sem_data,sem_data,sem6fixedhr,0,1)

            st.header('Updated Semester 6 Data')
            st.write(sem_data)
            if st.button('Save sem_data to CSV'):
                sem_data.to_csv('sem6update.csv', index=False)
                st.success('sem_data saved to sem6update.csv')
                sem6['APT']=APT
                sem6['LIB3']=LIB3
        if sem_num == 'sem8':
            sem_data = pd.read_csv('sem8.csv')

            st.header('Semester 8 Data')
            st.write(sem_data)

            semfixedhr = 0
            
            LIB4 = st.text_input('Enter LIB4 Allocated Hour (e.g.1-1,1-2,4-5,4-6):')
            print(LIB4)
            if(LIB4!=""):
                semfixedhr += 0 if not LIB4 else len(LIB4.split(','))

            sem_data.to_csv('sem8update.csv', index=False)

            # Perform calculation part 2
            total_lecture, total_practical = calculate_total_hours(sem_data)

            semfixedhr += total_lecture + total_practical

            # Perform calculation part 3
            semdif = 40 - semfixedhr

            for i in range(semdif-1):
                sem_data.loc[0, 'lecture'] += 1
            sem_data,semdifmod= perform_remaining_hours(sem_data, 0)

            for i in range(int(semdifmod)):
                remaining_subjects = sem_data.loc[sem_data['credit'] != sem_data['credit'].min()]
                selected_subject = st.selectbox(f"Select Subject {i+1} for Remaining Hours:", remaining_subjects['course code'], key=f"selectbox_{i}")
                sem_data.loc[sem_data['course code'] == selected_subject, 'lecture'] += 1

            st.header('Updated Semester 8 Data')
            
            st.write(sem_data)
            if st.button('Save sem_data to CSV'):
                sem_data.to_csv('sem8update.csv', index=False)
                st.success('sem_data saved to sem8update.csv')
                
                sem8['LIB4'] = LIB4



    if sem_type == 'Odd Semester':
        sem_num = st.radio("Select Semester", ('sem3', 'sem5' , 'sem7'))
        if sem_num == 'sem3':
            sem_data = pd.read_csv('sem3.csv')

            st.header('Semester 3 Data')
            st.write(sem_data)

            sem4fixedhr = 0

            SST = st.text_input('Enter SST Allocated Hour (e.g.1-1,1-2,4-5,4-6):')

            sem4fixedhr += 0 if not SST else len(SST.split(','))

            LIB2 = st.text_input('Enter LIB2 Allocated Hour (e.g.1-1,1-2,4-5,4-6):')
            sem4fixedhr += 0 if not LIB2 else len(LIB2.split(','))

            sem_data.to_csv('sem3update.csv', index=False)
            
            # Ask if any course title needs default hours
            default_hours_option = st.radio("Do any course titles need default hours?", ('Yes', 'No'))

            if default_hours_option == 'Yes':
                sem_data_updated,num_courses = crt_cal(sem_data)
            print(sem_data)

            if default_hours_option == 'Yes':
                #calculation part
                sem_data = sem(sem_data_updated,sem_data,sem4fixedhr,num_courses,1)
            else:
                sem_data = sem(sem_data,sem_data,sem4fixedhr,0,1)

            st.header('Updated Semester 3 Data')
            st.write(sem_data)
            if st.button('Save sem_data to CSV'):
                sem_data.to_csv('sem3update.csv', index=False)
                st.success('sem_data saved to sem3update.csv')
                sem3['SST']=SST
                sem3['LIB2']=LIB2
        if sem_num == 'sem5':
            sem_data = pd.read_csv('sem5.csv')

            st.header('Semester 5 Data')
            st.write(sem_data)

            sem6fixedhr = 0

            APT = st.text_input('Enter APT Allocated Hour (e.g.1-1,1-2,4-5,4-6):')
            sem6fixedhr += 0 if not APT else len(APT.split(','))


            LIB3 = st.text_input('Enter LIB3 Allocated Hour (e.g.1-1,1-2,4-5,4-6):')
            sem6fixedhr += 0 if not LIB3 else len(LIB3.split(','))

            # Ask for professional electives
            prof_elective_options = pd.read_csv('prof_elect_unique.csv')
            prof_elective_courses = list(prof_elective_options.apply(lambda x: f"{x['course code']} - {x['course title']}", axis=1))
            prof_electives = []
            for i in range(2):
                prof_elective_course = st.selectbox(f"Select Professional Elective Course {i+1}:", options=[''] + prof_elective_courses)
                if prof_elective_course:
                    selected_prof_elective = prof_elective_options[prof_elective_options['course code'] == prof_elective_course.split(" - ")[0]]
                    prof_electives.append(selected_prof_elective)
            sem_data = pd.concat([sem_data] + prof_electives, ignore_index=True)

            # Ask for mandatory course
            mandatory_options = pd.read_csv('mandatory_course.csv')
            mandatory_courses = list(mandatory_options.apply(lambda x: f"{x['course code']} - {x['course title']}", axis=1))
            mandatory_course = st.selectbox("Select Mandatory Course:", options=[''] + mandatory_courses)
            if mandatory_course:
                selected_mandatory_course = mandatory_options[mandatory_options['course code'] == mandatory_course.split(" - ")[0]]
                sem_data = pd.concat([sem_data, selected_mandatory_course], ignore_index=True)
            sem_data
            sem_data.to_csv('sem5update.csv', index=False)

            # Ask if any course title needs default hours
            default_hours_option = st.radio("Do any course titles need default hours?", ('Yes', 'No'))

            if default_hours_option == 'Yes':
                sem_data_updated,num_courses = crt_cal(sem_data)
            print(sem_data)

            if default_hours_option == 'Yes':
                #calculation part
                sem_data = sem(sem_data_updated,sem_data,sem6fixedhr,num_courses,1)
            else:
                sem_data = sem(sem_data,sem_data,sem6fixedhr,0,0)

            st.header('Updated Semester 5 Data')
            st.write(sem_data)
            if st.button('Save sem_data to CSV'):
                sem_data.to_csv('sem5update.csv', index=False)
                st.success('sem_data saved to sem5update.csv')
                sem5['APT']=APT
                sem5['LIB3']=LIB3
        if sem_num == 'sem7':
            sem_data = pd.read_csv('sem7.csv')

            st.header('Semester 7 Data')
            st.write(sem_data)

            sem6fixedhr = 0

            LIB4 = st.text_input('Enter LIB4 Allocated Hour (e.g.1-1,1-2,4-5,4-6):')
            sem6fixedhr += 0 if not LIB4 else len(LIB4.split(','))

            # Ask for management elective course code or title
            management_elect_options = pd.read_csv('management_elect.csv')
            management_elect_courses = list(management_elect_options.apply(lambda x: f"{x['course code']} - {x['course title']}", axis=1))
            management_elect_course = st.selectbox("Select Management Elective Course:", options=[''] + management_elect_courses)

            if management_elect_course:
                selected_management_elective = management_elect_options[(management_elect_options['course code'] == management_elect_course.split(" - ")[0]) | (management_elect_options['course title'] == management_elect_course.split(" - ")[1])]
                sem_data = pd.concat([sem_data, selected_management_elective], ignore_index=True)

            # Ask for open elective courses
            open_elect_options = pd.read_csv('open_elect.csv')
            open_elect_courses = list(open_elect_options.apply(lambda x: f"{x['course code']} - {x['course title']}", axis=1))
            open_elects = []
            for i in range(3):
                open_elect_course = st.selectbox(f"Select Open Elective Course {i+1}:", options=[''] + open_elect_courses)
                if open_elect_course:
                    selected_open_elective = open_elect_options[open_elect_options['course code'] == open_elect_course.split(" - ")[0]]
                    open_elects.append(selected_open_elective)
            sem_data = pd.concat([sem_data] + open_elects, ignore_index=True)

            # Ask if any course title needs default hours
            default_hours_option = st.radio("Do any course titles need default hours?", ('Yes', 'No'))

            #calculation part
            if default_hours_option == 'Yes':
                sem_data_updated,num_courses = crt_cal(sem_data)
            print(sem_data)

            if default_hours_option == 'Yes':
                #calculation part
                sem_data = sem(sem_data_updated,sem_data,sem6fixedhr,num_courses,1)
            else:
                sem_data = sem(sem_data,sem_data,sem6fixedhr,0,1)

            st.header('Updated Semester 7 Data')
            st.write(sem_data)
            if st.button('Save sem_data to CSV'):
                sem_data.to_csv('sem7update.csv', index=False)
                st.success('sem_data saved to sem7update.csv')
                sem7['LIB4']=LIB4


if __name__ == "__main__":
    main()