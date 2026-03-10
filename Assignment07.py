# ------------------------------------------------------------------------------------ #
# Title: Assignment07
# Desc: This assignment demonstrates using data classes
# with structured error handling
# Change Log: (Who, When, What)
#   RRoot,1/1/2030,Created Script
#   Alfredo Arnaiz, 20260308, Incorporated assignment requirements
# ------------------------------------------------------------------------------------ #
import _io
import json

# Define the Data Constants
MENU: str = '''
---- Course Registration Program --------
  Select from the following menu:  
    1. Register a Student for a Course
    2. Show current data  
    3. Save data to a file
    4. Exit the program
----------------------------------------- 
'''
FILE_NAME: str = "Enrollments.json"

# Define the Data Variables
students: list = []  # a table of student data
menu_choice: str = ""  # Hold the choice made by the user.


class Person:
    """
    A class representing person data.

    Properties:
    - first_name (str): The person's first name. Defaults to empty string.
    - last_name (str): The person's last name. Defaults to empty string.

    The __str__ method returns comma-separated first and last name,
    enabling extraction of data in a structured format.

    ChangeLog:
    Alfredo Arnaiz, 20260308, Created class.
    """

    def __init__(self, first_name: str = '', last_name: str = ''):
        self.first_name = first_name
        self.last_name = last_name

    @property
    def first_name(self):
        return self.__first_name.title()

    @first_name.setter
    def first_name(self, value: str):
        if value.isalpha() or value == "":
            self.__first_name = value
        else:
            raise ValueError("The first name should not contain numbers.")

    @property
    def last_name(self):
        return self.__last_name.title()

    @last_name.setter
    def last_name(self, value: str):
        if value.isalpha() or value == "":
            self.__last_name = value
        else:
            raise ValueError("The last name should not contain numbers.")

    def __str__(self):
        """Returns comma-separated first and last name for data extraction."""
        return f'{self.first_name},{self.last_name}'


class Student(Person):
    """
    A class representing student data, subclass of Person.

    Extends Person with a course_name property.

    Properties:
    - course_name (str): The name of the course. Defaults to empty string.

    The __str__ method returns comma-separated first name, last name, and course name,
    enabling extraction of all student data in a structured format.

    ChangeLog:
    Alfredo Arnaiz, 20260308, Created class.
    """

    def __init__(self, first_name: str = '', last_name: str = '', course_name: str = ''):
        super().__init__(first_name=first_name, last_name=last_name)
        self.course_name = course_name

    @property
    def course_name(self):
        return self.__course_name

    @course_name.setter
    def course_name(self, value: str):
        self.__course_name = value

    def __str__(self):
        """Returns comma-separated first name, last name, and course name for data extraction."""
        return f'{self.first_name},{self.last_name},{self.course_name}'


# Processing --------------------------------------- #
class FileProcessor:
    """
    A collection of processing layer functions that work with JSON files

    ChangeLog: (Who, When, What)
    RRoot,1.1.2030,Created Class
    Alfredo Arnaiz, 20260308, Adapted code to use Student objects instead of dictionaries
    """

    @staticmethod
    def read_data_from_file(file_name: str, student_data: list):
        """
        Reads data from a JSON file and loads it into the provided list as Student objects.

        Opens the specified JSON file, deserializes its contents, converts each record
        into a Student object, and returns the populated list.

        ChangeLog:
        RRoot, 1.1.2030, Created function
        Alfredo Arnaiz, 20260308, Adapted to return list of Student objects

        :param file_name: string with the name of the file to read from
        :param student_data: list to be filled with Student objects

        :return: list of Student objects
        """
        file: _io.TextIOWrapper = None

        try:
            file = open(file_name, "r")
            json_students = json.load(file)
            file.close()
            # Convert the list of dictionary rows into a list of Student objects
            for student in json_students:
                student_object: Student = Student(
                    first_name=student['FirstName'],
                    last_name=student['LastName'],
                    course_name=student['CourseName']
                )
                student_data.append(student_object)
        except Exception as e:
            IO.output_error_messages(message="Error: There was a problem with reading the file.", error=e)
        finally:
            if file is not None and not file.closed:
                file.close()
        return student_data

    @staticmethod
    def write_data_to_file(file_name: str, student_data: list):
        """
        Converts a list of Student objects to dictionary rows and writes them to a JSON file.

        Opens the specified file in write mode, serializes the student data as a list
        of dictionaries, and saves it using json.dump().

        ChangeLog:
        RRoot, 1.1.2030, Created function
        Alfredo Arnaiz, 20260308, Adapted to handle Student objects

        :param file_name: string with the name of the file to write to
        :param student_data: list of Student objects to be written to the file

        :return: None
        """
        file: _io.TextIOWrapper = None

        try:
            list_of_dictionary_data: list = []
            for student in student_data:  # Convert list of Student objects to list of dictionary rows
                student_json: dict = {
                    "FirstName": student.first_name,
                    "LastName": student.last_name,
                    "CourseName": student.course_name
                }
                list_of_dictionary_data.append(student_json)

            file = open(file_name, "w")
            json.dump(list_of_dictionary_data, file, indent=2)
            file.close()
            IO.output_student_courses(student_data=student_data)
        except Exception as e:
            message = "Error: There was a problem with writing to the file.\n"
            message += "Please check that the file is not open by another program."
            IO.output_error_messages(message=message, error=e)
        finally:
            if file is not None and not file.closed:
                file.close()


