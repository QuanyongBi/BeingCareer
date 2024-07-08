from openai import OpenAI
import openai
# TODO: set the .env related file to initialize openai api service.
# TODO: Replace the prompt to actual tested stable one.

# for testing purpose, put the api_key below.
client = OpenAI(
    api_key="sk-proj-Lp6WDAvf5rpvf45wCbhFT3BlbkFJP8Jqv0v6bY6exUA8j5kL"
)

sample_resume = """
"content": {"name": "John Doe","email": "john.doe@example.com","projects": [{"name": "Project Z","year": "2021","description": "Developed an innovative solution"}],"education": {"year": "2018-2022","major": "Computer Science","school_name": "University Y"},"experience": [{"year": "2020","title": "Developer","company": "Company X","description": "Worked on various projects"}]},"""

def generate_resume_content(initial_json):
    # current prompt for testing only purpose.
    prompt = """
        You are a professional resume writer. Here is some initial information about the user:
        {},
        Please generate a well-crafted resume (quantify the process and result, make the candidate's job significant) content 
        based on this information in JSON format.
        You need to follow the following format and NOT INCLUDE ANY newline characters in the response, 
        {}
        """.format(initial_json, sample_resume)

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        response_format={"type": "json_object" },
        messages=[
            {"role": "system",
             "content": "You are a professional resume writer."},
            {"role": "user", "content": prompt}
        ]
    )

    resume_content = completion.choices[0].message.content.replace('\\n', '')
    return resume_content
