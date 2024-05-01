import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_extras.metric_cards import style_metric_cards
import geopandas as gpd
import pydeck as pdk



st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center;'>Traffic Analysis of Cities in San Bernardino County - 2021</h1>", unsafe_allow_html=True)


cities_list = [
    'Select an Origin City Name:',  # Add a default option
    'Ontario', 'Fontana', 'Rialto', 'Highland', 'Victorville', 'Rancho Cucamonga',
    'Redlands', 'Yucaipa', 'San Bernardino', 'Chino Hills', 'Hesperia',
    'Chino', 'Colton', 'Upland', 'Apple Valley'
]
option = st.selectbox("Select a Origin City Name:", cities_list)

geojson_path = r"C:\Users\ayyag\Downloads\City_Boundaries.geojson"
gdf = gpd.read_file(geojson_path)
selected_city_gdf = gdf[gdf['CITY'] == option]
selected_city_geojson = selected_city_gdf.__geo_interface__

# Define the layer to visualize with pydeck
layer = pdk.Layer(
    'GeoJsonLayer',
    data=selected_city_geojson,
    get_fill_color='[200, 30, 0, 160]',  # RGBA color for the city area
    pickable=True
)

# Set the viewport location
view_state = pdk.ViewState(
    latitude=selected_city_gdf.geometry.centroid.y.mean(),
    longitude=selected_city_gdf.geometry.centroid.x.mean(),
    zoom=10,
    pitch=0)

# Render the map with pydeck
st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))


# Load data from CSV
# def load_data():
df = pd.read_csv(r"C:\Users\ayyag\Downloads\2021 VMT Data\Traffic_Analysis_Dataset.csv")

# Fetch list of cities

# Streamlit App
#st.title('Traffic Analysis of Cities in San Bernardino County', anchor='center')

# Load data
# df = load_data()

# City Selection Filter
cities = ['Ontario', 'Fontana', 'Rialto', 'Highland', 'Victorville', 'Rancho Cucamonga',
    'Redlands', 'Yucaipa', 'San Bernardino', 'Chino Hills', 'Hesperia',
    'Chino', 'Colton', 'Upland', 'Apple Valley', 'Other Cities in San Bernardino']

counties = ['Los Angeles', 'Orange', 'Imperial', 'San Diego', 'Riverside']




demo = pd.read_excel(r"C:\Users\ayyag\Downloads\2021 VMT Data\Demographics Data.xlsx")

demo1 = demo[demo['City Name']==option]

population_value = str(demo1['Population'].values[0]) if len(demo1['Population']) > 0 else "NA"
households_value = str(demo1['Households'].values[0]) if len(demo1['Households']) > 0 else "NA"
employment_value = str(demo1['Employment'].values[0]) if len(demo1['Employment']) > 0 else "NA"
income_value = str(demo1['Household Income'].values[0]) if len(demo1['Household Income']) > 0 else "NA"

# Update metric cards with the NA values
col9, col10, col11, col12 = st.columns(4)
col9.metric(label="Population", value=population_value)
col10.metric(label="Households", value=households_value)
col11.metric(label="Employment", value=employment_value)
col12.metric(label="Income", value=income_value)
style_metric_cards()


# Filter data based on selected cities
df1 = df[(df['Origin Zone Name']== option) & df['Destination Zone Name'].isin(cities) & (df['Day Type'] == "All Days") & (df['Day Part'] == "All Day (12am-12am)")].nlargest(10, 'Average Daily O-D Traffic (StL Index)')

# Filter DataFrame based on selected city
df2 = df[df['Origin Zone Name'].isin(cities) & (df['Destination Zone Name']== option) & (df['Day Type'] == "All Days") & (df['Day Part'] == "All Day (12am-12am)")].nlargest(10, 'Average Daily O-D Traffic (StL Index)')

# Filter data based on selected cities
df3 = df[(df['Origin Zone Name']== option) & df['Destination Zone Name'].isin(counties) & (df['Day Type'] == "All Days") & (df['Day Part'] == "All Day (12am-12am)")].nlargest(4, 'Average Daily O-D Traffic (StL Index)')

# Filter DataFrame based on selected city
df4 = df[df['Origin Zone Name'].isin(counties) & (df['Destination Zone Name']== option) & (df['Day Type'] == "All Days") & (df['Day Part'] == "All Day (12am-12am)")].nlargest(4, 'Average Daily O-D Traffic (StL Index)')

