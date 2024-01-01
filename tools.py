import os
import canvasapi
from pathlib import Path
from datetime import datetime, timedelta
import docx2txt
import PyPDF2
from config import CANVAS_API_TOKEN, CANVAS_API_URL
import random
from gpt_feedback import gpt_response
import datetime
import re
import requests

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
        user_folder = submissions_folder / user["sortable_name"].replace(", ", "_").replace("@", "")

        print("Creating Folder")
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
            try:
                for file in folder.iterdir():

                    text = None

                    absolute_path = os.path.abspath(file)

                    if file.suffix == ".docx":
                        # Convert the docx file to txt
                        try:
                            text = docx2txt.process(absolute_path)
                        except KeyError:
                            continue

                    
                    elif file.suffix == ".pdf":
                        # Convert the pdf file to txt
                        text = pdf_to_txt(absolute_path)

                    # if variable text exists
                    if text:
                    
                        with open(file.with_suffix(".txt"), "w", encoding="utf-8") as f:
                            f.write(text)                    

                    # Delete the file
                    file.unlink()
            except:
                continue

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

                references = extract_references(read_text(absolute_path))

                ref_fname = absolute_path.split(".")[0] + "_references.txt"

                # Write the text to a file
                with open(ref_fname, "w", encoding="utf-8") as f:
                    f.write(references)


def get_feedback_by_dir(prompt, dir="submissions", url_check=False):
    """
    Convert the submissions to plain text.
    """
    # Get the submissions folder
    submissions_folder = Path(dir)

    cost_info = []

    print("\n")

    # Convert the submissions to plain text
    for i, submission in enumerate(submissions_folder.iterdir()):
        # Check if the submission is a zip file

        print(f"Processing folder {i+1}/{len(list(submissions_folder.iterdir()))}")

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

                        if url_check:
                            # Check the URLs
 
                            check_url_string = check_urls(text)

                            if check_url_string == "":
                                response += "\n\nAll URLs in the reference list are correct."
                            else:
                                response += check_url_string


                        # Add disclaimer to response
                        response += f"""

For more information on how to correctly format your citations and reference list, please see the following link: https://www.mybib.com/tools/harvard-referencing-generator/cite-them-right

==============================

Disclaimer: This feedback was generated using Assistive Feedback v.1.0.

The feedback is not guaranteed to be 100% accurate.

==============================


                            """

                        cost_info.append(cost)

                        feedback_filename = absolute_path.split("_references")[0] + "_feedback.txt"

                        # Write the text to a file
                        with open(feedback_filename, "w", encoding="utf-8") as f:
                            f.write(response)

    return {
        "total_cost": '$ {0:.4f}'.format(sum(cost_info)),
        "cost_per_student": '$ {0:.4f}'.format(sum(cost_info)/len(cost_info))
    }

def find_urls(text):
    url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    urls = re.findall(url_pattern, text)
    return urls

def url_exists(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)'}

    # strip "." and trailing "/" form url
    url = url.strip(".")
    url = url.rstrip("/")

    try:
        response = requests.get(url, headers=headers)
        return response.status_code != 404
    except requests.exceptions.RequestException:
        return False

def check_urls(text):

    check_url_string = ""
    # find all URLS in text
    urls = find_urls(text)

    # Check all urls and count how many are broken
    broken_urls = 0
    for url in urls:
        if not url_exists(url):
            broken_urls += 1

    # Count how many urls do not contain "doi.org"
    no_doi_urls = 0
    for url in urls:
        if "doi.org" not in url:
            no_doi_urls += 1

    # If there are broken urls
    if broken_urls > 0:
        check_url_string += f"""

{broken_urls} of the {len(urls)} URLs in your reference list are broken. Please check that all URLs are correct.

        """
    
    # If there are urls that do not contain "doi.org"
    if no_doi_urls > 0:
        check_url_string += f"""

{no_doi_urls} of the {len(urls)} URLs in your reference list do not contain "doi.org". 
It is strongly recommended that you use the "doi.org" URL for each reference to ensure that the URL is permanently accessible to the reader.

        """

    return check_url_string


def get_submission_by_user_id(user_id, submissions):
    """
    Get the submission by user_id.
    """
    for submission in submissions:

        if submission.user_id == int(user_id):
            return submission

    return None

def post_to_canvas(submissions, dir="submissions"):
    # Get the submissions folder
    submissions_folder = Path(dir)

    print("\n")


    for i, submission in enumerate(submissions_folder.iterdir()):

        print(f"Processing folder {i+1}/{len(list(submissions_folder.iterdir()))}: {submission}")

        if submission.is_dir():
            # Get the folder name
            folder_name = submission.stem

            # Get the folder
            folder = submissions_folder / folder_name

            # Convert the files to plain text
            for file in folder.iterdir():
                absolute_path = os.path.abspath(file)

                # If absolute_path ends with "_references.txt"
                if absolute_path.endswith("feedback.txt"):

                    with open(absolute_path, 'r', encoding='utf-8') as f:
                        text = f.read()
                    
                    # Get user_id from absolute_path
                    user_id = file.stem.split("_")[0]

                    print("user_id:", user_id)

                    # Get the submission
                    sub = get_submission_by_user_id(user_id, submissions)

                    print(sub.__dict__)

                    if sub:
                        # Post the feedback to Canvas
                        sub.edit(comment={'text_comment': text})


def read_text(path):
    """
    Read the text from a file.
    """
    # Open the file
    with open(path, "r", encoding='utf-8', errors='ignore') as file:
        # Read the text
        text = file.read()

    return text


def extract_references(text):
    lines = text.split("\n")

    found_references = False

    markers = [
        "reference",
        "bibliography",
        "word count",
    ]
    
    # Find index of line that contains ["References", "REFERENCES", "Bibliography", "BIBLIOGRAPHY" etc]
    for index, line in enumerate(lines):
        
        # if line containes any of the markers
        if any(marker in line.strip().lower() for marker in markers) and len(line.strip()) < 100:
            found_references = True
            break
    
    if not found_references:
        return ""
    else:
        references = lines[index:]

        # join the lines with "\n"
        return "\n".join(references)

def save_references(references, fname):
    """
    Save the references to a file.
    """
    # Open the file
    with open(fname, "w", encoding='utf-8') as file:
        # Write the references
        file.write(references)
    