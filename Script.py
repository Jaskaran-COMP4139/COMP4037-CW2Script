%%writefile app.py 

import streamlit as st   # Importing necessary libraries
import plotly.express as px
import pandas as pd
import numpy as np


st.title("COMP4037 Research Methods")
st.title("Interactive Treemap Dashboard")


st.markdown("""       
    <style>
        .sidebar .sidebar-content {
            transform: translateX(calc(100% - 250px));
        }
        .title-wrapper {
            width: 100%;
        }
    </style>
""", unsafe_allow_html=True
           )


selected_df = st.sidebar.radio("Select Data:", options=['Kcal Adjusted', 'No Kcal Adjusted']) # Selecting Dataset
if selected_df == 'Kcal Adjusted':
    df = pd.read_csv("Results_21MAR2022.csv")
else:
    df = pd.read_csv("Results_21MAR2022_nokcaladjust.csv")


replace_dict = {'20-29' : 'Young Adults',   # Editing Categorical Features
                '30-39' : 'Early Adults', 
                '40-49' : 'Midlife Adults',
                '50-59' : 'Mature Adults',
                '60-69' : 'Senior Adults',
                '70-79' : 'Elders',
                }
df['age_group'] = df['age_group'].replace(replace_dict)


replace_dict = {'fish' : 'Pescatarians ',
                'meat100' : 'Heavy Meat Eaters',
                'meat50' : 'Low Meat Eaters',
                'meat' : 'Moderate Meat Eaters',
                'vegan' : 'Vegans',
                'veggie' : 'Vegetarian',
                }
df['diet_group'] = df['diet_group'].replace(replace_dict)


replace_dict = {'female' : 'Female ',
                'male' : 'Male',
                }
df['sex'] = df['sex'].replace(replace_dict)



selected_columns = ['mean_ghgs', 'mean_land', 'mean_watscar', 'mean_eut', 'mean_bio', 'mean_watuse', 'mean_acid'] # Selecting Features for Treemap
df_selected = df[selected_columns]
normalized_df = 100 * (df_selected - df_selected.min()) / (df_selected.max() - df_selected.min()) # Normalizing Features
df['Environmental Factor'] = normalized_df.mean(axis=1) # Calculating Environmental Factor



option = False
if option:
    st.subheader(f"Effect of: {option}")

with st.sidebar:
    st.title("Filter Options")
    age_groups = df['age_group'].unique().tolist()
    age_groups.insert(0, "All")  # Inserting "All" option
    grouping_option = st.selectbox("Select Age Group:", options=age_groups)
    option = st.radio("Select Feature to Visualize:", options=['mean_ghgs', 'mean_land', 'mean_watscar', 'mean_eut', 'mean_bio', 'mean_watuse', 'mean_acid', 'Environmental Factor'])


st.header("Treemap Visualization")

col1, col2 = st.columns([3, 8]) 

if grouping_option == 'All':
    filtered_df = df
else:
    filtered_df = df[df['age_group'] == grouping_option]



# Treemap Visualization
fig = px.treemap(data_frame=filtered_df,
                 path=['diet_group', 'age_group', 'sex'],
                 values=option,
                 color=option,
                 color_continuous_scale='RdYlGn_r',
                 width=2000,
                 height=1000)
fig.update_traces(textfont_size=25)  
fig.update_layout(coloraxis_colorbar=dict(len=1.0, yanchor='middle', y=0.5, title_font=dict(size=30)))  # Increasing color bar text size


col1.plotly_chart(fig, use_container_width=False)
empty_column = col2.empty()