col1, col2 = st.columns(2)
fig = px.pie(df1, values="Average Daily O-D Traffic (StL Index)", names="Destination Zone Name", title= f'Outgoing trips from {option} to other cities')
fig.update_traces(textposition='inside', textinfo='percent+label')
fig.update_layout(title_x=0.2)
col1.plotly_chart(fig, theme="streamlit")
# col1.dataframe(custom_df)

fig1 = px.pie(df2, values="Average Daily O-D Traffic (StL Index)", names="Origin Zone Name", title= f'Incoming trips to {option} from other cities')
fig1.update_traces(textposition='inside', textinfo='percent+label')
fig1.update_layout(title_x=0.2)
col2.plotly_chart(fig1, theme="streamlit")

col3, col4 = st.columns(2)
fig = px.pie(df3, values="Average Daily O-D Traffic (StL Index)", names="Destination Zone Name", title= f'Outgoing trips from {option} to surrounding counties')
fig.update_traces(textposition='inside', textinfo='percent+label')
fig.update_layout(title_x=0.2)
col3.plotly_chart(fig, theme="streamlit")
# col1.dataframe(custom_df)

fig1 = px.pie(df4, values="Average Daily O-D Traffic (StL Index)", names="Origin Zone Name", title= f'Incoming trips to {option} from surrounding counties')
fig1.update_traces(textposition='inside', textinfo='percent+label')
fig1.update_layout(title_x=0.2)
col4.plotly_chart(fig1, theme="streamlit")

# col1.dataframe(df)
# col2.dataframe(df)

list = [
    'Select a Destination City/County Name:',  # Add a default option
    'Ontario', 'Fontana', 'Rialto', 'Highland', 'Victorville', 'Rancho Cucamonga',
    'Redlands', 'Yucaipa', 'San Bernardino', 'Chino Hills', 'Hesperia',
    'Chino', 'Colton', 'Upland', 'Apple Valley', 'Other Cities of San Bernardino', 'Los Angeles', 'Imperial', 'San Diego', 'Orange', 'Riverside'
]

col5,col6 = st.columns(2)

destn = col5.selectbox("Select a Destination City/County Name:", list)

d1 = pd.read_csv(r"C:\Users\ayyag\Downloads\2021 VMT Data\Traffic_Analysis_Dataset.csv")

day_type = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
day_part = ['12AM', '1AM',
       '2AM', '3AM', '4AM', '5AM',
       '6AM', '7AM', '8AM',
       '9AM', '10AM', '11AM',
       '12PM', '1PM', '2PM',
       '3PM', '4PM', '5PM', '6PM',
       '7PM', '8PM', '9PM',
       '10PM', '11PM']

# Filter data based on selected cities
df5 = d1[(d1['Origin Zone Name'] == option) & (d1['Destination Zone Name'] == destn) & (d1['Day Type'].isin(day_type)) & (d1['Day Part'] == "All Day (12am-12am)")].sort_values(by='Day Type', key=lambda x: pd.Categorical(x, categories=day_type))

# Ensure the length of day_type matches the number of rows in df5
day_type = df5['Day Type'].unique()
fig = px.bar(df5, y="Average Daily O-D Traffic (StL Index)", x="Day Type", text_auto='.2s', title=f"Traffic from {option} to {destn} on days of the week")
fig.update_xaxes(title_text="")  # Modify x-axis label
fig.update_yaxes(title_text="Trip Count")
col5.plotly_chart(fig, theme="streamlit")

day = col6.selectbox("Select a Day:", day_type)

# Filter DataFrame based on selected city
df6 = d1[(d1['Origin Zone Name'] == option) & (d1['Destination Zone Name'] == destn) & (d1['Day Type'] == day) & (d1['Day Part'].isin(day_part))].sort_values(by='Day Part', key=lambda x: pd.Categorical(x, categories=day_part))

fig = px.line(df6, x="Day Part", y="Average Daily O-D Traffic (StL Index)", markers=True, title=f"Traffic from {option} to {destn} on {day}")
fig.update_xaxes(title_text="", tickangle=45, showgrid=True)  # Modify x-axis label
fig.update_yaxes(title_text="Trip Count", showgrid=True)
col6.plotly_chart(fig, theme="streamlit")

df7 = df[(df['Origin Zone Name'] == option) & (df['Destination Zone Name'] == destn) & (df['Day Type'] == "All Days") & (df['Day Part'] == "All Day (12am-12am)")]

