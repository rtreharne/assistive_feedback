# ASSISTIVE FEEDBACK

R. Treharne, K. Atkins and J. Foster

School of Life Sciences TEL Team. University of Liverpool

<img src="logo.jpg" alt="UoL logo" width="200"/>

## Summary

## Automated Feedback Generation

This program allows Canvas users with teacher or admin privileges to generate automated feedback on the reference sections of essay or report assignment submissions. The generated feedback can be posted as a submission comment on Canvas. This program helps improve the consistency of feedback received by students while reducing the marking workload for academic staff.

## Overview

The rapid adoption of Generative Artificial Intelligence (GAI) by students in higher education to complete written assignments is currently a contentious topic among academic teaching staff and is being debated continuously and fiercly. Equivalent attention is yet to be paid to ideas that involve using GAI to, where appropriate, automate the delivery of quality, trustworthy feedback to students on their written work. Such ideas could significantly improve the consistency of feeback received by students while dramatically reducing the marking workload of academic staff.

This project is a case study of how GAI, in this case Chat-GPT, can be used to provide automated feedback on student essays. Initially, the project is only concerned with providing feedback on the quality of an essay's reference list and not on the content of the essay directly. This allows us to circumnavigate concerns over submitting our student essays to a 3rd party tool, i.e. might Chat-GPT offer up an augmented version of one of our own student essays if provoked? Also, it allows us to narrow the focus of this project to a small, self-contained, reproducible task - perfect for the GAI arena.


## Usage

You will need to have Python 3 installed in order to use the program.

## Windows users

1. Install Git Bash

2. Using Git Bash navigate download the repository and cd into the created directory:

```{bash}
git clone https://github.com/rtreharne/assistive_feedback
cd assistive_feedback
```

3. Create a Virtual Environment and install the required packages.
```{bash}
python -m virtualenv venv
source ./venv/Scripts/activate
pip install -r requirements.txt
```

4. Create a `config.py` file using `config-example.py` as a template and update it with values for your `CANVAS_API_URL`, `CANVAS_API_TOKEN` and your `OPENAI_API_KEY`.
```{bash}
cp config-example.py config.py
nano config.py
```
For help obtaining your `CANVAS_API_KEY` visit [here](https://community.canvaslms.com/t5/Admin-Guide/How-do-I-manage-API-access-tokens-as-an-admin/ta-p/89).

For help obtaining your `OPEN_AI_KEY` visit [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-api-key). You will need to signup for a payment plan.

5. Run the Assistive Feedback program using the following command:
```{bash}
python main.py
```

## For Linux/Max OS

1. Open Terminal

2. Using Terminal, clone the repository and navigate to the created directory:

```{bash}
git clone https://github.com/rtreharne/assistive_feedback
cd assistive_feedback
```

3. Create a Virtual Environment and install the required packages.
```{bash}
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

4. Create a `config.py` file using `config-example.py` as a template and update it with values for your `CANVAS_API_URL`, `CANVAS_API_TOKEN` and your `OPENAI_API_KEY`.
```{bash}
cp config-example.py config.py
nano config.py
```
For help obtaining your `CANVAS_API_KEY` visit [here](https://community.canvaslms.com/t5/Admin-Guide/How-do-I-manage-API-access-tokens-as-an-admin/ta-p/89).

For help obtaining your `OPEN_AI_KEY` visit [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-api-key). You will need to signup for a payment plan.

5. Run the Assitive Feedback proram using the following command:
```{bash}
python3 main.py
```

## Example Prompt

The following is the default [prompt](./prompt.txt) used to elicit responses from Chat-GPT:

```{text}
You are a University lecturer tasked with providing feedback to students
on reference sections of student essays.

Specifically you need to ensure that the reference list adheres to the Harvard referencing style.

Make sure that the references are in the correct format: author name, (year), title, journal, volume, pages, doi/url

Check that the reference list should be organized according to ascending alphabetical order of first author suranme.
If they are orgainised correctly then give positive comment. If they are not organised correctly then provide recommendation to correct.

Author names for a single reference DO NOT need to be organised by ascending alphabetical order.

The reference list should include multiple references from multiple peer-reviewed sources.

Permit references that are books.

Identify any references that are not peer-reviewed sources and which are not? Insist that students find primary sources to cite.
If any identified, ask "did you forget to include volume and page numbers, doi/url?"

Do not comment on the essay.

Do not suggest that the student should provide a summary or critique of the reference list.

Do not criticise for the sake of doing so. If it's all good, then provide positive feedback.

Provide no more than 100 words of feedback to the student.

```

## Example Response

### Example Response 1

The following response was generated using [example_input_1.txt](./example_input_1.txt)


```{text}
The references provided are not organized in ascending alphabetical order of the first author's surname. Please rearrange the references in this order. Additionally, the references seem to be from reputable sources such as PubMed and PMC, which is good. However, it's important to ensure that the references are from peer-reviewed journals or books. It seems that some of the references may not be from peer-reviewed sources. Please double-check and ensure that all the references are from peer-reviewed sources. If any are not, please find primary sources to cite. Also, ensure that the references are in the correct Harvard referencing style format, including author name, year, title, journal, volume, pages, and doi/url.

1 of the 5 URLs in your reference list are broken. Please check that all URLs are correct.

5 of the 5 URLs in your reference list do not contain "doi.org". 
It is strongly recommended that you use the "doi.org" URL for each reference to ensure that the URL is permanently accessible to the reader.

For more information on how to correctly format your citations and reference list, please see the following link: https://www.mybib.com/tools/harvard-referencing-generator/cite-them-right

==============================

Disclaimer: This feedback was generated using Assistive Feedback v.1.0.

The feedback is not guaranteed to be 100% accurate.

==============================
```

### Example 2

The following response was generated using [example_input_2.txt](./example_input_2.txt)

```{text}
The references in your list are well-formatted in the Harvard referencing style, with the author names, publication years, titles, journal names, volume, pages, and dois/urls included where applicable. The references are also organized in ascending alphabetical order of the first author's surname, which is great. However, it's important to ensure that all the references are from peer-reviewed sources. The references from "UpToDate" and "Healthline" are not peer-reviewed sources. Please replace these with peer-reviewed articles. Also, for the reference "Dembic, Z. (2015)", did you forget to include volume and page numbers, doi/url? Overall, well done on the formatting and organization of the references!

1 of the 12 URLs in your reference list are broken. Please check that all URLs are correct.

12 of the 12 URLs in your reference list do not contain "doi.org". 
It is strongly recommended that you use the "doi.org" URL for each reference to ensure that the URL is permanently accessible to the reader.

For more information on how to correctly format your citations and reference list, please see the following link: https://www.mybib.com/tools/harvard-referencing-generator/cite-them-right

==============================

Disclaimer: This feedback was generated using Assistive Feedback v.1.0.

The feedback is not guaranteed to be 100% accurate.

==============================
                            
```











