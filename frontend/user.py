import streamlit as st
import pandas as pd
import pickle

# Define the Streamlit app function
def user():
    # Set Streamlit page configuration
    st.set_page_config(
        page_title="Your Custom Title",
        layout="wide",
    )
    # Initialize session state variables for signout
    if "signout" not in st.session_state:
        st.session_state.signout = False
    
    # Create a navigation bar with custom styling
    st.markdown(
        """
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
        <style>
            div.block-container {
                padding-top: 0 !important;
                padding-right: 0 !important;
                padding-left: 0 !important;
                }
            .st-emotion-cache-18ni7ap{
                display: none !important;
                padding:0 !important;
                }
            .navbar {
                background-color: #333;
            }
    
            .navbar a {
                color: #f2f2f2;
            }
    
            .navbar a:hover {
                background-color: #ddd;
                color: black;
            }
    
            .navbar a.active {
                background-color: #04AA6D;
                color: white;
            }
            .signout-btn {
                position: absolute;
                top: 8px;
                right: 8px;
                color: white;
                cursor: pointer;
                justify-content:center;
                align-items:center;
            }
            .logo{
                max-height: 10px;
                width: auto;
                height: auto;
                padding-top:0;
                align-items:center;
                }
        </style>
        <script>
            function signOut() {
                Streamlit.setComponentValue(true, "signout");
            }
        </script>
        <nav class="navbar navbar-expand-lg navbar-dark">
            <div class='logo'><img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSYQEN-P488zA8PbdEj3yS4nJSieq2jXDO2pUAX8KHOVke6LhASFKuuHHbekV1Sbjiqa9k&usqp=CAU" width="100" /></div>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav">
                    <li class="nav-item active">
                        <a class="nav-link" href="#">Home</a>
                    </li>
                </ul>
            </div>
            <div class="signout-btn" onclick="signOut()"><a class="nav-link">Sign Out</a></div>
        </nav>
        """,
        unsafe_allow_html=True,
    )
    
    # Create three columns for layout
    col1,col2,col3 = st.columns([2,2,2])
    
    # Using the second column for the form
    with col2:
        # Creating a form to collect user input
        with st.form("my_form"):
            #Heading to the form
           st.write("<h3 style='color: black;'>Please fill this form to analyze your Mental health!</h3>", unsafe_allow_html=True)
           
           #Age field
           Age = st.number_input("Age", min_value=0, max_value=100)
           
           #Gender field
           Gender = st.selectbox("Gender:",["Male","Female","Others"],index=None)
           
           #The country that the employee reside in or he works in
           Country = st.selectbox("Country:",['United States', 'Canada', 'United Kingdom', 'Bulgaria', 'France',
           'Portugal', 'Netherlands', 'Switzerland', 'Poland', 'Australia',
           'Germany', 'Russia', 'Mexico', 'Brazil', 'Slovenia', 'Costa Rica',
           'Austria', 'Ireland', 'India', 'South Africa', 'Italy', 'Sweden',
           'Colombia', 'Latvia', 'Romania', 'Belgium', 'New Zealand',
           'Zimbabwe', 'Spain', 'Finland', 'Uruguay', 'Israel',
           'Bosnia and Herzegovina', 'Hungary', 'Singapore', 'Japan',
           'Nigeria', 'Croatia', 'Norway', 'Thailand', 'Denmark',
           'Bahamas, The', 'Greece', 'Moldova', 'Georgia', 'China',
           'Czech Republic', 'Philippines', 'United States of America',
           'Serbia', 'Ukraine', 'Estonia', 'Mauritius', 'Saudi Arabia',
           'Kenya', 'Bangladesh', 'Ethiopia', 'Macedonia', 'Iceland',
           'Hong Kong', 'Turkey', 'Lithuania', 'Venezuela', 'Argentina',
           'Vietnam', 'Slovakia', 'Algeria', 'Pakistan', 'Afghanistan',
           'Other', 'Brunei', 'Iran', 'Ecuador', 'Chile', 'Guatemala',
           'Taiwan', 'Indonesia', 'Jordan', 'Belarus','Ghana'],index = None)
           
           #this indicated is the employee self-employed or not
           self_employed = st.radio("Are you employed: ",["Yes","No"],index = None)
           
           #This says If the employee has a mental health condition, asks if he feel that it interferes with your work?
           work_interfere = st.radio("If you have a mental health condition, do you feel that it interferes with your work?",["Yes","No"],index = None)
           

           # Question about the nature of the employer (tech or non-tech)
           tech_company = st.selectbox("Is your employer primarily a tech company/organization?", ["Yes", "No"], index=None)
            
            # Question about whether the employer provides mental health benefits
           mental_health_benefits = st.selectbox("Does your employer provide mental health benefits?", ["Yes", "No"], index=None)
            
            # Question about whether the employer provides resources for mental health support
           resources_to_help = st.selectbox("Does your employer provide resources to learn more about mental health issues and how to seek help?", ["Yes", "No"], index=None)
            
            # Question about the ease of taking medical leave for a mental health condition
           leave = st.selectbox("How easy is it for you to take medical leave for a mental health condition?", ["easy", "medium", "difficult"], index=None)
            
            # Question about willingness to discuss a mental health issue with coworkers
           coworkers = st.selectbox("Would you be willing to discuss a mental health issue with your coworkers?", ["Yes", "No", "May be"], index=None)
            
            # Question about willingness to discuss a mental health issue with direct supervisors
           supervisor = st.selectbox("Would you be willing to discuss a mental health issue with your direct supervisor(s)?", ["Yes", "No", "May be"], index=None)
            
            # Question about the perception of employer's seriousness about mental health compared to physical health
           mental_vs_physical = st.selectbox("Do you feel that your employer takes mental health as seriously as physical health?", ["Yes", "No", "Equal"], index=None)
            
            # Question about family history of mental illness
           family_history = st.selectbox("Do you have a family history of mental illness?", ["Yes", "No"], index=None)
            
            # Question about bringing up a mental health issue in a job interview
           mental_health_interview = st.selectbox("Would you bring up a mental health issue with a potential employer in an interview?", ["Yes", "No", "May be"], index=None)
            
            # Question about bringing up a physical health issue in a job interview
           physical_health_interview = st.selectbox("Would you bring up a physical health issue with a potential employer in an interview?", ["Yes", "No", "May be"], index=None)

           #submit button to the form
           submitted = st.form_submit_button("Submit")
           
           # Handle form submission
           if submitted:
               # Validate that all fields are filled or not
               if not Age or not Gender or not Country or not self_employed or not work_interfere or not tech_company \
                   or not mental_health_benefits or not resources_to_help or not leave or not coworkers \
                       or not supervisor or not mental_vs_physical or not family_history:
                           st.error("Please fill in all the fields before submitting.")
               elif submitted:
                   # Process the user input and make predictions
                   data = {
                    "Age": [Age],
                    "Gender": [Gender],
                    "Country": [Country],
                    "self_employed": [self_employed],
                    "work_interfere": [work_interfere],
                    "tech_company": [tech_company],
                    "mental_health_benefits": [mental_health_benefits],
                    "resources_to_help": [resources_to_help],
                    "leave": [leave],
                    "coworkers": [coworkers],
                    "supervisor": [supervisor],
                    "mental_vs_physical": [mental_vs_physical],
                    "family_history": [family_history],
                    "mental_health_interview": [mental_health_interview],
                    "physical_health_interview": [physical_health_interview]
                }
                   #Taking the user input and converting into a dataframe
                   dataset = pd.DataFrame(data)
                   
                   # Encode categorical variables
                   dataset[['work_interfere', 'tech_company', 'mental_health_benefits', 'resources_to_help', 'leave', 'coworkers', 'supervisor', 'family_history', 'mental_health_interview', 'physical_health_interview', 'Country','self_employed','mental_vs_physical','Gender',]] = dataset[['work_interfere', 'tech_company', 'mental_health_benefits', 'resources_to_help', 'leave', 'coworkers', 'supervisor', 'family_history', 'mental_health_interview', 'physical_health_interview', 'Country','self_employed','mental_vs_physical','Gender']].apply(lambda x: pd.factorize(x)[0])
                   dataset[['Gender','work_interfere', 'tech_company', 'mental_health_benefits', 'resources_to_help', 'leave', 'coworkers', 'supervisor', 'family_history', 'mental_health_interview', 'physical_health_interview', 'Country','self_employed','mental_vs_physical',]]= dataset[['Gender','work_interfere', 'tech_company', 'mental_health_benefits', 'resources_to_help', 'leave', 'coworkers', 'supervisor', 'family_history', 'mental_health_interview', 'physical_health_interview', 'Country','self_employed','mental_vs_physical']].apply(lambda x: x.astype('category'))
                   
                   # Load the pre-trained machine learning model(Voting classifier which is used in Phase 2)
                   with open('model_1.pkl', 'rb') as file:
                       loaded_model = pickle.load(file)
                   
                   # Make predictions using the model 
                   y_test = loaded_model.predict(dataset)
                   
                   # Display the result based on predictions
                   if y_test == 1:
                       #if the user needs treatment then giving suggestions to necessary websites
                       st.write("Sorry to say this, we think you might need some treatment regarding your mental health")
                       st.markdown("Here are some resources for mental health support:")
                       st.markdown("- [Mental Health Association](https://www.mentalhealthassociation.org/)", unsafe_allow_html=True)
                       st.markdown("- [World Health Organization](https://www.who.int/)",unsafe_allow_html=True)
                       st.markdown("- [United for Global Mental Health](https://unitedgmh.org/)", unsafe_allow_html=True)
                       st.markdown("- [American Psychiatric Association](https://www.psychiatry.org/psychiatrists/international/global-mental-health)",unsafe_allow_html=True)
                   #If he is not mentally ill then saying he is perfect
                   if y_test == 0:
                       st.write("Hurray! You are all set")
    # Handling signout
    if st.session_state.signout:
        # Clear the signout state
        st.session_state.signout = False
        # Rerun the app to handle the signout
        st.experimental_rerun()