col7, col8 = st.columns(2)

home_to_work_sum = df7['Home to Work'].sum()
home_to_other_sum = df7['Home to Other'].sum()
non_home_based_trip_sum = df7['Non-Home Based Trip'].sum()

# Calculate percentages
total_trips = home_to_work_sum + home_to_other_sum + non_home_based_trip_sum
home_to_work_percentage = (home_to_work_sum / total_trips) * 100
home_to_other_percentage = (home_to_other_sum / total_trips) * 100
non_home_based_trip_percentage = (non_home_based_trip_sum / total_trips) * 100

# Data for pie chart
labels = ['Home to Work', 'Home to Other', 'Non-Home Based Trip']
values = [home_to_work_percentage, home_to_other_percentage, non_home_based_trip_percentage]

fig = px.pie(values=values, names=labels, title= f'Trip Distribution from  {option} to {destn}')
fig.update_traces(textposition='inside', textinfo='percent+label')
col7.plotly_chart(fig, theme="streamlit")

speed = df7['Avg All Trip Speed (mph)']
length = df7['Avg All Trip Length (mi)']
time = df7['Avg All Travel Time (sec)'] / 60

label1 = ['Average Trip Speed (mph)', 'Average Trip Length (mi)', 'Average Travel Time (min)']
value1 = [speed.mean(), length.mean(), time.mean()]

#fig = go.Figure(go.Bar(x=value1, y=label1, orientation='h'))

fig = go.Figure(go.Bar(x=value1, y=label1, orientation='h', marker=dict(color=['red', 'blue', 'green'])))
fig.update_layout(title=f"Trip Metrics from {option} to {destn}", xaxis_title="Value", yaxis_title="Metrics")
col8.plotly_chart(fig, use_container_width=True)

st.divider()

st.markdown("<h2 style='text-align: center;'>Vehicle Miles Traveled (VMT)</h2>", unsafe_allow_html=True)

vmt_list = [
    'Apple Valley', 'Chino', 'Chino Hills', 'Colton', 'Fontana', 'Highland', 
    'Hesperia', 'Ontario', 'Rancho Cucamonga', 'Redlands', 'Rialto', 
    'San Bernardino', 'Upland', 'Victorville', 'Yucaipa'
]

vmt_data_origin = df[df['Origin Zone Name'].isin(vmt_list) & df['Destination Zone Name'].isin(vmt_list)]
vmt_data_destination = df[df['Origin Zone Name'].isin(vmt_list) & df['Destination Zone Name'].isin(vmt_list)]

# Combine data for both origin and destination
combined_vmt_data = pd.concat([vmt_data_origin, vmt_data_destination])

# Calculate total VMT for each city
combined_vmt_data['Total VMT'] = combined_vmt_data['Average Daily O-D Traffic (StL Index)'] * combined_vmt_data['Avg All Trip Length (mi)']
total_vmt_per_city = combined_vmt_data.groupby('Origin Zone Name')['Total VMT'].sum().reset_index().nlargest(15, 'Total VMT')

# Calculate home VMT for each city
combined_vmt_data['Commute VMT'] = combined_vmt_data['Home to Work'] * combined_vmt_data['Avg All Trip Length (mi)']
home_vmt_per_city = combined_vmt_data.groupby('Origin Zone Name')['Commute VMT'].sum().reset_index().nlargest(15, 'Commute VMT')

# Create radio button to select between Total VMT and Home VMT
selected_option = st.radio("Select VMT Type", ('Total VMT', 'Commute VMT'))

# Update chart based on selected option
if selected_option == 'Total VMT':
    fig = px.bar(total_vmt_per_city, x='Origin Zone Name', y='Total VMT', text_auto='.2s', text='Total VMT', title="Total Vehicle Miles Traveled (VMT) per City")
    fig.update_xaxes(title_text="")  # Modify x-axis label
    fig.update_yaxes(title_text="Vehicle Miles Traveled")
else:
    fig = px.bar(home_vmt_per_city, x='Origin Zone Name', y='Commute VMT', text_auto='.2s', text='Commute VMT', title="Commute Vehicle Miles Traveled (VMT) per City")
    fig.update_xaxes(title_text="")  # Modify x-axis label
    fig.update_yaxes(title_text="Vehicle Miles Traveled")

st.plotly_chart(fig, use_container_width=True)