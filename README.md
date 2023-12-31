# ASSISTIVE FEEDBACK

R. Treharne, K. Atkins and J. Foster

School of Life Sciences TEL Team. University of Liverpool

<img src="logo.jpg" alt="UoL logo" width="200"/>

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








