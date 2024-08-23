# Importing all the libraries
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import json
import plotly.express as px
from PIL import Image


# Reading the cleaned data 
airbnb_df = pd.read_csv(r"D:/Airbnb_Project/airbnb_data.csv")



# Functions for user input buttons
def inp_butt_location(df, cat):       
    grp_df1 = df.groupby("Country", as_index=False)[cat].mean().round(2)

    bar1 = px.bar(grp_df1,x= "Country",y = cat, title = "Average" + " " + cat + " " + "by" + " " + "Country", 
                    color_discrete_sequence = px.colors.sequential.BuGn_r, height = 500, text_auto=True)
    
    st.plotly_chart(bar1)


# Function for country input buttons
def country_buttons(k):
    country_lst = list(airbnb_df["Country"].unique())
    ctry = st.selectbox("Select any Country",country_lst, index= None, key = k)
    return ctry



# Function for country visualizations
def country_visuals(df, cat,k):
    country = country_buttons(k)

    if country:
        country_data = df[df['Country'] == country]
        grp_df2 = country_data.groupby(["Country","Area"] ,as_index=False)[cat].mean().round(2)

        bar2 = px.bar(grp_df2,x= "Area",y = cat, title = "Average" + " " + cat + " " + "by" + " " + "Area", 
                     color_discrete_sequence = px.colors.sequential.Cividis, height = 500, text_auto=True)
        
        bar2.update_xaxes(tickangle=90)
        
        st.plotly_chart(bar2)



# Function for availabilty group data
def availability_group(df,groups):
    grp_df3 = df.groupby(groups).agg({'Availability_30': 'mean', 'Availability_60': 'mean', 'Availability_90': 'mean', 'Availability_365': 'mean'}).reset_index()
    grp_df3 = grp_df3.round(0)
    return grp_df3


# Function for availabilty input buttons
def availability_button():
    sel_radio = st.radio("Choose an option", ["Availability_30", "Availability_60", "Availability_90", 
                        "Availability_365"],index=0)
    return sel_radio



# Functions for availabilty visualizations
def available_visuals(df):
    sel = availability_button()

    ava_df = availability_group(df,"Country")

    p1 = px.pie(ava_df, names= 'Country', values = sel, title = sel + " " + "by Countries",
                        color_discrete_sequence = px.colors.sequential.haline_r,hole=0.5, height = 600, width=600)
    
    st.plotly_chart(p1)



def ctry_ava_visual(df):
    country = country_buttons('c')

    if country:

        sel = availability_button()
        
        if sel:
            ava_df1 = availability_group(df,["Country","Area"])

            country_data = ava_df1[ava_df1['Country'] == country]

            bar3 = px.bar(country_data,x= "Area",y = sel, title = "Average" + " " + sel + " " + "by" + " " + "Area", 
                        color_discrete_sequence = px.colors.sequential.Oryel_r, height = 500, text_auto=True)
            
            bar3.update_xaxes(tickangle=90)
                
            st.plotly_chart(bar3)



# Functions for Type visualizations
def type_visuals(df, cat1,cat2):

    country = country_buttons('z')

    if country:
        country_data = df[df['Country'] == country]
        type_df1 = pd.DataFrame(country_data[cat1].value_counts()).reset_index()

        bar4 = px.bar(type_df1,x= cat1,y = "count", title = "Number of "  + cat1 + " for " + country, 
                    color_discrete_sequence = px.colors.sequential.Emrld_r, height = 500, text_auto=True)
        
        bar4.update_xaxes(tickangle=90)
            
        st.plotly_chart(bar4)


        type_df2 = pd.DataFrame(country_data[cat2].value_counts()).reset_index()

        p2 = px.pie(type_df2, names= cat2, values = "count", title = cat2 + " for " + country,
                            color_discrete_sequence = px.colors.sequential.Sunset_r,hole=0.5, height = 600, width=600)
        
        st.plotly_chart(p2)



