from pymongo import MongoClient
import pymongo
import pandas as pd
import numpy as np
import streamlit as st
from streamlit_option_menu import option_menu
import pymysql
import plotly.express as px 
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
#import geopandas as go

zomato_df = pd.read_excel(r"F:\data science\VS\DataScience projects\zomato\zomato.xlsx")
zomato_exploded_df = pd.read_excel(r"F:\data science\VS\DataScience projects\zomato\zomato_exploded.xlsx")

## Below code will do page title(tab Name) configuration
st.set_page_config(page_title= "Zomato data Visualization",
                   layout= "wide")

## Below code will create the header tabs in the screen 
selected = option_menu(None, ["Home","Explore More Data","Data Analysis on INDIA"], 
            icons=["house","bar-chart-line","flag-fill"],
            menu_icon= "menu-button-wide",
            default_index=0,
            orientation= "horizontal",
            styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px", "--hover-color": "#6F36AD"},
                    "nav-link-selected": {"background-color": "#6F36AD"}})

if selected == "Home":

    st.markdown("# Zomato Data Visualization and Exploration")
    st.write(" ")
    st.markdown("### :blue[What is Zomato? :]")
    st.markdown("### Zomato is a popular restaurant discovery and food delivery service. It is India's largest online food ordering and delivery service. It was founded in 2010 by Arvind Narayanan and Rohit Kumar. It has been featured in Forbes, Top 100, and many other publications.")
    st.write(" ")
    st.markdown("### :blue[Overview :]")
    st.markdown("#### This streamlit app aims to give users a friendly environment which can be used to visualize the Zomato data and gain lots of insights on Top restaurants.")
    st.write(" ")
    st.markdown("### :blue[Technologies used :]")
    st.markdown("#### - Python, Pandas")
    st.markdown("#### - Streamlit and Plotly")

