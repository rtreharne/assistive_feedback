# Imports
import os
import canvasapi
from pathlib import Path
from datetime import datetime, timedelta
import docx2txt
import PyPDF2
from config import CANVAS_API_TOKEN, CANVAS_API_URL
import random
import tools
from gpt_feedback import gpt_response

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


def download_submissions(submissions, dir="submissions"):
    """
    Download the submissions to a folder.
    """

    downloaded_submissions = []

    # Create a folder for the submissions
    submissions_folder = Path(dir)
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

        print("Creating Folder", user_folder)
        user_folder.mkdir(exist_ok=True)

        # Download the submission
        try:
            attachment = submission.attachments[0]
            filename = str(submission.user_id) + "_" + attachment.filename
            attachment.download(user_folder / filename)
            downloaded_submissions.append(submission)
        except:
            continue
    
    return downloaded_submissions


def convert_to_text(dir="submissions"):
    """
    Convert the submissions to plain text.
    """
    print("\n\n")
    # Get the submissions folder
    submissions_folder = Path(dir)

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

                text = None

                absolute_path = os.path.abspath(file)
                print(f"Creating file in folder {folder}: {file}")

                if file.suffix == ".docx":
                    # Convert the docx file to txt
                    text = docx2txt.process(absolute_path)

                
                elif file.suffix == ".pdf":
                    # Convert the pdf file to txt
                    text = pdf_to_txt(absolute_path)

                # if variable text exists
                if text:
                
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


def get_references_by_dir(dir="submissions"):
    """
    Convert the submissions to plain text.
    """
    # Get the submissions folder
    submissions_folder = Path(dir)

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

                references = tools.extract_references(tools.read_text(absolute_path))

                ref_fname = absolute_path.split(".")[0] + "_references.txt"

                # Write the text to a file
                with open(ref_fname, "w", encoding="utf-8") as f:
                    f.write(references)


def get_feedback_by_dir(prompt, dir="submissions"):
    """
    Convert the submissions to plain text.
    """
    # Get the submissions folder
    submissions_folder = Path(dir)

    cost_info = []

    print("\n\n")

    # Convert the submissions to plain text
    for i, submission in enumerate(submissions_folder.iterdir()):
        # Check if the submission is a zip file

        print(f"Processing folder {i}/{len(list(submissions_folder.iterdir()))}: {submission}")

        if submission.is_dir():
            # Get the folder name
            folder_name = submission.stem

            # Get the folder
            folder = submissions_folder / folder_name

            # Convert the files to plain text
            for file in folder.iterdir():
                absolute_path = os.path.abspath(file)

                # If absolute_path ends with "_references.txt"
                if absolute_path.endswith("_references.txt"):

                    with open(absolute_path, 'r', encoding='utf-8') as f:
                        text = f.read()

                    if len(text) > 100:
                        response, cost = gpt_response(prompt, text)

                        cost_info.append(cost)

                        feedback_filename = absolute_path.split("_references")[0] + "_feedback.txt"

                        # Write the text to a file
                        with open(feedback_filename, "w", encoding="utf-8") as f:
                            f.write(response)

    return {
        "total_cost": '$ {0}'.format(sum(cost_info)),
        "cost_per_student": '$ {0}'.format(sum(cost_info)/len(cost_info))
    }
                    


def main():
    """
    Main function.
    """
    while True:


        print(
        r"""
    ___   __________ ____________________    ________
   /   | / ___/ ___//  _/ ___/_  __/  _/ |  / / ____/
  / /| | \__ \\__ \ / / \__ \ / /  / / | | / / __/   
 / ___ |___/ /__/ // / ___/ // / _/ /  | |/ / /___   
/_/ _|_/____/____/___//____//_/_/___/  |___/_____/_  
   / ____/ ____/ ____/ __ \/ __ )/   | / ____/ //_/  
  / /_  / __/ / __/ / / / / __  / /| |/ /   / ,<     
 / __/ / /___/ /___/ /_/ / /_/ / ___ / /___/ /| |    
/_/   /_____/_____/_____/_____/_/  |_\____/_/ |_|    
                                                       

By R. Treharne, K. Atkins and J. foster - University of Liverpool. (2023)

        """
        )

        print("\nOptions:")
        print("1. Start")
        print("2. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            start()
        elif choice == '2':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")

    
def start():
    # Canvas Course ID
    course_id = input("Input Canvas course ID (e.g. 60973): ")

    # Canvas Assignment ID
    assignment_id = input("Input Canvas assignment ID (e.g. 208946): ")

    # Get the submissions
    print("\n\nGetting submissions...")
    submissions = get_submissions(course_id, assignment_id)

    # Seed random
    #random.seed(42)

    # Get a sample of 10 submissions.

    # Ask user for number of submissions to sample, or ask to hit "Enter" to use all submissions
    num_submissions = input("\n\nHow many submissions do you want to sample? (Hit Enter to use all submissions): ")

    if num_submissions:
        submissions = random.sample(submissions, int(num_submissions))

    # Download the submissions
    print("\n\nDownloading submissions...")
    dir = "submissions"
    submissions = download_submissions(submissions)

    # Convert the submissions to plain text
    print("\n\nConverting submissions to plain text...")
    convert_to_text()

    # Get the references
    print("\n\nExtracting references from submissions...")
    get_references_by_dir()

    # Ask user if they want to use chat-gpt to get feedback on the references
    use_chat_gpt = input("\n\nDo you want to use chat-gpt to get feedback on the references? (y/n): ")

    if use_chat_gpt.lower() == "y":
        # Get prompt text from prompt.txt

        
        with open('prompt.txt', 'r', encoding='utf-8') as f:
            prompt = f.read()

        # Get feedback from GPT-3.5
        print("\n\nGetting feedback from GPT-3.5...")
        cost = get_feedback_by_dir(prompt)

        print("\n\nProcessing complete!")
        print("\n\nTotal cost: {0}".format(cost["total_cost"]))

    # Ask the user if they want to post feedback to Canvas
    post_feedback = input("\n\nDo you want to post feedback to Canvas? (y/n): ")


# Main function
if __name__ == "__main__":

    main()






