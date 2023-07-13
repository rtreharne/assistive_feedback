# Imports
import os
import canvasapi
from pathlib import Path
from datetime import datetime, timedelta
import docx2txt
import PyPDF2
from config import CANVAS_API_TOKEN, CANVAS_API_URL




# Functions
def get_submissions(course_id, assignment_id):
    """
    Get the submissions for a given assignment.
    """
    # Create a new Canvas object
    canvas = canvasapi.Canvas(CANVAS_API_URL, CANVAS_API_TOKEN)

    # Get the course
    course = canvas.get_course(course_id)

    # Get the assignment
    assignment = course.get_assignment(assignment_id)

    # Get all the submissions
    submissions = [x for x in assignment.get_submissions(include=["user"]) if x.workflow_state == "graded"]

    return submissions


def download_submissions(submissions):
    """
    Download the submissions to a folder.
    """
    # Create a folder for the submissions
    submissions_folder = Path("submissions")
    submissions_folder.mkdir(exist_ok=True)

    # Download the submissions
    for submission in submissions:
        # Get the user
        try:
            user = submission.user
        except:
            continue

        # Create a folder for the user
        user_folder = submissions_folder / user["sortable_name"].replace(", ", "_")

        print("User Folder", user_folder)
        user_folder.mkdir(exist_ok=True)

        # Download the submission
        try:
            attachment = submission.attachments[0]
            attachment.download(user_folder / attachment.filename)
        except:
            continue


def convert_to_text():
    """
    Convert the submissions to plain text.
    """
    # Get the submissions folder
    submissions_folder = Path("submissions")

    # Convert the submissions to plain text
    for submission in submissions_folder.iterdir():
        # Check if the submission is a zip file

        if submission.is_dir():
            # Get the folder name
            folder_name = submission.stem

            # Get the folder
            folder = submissions_folder / folder_name

            # Convert the files to plain text
            for file in folder.iterdir():

                absolute_path = os.path.abspath(file)
                print(absolute_path)

                if file.suffix == ".docx":
                    # Convert the docx file to txt
                    text = docx2txt.process(absolute_path)

                
                elif file.suffix == ".pdf":
                    # Convert the pdf file to txt
                    text = pdf_to_txt(absolute_path)

                # Write the text to a file
                with open(file.with_suffix(".txt"), "w", encoding="utf-8") as f:
                    f.write(text)                    

                # Delete the file
                file.unlink()

def pdf_to_txt(pdf_path):
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page_number in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_number]
            text += page.extract_text()
    return text



def main():
    """
    Main function.
    """

    # Canvas Course ID
    course_id = input("Input Canvas course ID (e.g. 60973): ")

    # Canvas Assignment ID
    assignment_id = input("Input Canvas assignment ID (e.g. 208946): ")

    # Get the submissions
    submissions = get_submissions(course_id, assignment_id)

    # Download the submissions
    download_submissions(submissions)

    # Convert the submissions to plain text
    convert_to_text()


# Main function
if __name__ == "__main__":
    main()