# Presentation --------------------------------------- #
class IO:
    """
    A collection of presentation layer functions that manage user input and output

    ChangeLog: (Who, When, What)
    RRoot,1.1.2030,Created Class
    RRoot,1.2.2030,Added menu output and input functions
    RRoot,1.3.2030,Added a function to display the data
    RRoot,1.4.2030,Added a function to display custom error messages
    """

    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        """
        Displays a custom error message to the user, with optional technical detail.

        If an Exception object is provided, its type, message, and docstring are
        also printed for debugging purposes.

        ChangeLog:
        RRoot, 1.3.2030, Created function
        Alfredo Arnaiz, 20260308, Edited docstring

        :param message: string with the error message to display to the user
        :param error: optional Exception object with technical details to display

        :return: None
        """
        print(message, end="\n\n")
        if error is not None:
            print("-- Technical Error Message -- ")
            print(error, error.__doc__, type(error), sep='\n')

    @staticmethod
    def output_menu(menu: str):
        """
        Displays the program menu of choices to the user.

        ChangeLog:
        RRoot, 1.1.2030, Created function

        :param menu: string containing the formatted menu to display

        :return: None
        """
        print()  # Adding extra space to make it look nicer.
        print(menu)
        print()  # Adding extra space to make it look nicer.

    @staticmethod
    def input_menu_choice():
        """
        Prompts the user to enter a menu choice and validates it is 1–4.

        Raises an exception (handled internally) if the choice is not valid.

        ChangeLog:
        RRoot, 1.1.2030, Created function
        Alfredo Arnaiz, 20260308, Edited docstring

        :return: string with the user's validated menu choice
        """
        choice = "0"
        try:
            choice = input("Enter your menu choice number: ")
            if choice not in ("1", "2", "3", "4"):  # Note these are strings
                raise Exception("Please, choose only 1, 2, 3, or 4")
        except Exception as e:
            IO.output_error_messages(e.__str__())  # Not passing e to avoid the technical message

        return choice

    @staticmethod
    def output_student_courses(student_data: list):
        """
        Displays each student's comma-separated registration data to the user.

        Iterates through the list of Student objects and prints a formatted
        string of each student's first name, last name, and course name.

        ChangeLog:
        RRoot, 1.1.2030, Created function
        Alfredo Arnaiz, 20260308, Edited docstring, set it to use Student str method
        override

        :param student_data: list of Student objects to be displayed

        :return: None
        """
        print("-" * 50)
        for student in student_data:
            print(student)
        print("-" * 50)

    @staticmethod
    def input_student_data(student_data: list):
        """
        Prompts the user to enter a student's first name, last name, and course name,
        then appends a new Student object to the provided list.

        Validates that name fields contain only alphabetic characters via the
        Student class property setters. Handles ValueError for invalid input
        and generic Exception for unexpected errors.

        ChangeLog:
        RRoot, 1.1.2030, Created function
        Alfredo Arnaiz, 20260308, Adapted code to work with Student class,
        edited docstring

         :param student_data: list of Student objects to append the new entry to

         :return: list with the new Student object appended
        """

        try:
            student = Student()
            student.first_name = input("Enter the student's first name: ")
            student.last_name = input("Enter the student's last name: ")
            student.course_name = input("Please enter the name of the course: ")
            student_data.append(student)
        except ValueError as e:
            IO.output_error_messages(message="This value is not the correct type of data!", error=e)
        except Exception as e:
            IO.output_error_messages(message="Error: There was a problem with your entered data.", error=e)
        return student_data


# Start of main body

# When the program starts, read the file data into a list of Student objects
students = FileProcessor.read_data_from_file(file_name=FILE_NAME, student_data=students)

# Present and Process the data
while True:

    # Present the menu of choices
    IO.output_menu(menu=MENU)

    menu_choice = IO.input_menu_choice()

    # Input user data
    if menu_choice == "1":
        students = IO.input_student_data(student_data=students)
        continue

    # Present the current data
    elif menu_choice == "2":
        IO.output_student_courses(students)
        continue

    # Save the data to a file
    elif menu_choice == "3":
        FileProcessor.write_data_to_file(file_name=FILE_NAME, student_data=students)
        continue

    # Stop the loop
    elif menu_choice == "4":
        break

    else:
        print("Please only choose option 1, 2, 3, or 4")

print("Program Ended")
