import datetime
import uuid
import streamlit as st


from css import *
from generate_plan import *
from generate_creatives import *

@st.experimental_dialog("Processing", width="large")
def display_splash(item):
    with st.status("Talking to the Alkimist", expanded=False) as status:
        response_json = call_bedrock_llama3(item)
    if 'generation' in response_json:
        system_response = response_json['generation']
    else:
        system_response = "Error: 'generation' not found in the response."
    # status.update(label=system_response, state="complete", expanded=True)
    st.write(system_response)

@st.experimental_dialog("Processing", width = "large")
def creatives_splash(item):
    with st.status("Generating Creatives", expanded = True) as Status:
        image_dir = str(uuid.uuid4())
        st.write("Generating creative 1")
        store_image_1(item, image_dir)
        st.write("Generating creative 2")
        store_image_2(item, image_dir)
        st.write("Generating creative 3")
        store_image_3(item, image_dir)
        Status.update(label = "Generation complete", state = "complete", expanded=True)
        st.write("https://cannes-demo.s3.eu-west-2.amazonaws.com/alkimi-blog.html?ad-id="+image_dir)

def main():
    if 'new_session' not in st.session_state:
        st.session_state['new_session'] = True

    if st.session_state['new_session']:
        st.session_state['conversation_history'] = []
        st.session_state['uploaded_file'] = None
        st.session_state['Company_details'] = ""
        st.session_state['demographics'] = ""
        st.session_state['Min_Age'] = ""
        st.session_state['Max_Age'] = ""
        st.session_state['start_date'] = ""
        st.session_state['end_date'] = ""
        st.session_state['Bidding_amount'] = ""
        st.session_state['pdf_text'] = ""
        st.session_state['new_session'] = False

    title = '<h1 style="font-family:Impact; color:White; font-size: 58px; text-align: center; text-weight: bold ">ALKIMI INTELLIGENCE</h1>'
    st.markdown(title, unsafe_allow_html=True)
    st.markdown(page_bg_img, unsafe_allow_html=True)

    with st.container(border=True):
        title_company_details = '<p style="font-family:Impact; color:White; font-size: 20px; text-align: center; text-weight: bold ">Please type in some details about the product you want to advertise</p>'
        st.markdown(title_company_details, unsafe_allow_html=True)
        Company_details = st.text_area("", value=st.session_state['Company_details'],height=30, key='Company_details', placeholder="")

    with st.container(border=True):
        title_demographics_details = '<p style="font-family:Impact; color:White; font-size: 20px; text-align: center; text-weight: bold ">Please type in the locations</p>'
        st.markdown(title_demographics_details, unsafe_allow_html=True)
        demographics = st.selectbox(
            "Enter the geographical location",
            ("North America", "Europe", "Australia", "Asia", "South America", "Africa"),
            label_visibility = "collapsed"
        )

    with st.container(border=True):
        cols1, cols2 = st.columns([1, 1])
        with cols1:
            title_min_age_details = '<p style="font-family:Impact; color:White; font-size: 20px; text-align: center; text-weight: bold ">Minimum Age</p>'
            st.markdown(title_min_age_details, unsafe_allow_html=True)
            MinAge = st.selectbox(
                "Enter the minimum age",
                ("10", "20", "30", "40", "50+"),
                label_visibility = "collapsed"
            )

        with cols2:
            title_max_age_details = '<p style="font-family:Impact; color:White; font-size: 20px; text-align: center; text-weight: bold ">Maximum Age</p>'
            st.markdown(title_max_age_details, unsafe_allow_html=True)
            MaxAge = st.selectbox(
                "Enter the maximum age",
                ("10", "20", "30", "40", "50+"),
                label_visibility = "collapsed"
            )

    with st.container(border=True):
        cols_date1, cols_date2 = st.columns([1,1])
        with cols_date1:
            title_min_date_details = '<p style="font-family:Impact; color:White; font-size: 20px; text-align: center; text-weight: bold ">Start Date</p>'
            st.markdown(title_min_date_details, unsafe_allow_html=True)
            Start_Date = st.date_input("Start Date", value = datetime.date(2024,6,13 ), label_visibility = "collapsed")

        with cols_date2:
            title_max_date_details = '<p style="font-family:Impact; color:White; font-size: 20px; text-align: center; text-weight: bold ">End Date</p>'
            st.markdown(title_max_date_details, unsafe_allow_html=True)
            End_Date  = st.date_input("End Date", value = datetime.date(2024,6,13 ), label_visibility = "collapsed")

    with st.container(border=True): 
        title_bidding_details = '<p style="font-family:Impact; color:White; font-size: 20px; text-align: center; text-weight: bold ">Please Select the Campaign Budget</p>'
        st.markdown(title_bidding_details, unsafe_allow_html=True)  
        #Bidding_amount = st.text_input("", value=st.session_state['Bidding_amount'], key='Bidding_amount', placeholder="Please Select the Campaign Budget for your ad")
        Bidding_amount = st.selectbox(
            "Enter the Budject",
            ("$100,000 - $200,000", "$200,000 - $500,000", "$500,000 - $1,000,000", "$1,000,000 - $5,000,000", "$5,000,000+"),
            label_visibility = "collapsed"
        )

    input_txt = "Create a campaign for my demand supply platform. I run a company that manufactures " + str(Company_details) + " I tend to advertise my product in " + str(demographics) + " I want the ads to be delivered to the people of ages between " + str(MinAge) + " and " + str(MaxAge) + " based in " + str(demographics) + " I want to run the ads from " + str(Start_Date) + " to " + str(End_Date) + ". I have " + str(Bidding_amount) + " for the bidding. Hence, create a good and detailed campaign"
    st.markdown("", unsafe_allow_html=True)
    st.markdown("", unsafe_allow_html=True)
    st.markdown("", unsafe_allow_html=True)
    col1, col2 = st.columns([1,1])


    with col1:
        if st.button("Generate Media Plan", use_container_width=True):
            if input_txt:
                input_txt_str = str(input_txt).replace("{", "{{").replace("}", "}}").replace("#", "#")

                display_splash(input_txt_str)

    with col2:
        if st.button("Generate Creatives", use_container_width=True):
            creatives_splash(str(Company_details))


if __name__ == '__main__':
    main()