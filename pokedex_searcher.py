import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import requests

st.title("Pokemon Explorer!")

### stretch goal -> carousel wheel to flick through sprites of all generations

# Use whole pokedex!

#@st.cache_data will only run when the cache is unavailable


type_colors = {'ground': 'brown',
               'electric': 'yellow',
               'water': 'blue',
               'poison': 'darkviolet',
               'grass': 'green',
               'fire': 'red',
               'rock': 'darkgoldenrod',
               'normal': 'gray',
               'ice': 'turquoise',
               'fighting': 'maroon',
               'flying': 'violet',
               'psychic': 'fuchsia',
               'bug': 'lime',
               'ghost': 'purple',
               'dragon': 'blueviolet',
               'dark': 'darkred',
               'steel': 'silver',
               'fairy': 'pink'
               }

def get_details(poke_number):
    try:
        url = f'https://pokeapi.co/api/v2/pokemon/{poke_number}/'
        response = requests.get(url)
        pokemon = response.json()
        return pokemon['name'], pokemon['height'], pokemon['weight'], len(pokemon['moves'])
    except:
        return 'Error', None, None, None, None, None
    

def get_sprites(poke_number):
    try:
        url = f'https://pokeapi.co/api/v2/pokemon/{poke_number}/'
        response = requests.get(url)
        pokemon = response.json()
        return pokemon['sprites']
    except:
        return 'Error'

def get_cries(poke_number):
    try:
        url=f'https://pokeapi.co/api/v2/pokemon/{poke_number}/'
        response = requests.get(url)
        pokemon = response.json()
        return pokemon['cries']['latest']
    except:
        return "crying error :'("

def get_types(poke_number):
    try:
        url=f'https://pokeapi.co/api/v2/pokemon/{poke_number}/'
        response = requests.get(url)
        pokemon = response.json()
        types = []
        for tp in pokemon['types']:
            types.append(tp['type']['name'])
        return types
    except:
        return 'typing error'



pokemon_number = st.slider("Pick a Pokemon",
                           min_value=1,
                           max_value=1025
                           )

name, height, weight, moves = get_details(pokemon_number)
height = height * 10
weight = weight / 10
sprites = get_sprites(pokemon_number)
cry = get_cries(pokemon_number)
types = get_types(pokemon_number)
height_data = {'Pokemon': ['Caterpie', name.title(), 'Arbok'],
               'Height /cm': [30, height, 350]}

colors = [type_colors['bug'], type_colors[types[0]], type_colors['poison']]

graph = sns.barplot(data = height_data,
                    x = 'Pokemon',
                    y = 'Height /cm',
                    palette = colors)

st.image(sprites['front_default'], use_column_width='auto', clamp=False, channels="RGB", output_format="auto")
st.audio(cry, format="audio/wav")
name_stat, height_stat, weight_stat, move_stat, type_stat = st.columns(5)
if len(types) > 1:
    type_text = "Types"
else:
    type_text = "Type"

with name_stat:
    st.write('Name')
    st.write(name.title())
with height_stat:
    st.write('Height') 
    st.write(f'{height} cm')
with weight_stat:
    st.write('Weight') 
    st.write(f'{weight} kg')
with move_stat:
    st.write('Move Count') 
    st.write(str(moves))
with type_stat:
    st.write(type_text) 
    st.write(", ".join(types))

st.pyplot(graph.figure)