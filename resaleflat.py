import streamlit as st
from streamlit_option_menu import option_menu
import numpy as np
import datetime
import pickle

# Set up page configuration for Streamlit
st.set_page_config(
    page_title='Singapore Flat Resale Price Predictor',
    page_icon='🏠',
    initial_sidebar_state='expanded',
    layout='wide',
    menu_items={"about": 'This Streamlit application developed for Singapore flat Resale price prediction'}
)

# Display the page title at the top of your app
st.title('Singapore Flat Resale Price Predictor')

st.markdown("""
    <style>
    .st-eb {font-size: 20px; margin-top: -40px;}
    .st-cb {padding: 20px;}
    .st-da {margin-top: 20px; padding-top: 30px; text-align: center; background-color: #3498db; padding-bottom: 10px; border-radius: 10px;}
    </style>
    """, unsafe_allow_html=True)


# sidebar with optionmenu
with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",  
        options=["Home", "Prediction Dashboard"], 
        icons=['house', "lightbulb"],  
        default_index=0, 
        orientation="vertical",
        styles={
            "container": {"padding": "5px","border": "2px ridge ", "background-color": "#002b36"},
            "icon": {"color": 'yellow', "font-size": "25px"},
            "nav-link": {"font-size": "18px", "text-align": "center", "margin": "0px", "--hover-color": "#586e75"},
            "nav-link-selected": {"background-color":"#247579"},  
                })

#user input values for selectbox and encoded for respective features
class option:

    option_months = ["January","February","March","April","May","June","July","August","September","October","November","December"]

    encoded_month= {"January" : 1,"February" : 2,"March" : 3,"April" : 4,"May" : 5,"June" : 6,"July" : 7,"August" : 8,"September" : 9,
            "October" : 10 ,"November" : 11,"December" : 12}

    option_town=['ANG MO KIO', 'BEDOK', 'BISHAN', 'BUKIT BATOK', 'BUKIT MERAH','BUKIT TIMAH', 'CENTRAL AREA', 'CHOA CHU KANG', 'CLEMENTI',
        'GEYLANG', 'HOUGANG', 'JURONG EAST', 'JURONG WEST','KALLANG/WHAMPOA', 'MARINE PARADE', 'QUEENSTOWN', 'SENGKANG','SERANGOON',
        'TAMPINES', 'TOA PAYOH', 'WOODLANDS', 'YISHUN','LIM CHU KANG', 'SEMBAWANG', 'BUKIT PANJANG', 'PASIR RIS','PUNGGOL']
    
    encoded_town={'ANG MO KIO' : 0 ,'BEDOK' : 1,'BISHAN' : 2,'BUKIT BATOK' : 3,'BUKIT MERAH' : 4,'BUKIT PANJANG' : 5,'BUKIT TIMAH' : 6,
        'CENTRAL AREA' : 7,'CHOA CHU KANG' : 8,'CLEMENTI' : 9,'GEYLANG' : 10,'HOUGANG' : 11,'JURONG EAST' : 12,'JURONG WEST' : 13,
        'KALLANG/WHAMPOA' : 14,'LIM CHU KANG' : 15,'MARINE PARADE' : 16,'PASIR RIS' : 17,'PUNGGOL' : 18,'QUEENSTOWN' : 19,
        'SEMBAWANG' : 20,'SENGKANG' : 21,'SERANGOON' : 22,'TAMPINES' : 23,'TOA PAYOH' : 24,'WOODLANDS' : 25,'YISHUN' : 26}
    
    option_flat_type=['1 ROOM', '2 ROOM','3 ROOM', '4 ROOM', '5 ROOM', 'EXECUTIVE','MULTI-GENERATION']

    encoded_flat_type={'1 ROOM': 0,'2 ROOM' : 1,'3 ROOM' : 2,'4 ROOM' : 3,'5 ROOM' : 4,'EXECUTIVE' : 5,'MULTI-GENERATION' : 6}

    option_flat_model=['2-ROOM','3GEN','ADJOINED FLAT', 'APARTMENT' ,'DBSS','IMPROVED' ,'IMPROVED-MAISONETTE', 'MAISONETTE',
                    'MODEL A', 'MODEL A-MAISONETTE','MODEL A2' ,'MULTI GENERATION' ,'NEW GENERATION', 'PREMIUM APARTMENT',
                    'PREMIUM APARTMENT LOFT', 'PREMIUM MAISONETTE','SIMPLIFIED', 'STANDARD','TERRACE','TYPE S1','TYPE S2']

    encoded_flat_model={'2-ROOM' : 0,'3GEN' : 1,'ADJOINED FLAT' : 2,'APARTMENT' : 3,'DBSS' : 4,'IMPROVED' : 5,'IMPROVED-MAISONETTE' : 6,
                'MAISONETTE' : 7,'MODEL A' : 8,'MODEL A-MAISONETTE' : 9,'MODEL A2': 10,'MULTI GENERATION' : 11,'NEW GENERATION' : 12,
                'PREMIUM APARTMENT' : 13,'PREMIUM APARTMENT LOFT' : 14,'PREMIUM MAISONETTE' : 15,'SIMPLIFIED' : 16,'STANDARD' : 17,
                'TERRACE' : 18,'TYPE S1' : 19,'TYPE S2' : 20}
    
