# ------------------------------------------------------------------------------------------ #
# Title: Assignment06_ThomasPerkins
# Desc: This assignment demonstrates using functions
# with structured error handling.
# Change Log: (Who, When, What)
#   TPerkins,11/23/2023,Created Script for Assignment 6
# ------------------------------------------------------------------------------------------ #

import json
import os
import io as _io

# Define the Data Constants
MENU: str = '''
---- Course Registration Program ----
  Select from the following menu:  
    1. Register a Student for a Course.
    2. Show current data.  
    3. Save data to a file.
    4. Exit the program.
----------------------------------------- 
'''
FILE_NAME: str = "Enrollments.json"

# Define the Data Variables
menu_choice: str  # Hold the choice made by the user.
students: list = []  # a table of student data
file = _io.TextIOWrapper  # the default item type for this type of file.

class FileProcessor:
    """
    A collection of processing layer functions that work with Json files

    ChangeLog: (Who, When, What)
    TPerkins, 11/23/2023, Created for Assignment06
    """

    # When the program starts, read the file data into a list of lists (table)
    # Extract the data from the file
    @staticmethod
    def read_data_from_file(file_name: str, student_data: list) -> list:
        """
        This function reads a json file and creates a list of student data from the contents

        ChangeLog: (Who, When, What)
        TPerkins, 11/23/2023, Created for Assignment06
        :param file_name: Name of file to be read.
        :param student_data: List of student data.
        :return: list
        """
        global file
        try:
            if os.path.exists(file_name):
                file = open(file_name, "r")
            else:
                file = open(file_name, "w")
                file.write("[]")
                file.close()
                file = open(file_name, "r")
            student_data = json.load(file)
            file.close()
        except Exception as e:
            IO.output_error_messages("There was an error opening the file!", e)
        finally:
            if not file.closed:
                file.close()
        return student_data

    @staticmethod
    def write_data_to_file(file_name: str, student_data: list):
        """
        This function writes the student data list to the json file.
        
        ChangeLog: (Who, When, What)
        TPerkins, 11/23/2023, Created for Assignment06
        :param file_name: 
        :param student_data: 
        :return: None
        """
        global file
        global num_records
        try:
            file = open(file_name, "w")
            json.dump(student_data, file)
            file.close()
            print("The following data was saved to the file:")
            counter = 0
            for student in student_data:
                counter += 1
                if counter > num_records:
                    print(f'Student {student["FirstName"]} '
                          f'{student["LastName"]} is enrolled in {student["CourseName"]}')
            num_records = counter
        except Exception as e:
            if not file.closed:
                file.close()
            IO.output_error_messages("There was an error writing the data to the file. ", e)


class IO:
    """
    A collection of presentation layer functions that manage user input and output

    ChangeLog: (Who, When, What)
    TPerkins, 11/23/2023, Created for Assignment06
    """

    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        """ This function displays a custom error messages to the user.

        ChangeLog: (Who, When, What)
        TPerkins, 11/23/2023, Created for Assignment06

        :return: None
        """
        print(message, end="\n\n")
        if error is not None:
            print("-- Technical Error Message -- ")
            print(error, error.__doc__, type(error), sep='\n')

    @staticmethod
    def output_menu(menu: str):
        """ This function displays a menu of choices to the user.

        ChangeLog: (Who, When, What)
        TPerkins, 11/23/2023, Created for Assignment06

        :return: None
        """
        print()
        print(menu)
        print()  # Adding extra space to make it look nicer.

    @staticmethod
    def input_menu_choice() -> str:
        """ This function gets a menu choice from the user.

        ChangeLog: (Who, When, What)
        TPerkins, 11/23/2023, Created for Assignment06

        :return: string with the users choice
        """
        choice = "0"
        try:
            choice = input("Enter your menu choice number: ")
            if choice not in ("1", "2", "3", "4"):  # Note these are strings
                raise Exception("Please, choose only 1, 2, 3, or 4")
        except Exception as e:
            IO.output_error_messages(e.__str__())  # Not passing the exception object to avoid the technical message
        return choice

    @staticmethod
    def output_student_courses(student_data: list):
        """ This function displays the current list of student course data

        ChangeLog: (Who, When, What)
        TPerkins, 11/23/2023, Created for Assignment06

        :return: None
        """
        # Process the data to create and display a custom message
        print("-" * 50)
        for student in student_data:
            print(f'Student {student["FirstName"]} '
                  f'{student["LastName"]} is enrolled in {student["CourseName"]}')
        print("-" * 50)

    @staticmethod
    def input_student_data(student_data: list):
        """ This function records user input for student first name, last name,
        and course number.

        ChangeLog: (Who, When, What)
        TPerkins, 11/23/2023, Created for Assignment06

        :return: list
        """

        try:
            student_first_name = input("Enter the student's first name: ")
            if len(student_first_name) == 0:
                raise ValueError("The first name should not be blank.")
            elif not student_first_name.isalpha():
                raise ValueError("The first name should not contain numbers.")
            student_last_name = input("Enter the student's last name: ")
            if len(student_last_name) == 0:
                raise ValueError("The last name should not be blank.")
            elif not student_last_name.isalpha():
                raise ValueError("The last name should not contain numbers.")
            course_name = input("Please enter the name of the course: ")
            if len(course_name) == 0:
                raise ValueError("The course name should not be blank.")
            elif course_name.isalpha():
                raise ValueError("The course name should contain a number.")
            student_record = {"FirstName": student_first_name,
                              "LastName": student_last_name,
                              "CourseName": course_name}
            student_data.append(student_record)
            print(f"You have registered {student_first_name} {student_last_name} for {course_name}.")
        except ValueError as e:
            IO.output_error_messages(ValueError.__doc__, e)
        except Exception as e:
            IO.output_error_messages("There was a non-specific error!", e)
        return student_data


# Open the data file
students = FileProcessor.read_data_from_file(FILE_NAME, students)
num_records = len(students)

# Present and Process the data
while True:

    # Present the menu of choices
    IO.output_menu(MENU)
    menu_choice = IO.input_menu_choice()

    # Input user data
    if menu_choice == "1":
        students = IO.input_student_data(students)
        continue

    # Present the current data
    elif menu_choice == "2":
        IO.output_student_courses(students)
        continue

    # Save the data to a file
    elif menu_choice == "3":
        FileProcessor.write_data_to_file(FILE_NAME, students)
        continue

    # Stop the loop
    elif menu_choice == "4":
        break  # out of the loop
    else:
        print("Please only choose option 1, 2, or 3")

print("Program Ended")
