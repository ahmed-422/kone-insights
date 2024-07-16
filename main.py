from groq import Groq
import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()

def default_config():
    st.set_page_config(
        layout="wide",
        page_title="Idea Insight",
        page_icon="💡" 
    )

default_config()
# hide_streamlit_style = """
#             <style>
#             [data-testid="stToolbar"] {visibility: hidden !important;}
#             footer {visibility: hidden !important;}
#             </style>
#             """
# st.markdown(hide_streamlit_style, unsafe_allow_html=True)


def main():
    
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        login()
    else:
        home()

def login():
    st.title("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if authenticate(username, password):
            st.session_state.authenticated = True
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")

def authenticate(username, password):
    # Replace with your own authentication logic
    return username == os.getenv("USER_NAME") or username == os.getenv("USER_NAME1") and password == os.getenv("ST_PASSWORD")

def home():
    st.title("Data insights MVP")
    st.write("Ask anything, and I'll provide an answer with references!")
    
    # Text input field
    user_query = st.text_input("Enter Text:", placeholder="Enter Only Keyword to find Insights")
    
    # Send button
    if st.button("Send"):
        
        st.write("Entered Text:", user_query)
        with st.spinner("Searching and Summarizing..."):
            col1, col2 = st.columns(2)
        # Call function to get Groq completions for each question
            for question_format in questions:
                question = question_format.format(user_query=user_query)
                response = get_groq_completion(question)
                json_response = get_groq_json(response)
                # st.write("Question:", question)
                if question.startswith("How many patents"):
                    cell=col1.container(border=True)
                    cell.markdown("""<h2><span style='color: red;'>Patent</span></h2>""", unsafe_allow_html=True)
                    cell.write(response)
                    json_content="Response"+"\n"+json_response
                    expander = cell.expander("JSON data")
                    expander.code(json_content,language='json',line_numbers=True)
                elif question.startswith("What is the competitor"):
                    cell=col2.container(border=True)
                    cell.markdown("""<h2><span style='color: blue;'>Competitor Analysis</span></h2>""", unsafe_allow_html=True)
                    cell.write(response)
                    json_content="Response"+"\n"+json_response
                    expander = cell.expander("JSON data")
                    expander.code(json_content,language='json',line_numbers=True)
                elif question.startswith("How many Technical Landscape"):
                    cell=col1.container(border=True)
                    cell.markdown("""<h2><span style='color: green;'>Technical Landscape</span></h2>""", unsafe_allow_html=True)
                    cell.write(response)
                    json_content="Response"+"\n"+json_response
                    expander = cell.expander("JSON data")
                    expander.code(json_content,language='json',line_numbers=True)
                elif question.startswith("How many Startup"):
                    cell=col2.container(border=True)
                    cell.markdown("""<h2><span style='color: brown;'>Startup</span></h2>""", unsafe_allow_html=True)
                    cell.write(response)
                    json_content="Response"+"\n"+json_response
                    expander = cell.expander("JSON data")
                    expander.code(json_content,language='json',line_numbers=True)
                elif question.startswith("How many University"):
                    cell=col1.container(border=True)
                    cell.markdown("""<h2><span style='color: yellow;'>University</span></h2>""", unsafe_allow_html=True)
                    cell.write(response)
                    json_content="Response"+"\n"+json_response 
                    expander = cell.expander("JSON data")
                    expander.code(json_content,language='json',line_numbers=True)



@st.cache_data
def get_groq_completion(question):
    GROQ_API_ID=os.getenv('Groq_API_ID')
    client = Groq(api_key=GROQ_API_ID)

    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "system",
                "content": "Consider yourself as a Browser Information Scratching expert, Now Scratch the Precise accurate Information from Browser for Given Question."
            },
            {
                "role": "user",
                "content": question
            }
        ],
        temperature=0,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    groq_response = ""
    for chunk in completion:
        groq_response += chunk.choices[0].delta.content or ""
    
    return groq_response

@st.cache_data
def get_groq_json(content):
    GROQ_API_ID=os.getenv('Groq_API_ID')
    client = Groq(api_key=GROQ_API_ID)

    completion = client.chat.completions.create(
        
        model="llama3-8b-8192",
        messages=[
            {
                "role": "system",
                "content": f"Consider yourself as a Expert JSON Parser,Now parse the exact details from the given Content that is\n{content}"
            },
            {
                "role": "user",
                "content": """The Parsed JSON Should be a form of ,The JSON should be like
                    {
                        Index: Only Total number from the Given Content,
                        Brief: Short Brief Insight Explanation from the Given Content,
                        Links: "Reference Links from the Given Content
                    }
                """
            }
        ],
        temperature=0,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    groq_response = ""
    for chunk in completion:
        groq_response += chunk.choices[0].delta.content or ""
    
    return groq_response

questions = [
    "How many patents are there for {user_query} ? In term of Total Numbers of Patents and short brief about it with some reference link for it?",
    "What is the competitor Analysis for {user_query}? In term of Total Numbers of Competions and short brief about it with some reference link for it?",
    "How many Technical Landscape are there in {user_query}? In term of Total Numbers of Technical Landscape and short brief about it with some reference link for it?",
    "How many Startup are there in {user_query} Domain ? In term of Total Numbers of Startup and short brief about it with some reference link for it?",
    "How many University are there in {user_query}? In term of Total Numbers of University and short brief about it with some reference link for it?"
]

if __name__ == "__main__":
    main()
