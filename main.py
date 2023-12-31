# Imports
from tools import *
import time
                

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
        choice = input("\n\nEnter your choice: ")

        if choice == '1':
            start()
        elif choice == '2':
            print("\n\nExiting...")
            break
        else:
            print("\n\nInvalid choice. Please enter 1 or 2.")

    
def start():

    duration = None

    # Canvas Course ID
    course_id = input("\n\nInput Canvas course ID (e.g. 60973): ")

    # Canvas Assignment ID
    assignment_id = input("\n\nInput Canvas assignment ID (e.g. 208946): ")

    # Get the submissions
    print("\n\nGetting submissions...")

    try:
        submissions = get_submissions(course_id, assignment_id)
    except:
        print("\n\nInvalid course ID or assignment ID. Please try again.")
        return

    # Seed random
    #random.seed(42)

    # Get a sample of 10 submissions.

    # Ask user for number of submissions to sample, or ask to hit "Enter" to use all submissions
    num_submissions = input("\n\nHow many submissions do you want to sample? (Hit Enter to use all submissions): ")

    if num_submissions:
        submissions = random.sample(submissions, int(num_submissions))

    # Download the submissions
    print("\n\nDownloading submissions...")
    datestamp_string = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    dir = datestamp_string + "submissions"
    submissions = download_submissions(submissions, dir=dir)

    # Convert the submissions to plain text
    print("\n\nConverting submissions to plain text...")
    
    convert_to_text(dir=dir)
    

    # Get the references
    print("\n\nExtracting references from submissions...")
    get_references_by_dir(dir=dir)


    # Ask user if they want to use chat-gpt to get feedback on the references
    use_chat_gpt = input("\n\nDo you want to use chat-gpt to get feedback on the references? (y/n): ")

    

    if use_chat_gpt.lower() == "y":

        start = time.time()


        url_check = input("\n\nDo you want to check the URLs in the references? (y/n): ")

        if url_check.lower() == "y":
            url_check = True
        else:
            url_check = False
        
        with open('prompt.txt', 'r', encoding='utf-8') as f:
            prompt = f.read()

        # Get feedback from GPT-3.5
        print("\n\nGetting feedback from GPT-3.5...")

        try:
            cost = get_feedback_by_dir(prompt, dir=dir, url_check=url_check)
        except ZeroDivisionError:
            return

        print("\n\nProcessing complete!")
        print("\n\nTotal cost: {0}".format(cost["total_cost"]))

        finish = time.time()

        duration = finish - start

    # Ask the user if they want to post feedback to Canvas
    post_feedback = input("\n\nDo you want to post feedback to Canvas? (y/n): ")

    if post_feedback.lower() == "y":
        # Ask user to input random word to prevent accidental posting of feedback
        random_word = input("\n\nEnter the word 'post' to post feedback to Canvas: ")

        if random_word.lower() != "post":
            print("\n\nInvalid word. Feedback not posted.")
            post_feedback = "n"

    if post_feedback.lower() == "y":
        # Post feedback to Canvas
        print("\n\nPosting feedback to Canvas...")
        post_to_canvas(submissions, dir=dir)

        print("\n\nFeedback posted to Canvas!")

    # Count how many files that cointain "_feedback" in the filename in the dir (including subdirectories)
    total_feedback_files = len(list(Path(dir).rglob("*_feedback.txt")))

    # Report on how many submissions were processed out of the total number of submissions
    print("\n\n{0} out of {1} submissions processed.".format(total_feedback_files, len(submissions)))

    # Average time taken to process each submission
    if duration:
        print("\n\nAverage time per submission: {0:.1f} seconds.".format(duration/total_feedback_files))

    # Total time
    if duration:
        print("\n\nTotal time: {0:.0f} seconds.".format(duration))

    



# Main function
if __name__ == "__main__":

    main()