# Function for dynamic catergorical analysis and visualizations
def visual_property_room(df,sel_cat1, sel_cat2):

    grp_df5 = df.groupby(sel_cat1, as_index=False)[sel_cat2].mean().round(2).sort_values(by = sel_cat2, ascending=False).reset_index(drop=True)

    if sel_cat1 in ["Property_type", "City"]:

        bar5 = px.bar(grp_df5,x= sel_cat1,y =sel_cat2, title = "Average " + sel_cat2 + " by " + sel_cat1, 
                    color_discrete_sequence = px.colors.sequential.Sunsetdark_r, height = 500, text_auto=True)
        
        bar5.update_xaxes(tickangle=90)
            
        st.plotly_chart(bar5)


    elif sel_cat1 in ["Room_type", "Bed_type"]:

        c1,c2 = st.columns(2)

        with c1:
            p3 = px.pie(grp_df5, names= sel_cat1, values = sel_cat2, title = "Average " + sel_cat2 + " by " + sel_cat1,
                        color_discrete_sequence = px.colors.sequential.Inferno_r,hole=0.5, height = 600, width=600)
            
            st.plotly_chart(p3)
        
        with c2:
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write(grp_df5)
        



# streamilt UI functions
st.set_page_config(layout="wide")

st.markdown("<h1 style='text-align: center;color: red; font-size: 50px;'>Airbnb Analysis</h1>", unsafe_allow_html=True)

option = option_menu(None,options = ["Home","Analysis"],
                       icons = ["house-door","binoculars"],
                       default_index=0,
                       orientation="horizontal", 
                       styles={"nav-link-selected": {"background-color": "#f52007"}})



if option == "Home":

    st.subheader(":red[About]")

    st.image(Image.open("D:/Airbnb_Project/airbnb_image.jpeg"),width=500)

    st.write("")

    st.markdown('''Airbnb is an online marketplace that connects people who want to rent out their homes with people looking for 
                accommodations in specific locales. The company has come a long way since 2007, when its co-founders first came up 
                with the idea to invite paying guests to sleep on an air mattress in their living room. 
                According to Airbnb's latest data, it now has more than 7 million listings, covering some 100,000 cities and towns 
                in 220-plus countries and regions worldwide.''')

    st.write("")

    st.markdown('''Airbnb offers hosts a relatively easy way to earn some income from their property.
                Guests often find that Airbnb rentals are cheaper and homier than hotels.
                Airbnb makes the bulk of its revenue by charging fees to both guests and hosts.''')

    st.write("")

    st.markdown('''Here we have used the Airbnb data to analyze and gain insights into pricing variations, 
                availability patterns, and location-based trends.''')






elif option == "Analysis":

    selected = option_menu(None,options=["Location Analysis", "Categorical Analysis"],
                            icons = ["geo","buildings"],
                            default_index=0,
                            orientation="horizontal",
                            styles={"nav-link-selected": {"background-color": "#f52007"}})



    if selected == "Location Analysis":

        tab1,tab2,tab3,tab4 = st.tabs(["Price", "Ratings", "Availabilty", "Types"])

        with tab1 :
            ct = st.toggle("Country wise",key=1)
            if ct:
                country_visuals(airbnb_df, "Price",'a')

            else:
                inp_butt_location(airbnb_df, "Price")


        with tab2 :
            ct = st.toggle("Country wise",key=2)
            if ct:
                country_visuals(airbnb_df, "Ratings", 'b')

            else:
                inp_butt_location(airbnb_df, "Ratings")


        with tab3 :
            ct = st.toggle("Country wise",key=3)

            if ct:
                ctry_ava_visual(airbnb_df)

            else:
                available_visuals(airbnb_df)


        with tab4 :
                
            type_visuals(airbnb_df, "Property_type", "Room_type")





    elif selected == "Categorical Analysis":

        sel_cat1 = st.selectbox("Choose a Category", ["Property_type", "Room_type", "Bed_type", "City"], index= None)

        if sel_cat1:

            sel_cat2 = st.selectbox("Choose another Category",["Price", "Ratings", "Availability_365"], index= None)

            if sel_cat1 and sel_cat2:

                visual_property_room(airbnb_df,sel_cat1, sel_cat2)





            