elif selected == "Explore More Data":
    st.write("### :violet[Explore More Data using interactive visuals]")
    st.write(" ")
    st.write(" ")
    st.markdown("In here we will see each Country and its individual City analysis based on its top Recommended cuisine, Restaurants, How many Online deliveries and How many Dine-in services were made  ")
    

    col1, col2 = st.columns([2,2],gap="large")

    with col1:

        result = st.selectbox("Please select the country to see individual analysis",zomato_df["Country"].unique(),index=0)
        df = zomato_df[zomato_df["Country"] == result]
        df_exploded = zomato_exploded_df[zomato_exploded_df["Country"] == result]
    
    with col2:
        total = int(df["Restaurant Name"].count())
        st.markdown(f"### :orange[Total listed Restaurants in :red[{result}]]: :green[{total}]")
        most_costly_cuisine = df_exploded.groupby('Cuisines')['INR_currency'].mean().idxmax()
        st.markdown(f'### :orange[Most costlier cuisine is] :green[{most_costly_cuisine}]')
        st.write(" ")

    col1,col2= st.columns([2,2],gap="small")

    with col1:
        df1 = df[df["Aggregate rating"] == df["Aggregate rating"].max()][["Restaurant Name","Votes","Cuisines"]].sort_values(by = "Votes",ascending=False).head(5)
        
        fig = px.bar(df1,x="Restaurant Name",y="Votes",color="Restaurant Name",hover_name="Votes",text="Cuisines",color_discrete_sequence=px.colors.sequential.Blackbody,
        labels={"Restaurant Name":"Restaurant Names","Votes":"Total Recommendations"})
        fig.update_layout(
            width=500,
            height=500
        )
        fig.update_traces(marker_line_color = 'black',
                marker_line_width = 2, opacity = 1)
        fig.update_layout(title_text="Top High rated Restaurant's in "+result, title_x=0.2,title_font_color="orange")
        st.write(fig)
        st.write(" ")


    with col2:
        df1 = df_exploded.groupby("Cuisines")[["Aggregate rating","Votes"]].mean().reset_index().sort_values(["Aggregate rating","Votes"],ascending=False).head(8)
        
        fig = px.bar(df1,x="Aggregate rating",y="Cuisines",color="Cuisines",hover_name="Votes",text="Votes",orientation="h",color_discrete_sequence=px.colors.sequential.YlGn,
        labels={"Cuisines":"Top Cuisines","Votes":"Total Recommendations"})
        fig.update_layout(
            width=600,
            height=400
        )
        fig.update_traces(marker_line_color = 'black',
                marker_line_width = 2, opacity = 1)
        fig.update_layout(title_text="Top Recommende Cuisines in "+result, title_x=0.2,title_font_color="orange")
        st.write(fig)
        st.write(" ")

    st.header(":rainbow[Average Cost of Two in Each city:]",divider='rainbow')
    st.markdown("Based on the chart we could see the Cost of two differes from city to city as well its location. Below it shows the Cities to the right must be of high living cost and to the left it should be of low living cost. Based on these report Zomato should always prefere giving the foods with lower cost for places where the cost of living is very low because mostly the people who live there are getting less salaries. So in those areas if they sell the product with higer cost definitely it will not be sold and it will be a loss. Whereas on the other hand where the Cost of living is higher Zomato can focus foods that are more in cost because in these places definitelty people are going to get more salaries since the cost of living is higher. So here Zomota can get good profit which can be equalized in low cost of living area")

    df_city = df.groupby("City")["Average Cost for two"].mean().sort_values(ascending=True).reset_index()
    fig = px.line(df_city,x="City",y="Average Cost for two",markers=True,color_discrete_sequence=px.colors.sequential.YlOrBr,labels={"City":"City Names","Average Cost for two":"Average Cost for two"})
    fig.update_layout(
            width=1200,
            height=400
    )
    fig.update_traces(marker_line_color = 'black',
            marker_line_width = 2, opacity = 1)
    fig.update_layout(title_text="Average Cost of Two in Each city of "+result, title_x=0.4,title_font_color="orange")
    st.write(fig)
    st.write(" ")

    df_online = df.groupby(['City', 'Has Online delivery']).size().reset_index()
    fig = px.bar(df_online,x="City",y=0,color="Has Online delivery",hover_name="City",text="Has Online delivery",labels={"City":"City Names","0":"Online Delivery count"})
    fig.update_layout(
            width=1200,
            height=400
    )
    fig.update_traces(marker_line_color = 'black',
            marker_line_width = 2, opacity = 1)
    fig.update_layout(title_text="Online delivery count in Each city of "+result, title_x=0.4,title_font_color="orange")
    st.write(fig)
    

    st.write(" ")
    st.header(":rainbow[Total Cuisines list in Each city:]",divider='rainbow')
    st.markdown("We can see from the below based on people interest the Cuisines count is also increases the left most is high prefered Cuisine in the country which stands top with respect to people interest and rating. So Zomato can try to partner with the top rated cuisines and give it to the best offer ")
    df_cus = df_exploded.groupby(["Cuisines"]).agg({"Cuisines":"count"}).rename(columns={"Cuisines":"count"}).reset_index().sort_values(by="count",ascending=False)
    fig = px.bar(df_cus,x="Cuisines",y="count",color="Cuisines",labels={"Cuisines":"Cuisines List","count":"Total Count"},color_discrete_sequence=px.colors.sequential.Hot)
    fig.update_layout(
            width=1200,
            height=400
    )
    fig.update_traces(marker_line_color = 'black',
            marker_line_width = 2, opacity = 1)
    fig.update_layout(title_text="Cuisines count in "+result, title_x=0.4,title_font_color="orange")
    st.write(fig)

    col1,col2,col3= st.columns([2,2,2],gap="small")
    
    with col1:
        fig = px.pie(df.drop_duplicates(subset=['Restaurant Name']), names='Has Online delivery', color_discrete_sequence=px.colors.sequential.Sunset,width=300,height=300)
        fig.update_traces(marker_line_color = 'black',
                marker_line_width = 2, opacity = 1)
        fig.update_layout(title_text="Online Delivery in "+result, title_x=0,title_font_color="orange")
        st.write(fig)

    with col2:
        fig = px.pie(df.drop_duplicates(subset=['Restaurant Name']), names='Has Table booking', color_discrete_sequence=px.colors.sequential.Turbo,width=300,height=300)
        fig.update_traces(marker_line_color = 'black',
                marker_line_width = 2, opacity = 1)
        fig.update_layout(title_text="Dine-in Services in "+result, title_x=0.1,title_font_color="orange")
        st.write(fig)

    with col3:
        fig = px.box(df_exploded.groupby('Cuisines').agg({'INR_currency': 'mean'}).reset_index(),
                           x='Cuisines', y='INR_currency')
        fig.update_layout(
            width=600,
            height=400
        )
        fig.update_traces(marker_line_color = 'black',
                marker_line_width = 2, opacity = 1)
        fig.update_layout(title_text="Cost Analysis with respect to Indian Currency", title_x=0.2,title_font_color="orange")
        st.write(fig)

    

    st.write(" ")
    st.header(":rainbow[individual City analysis:]",divider='rainbow')
    st.markdown("From below analysis we will get to know the Number of listed restaurants in each city, Recommended Restaurant in City, Which Cuisines is most preferred in that city, What is the average Cost of Two people for a meal, How many online deliveries are happening, How many dine-in are happening.  ")
    st.write(" ")
    col1, col2 = st.columns([2,2],gap="large")

    with col1:
        result1 = st.selectbox(f"Cities of :red[{result}] to see individual analysis",df["City"].unique(),index=0)
        df1 = df[df["City"] == result1]
        df1_exploded = df_exploded[df_exploded["City"] == result1]

    with col2:
        total = int(df1["Restaurant Name"].count())
        st.markdown(f"##### :orange[Total listed Restaurants in :green[{result1}]]: :red[{total}]")
        total = df1[df1["Aggregate rating"] == df1["Aggregate rating"].max()][["Cuisines","Votes","Restaurant Name"]].sort_values(by = "Votes",ascending=False).reset_index().head(1)
        tot = total["Restaurant Name"][0]
        st.markdown(f"##### :orange[Top Recommended Restaurant] :green[{tot}]")
        total = df1_exploded.groupby("Cuisines")[["Aggregate rating","Votes"]].mean().reset_index().sort_values(["Aggregate rating","Votes"],ascending=False).reset_index()
        tot = total["Cuisines"][0]
        st.markdown(f"##### :orange[Famous Cusine] :green[{tot}]")
        total = df1["Average Cost for two"].mean()
        st.markdown(f"##### :orange[Average Cost of Two]: :red[{total}]")
        st.write(" ")

    col1,col2,col3 = st.columns([2,2,2],gap="small")

    with col1:
        df_count = df1["Rating text"].value_counts().reset_index()
        fig = px.bar(df_count,x="Rating text",y="count",color="Rating text",hover_name="count",color_discrete_sequence=px.colors.sequential.Rainbow,
        labels={"Rating text":"Rating Category","count":"Total Count"})
        fig.update_layout(
            width=400,
            height=400
        )
        fig.update_traces(marker_line_color = 'black',
                marker_line_width = 2, opacity = 1)
        fig.update_layout(title_text="Rating count in "+result1, title_x=0.3,title_font_color="orange")
        st.write(fig)

    with col2:
        fig = px.pie(df1, names='Has Table booking',color_discrete_sequence=px.colors.sequential.Turbo,width=300,height=300)
        fig.update_traces(marker_line_color = 'black',
                marker_line_width = 2, opacity = 1)
        fig.update_layout(title_text="Dine-in Services in "+result1, title_x=0.1,title_font_color="orange")
        st.write(fig)

    with col3:
        fig = px.pie(df1, names='Has Online delivery',color_discrete_sequence=px.colors.sequential.thermal,width=300,height=300)
        fig.update_traces(marker_line_color = 'black',
                marker_line_width = 2, opacity = 1)
        fig.update_layout(title_text="Online Deliveries in "+result1, title_x=0.1,title_font_color="orange")
        st.write(fig)

    df1 = df1_exploded.groupby("Cuisines")[["Aggregate rating","Votes"]].mean().reset_index().sort_values(["Aggregate rating","Votes"],ascending=False).head(10)
    fig = px.bar(df1,x="Aggregate rating",y="Cuisines",color="Cuisines",hover_name="Votes",text="Votes",orientation="h",barmode="group",color_discrete_sequence=px.colors.sequential.OrRd,
    labels={"Cuisines":"Top Cuisines","Votes":"Total Recommendations"})
    fig.update_layout(
        width=600,
        height=400
    )
    fig.update_traces(marker_line_color = 'black',
            marker_line_width = 2, opacity = 1)
    fig.update_layout(title_text="Top Recommende Cuisines in "+result1, title_x=0.2,title_font_color="orange")
    st.write(fig)
    st.write(" ")

