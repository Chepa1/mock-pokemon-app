import streamlit as st
import requests
import pandas as pd

# Default page config with custom width
st.set_page_config(
    layout="centered",
    initial_sidebar_state="collapsed",
    page_title="Pokemon Filter"
)

# Add custom CSS to increase the main content width and hide scrollbars
st.markdown("""
    <style>
        .block-container {
            max-width: 1500px;
            padding-top: 1rem;
            padding-bottom: 0rem;
        }
        section[data-testid="stSidebar"][aria-expanded="true"], 
        section[data-testid="stSidebar"][aria-expanded="false"] {
            display: none !important;
        }
        div[data-testid="stDataFrame"] > div {
            overflow: hidden !important;
        }
    </style>
""", unsafe_allow_html=True)

st.title("Pokemon Filter")

# Initialize session state
if 'selected_letter' not in st.session_state:
    st.session_state.selected_letter = None

with st.expander("Filter by letter"):
    letter_filter_options = ["Starts with", "Contains", "Ends with"]
    letter_filter_selected = st.segmented_control(
        label="Filter by",
        options=letter_filter_options,
        selection_mode="single"
    )
    
    # Alphabet buttons
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    letter_display = st.empty()

    # Create letter buttons in rows of 13
    for i, letter in enumerate(alphabet):
        if i % 13 == 0:
            cols = st.columns(13)
        with cols[i % 13]:
            if st.button(letter, key=letter):
                st.session_state.selected_letter = letter

    letter_display.write(f"Selected letter: {st.session_state.selected_letter}")

    if st.button("Filter"):
        if st.session_state.selected_letter and letter_filter_selected:
            try:
                BACKEND_URL = "https://web-production-bd54.up.railway.app"
                response = requests.get(f"{BACKEND_URL}/letter_filter/{letter_filter_selected}/{st.session_state.selected_letter}")
                if response.status_code == 200:
                    pokemon_list = response.json()
                    if pokemon_list:
                        df = pd.DataFrame(pokemon_list)
                        columns_order = ['Name', 'Type1', 'Type2', 'Total', 'HP', 'Attack', 
                                       'Defense', 'SpAtk', 'SpDef', 'Speed', 'Height', 'Weight']
                        df = df[columns_order]
                        st.write(f"Found {len(pokemon_list)} Pokemon:")
                        
                        # Calculate dynamic height
                        row_height = 35
                        dynamic_height = (len(pokemon_list) + 2) * row_height
                        
                        st.dataframe(
                            df,
                            hide_index=True,
                            use_container_width=True,
                            height=dynamic_height,
                            column_config={
                                "Name": st.column_config.TextColumn(width=150),
                                "Type1": st.column_config.TextColumn(width=100),
                                "Type2": st.column_config.TextColumn(width=100),
                                "Total": st.column_config.NumberColumn(width=100),
                                "HP": st.column_config.NumberColumn(width=100),
                                "Attack": st.column_config.NumberColumn(width=100),
                                "Defense": st.column_config.NumberColumn(width=100),
                                "SpAtk": st.column_config.NumberColumn(width=100),
                                "SpDef": st.column_config.NumberColumn(width=100),
                                "Speed": st.column_config.NumberColumn(width=100),
                                "Height": st.column_config.NumberColumn(width=100),
                                "Weight": st.column_config.NumberColumn(width=100)
                            }
                        )
                    else:
                        st.write("No Pokemon found matching your criteria.")
                else:
                    st.error("Failed to fetch Pokemon data")
            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to the backend: {str(e)}")
            