#set up information for the 'get prediction' menu
if selected == "Prediction Dashboard":
    st.write('')
    st.markdown("<h5 style=color:orange>To Predict the Resale Price of a Flat, Please Provide the Following Information:",unsafe_allow_html=True)
    st.write('')

    # creted form to get the user input 
    with st.form('prediction'):
        col1,col2=st.columns(2)
        with col1:

            user_month=st.selectbox(label='Month',options=option.option_months,index=None)

            user_town=st.selectbox(label='Town',options=option.option_town,index=None)

            user_flat_type=st.selectbox(label='Flat Type',options=option.option_flat_type,index=None)

            user_flat_model=st.selectbox(label='Flat Model',options=option.option_flat_model,index=None)

            floor_area_sqm=st.number_input(label='Floor area sqm',min_value=10.0)

            price_per_sqm=st.number_input(label='Price Per sqm',min_value=100.00)

        with col2:

            year=st.text_input(label='year',max_chars=4)

            block=st.text_input(label='Block',max_chars=3)

            lease_commence_date=st.text_input(label='Year of lease commence',max_chars=4)

            remaining_lease=st.number_input(label='Remaining lease year',min_value=0,max_value=99)

            years_holding=st.number_input(label='Years Holding',min_value=0,max_value=99)

            c1,c2=st.columns(2)
            with c1:
                storey_start=st.number_input(label='Storey start',min_value=1,max_value=50)
            with c2:
                storey_end=st.number_input(label='Storey end',min_value=1,max_value=51)
            
            st.markdown('<br>', unsafe_allow_html=True)

            button=st.form_submit_button('PREDICT',use_container_width=True)

    if button:
        with st.spinner("Predicting..."):

            #check whether user fill all required fields
            if not all([user_month,user_town,user_flat_type,user_flat_model,floor_area_sqm,price_per_sqm,year,block,
                        lease_commence_date,remaining_lease,years_holding,storey_start,storey_end]):
                st.error("Please fill in all required fields.")

            else:
                #create features from user input 
                current_year=datetime.datetime.now().year

                current_remaining_lease=remaining_lease-(current_year-(int(year)))
                age_of_property=current_year-int(lease_commence_date)


                month=option.encoded_month[user_month]
                town=option.encoded_town[user_town]
                flat_type=option.encoded_flat_type[user_flat_type]
                flat_model=option.encoded_flat_model[user_flat_model]

                floor_area_sqm_log=np.log(floor_area_sqm)
                remaining_lease_log=np.log1p(remaining_lease)
                price_per_sqm_log=np.log(price_per_sqm)

                #opened pickle model and predict the resale price with user data
                with open('Decisiontree.pkl','rb') as files:
                    model=pickle.load(files)
                
                user_data=np.array([[month, town, flat_type, block, flat_model, lease_commence_date, year, storey_start,
                                    storey_end, years_holding, current_remaining_lease, age_of_property, floor_area_sqm_log, 
                                    remaining_lease_log,price_per_sqm_log ]])

                predict=model.predict(user_data)
                resale_price=np.exp(predict[0])

                #display the predicted selling price 
                st.subheader(f"Predicted Resale price is: :green[{resale_price:.2f}]")


# set up the information for 'Home' menu
if selected == "Home":
        st.markdown('<br>', unsafe_allow_html=True)  # Add some space before the topic
        st.subheader(':green[About HDB]')
        st.markdown('''<p style='color:#6C7A89;font-size:14px'>The Housing & Development Board (HDB) is a statutory board under the Ministry of National Development responsible for public housing in Singapore.
                    Established in 1960, HDB initially focused on emergency housing and resettlement. In the 1990s and 2000s, it introduced upgrading and redevelopment schemes for mature estates and new housing types for 
                    different income groups. In 2003, HDB was reorganized to better suit Singapore's housing market. Its vision is to create endearing homes, its mission is to provide affordable, quality housing,
                    and its values include integrity, learning, teamwork, excellence, and care.</p>''',
        unsafe_allow_html=True)
        st.markdown('<br>', unsafe_allow_html=True)  # Add some space after the topic  
        st.markdown('<br>', unsafe_allow_html=True)
                
        st.subheader(":green[***Singapore's Rapid Growth***]")
        st.markdown('''<p style='color:#6C7A89;font-size:14px'>In the 1940s and 1950s, Singapore saw rapid population growth, 
                    reaching 1.7 million from 940,700 between 1947 and 1957. Living conditions deteriorated, 
                    with many in informal settlements or cramped shophouses. The Singapore Improvement Trust (SIT), 
                    responsible for public housing, struggled to provide affordable options. 
                    Delays in new housing approvals slowed construction by 1958.
                    <br>In the mid-1950s, efforts to replace the SIT resulted in the Housing and Development Bill, 
                    which formed the HDB in February 1960, taking over public housing responsibilities from the SIT.</p>''',
                    unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            st.image('https://media2.malaymail.com/uploads/articles/2020/2020-07/20200725_Singapore-HDB.jpg', use_column_width=True)
        with c2:
            st.image('https://dollarsandsense.sg/wp-content/uploads/2020/09/nguyen-thu-hoai-a15b7LYrfbk-unsplash.jpg', use_column_width=True)


        st.link_button(label='Official Website', url='https://www.hdb.gov.sg/cs/infoweb/homepage', use_container_width=True)

        st.subheader(':orange[**check out**]')
        col1, col2 = st.columns(2)
        with col1:
            st.video('https://www.youtube.com/watch?v=j5mWJsvXQk4')

        with col1:
            st.markdown(" ")
            st.markdown(" ")
            st.markdown(" ")
            st.markdown(" ")