else:
    st.write("### :violet[Exploring INDIA on Zomato Data using interactive visuals]")
    st.write(" ")
    st.markdown(" In here we will see some interesting insights on Zomato data how it is used in India and its Cities. This will help in understanding the data better on impact with Indian Cities whether it is taking more online deliveries or still people prefer more in Dine-in and which Cuisines are most preferred in India.")
    df = zomato_df[zomato_df["Country"] == "India"]
    df_exploded = zomato_exploded_df[zomato_exploded_df["Country"] == "India"]

    col1, col2 = st.columns([2,2],gap="large")

    with col1:
        df1 = df[df["Aggregate rating"] == df["Aggregate rating"].max()][["Restaurant Name","Votes","Cuisines"]].sort_values(by = "Votes",ascending=False).head(5)
        fig = px.bar(df1,x="Restaurant Name",y="Votes",color="Restaurant Name",hover_name="Votes",text="Cuisines",color_discrete_sequence=px.colors.sequential.Blackbody,
        labels={"Restaurant Name":"Restaurant Names","Votes":"Total Recommendations"})
        fig.update_layout(
            width=500,
            height=500
        )
        fig.update_traces(marker_line_color = 'black',
                marker_line_width = 2, opacity = 1)
        fig.update_layout(title_text="Top High rated Restaurant's in INDIA", title_x=0.2,title_font_color="orange")
        st.write(fig)
        st.write(" ")

    with col2:
        total = int(df["Restaurant Name"].count())
        st.markdown(f"##### :orange[Total listed Restaurants in :red[INDIA]]: :green[{total}]")
        most_costly_cuisine = df_exploded.groupby('Cuisines')['INR_currency'].mean().idxmax()
        st.markdown(f'##### :orange[Most costlier cuisine is] :green[{most_costly_cuisine}]')
        st.write(" ")
        st.header(" :rainbow[High Rated restaurants in INDIA:]",divider='rainbow')
        st.markdown("The Bar chart clearly shows people visits BBQ type restaurants most often as the two top most refers to the same from the list where it has more votes with good rating.")

    col1, col2 = st.columns([2,2],gap="large")
    with col1:
        st.header(":rainbow[Recommended Cuisines:]",divider='rainbow')
        st.markdown("Based on the chart we could see in INDIA the top cuisines are of other Countries. So this tells us Most of INDIANS are preffering other country Cuisines than INDIAN Cuisines. Where they want to try and explore some different/New foods than usual.")
    
    with col2:
        df1 = df_exploded.groupby("Cuisines")[["Aggregate rating","Votes"]].mean().reset_index().sort_values(["Aggregate rating","Votes"],ascending=False).head(8)
        
        fig = px.bar(df1,x="Aggregate rating",y="Cuisines",color="Cuisines",hover_name="Votes",text="Votes",orientation="h",color_discrete_sequence=px.colors.sequential.YlGn,
        labels={"Cuisines":"Top Cuisines","Votes":"Total Recommendations"})
        fig.update_layout(
            width=600,
            height=400
        )
        fig.update_traces(marker_line_color = 'black',
                marker_line_width = 2, opacity = 1)
        fig.update_layout(title_text="Top Recommende Cuisines in INDIA", title_x=0.2,title_font_color="orange")
        st.write(fig)
        st.write(" ")
    

    st.header(":rainbow[Highly Spent Cities on Online Delivery:]",divider='rainbow')
    st.markdown(f"We could see :grey[New Delhi] spends more on Online Delivery than other Cities which is a good sign to Zomato in 'NEW DELHI'. Where as rest of the Cities like ':red[Kochi, Mohali]' are speding very less in case of online delivery this is where Zomato need to give more offers at some initial stage based on their need to bring in more customers")
    st.write(" ")
    df1 = df[df["Has Online delivery"] == "Yes"]
    df1 = df1.groupby(["City"])["Average Cost for two"].sum().reset_index().sort_values("Average Cost for two",ascending=False)
    fig = px.bar(df1,x="City",y="Average Cost for two",color="City",text="Average Cost for two",color_discrete_sequence=px.colors.sequential.YlGn,
    labels={"City":"City Names","Average Cost for two":"Amount Spent"})
    fig.update_layout(
        width=1200,
        height=600
    )
    fig.update_traces(marker_line_color = 'black',
            marker_line_width = 2, opacity = 1)
    fig.update_layout(title_text="Highly Spent Cities on Online Delivery in INDIA", title_x=0.4,title_font_color="orange")
    st.write(fig)

    st.header(":rainbow[Highly Spent Cities on Dine-in:]",divider='rainbow')
    st.markdown(f"We could see again :grey[New Delhi] spends more on Dine-in as well this indicates that equal amount of people in New Delhi wanted to spend time with family. In Zomato's view New Delhi is giving good profit where as in other cities they are prefering more Dine-in Services which is not good for Zomato. So in those places Zomato need to partner with local restaurants and give better offers during night for people who are working in night shifts. This will significantly improve their business")
    st.write(" ")
    df2 = df[df["Has Table booking"] == "Yes"]
    df2 = df2.groupby(["City"])["Average Cost for two"].sum().reset_index().sort_values("Average Cost for two",ascending=False)
    fig = px.bar(df2,x="City",y="Average Cost for two",color="City",text="Average Cost for two",color_discrete_sequence=px.colors.sequential.YlGn,
    labels={"City":"City Names","Average Cost for two":"Amount Spent"})
    fig.update_layout(
        width=1200,
        height=600
    )
    fig.update_traces(marker_line_color = 'black',
            marker_line_width = 2, opacity = 1)
    fig.update_layout(title_text="Highly Spent Cities on Dine-in in INDIA", title_x=0.4,title_font_color="orange")
    st.write(fig)
    

    st.header(":rainbow[Individual city analysis:]",divider='rainbow')
    st.markdown(f"From the below we could get insights like, How Many restaurants are listed in each City, Recommended Restaurant in City, Which Cuisine is most preferred in that City, What is the average Cost of Two people for a meal, How many online Deliveries are happening, How many Dine-in are happening  ")

    col1, col2 = st.columns([2,2],gap="large")

    with col1:
        result2 = st.selectbox(f"Cities of :red[INDIA] to see individual analysis",df["City"].unique(),index=0)
        df1 = df[df["City"] == result2]
        df1_exploded = df_exploded[df_exploded["City"] == result2]

    with col2:
        total = int(df1["Restaurant Name"].count())
        st.markdown(f"##### :orange[Total listed Restaurants in :green[{result2}]]: :red[{total}]")
        total = df1[df1["Aggregate rating"] == df1["Aggregate rating"].max()][["Cuisines","Votes","Restaurant Name"]].sort_values(by = "Votes",ascending=False).reset_index().head(1)
        tot = total["Restaurant Name"][0]
        st.markdown(f"##### :orange[Top Recommended Restaurant] :green[{tot}]")
        total = df1_exploded.groupby("Cuisines")[["Aggregate rating","Votes"]].mean().reset_index().sort_values(["Aggregate rating","Votes"],ascending=False).reset_index()
        tot = total["Cuisines"][0]
        st.markdown(f"##### :orange[Famous Cusine] :green[{tot}]")
        total = df1["Average Cost for two"].mean()
        st.markdown(f"##### :orange[Average Cost of Two]: :red[{total}]")
        st.write(" ")
    
    col1, col2, col3 = st.columns([2,2,2],gap="small")

    with col1:
        df_count = df1["Rating text"].value_counts().reset_index()
        fig = px.bar(df_count,x="Rating text",y="count",color="Rating text",hover_name="count",color_discrete_sequence=px.colors.sequential.Rainbow,
        labels={"Rating text":"Rating Category","count":"Total Count"})
        fig.update_layout(
            width=400,
            height=400
        )
        fig.update_traces(marker_line_color = 'black',
                marker_line_width = 2, opacity = 1)
        fig.update_layout(title_text="Rating count in "+result2, title_x=0.3,title_font_color="orange")
        st.write(fig)

    with col2:
        fig = px.pie(df1, names='Has Table booking',color_discrete_sequence=px.colors.sequential.Turbo,width=300,height=300)
        fig.update_traces(marker_line_color = 'black',
                marker_line_width = 2, opacity = 1)
        fig.update_layout(title_text="Dine-in Services in "+result2, title_x=0.1,title_font_color="orange")
        st.write(fig)

    with col3:
        fig = px.pie(df1, names='Has Online delivery',color_discrete_sequence=px.colors.sequential.thermal,width=300,height=300)
        fig.update_traces(marker_line_color = 'black',
                marker_line_width = 2, opacity = 1)
        fig.update_layout(title_text="Online Deliveries in "+result2, title_x=0.1,title_font_color="orange")
        st.write(fig)
    
    fig = px.scatter_mapbox(df, lat="Latitude", lon="Longitude", hover_name="City", hover_data="INR_currency", width=800, height=800, zoom=2, opacity=1, color_continuous_scale="red", color_discrete_sequence=["orange", "red", "green", "blue", "purple"],title="Map view with Price range for each location")
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(title_text="Geographical representation of Price range for each location", title_x=0,title_font_color="orange")
    st.plotly_chart(fig, use_container_width=True)