import streamlit as st
import hashlib
import json
import os

# Define CSS styles
css = """
body {
    background-color: #f0f2f6;
    font-family: 'Helvetica Neue', sans-serif;
}
.sidebar .sidebar-content {
    background-color: #f8f9fa;
}
h1, h2, h3 {
    color: #333;
}
.stButton>button {
    color: #fff;
    background-color: #007bff;
    border-color: #007bff;
}
.stButton>button:hover {
    background-color: #0056b3;
    border-color: #004085;
}
"""

st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

# Helper functions for password hashing and authentication
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return True
    return False

# Load existing users from a JSON file
def load_users():
    if os.path.exists('users.json'):
        with open('users.json', 'r') as f:
            return json.load(f)
    return {}

# Save users to a JSON file
def save_users(users):
    with open('users.json', 'w') as f:
        json.dump(users, f)

# User authentication function
def authenticate_user(username, password):
    users = load_users()
    if username in users and check_hashes(password, users[username]['password']):
        return True
    return False

# Function to register a new user
def register_user(username, password):
    users = load_users()
    if username in users:
        return False  # Username already exists
    users[username] = {'password': make_hashes(password)}
    save_users(users)
    return True

# Registration page
def registration_page():
    st.title("User Registration")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    password_confirm = st.text_input("Confirm Password", type="password")
    
    if st.button("Register"):
        if password != password_confirm:
            st.error("Passwords do not match!")
        else:
            if register_user(username, password):
                st.success("You have successfully registered!")
                st.info("Now go to the Login page to access the content.")
            else:
                st.error("Username already exists! Please choose another.")

