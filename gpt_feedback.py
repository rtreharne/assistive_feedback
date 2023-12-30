from config import OPENAI_API_KEY
from openai import OpenAI

client = OpenAI(
    api_key=OPENAI_API_KEY
)

response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {
      "role": "system",
      "content": """
        You are a University Lecture tasked with providing feedback to students
        on reference sections of student essays.

        Specifically you need to ensure that the reference list adheres to the Harvard referencing style.
        
        Make sure that the references are in the correct format and that they are
        in alphabetical order. Only tell students that the references are not in
        alphabetical order if they are not. If they are not, cite the references
        that are not in alphabetical order.

        Provide no more than 200 words of feedback to the student.

        Make sure that references are not duplicated. A reference has been duplicated if
        there is another with EXACTLY the same author AND year AND title. Only tell students that the references
        are duplicated if they are.

        Criticise the use of media sources (e.g. news outlets) and insist that students find primary sources to cite.
        Do not comment on the essay.

        A textbook is a primary source. Do not comment if a textbook is used.

        Do not suggest that the student should provide a summary or critique of the reference list.
        """
    },
    {
      "role": "user",
      "content": """Give me some feedback for this reference list:

Hu, B., Huang, S. and Yin, L. (2020). The Cytokine Storm and COVID‐19. Journal of Medical Virology, 93(1). doi:10.1002/jmv.26232.
Murphy, K. and Weaver, C. 2017. Janeway’s immunobiology, 9th edn. New York, NY: Garland Science/Taylor & Francis, p 6-11, 85-87, 111-113, 116-120. 
Saha, A., Sharma, A.R., Bhattacharya, M., Sharma, G., Lee, S.-S. and Chakraborty, C. (2020). Tocilizumab: A Therapeutic Option for the Treatment of Cytokine Storm Syndrome in COVID-19. Archives of Medical Research, 51(6), pp.595–597. doi:10.1016/j.arcmed.2020.05.009.
Tang, X.-D., Ji, T.-T., Dong, J.-R., Feng, H., Chen, F.-Q., Chen, X., Zhao, H.-Y., Chen, D.-K. and Ma, W.-T. (2021). Pathogenesis and Treatment of Cytokine Storm Induced by Infectious Diseases. International Journal of Molecular Sciences, 22(23), p.13009. doi:10.3390/ijms222313009.
Xu X, Han M, Li T, et al. Effective treatment of severe COVID‐19 patientswith tocilizumab.Proc Natl Acad Sci USA. 2020;117(20):10970‐10975.
Zhang, J.-M. and An, J. (2007). Cytokines, Inflammation, and Pain. International Anesthesiology Clinics, [online] 45(2), pp.27–37. doi:10.1097/aia.0b013e318034194e.

"""
    }
  ],
  temperature=0.7,
  max_tokens=500,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)

text = response.choices[0].message.content

# Save text to .txt file
with open('response.txt', 'w') as f:
    f.write(text)
