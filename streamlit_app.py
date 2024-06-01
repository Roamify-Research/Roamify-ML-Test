import pandas as pd
import streamlit as st

def load_data():
    attractions_data = pd.read_csv('final_attractions.csv', usecols=['Name', 'State', 'City', 'Opening Hours', 'Description'])
    user_ratings_data = pd.read_csv('user_ratings.csv', usecols=['Attraction', 'Noel', 'Harsh', 'Vikranth', 'Muthuraj', 'Armaan'])
    return attractions_data, user_ratings_data

def load_user_data(user):
    attractions_data = pd.read_csv('final_attractions.csv', usecols=['Rating', 'Name', 'State', 'City', 'Country', 'Opening Hours', 'Description'])
    user_ratings_data = pd.read_csv('user_ratings.csv', usecols=['Attraction', user])
    
    attractions_data.rename(columns={'Rating': 'Google_Rating'}, inplace=True)
    attractions_data['User_Rating'] = user_ratings_data[user]

    usecols=['Name','Google_Rating','User_Rating', 'State', 'City','Country', 'Opening Hours', 'Description']
    return attractions_data[usecols]

def get_recommendations(state, number_of_attractions, user):
    attractions_data, user_ratings_data = load_data()
    
    attraction_names = []
    attractions_description = {}
    for i in range(len(attractions_data)):
        if attractions_data['State'][i] == state:
            attraction_names.append(attractions_data['Name'][i])
            attractions_description[attractions_data['Name'][i]] = [
                attractions_data['City'][i], 
                attractions_data['Opening Hours'][i], 
                attractions_data['Description'][i]
            ]

    attractions = {}
    for i in range(len(user_ratings_data)):
        if user_ratings_data['Attraction'][i] in attraction_names:
            attractions[user_ratings_data['Attraction'][i]] = user_ratings_data[user][i]

    attractions_sorted = dict(sorted(attractions.items(), key=lambda item: item[1], reverse=True))

    if len(attractions_sorted) < number_of_attractions:
        message = f"Only {len(attractions_sorted)} attractions are available in {state} for {user}."
        number_of_attractions = len(attractions_sorted)
    else:
        message = None

    recommendations = []
    count = 0
    for name in attractions_sorted.keys():
        if count == number_of_attractions:
            break
        count += 1
        recommendations.append({
            'Name': name,
            'City': attractions_description[name][0],
            'Opening Hours': attractions_description[name][1],
            'Description': attractions_description[name][2]
        })

    return recommendations, message


attractions_data, user_ratings_data = load_data()

st.markdown("<h1 style='text-align: center;'>Roamify</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Tourist Attraction Recommendation System</h3>", unsafe_allow_html=True)

state = st.selectbox('Select State', attractions_data['State'].unique())

number_of_attractions = st.number_input('Number of Attractions', min_value=1, max_value=20, value=5, step=1)

user = st.selectbox('Select User', user_ratings_data.columns[1:]) 

if st.button('Get Recommendations'):
    recommendations, message = get_recommendations(state, number_of_attractions, user)
    
    if message:
        st.warning(message)

    st.write(f"<h3>Top {number_of_attractions} attractions in {state} for {user}:</h2>", unsafe_allow_html=True)
    st.write("***************************************************")
    for rec in recommendations:
        st.write(f"**Attraction name:** {rec['Name']}")
        st.write(f"**City:** {rec['City']}")
        st.write(f"**Opening Hours:** {rec['Opening Hours']}")
        st.write(f"**Description:** {rec['Description']}")
        st.write("***************************************************")

if st.checkbox('Show Raw Data'):
    st.write('Attractions and User Ratings Data')
    user_ratings_data = load_user_data(user)
    st.dataframe(user_ratings_data)