# Login page
def login_page():
    st.title("User Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if authenticate_user(username, password):
            st.success(f"Welcome, {username}!")
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
        else:
            st.error("Invalid username or password!")

# Main content for logged-in users
def main_app():
    st.title("Welcome to the Learning Style Quiz")
    
    if "logged_in" in st.session_state and st.session_state["logged_in"]:
        st.write(f"Hello, {st.session_state['username']}! You are logged in.")

        # Step 1: Ask for the student's course
        selected_course = st.text_input("Enter your course of study:")

        # Step 2: Render the quiz
        if selected_course:
            dominant_style = render_quiz()
                
            # Step 3: Provide resources based on learning style and course
            if dominant_style:
                provide_resources(dominant_style, selected_course)
    else:
        st.warning("You need to log in to access the content.")

# Function to render the quiz and evaluate it (from previous code)
def render_quiz():
    st.subheader("Learning Style Quiz")
    
    questions = [
        "How do you prefer to learn new information?",
        "What helps you remember things better?",
        "How do you solve problems?",
        "What kind of study materials do you prefer?",
        "When studying, how do you best absorb the information?",
        "How do you approach complex tasks or challenges?",
        "What study environments do you find most effective?",
        "How do you prepare for exams or assessments?",
        "What role does technology play in your learning process?",
        "How do you use feedback to improve your understanding?"
    ]
    
    responses = []
    
    for question in questions:
        response = st.text_input(question)
        responses.append(response)
    
    if st.button("Submit Quiz"):
        dominant_style = evaluate_quiz(responses)
        return dominant_style
    return None

# Function to evaluate the quiz and provide resources (from previous code)
def evaluate_quiz(responses):
    scores = {"Visual": 0, "Auditory": 0, "Kinesthetic": 0, "Reading/Writing": 0}
    
    for response in responses:
        if 'see' in response.lower() or 'diagram' in response.lower() or 'watch' in response.lower():
            scores["Visual"] += 1
        elif 'listen' in response.lower() or 'hear' in response.lower() or 'discuss' in response.lower():
            scores["Auditory"] += 1
        elif 'do' in response.lower() or 'hands-on' in response.lower() or 'practice' in response.lower():
            scores["Kinesthetic"] += 1
        elif 'read' in response.lower() or 'write' in response.lower() or 'text' in response.lower():
            scores["Reading/Writing"] += 1
            
    dominant_style = max(scores, key=scores.get)
    return dominant_style

# Provide resources based on the dominant learning style and selected course
def provide_resources(dominant_style, course):
    resources = {
        "Visual": {
            "Health Sciences": [
                "Watch [visual health sciences tutorials](https://www.khanacademy.org/science/health-and-medicine).",
                "Use [anatomy visualization tools](https://www.visiblebody.com/)."
            ],
             "Computer Sciences": [
                "Learn coding with [visual programming platforms](https://scratch.mit.edu/).",
                "Watch [visual tutorials on YouTube](https://www.youtube.com/results?search_query=programming+tutorials)."
            ],
            "Humanities": [
                "Explore [visual lecture series](https://www.coursera.org/courses?query=humanities).",
                "Watch [documentaries and visual content](https://www.netflix.com/browse/genre/6839) on historical and cultural topics."
            ],
            "Art": [
                "Watch [art tutorials and demonstrations](https://www.youtube.com/results?search_query=art+tutorials).",
                 "Use [visual art resources and galleries](https://www.artsy.net/)."
            ],
            "Politics": [
                "Watch [political science lectures](https://www.youtube.com/results?search_query=political+science+lectures).",
                "Explore [visual guides and infographics](https://www.visualcapitalist.com/)."
            ],
            "Agriculture": [
                "Watch [YouTube videos on sustainable farming](https://www.youtube.com/results?search_query=sustainable+farming).",
                "Explore [visual guides on plant care](https://www.gardeningknowhow.com/)."
            ],
            "Statistics": [
                "Use [visual statistics tools](https://www.tableau.com/).",
                "Watch [statistics tutorials](https://www.khanacademy.org/math/statistics-probability)."
            ],
            "Biochemistry": [
                "Watch [biochemistry tutorials](https://www.khanacademy.org/science/biology/biochemistry).",
                "Use [molecular visualization tools](https://www.chemeddl.org/resources/models360/models.php)."
            ],
            "Law": [
                "Watch [legal studies lectures](https://www.youtube.com/results?search_query=legal+studies+lectures).",
                "Explore [visual legal guides and case studies](https://www.cali.org/)."
            ]
        },
        "Auditory": {
            "Health Sciences": [
                "Listen to [health sciences podcasts](https://www.listennotes.com/search/?q=health+science).",
                "Watch [lecture series with auditory explanations](https://www.youtube.com/results?search_query=health+science+lectures)."
            ],
            "Computer Sciences": [
                "Listen to [programming podcasts](https://www.listennotes.com/search/?q=programming).",
                "Watch [talks and lectures on coding](https://www.youtube.com/results?search_query=programming+lectures)."
            ],
            "Humanities": [
                "Listen to [humanities podcasts](https://www.listennotes.com/search/?q=humanities).",
                "Watch [lecture series on YouTube](https://www.youtube.com/results?search_query=humanities+lectures)."
            ],
            "Art": [
                "Listen to [art-related podcasts](https://www.listennotes.com/search/?q=art).",
                "Watch [art history lectures](https://www.youtube.com/results?search_query=art+history+lectures)."
            ],
            "Politics": [
                "Listen to [political podcasts](https://www.listennotes.com/search/?q=politics).",
                "Watch [political science lectures](https://www.youtube.com/results?search_query=political+science+lectures)."
            ],
            "Agriculture": [
                "Listen to [agriculture podcasts](https://www.listennotes.com/search/?q=agriculture).",
                "Attend [webinars or online lectures](https://www.eventbrite.com/d/online/agriculture/)."
            ],
            "Statistics": [
                "Listen to [statistics podcasts](https://www.listennotes.com/search/?q=statistics).",
                "Watch [lectures on statistical methods](https://www.youtube.com/results?search_query=statistics+lectures)."
            ],
            "Biochemistry": [
                 "Listen to [biochemistry podcasts](https://www.listennotes.com/search/?q=biochemistry).",
                "Watch [biochemistry lecture series](https://www.youtube.com/results?search_query=biochemistry+lectures)."
            ],
            "Law": [
                "Listen to [legal podcasts](https://www.listennotes.com/search/?q=law).",
                "Watch [law school lectures](https://www.youtube.com/results?search_query=law+lectures)."
            ]
        },
        "Kinesthetic": {
            "Health Sciences": [
                "Engage in [hands-on medical simulations](https://www.ama-assn.org/delivering-care/public-health/medical-simulation).",
                "Participate in [health science workshops](https://www.eventbrite.com/d/online/health--workshops/)."
            ],
            "Computer Sciences": [
                "Participate in [coding bootcamps](https://www.coursereport.com/).",
                "Engage in [hackathons and coding challenges](https://www.hackerearth.com/challenges/)."
            ],
            "Humanities": [
                "Join [interactive history workshops](https://www.eventbrite.com/d/online/history--workshops/).",
                "Engage in [cultural immersion activities](https://www.couchsurfing.com/)."
            ],
            "Art": [
                "Join [art workshops and classes](https://www.eventbrite.com/d/online/art--classes/).",
                "Participate in [interactive art projects](https://www.instructables.com/art/)."
            ],
            "Politics": [
                "Engage in [political science workshops](https://www.eventbrite.com/d/online/political-science--workshops/).",
                "Participate in [model UN or debate clubs](https://www.unausa.org/model-un/)."
            ],
            "Agriculture": [
                "Participate in [hands-on farming workshops](https://www.eventbrite.com/d/online/farming--workshops/).",
                "Engage in [community gardening projects](https://www.garden.org/)."
            ],
            "Statistics": [
                "Use [interactive statistics tools](https://www.gapminder.org/tools/).",
                "Participate in [data analysis projects](https://www.kaggle.com/)."
            ],
            "Biochemistry": [
                "Engage in [biochemistry lab simulations](https://phet.colorado.edu/en/simulations/category/chemistry).",
                "Participate in [biochemistry workshops](https://www.eventbrite.com/d/online/biochemistry--workshops/)."
            ],
            "Law": [
                "Engage in [mock trials](https://www.americanbar.org/groups/public_education/resources/mock_trial/).",
                "Participate in [legal workshops and clinics](https://www.eventbrite.com/d/online/legal--workshops/)."
            ]
        },
        "Reading/Writing": {
            "Health Sciences": [
                "Study with [PDF guides and eBooks on health sciences](https://www.openstax.org/subjects/science).",
                "Read [health science articles and journals](https://www.ncbi.nlm.nih.gov/pmc/)."
            ],
            "Computer Sciences": [
                "Read [programming books and eBooks](https://www.oreilly.com/library/view/).",
                "Explore [documentation and written tutorials](https://www.w3schools.com/)."
            ],
            "Humanities": [
                "Read [historical texts and eBooks](https://www.gutenberg.org/).",
                "Explore [academic papers and articles](https://www.jstor.org/)."
            ],
            "Art": [
                "Read [art theory books](https://www.goodreads.com/shelf/show/art-theory).",
                "Explore [written art tutorials](https://www.drawing-tutorials-online.com/)."
            ],
            "Politics": [
                "Read [political science books](https://www.goodreads.com/shelf/show/political-science).",
                "Explore [policy papers and articles](https://www.brookings.edu/)."
            ],
            "Agriculture": [
                "Read [agriculture guides and eBooks](https://www.openstax.org/subjects/science).",
                "Explore [articles on sustainable farming](https://www.sciencedirect.com/journal/agriculture-and-sustainable-development)."
            ],
            "Statistics": [
                "Read [statistics textbooks and eBooks](https://www.openintro.org/).",
                "Explore [academic papers on statistics](https://www.jstor.org/)."
            ],
            "Biochemistry": [
                "Read [biochemistry textbooks](https://www.ncbi.nlm.nih.gov/books/NBK21154/).",
                "Explore [research papers on biochemistry](https://www.sciencedirect.com/journal/biochemistry)."
            ],
            "Law": [
                "Read [law textbooks and case studies](https://www.oxfordlawtrove.com/).",
                "Explore [legal journals and articles](https://heinonline.org/)."
            ]
        }
    }

    if dominant_style in resources and course in resources[dominant_style]:
        st.subheader(f"Recommended Resources for {course} ({dominant_style} Learner):")
        for resource in resources[dominant_style][course]:
            st.write(f"- {resource}")
    else:
        st.write("Sorry, we don't have specific resources for this course yet. Please try another course.")

# Define the homepage content
def home():
    st.title("Welcome to the Learning Style Assessment App")
    st.write("""
        This app helps you identify your dominant learning style and provides tailored resources for the course you are studying.
        Use the navigation menu on the left to access different pages.
    """)
    st.image("homepage-image.jpg")  # Add a relevant image if needed

# Define the about page content
def about():
    st.title("About This App")
    st.write("""
        This Learning Style Assessment App was created to help students identify their preferred learning style 
        and access resources tailored to their learning preferences. By understanding how you learn best, you 
        can optimize your study habits and improve your educational experience.
        
        This app covers various subjects and allows you to enter your course to get personalized recommendations. 
        Whether you're a visual learner who benefits from diagrams and videos, or an auditory learner who excels 
        with verbal explanations, you'll find resources here that match your style.
    """)
    st.image("about-image.jpg")  # Add a relevant image if needed

# Main app function
def main():
    st.sidebar.title("User Authentication")
    page = st.sidebar.selectbox("Choose a page", ["Login", "Register", "Main", "Home", "About"])

    if page == "Register":
        registration_page()
    elif page == "Login":
        login_page()
    elif page == "Main":
        main_app()
    elif page == "Home":
        home()
    elif page == "About":
        about()
    st.image("learn.jpg")

if __name__ == "__main__":
    if 'logged_in' not in st.session_state:
        st.session_state["logged_in"] = False
    main()
