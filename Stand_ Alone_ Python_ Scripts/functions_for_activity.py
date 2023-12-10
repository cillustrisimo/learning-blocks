import openpyxl
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import requests
import csv
import re
from matplotlib.backends.backend_pdf import PdfPages

# Works specifically with the "PrintQueryReport_20231203_190..." excel file 
def excelToIDList(excel_df):
    pd.set_option('display.max_columns', None)
    temp_list = excel_df['Student ID'].tolist() 
    
    # removing nan from list
    temp_list = [x for x in temp_list if str(x) != 'nan']

    # removing 'student demographic...' and 'student id'... from list
    temp_list = [x for x in temp_list 
    if x != 'Student Demographic Information Report' and x !='Student ID']

    return temp_list

def listToIDList(workingList):
    #  This RegEx pattern variable will capture any non digit character 
    # in a given string. Thus used in split, we get only ID numbers
    pattern = re.compile("^\s+|\s*\D\s*|\s+$")

    # This list comprehension is to extract the integers
    temp_list = [int(i) for i in pattern.split(workingList) if i.isdigit()]

    return temp_list

def outputFiles(dataframe, by_grade=True):
    if by_grade == True:
        key = "Grade"
    else:
        key = "Program"

    # Outputting CSV and JSON
    dataframe.to_json(f'{key}_JSON.json')
    dataframe.to_csv(f'{key}_CSV.csv', index=True)
    
    # creating matplotlib table
    fig, ax = plt.subplots(figsize=(12, 4))

    # this code removes the figure plot (so the table exists as a standalone
    ax.axis('off')

    table = ax.table(cellText=dataframe.values, rowLabels=dataframe.index
    ,colLabels=dataframe.columns)

    # This following code is to ensure the index is kept in the plt table
    w, h = table[0, 1].get_width(), table[0, 1].get_height()
    table.add_cell(0, -1, w, h, text=dataframe.index.name)


    #Outputting all other files (excel, PDF, SQL Table)
    pdf = PdfPages(f'{key}_table.pdf')
    pdf.savefig(fig)
    pdf.close()


    dataframe.to_excel(f'{key}_excel.xlsx')

    # Create SQL Tables
    database = create_engine("postgresql://username:password@localhost:5432/mydatabase")
    dataframe.to_sql(name=f'{key}_table', database)

def attendanceDictionary(studentID, dict, by_grade = True, schoolID=994):
    if (by_grade == True):
        key = "Grade"
    else:
        key = "AttendanceProgramCodePrimary"

    # Making API request
    API_HOST = f"https://demo.aeries.net/aeries/api/v5/schools/{schoolID}/students/{studentID}"

    requestHeaders = {"formatType": "text/json",
                    "AERIES-CERT": "477abe9e7d27439681d62f4e0de1f5e1"}

    request = requests.get(API_HOST, headers=requestHeaders)
    requesttool = request.json()  # turns request to json request

    raw_data = pd.DataFrame.from_dict(requesttool)

    filtered_data = raw_data.filter(['StudentID', 'Grade', 'AttendanceProgramCodePrimary',
                                    'InactiveStatusCode'], axis=1)

    # Now I am counting each occurrence of active or inactive by grade
    for index, row in filtered_data.iterrows():
        if row[key] not in dict:
            dict[row[key]] = 0
        # Inactive students
        if f"{row[key]}_inactive" not in dict:
            dict[f"{row[key]}_inactive"] = 0

        if row['InactiveStatusCode'] == '':  
            dict[row[key]] = dict[row[key]] + 1
        else:
            dict[f"{row[key]}_inactive"] = dict[f"{row[key]}_inactive"] + 1

def aggregateData(workingList, excel_input = True, schoolID=994):
    if (excel_input == True):
        IDList = excelToIDList(workingList)
    else:
        IDList = listToIDList(workingList)

    # Making the API Requests here
    # Setting by_grade = True (default) returns dictionary sorted by grade.

    grade_dict = {}
    program_dict = {}

    # this is hardcoded for testing purposes. on cli you can type 99400001 to test as well
    attendanceDictionary(99400001, grade_dict)
    attendanceDictionary(99400001, program_dict, by_grade=False)

    # UNCOMMENT THIS FOR PROPER COUNTING OF ATTENDANCE
    # for ID in IDList:
    #     attendanceDictionary(ID, grade_dict)
    #     attendanceDictionary(ID, program_dict, by_grade = False)

    # Creating our tables
    grade_table_data = pd.DataFrame(columns=['Active', 'Inactive'])
    program_table_data = pd.DataFrame(columns=['Active', 'Inactive'])

    # Adding keys for our tables
    grade_index = [i for i in list(grade_dict.keys()) if isinstance(i, int)]
    grade_table_data.insert(loc=0, column="Grade", value=grade_index)

    program_index = [i for i in list(program_dict.keys()) if "_" not in i]
    program_table_data.insert(loc=0, column="Program Code", value=program_index)

    # Set all NaN to 0
    grade_table_data = grade_table_data.replace(np.nan, 0)
    program_table_data = program_table_data.replace(np.nan, 0)

    # get rid of duplicate Grades and Program Codes
    grade_table_data = grade_table_data.drop_duplicates()
    program_table_data = program_table_data.drop_duplicates()

    # Set new index by grade and program code
    grade_table_data = grade_table_data.set_index('Grade')
    program_table_data = program_table_data.set_index('Program Code')


    # Placing counts in their respective locations for grade and program code
    for index, row in grade_table_data.iterrows():
        if index in grade_dict:
            grade_table_data.at[index, 'Active'] = grade_dict[index]
            grade_table_data.at[index, 'Inactive'] = grade_dict[f"{index}_inactive"]

    for index, row in program_table_data.iterrows():
        if index in program_dict:
            program_table_data.at[index, 'Active'] = program_dict[index]
            program_table_data.at[index, 'Inactive'] = program_dict[f"{index}_inactive"]

    # Finally, outputting CSV, JSON, Excel, PDFs, and SQL Tables
    outputFiles(grade_table_data)
    outputFiles(program_table_data, by_grade=False)




# Obviously this is just for testing purposes, should be linked
# the application itself will intake data
selection = input('0 = CSV, 1 = list \n')
if (int(selection) == 0):
    current_excel = pd.read_excel('Learning_Blocks\excel_sheets\PrintQueryReport_20231203_190623_7549096.xlsx', header=2)
    aggregateData(current_excel)
else:
    list_entry = input('ID Numbers: ')
    aggregateData(list_entry, excel_input=False)










