import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def app():
    """
    Streamlit web application for displaying machine learning results and personalized suggestions.
    
    The application is divided into two main sections:
    1. 'Results': Displays predictions from a machine learning model and provides personalized suggestions.
    2. 'EDA': Performs exploratory data analysis on a preprocessed dataset and visualizes relevant insights.
    
    The page layout is set to 'wide' with a custom title.

    """
    st.set_page_config(
        page_title="Your Custom Title",
        layout="wide",
    )
    
    def results():
        """
        Section that reads a preprocessed dataset, applies a machine learning model, and visualizes predictions.
        
        - Reads the preprocessed dataset from a CSV file.
        - Encodes categorical variables using factorization.
        - Drops unnecessary columns.
        - Loads a pre-trained machine learning model from a pickle file.
        - Predicts outcomes and visualizes the results using a bar chart.
        - Provides personalized suggestions based on the predictions.
        
        """
        # Reading the preprocessed dataset that was obtained after uploading
        dataset = pd.read_csv("preprocessed_dataset.csv")
        
        # Encode categorical variables using factorization
        dataset[['work_interfere', 'tech_company', 'mental_health_benefits', 'resources_to_help', 'leave', 'coworkers', 'supervisor', 'family_history', 'mental_health_interview', 'physical_health_interview', 'Country','self_employed','mental_vs_physical','Gender',]] = dataset[['work_interfere', 'tech_company', 'mental_health_benefits', 'resources_to_help', 'leave', 'coworkers', 'supervisor', 'family_history', 'mental_health_interview', 'physical_health_interview', 'Country','self_employed','mental_vs_physical','Gender']].apply(lambda x: pd.factorize(x)[0])
        dataset[['Gender','work_interfere', 'tech_company', 'mental_health_benefits', 'resources_to_help', 'leave', 'coworkers', 'supervisor', 'family_history', 'mental_health_interview', 'physical_health_interview', 'Country','self_employed','mental_vs_physical',]]= dataset[['Gender','work_interfere', 'tech_company', 'mental_health_benefits', 'resources_to_help', 'leave', 'coworkers', 'supervisor', 'family_history', 'mental_health_interview', 'physical_health_interview', 'Country','self_employed','mental_vs_physical']].apply(lambda x: x.astype('category'))
        
        # Drop unnecessary columns
        dataset = dataset.drop(columns = ["total_employees","Age-Group","year"])
        
        # Load the machine learning model(Voting classifer)
        with open('model_1.pkl', 'rb') as file:
            loaded_model = pickle.load(file)
        
        # Making predictions
        y_test = loaded_model.predict(dataset)
        
        # Visualize predictions using a bar chart
        fig, ax = plt.subplots(figsize=(3, 3))
        counts = np.bincount(y_test)
        labels = ["no treatment", "treatment"]
        ax.bar(labels, counts[:2], color=['skyblue', 'salmon'])
        ax.set_xlabel('Predictions', fontsize=7)
        ax.set_ylabel('Count', fontsize=7)
        ax.tick_params(axis='both', labelsize=12)
        st.pyplot(fig)
        
        # Display personalized suggestions based on predictions
        if counts[1] > counts[0]:
            st.write("Based on the analysis, it seems that there is a higher likelihood of individuals needing treatment regarding their mental health.")
            st.markdown("Here are some personalized suggestions:")
            st.markdown("- Consider providing mental health resources and support within the workplace.")
            st.markdown("- Offer workshops or sessions on stress management and well-being.")
            st.markdown("- Encourage an open dialogue about mental health to reduce stigma.")
        else:
            st.write("It appears that individuals in the dataset may not require immediate treatment.")
    
    def eda():
        """
        Section for Exploratory Data Analysis (EDA).
        
        - Reads a preprocessed dataset from a CSV file.
        - Allows the user to select a graph type using a Streamlit selectbox.
        - Generates and visualizes the selected graph using Seaborn and Matplotlib.
        - Provides suggestions based on the counts in the generated graph.
        
        """
        # Read the preprocessed dataset
        dataset = pd.read_csv("preprocessed_dataset.csv")
        
        # User selects the type of graph using a selectbox
        option = st.selectbox("Select a graph:",["work interference vs resources to help","Coworkers vs. Supervisor","mental_health_benefits vs. mental_vs_physical","leave vs mental_vs_physical"],index=None)
        
        # Condition based on the selected graph type
        if option == "work interference vs resources to help":
            # Create a subplot for the count plot
            fig, ax = plt.subplots(figsize=(8, 6))
            plt.xticks(rotation=45, ha="right")
            
            # Generate a count plot for 'work interference' vs 'resources to help'
            sns.countplot(x="work_interfere", hue="resources_to_help", data=dataset, ax=ax, palette="Set1")
            
            # Set labels and title for the plot
            ax.set_title("Work Interference vs. Access to Mental Health Resources")
            ax.set_xlabel("Work Interference")
            ax.set_ylabel("Count")
            ax.tick_params(axis='both', labelsize=12)
            st.pyplot(fig)
            
            # Calculate counts based on 'work_interfere' and 'resources_to_help'
            counts = dataset.groupby(['work_interfere', 'resources_to_help']).size().unstack(fill_value=0)
            # Provide suggestions based on the counts
            if counts.loc['Yes', 'Yes'] > counts.loc['No', 'Yes']:
                st.write("Employees who are facing challenges with work interference and have access to resources for assistance may find value in receiving targeted support and intervention.")
                st.write("Suggestion: Consider organizing additional mental health workshops or providing easily accessible resources.")
            elif counts.loc['No', 'Yes'] > counts.loc['Yes', 'Yes']:
                st.write("Employees not experiencing 'Work Interference' but with access to resources for help may be proactively seeking support.")
                st.write("Suggestion: Maintain a supportive environment and consider periodic check-ins.")
            else:
                st.write("The distribution of employees facing 'Work Interference' and having access to resources is balanced.")
                st.write("No specific action is immediately recommended based on the current analysis.")
        
        # Check if the user selected "Coworkers vs. Supervisor" from the dropdown options
        elif option == "Coworkers vs. Supervisor":
            
            # Create a subplot for the count plot with a specified size
            fig, ax = plt.subplots(figsize=(8, 6))
            # Generate a count plot for 'coworkers' vs 'supervisor' using Seaborn
            sns.countplot(x="coworkers", hue="supervisor", data=dataset, ax=ax, palette="Set2")
            
            # Set title and labels for the plot
            ax.set_title("Coworkers vs. Supervisor")
            ax.set_xlabel("Coworkers")
            ax.set_ylabel("Count")
            ax.tick_params(axis='both', labelsize=12)
            st.pyplot(fig)
            
            # Subheader for suggestions based on the 'Maybe' section of the 'coworkers' variable
            st.subheader("Suggestions based on the maybe section of the coworkers:")
            # Count the occurrences of different combinations of 'coworkers' and 'supervisor'
            coworkers_maybe_supervisor_yes_count = dataset[(dataset['coworkers'] == 'Maybe') & (dataset['supervisor'] == 'Yes')].shape[0]
            coworkers_maybe_supervisor_no_count = dataset[(dataset['coworkers'] == 'Maybe') & (dataset['supervisor'] == 'No')].shape[0]
            coworkers_maybe_supervisor_maybe_count = dataset[(dataset['coworkers'] == 'Maybe') & (dataset['supervisor'] == 'Maybe')].shape[0]
        
            # Compare the counts and provide a suggestion
            if coworkers_maybe_supervisor_yes_count > coworkers_maybe_supervisor_no_count and coworkers_maybe_supervisor_yes_count > coworkers_maybe_supervisor_maybe_count:
                st.write("Employees who are uncertain about discussing mental health with coworkers but are open to it with supervisors may benefit from targeted awareness programs. Highlight the importance of peer support and provide resources for mental health initiatives.")
        
            elif coworkers_maybe_supervisor_no_count > coworkers_maybe_supervisor_yes_count and coworkers_maybe_supervisor_no_count > coworkers_maybe_supervisor_maybe_count:
                st.write("Employees who are uncertain about discussing mental health with both coworkers and supervisors may require a more comprehensive approach. Consider implementing workshops or training sessions to foster a workplace culture that encourages open communication about mental health.")
        
            elif coworkers_maybe_supervisor_maybe_count > coworkers_maybe_supervisor_yes_count and coworkers_maybe_supervisor_maybe_count > coworkers_maybe_supervisor_no_count:
                st.write("Some employees are uncertain about discussing mental health with both coworkers and supervisors. It's essential to address workplace stigma around mental health. Implement initiatives to create a supportive environment and provide resources for seeking help.")
            
            # Subheader for suggestions based on the 'Yes' section of the 'coworkers' variable
            st.subheader("Suggestions based on the yes section of the coworkers:")
            # Count the occurrences of different combinations of 'coworkers' and 'supervisor'
            coworkers_yes_supervisor_yes_count = dataset[(dataset['coworkers'] == 'Yes') & (dataset['supervisor'] == 'Yes')].shape[0]
            coworkers_yes_supervisor_no_count = dataset[(dataset['coworkers'] == 'Yes') & (dataset['supervisor'] == 'No')].shape[0]
            coworkers_yes_supervisor_maybe_count = dataset[(dataset['coworkers'] == 'Yes') & (dataset['supervisor'] == 'Maybe')].shape[0]
        
            # Compare the counts and provide a suggestion
            if coworkers_yes_supervisor_yes_count > coworkers_yes_supervisor_no_count and coworkers_yes_supervisor_yes_count > coworkers_yes_supervisor_maybe_count:
                st.write("Employees comfortable discussing mental health with both coworkers and supervisors contribute to a positive workplace culture. Encourage them to share their experiences and insights during team meetings, fostering an environment of mutual support.")
        
            elif coworkers_yes_supervisor_no_count > coworkers_yes_supervisor_yes_count and coworkers_yes_supervisor_no_count > coworkers_yes_supervisor_maybe_count:
                st.write("Some employees are comfortable discussing mental health with coworkers but not with supervisors. Implement initiatives to bridge this gap, such as organizing workshops to enhance supervisor-employee relationships and communication around mental health.")
        
            elif coworkers_yes_supervisor_maybe_count > coworkers_yes_supervisor_yes_count and coworkers_yes_supervisor_maybe_count > coworkers_yes_supervisor_no_count:
                st.write("Certain employees are comfortable discussing mental health with coworkers but uncertain about it with supervisors. Provide resources and training to supervisors to create an open and supportive environment, encouraging employees to discuss mental health concerns.")
            
            # Subheader for suggestions based on the 'No' section of the 'coworkers' variable
            st.subheader("Suggestions based on the no section of the coworkers:")
            # Count the occurrences of different combinations of 'coworkers' and 'supervisor'
            coworkers_no_supervisor_yes_count = dataset[(dataset['coworkers'] == 'No') & (dataset['supervisor'] == 'Yes')].shape[0]
            coworkers_no_supervisor_no_count = dataset[(dataset['coworkers'] == 'No') & (dataset['supervisor'] == 'No')].shape[0]
            coworkers_no_supervisor_maybe_count = dataset[(dataset['coworkers'] == 'No') & (dataset['supervisor'] == 'Maybe')].shape[0]

            # Compare the counts and provide a suggestion
            if coworkers_no_supervisor_yes_count > coworkers_no_supervisor_no_count and coworkers_no_supervisor_yes_count > coworkers_no_supervisor_maybe_count:
                st.write("For employees not comfortable discussing mental health with coworkers but open to discussions with supervisors, consider implementing mentorship programs. Pair them with supportive supervisors who can provide guidance and foster a sense of trust.")

            elif coworkers_no_supervisor_no_count > coworkers_no_supervisor_yes_count and coworkers_no_supervisor_no_count > coworkers_no_supervisor_maybe_count:
                st.write("If employees are not comfortable discussing mental health with both coworkers and supervisors, consider organizing confidential support sessions. These can provide a safe space for employees to share their concerns and access resources without fear of judgment.")

            elif coworkers_no_supervisor_maybe_count > coworkers_no_supervisor_yes_count and coworkers_no_supervisor_maybe_count > coworkers_no_supervisor_no_count:
                st.write("Certain employees are not comfortable discussing mental health with coworkers and are uncertain about it with supervisors. Implement awareness programs to destigmatize mental health discussions in the workplace and encourage open conversations.")
        
        elif option=="mental_health_benefits vs. mental_vs_physical":
            # Define the order of categories for 'mental_health_benefits' and 'mental_vs_physical'
            mental_health_benefits_categories = ['No', 'Yes']
            mental_vs_physical_categories = ['No', 'Yes', 'Equal']
            # Define the order of categories for 'mental_health_benefits' and 'mental_vs_physical'
            dataset['mental_health_benefits'] = pd.Categorical(dataset['mental_health_benefits'], categories=mental_health_benefits_categories, ordered=True)
            dataset['mental_vs_physical'] = pd.Categorical(dataset['mental_vs_physical'], categories=mental_vs_physical_categories, ordered=True)
            # Create a crosstab to analyze the relationship between 'mental_health_benefits' and 'mental_vs_physical'
            crosstab = pd.crosstab(dataset['mental_health_benefits'], dataset['mental_vs_physical'])
            
            # Create a subplot for the heatmap with a specified size
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.heatmap(crosstab, annot=True, fmt='d', cmap='viridis', ax=ax)
            ax.set_xlabel("Mental vs Physical")
            ax.set_ylabel("Mental Health Benefits")
            ax.set_title("Mental Health Benefits vs Mental vs Physical (Heatmap)")
            st.pyplot(fig)
            
            # Subheader for suggestions based on the comparison
            st.subheader("Suggestions based on the comparison:")
        
            # Extract counts from crosstab
            no_mental_health_benefits = crosstab.loc['No'].sum()
            yes_mental_health_benefits = crosstab.loc['Yes'].sum()
        
            no_mental_vs_physical = crosstab['No'].sum()
            yes_mental_vs_physical = crosstab['Yes'].sum()
            equal_mental_vs_physical = crosstab['Equal'].sum()
        
            # Compare the counts and provide suggestions
            if yes_mental_health_benefits > no_mental_health_benefits:
                st.write("The heatmap suggests that employees with mental health benefits are more likely to consider mental health as important as physical health. Consider expanding mental health benefit programs and raising awareness about their availability.")
        
            if yes_mental_vs_physical > no_mental_vs_physical and yes_mental_vs_physical > equal_mental_vs_physical:
                st.write("Employees who consider mental health as important as physical health are more likely to have mental health benefits. Reinforce the importance of mental well-being in the workplace and promote available mental health resources.")
            if equal_mental_vs_physical > no_mental_vs_physical and equal_mental_vs_physical > yes_mental_vs_physical:
                st.write("There is a significant number of employees who view mental health as equal to physical health but may not have mental health benefits. Consider evaluating the accessibility and awareness of mental health resources for this group.")

            if no_mental_vs_physical > yes_mental_vs_physical and no_mental_vs_physical > equal_mental_vs_physical:
                st.write("Employees who do not consider mental health as important as physical health may benefit from awareness campaigns and education on the importance of mental well-being in the workplace.")
        # Check if the user selected "leave vs mental_vs_physical" from the dropdown options
        elif option == "leave vs mental_vs_physical":
            # Factorize categorical columns to numeric values for analysis
            dataset[['work_interfere', 'tech_company', 'mental_health_benefits', 'resources_to_help', 'leave', 'coworkers', 'supervisor', 'family_history', 'mental_health_interview', 'physical_health_interview', 'Country','self_employed','mental_vs_physical','Gender',]] = dataset[['work_interfere', 'tech_company', 'mental_health_benefits', 'resources_to_help', 'leave', 'coworkers', 'supervisor', 'family_history', 'mental_health_interview', 'physical_health_interview', 'Country','self_employed','mental_vs_physical','Gender']].apply(lambda x: pd.factorize(x)[0])
            dataset[['Gender','work_interfere', 'tech_company', 'mental_health_benefits', 'resources_to_help', 'leave', 'coworkers', 'supervisor', 'family_history', 'mental_health_interview', 'physical_health_interview', 'Country','self_employed','mental_vs_physical',]]= dataset[['Gender','work_interfere', 'tech_company', 'mental_health_benefits', 'resources_to_help', 'leave', 'coworkers', 'supervisor', 'family_history', 'mental_health_interview', 'physical_health_interview', 'Country','self_employed','mental_vs_physical']].apply(lambda x: x.astype('int'))
            # Create a violin plot to compare 'leave' and 'mental_vs_physical'
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.violinplot(x='leave', y='mental_vs_physical', data=dataset, ax=ax, palette='viridis')
    
            # Set labels and title
            ax.set_xlabel("Leave")
            ax.set_ylabel("Mental vs Physical Health")
            ax.set_title("Violin Plot: Leave vs Mental vs Physical Health")
    
            # Display the plot in Streamlit
            st.pyplot(fig)
            # Subheader for suggestions based on the comparison
            st.subheader("Suggestions based on the comparison:")

            # Extract counts from the dataset for different leave categories
            easy_leave_count = dataset[dataset['leave'] == 0]['leave'].count()
            medium_leave_count = dataset[dataset['leave'] == 1]['leave'].count()
            difficult_leave_count = dataset[dataset['leave'] == 2]['leave'].count()
        
            # Compare the counts and provide suggestions
            if easy_leave_count > medium_leave_count and easy_leave_count > difficult_leave_count:
                st.write(
                    "Employees who find it easy to take medical leave for a mental health condition are more likely to consider mental health as important as physical health. "
                    "Ensure that the ease of taking leave is communicated effectively and encourage employees to utilize mental health resources."
                )
            
                # Reasoning
                st.markdown("### Reasoning:")
                st.markdown(
                    "The data suggests that a significant proportion of employees find it easy to take medical leave for mental health reasons. "
                    "This is positive, as employees who perceive it as easy may already feel supported in prioritizing their mental well-being. "
                    "By reinforcing the importance of mental health resources, you can further encourage them to make use of available support."
                )
            
            if medium_leave_count > easy_leave_count and medium_leave_count > difficult_leave_count:
                st.write(
                    "Employees who find it moderately easy to take medical leave may benefit from additional support in understanding and accessing mental health resources. "
                    "Consider providing informational sessions and making resources easily accessible."
                )
            
                # Reasoning
                st.markdown("### Reasoning:")
                st.markdown(
                    "The data indicates that a considerable number of employees find it moderately easy to take medical leave for mental health reasons. "
                    "This group may be open to seeking mental health support but might need more information or improved accessibility. "
                    "By offering informational sessions and ensuring easy access to resources, you can enhance their engagement with mental health services."
                )
            
            if difficult_leave_count > easy_leave_count and difficult_leave_count > medium_leave_count:
                st.write(
                    "Employees who find it difficult to take medical leave for a mental health condition may need targeted interventions to address barriers. "
                    "Explore ways to streamline the leave application process and raise awareness about the importance of mental well-being."
                )
            
                # Reasoning
                st.markdown("### Reasoning:")
                st.markdown(
                    "The data highlights that some employees find it difficult to take medical leave for mental health reasons. "
                    "This may indicate the presence of systemic barriers that need attention. By streamlining the leave application process and promoting awareness, "
                    "you can contribute to a more inclusive and supportive workplace for mental health."
                )
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
        <nav class="navbar navbar-expand-lg navbar-dark">
            <div class='logo'><img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSYQEN-P488zA8PbdEj3yS4nJSieq2jXDO2pUAX8KHOVke6LhASFKuuHHbekV1Sbjiqa9k&usqp=CAU" width="100" /></div>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav">
                    <li class="nav-item active">
                        <a class="nav-link" href="#">Home</a>
                    </li>
                </ul>
            </div>
            <div class="signout-btn" onclick="signOut()"><a class="nav-link" href="http://localhost:8501/#"">Sign Out</a></div>
        </nav>
        """,
        unsafe_allow_html=True,
    )
    
    # HTML style to center the file uploader and add some styling
    center_file_uploader_style = """
        <style>
            div[data-testid="stFileUploader"] {
                display: flex;
                flex-direction: column;
                align-items: center;
                width: 200vh;
            }
            .upload-btn, .read-btn, .analysis-btn{
                display: inline-block;
                padding: 10px 5px;
                background-color: #4CAF50;
                color: white;
                text-align: center;
                text-decoration: none;
                font-size: 16px;
                cursor: pointer;
                justify-content:center;
                align-items:center;
                border-radius: 8px;
                }
            .st-emotion-cache-900wwq{
                display:flex
                flex-direction: row;
                justify-content:center;
                align-items:center;
                padding-top: 30px;
                }
    
        </style>
    """
    # Apply the HTML style to center the file uploader
    st.markdown(center_file_uploader_style, unsafe_allow_html=True)
    # File uploader widget to upload a CSV file
    dataset = st.file_uploader("Upload your file here", type=["csv"])
    # Creating columns for buttons and layout
    col1, col2, col3,col4,col5 = st.columns([2,1,1,2,2])
    
    # Button to upload the file
    with col2:
        upload_button = st.button("Upload", key = "upload-btn",help="Click to upload the file")
    # Button to read the file
    with col3:
        read_button = st.button("Read File", key="read-btn", help="Click to read the file")
    # Dropdown to select the type of analysis (Results or EDA)
    with col4:
        analize_button = st.selectbox(label="Select Analysis:", options=["Results", "EDA"],index=None)
    
    # Columns for displaying analysis results or EDA based on the selected option
    col1,col2,col3 = st.columns([2,2,2])
    
    # Perform the selected analysis when the user clicks the button
    with col2:
        if analize_button == "Results":
            results()
        if analize_button == "EDA":
            eda()
    # Read and display the CSV file if the user clicks the "Read File" button
    if read_button and dataset is not None:
            df = pd.read_csv(dataset)
            st.dataframe(df)
    if upload_button:
        # Read the uploaded dataset into a pandas DataFrame
            dataset = pd.read_csv(dataset)
            
            # Rename columns for consistency and clarity
            dataset.rename(
            columns={"Are you self-employed?": "self_employed",
                      "If you have a mental health condition, do you feel that it interferes with your work?": "work_interfere",
                    "How many employees does your company or organization have?": "total_employees",
                    "Is your employer primarily a tech company/organization?":"tech_company",
                    "Does your employer provide mental health benefits?":"mental_health_benefits",
                    "Does your employer provide resources to learn more about mental health issues and how to seek help?":"resources_to_help",
                    "How easy is it for you to take medical leave for a mental health condition?":"leave",
                    "Would you be willing to discuss a mental health issue with your coworkers?":"coworkers",
                    "Would you be willing to discuss a mental health issue with your direct supervisor(s)?" : "supervisor",
                    "Do you feel that your employer takes mental health as seriously as physical health?":"mental_vs_physical",
                    "Do you have a family history of mental illness?":"family_history",
                    "Would you bring up a mental health issue with a potential employer in an interview?":"mental_health_interview",
                    "Would you bring up a physical health issue with a potential employer in an interview?":"physical_health_interview"},
            inplace=True,
                    )
            # Drop duplicate rows from the dataset
            dataset = dataset.drop_duplicates()
            # Drop rows with missing values in specific columns
            dataset = dataset.dropna(subset=["Age","Gender","Country","self_employed"])
            # Reset the index after dropping rows
            dataset = dataset.reset_index(drop=True)
            # Convert all string values to lowercase
            dataset = dataset.apply(lambda x: x.lower() if isinstance(x, str) else x)
           
            #Changing the string formates of each column
            dataset["work_interfere"].fillna('', inplace=True)
            dataset.loc[dataset["work_interfere"].str.contains('sometimes|often|rarely|unsure' ,case=False, regex=True), 'work_interfere'] = 'Sometimes'
            dataset.loc[dataset["work_interfere"].str.contains('yes' ,case=False, regex=True), 'work_interfere'] = 'Yes'
            dataset.loc[dataset["work_interfere"].str.contains('no|never' ,case=False, regex=True), 'work_interfere'] = 'No'
            
            dataset["tech_company"].fillna('', inplace=True)
            dataset.loc[dataset["tech_company"].str.contains('yes|1|true' ,case=False, regex=True), 'tech_company'] = 'Yes'
            dataset.loc[dataset["tech_company"].str.contains('no|false|0' ,case=False, regex=True), 'tech_company'] = 'No'
            
            dataset["mental_health_benefits"].fillna('', inplace=True)
            dataset.loc[dataset["mental_health_benefits"].str.contains('yes' , case=False,regex=True), 'mental_health_benefits'] = 'Yes'
            dataset.loc[dataset["mental_health_benefits"].str.contains("no|don't know|not eligible for coverage / na|i don't know|not eligible for coverage / n/a" ,case=False, regex=True), 'mental_health_benefits'] = 'No'
            
            dataset["resources_to_help"].fillna('', inplace=True)
            dataset.loc[dataset["resources_to_help"].str.contains('yes' ,case=False, regex=True), 'resources_to_help'] = 'Yes'
            dataset.loc[dataset["resources_to_help"].str.contains("no|i don't know|don't know" ,case=False, regex=True), 'resources_to_help'] = 'No'
            
            dataset["leave"].fillna('', inplace=True)
            dataset.loc[dataset["leave"].str.contains('somewhat easy|very easy' ,case=False, regex=True), 'leave'] = 'easy'
            dataset.loc[dataset["leave"].str.contains("neither easy nor difficult|don't know|i don't know" ,case=False, regex=True), 'leave'] = 'medium'
            dataset.loc[dataset["leave"].str.contains("somewhat difficult|very difficult|difficult" ,case=False, regex=True), 'leave'] = 'difficult'
            
            dataset["coworkers"].fillna('', inplace=True)
            dataset.loc[dataset["coworkers"].str.contains('some of them|maybe' ,case=False, regex=True), 'coworkers'] = 'Maybe'
            dataset.loc[dataset["coworkers"].str.contains('yes' ,case=False, regex=True), 'coworkers'] = 'Yes'
            dataset.loc[dataset["coworkers"].str.contains('no' ,case=False, regex=True), 'coworkers'] = 'No'
            
            dataset["supervisor"].fillna('', inplace=True)
            dataset.loc[dataset["supervisor"].str.contains("some of them|maybe|some of my previous supervisors|i don't know" ,case=False, regex=True), 'supervisor'] = 'Maybe'
            dataset.loc[dataset["supervisor"].str.contains('yes|yes, all of my previous supervisors' ,case=False, regex=True), 'supervisor'] = 'Yes'
            dataset.loc[dataset["supervisor"].str.contains('no|no, none of my previous supervisors' ,case=False, regex=True), 'supervisor'] = 'No'
            
            dataset["mental_vs_physical"].fillna('', inplace=True)
            dataset.loc[dataset["mental_vs_physical"].str.contains("don't know|i don't know|Same level of comfort for each" ,case=False, regex=True), 'mental_vs_physical'] = 'Equal'
            dataset.loc[dataset["mental_vs_physical"].str.contains('yes|mental health' ,case=False, regex=True), 'mental_vs_physical'] = 'Yes'
            dataset.loc[dataset["mental_vs_physical"].str.contains('no|physical health' ,case=False, regex=True), 'mental_vs_physical'] = 'No'
            
            dataset.loc[dataset["Gender"].str.contains('them|trans|undecided|contextual|transgender|nb|unicorn|queer|nb|binary|enby|human|little|androgynous|androgyne|neutral|agender|fluid|genderFluid|enderflux|genderqueer' ,case=False, regex=True), 'Gender'] = 'Others'
            dataset.loc[dataset['Gender'].str.contains('female|woman|w|womail|cis female| female (cis)|cis Female|cis female|cis woman|f' ,case=False, regex=True), 'Gender'] = 'Female'
            cond1 = dataset['Gender']!='Female'
            cond2 = dataset['Gender']!='Others'
            dataset.loc[cond1 & cond2, 'Gender'] = 'Male'
            
            dataset.loc[dataset["self_employed"].str.contains('yes|true|1' ,case=False, regex=True), 'self_employed'] = 'Yes'
            dataset.loc[dataset["self_employed"].str.contains('no|0|false' ,case=False, regex=True), 'self_employed'] = 'No'
            
            dataset.loc[dataset["family_history"].str.contains('yes' ,case=False, regex=True), 'family_history'] = 'Yes'
            dataset.loc[dataset["family_history"].str.contains("no|i don't know",case=False, regex=True), 'family_history'] = 'No'
            
            dataset.loc[dataset["Country"].str.contains('united states of america|united states' ,case=False, regex=True), 'Country'] = 'united states'
            
            #outliers removal
            year = [2014,2016,2017,2018,2019]
            outliers = dataset[(dataset['year'] != 2014) & (dataset['year'] != 2016)&(dataset['year'] != 2017)&(dataset['year'] != 2018)&(dataset['year'] != 2019)]
            dataset = dataset.drop(outliers.index)
            
            #age outlier
            dataset['Age'] = dataset['Age'].astype(int)
            outliers_age = dataset[(dataset['Age'] <= 0)]
            dataset = dataset.drop(outliers_age.index)
            
            
            #age outliers
            outliers_age_2 = dataset[(dataset['Age'] > 100)]
            dataset = dataset.drop(outliers_age_2.index)
            dataset = dataset.reset_index(drop=True)
            
            mode_values = dataset.mode().iloc[0]
            dataset = dataset.apply(lambda col: col.replace("", mode_values[col.name]))
        
            #As there is one column in country which has a special character we are removing that
            dataset = dataset.drop(962)
            dataset = dataset.reset_index(drop=True)
            # Create a new column "Age-Group" by binning the 'Age' column
            dataset['Age-Group'] = pd.cut(dataset['Age'], [0, 20, 30, 40, 65, 100], labels=["0-20", "21-30", "31-40", "41-65", "66-100"], include_lowest=True)
            # Display the preprocessed dataset
            st.write("Your pre-processed file is: ")
            st.dataframe(dataset)
            
            # Save the preprocessed dataset to a new CSV file
            preprocessed_file_path = "preprocessed_dataset.csv"
            dataset.to_csv(preprocessed_file_path, index=False)
            st.success(f"Preprocessed dataset saved to {preprocessed_file_path}")
            
    
