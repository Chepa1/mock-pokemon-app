import streamlit as st
import requests
import pandas as pd

# Default page config with custom width
st.set_page_config(
    layout="centered",
    initial_sidebar_state="collapsed",
    page_title="Pokemon Filter"
)

# Add custom CSS to increase the main content width and hide sidebar
st.markdown("""
    <style>
        .block-container {
            max-width: 1500px;  /* Increased from 1200px */
            padding-top: 1rem;
            padding-bottom: 0rem;
        }
        section[data-testid="stSidebar"][aria-expanded="true"] {
            display: none !important;
        }
        section[data-testid="stSidebar"][aria-expanded="false"] {
            display: none !important;
        }
        .st-emotion-cache-1cypcdb {
            display: none !important;
        }
        .stDataFrame div[data-testid="stHorizontalBlock"] {
            overflow: hidden;
        }
        /* Hide all scrollbars */
        ::-webkit-scrollbar {
            display: none;
        }
        .element-container {
            scrollbar-width: none;  /* Firefox */
            -ms-overflow-style: none;  /* IE and Edge */
        }
        div[data-testid="stDataFrame"] > div {
            overflow: hidden !important;
        }
        /* Additional selectors for scrollbars */
        .main .block-container {
            overflow-x: hidden;
            max-width: 1500px;  /* Match the container width */
        }
        [data-testid="stDataFrame"] {
            width: 100%;
            max-width: 1500px;  /* Match the container width */
        }
        iframe {
            width: 100%;
            max-width: 1500px;  /* Match the container width */
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
                response = requests.get(
                    f"http://localhost:8000/letter_filter/{letter_filter_selected}/{st.session_state.selected_letter}"
                )
                if response.status_code == 200:
                    pokemon_list = response.json()
                    if pokemon_list:
                        # Convert the list of dictionaries to a pandas DataFrame
                        df = pd.DataFrame(pokemon_list)
                        # Reorder columns if needed
                        columns_order = ['Name', 'Type1', 'Type2', 'Total', 'HP', 'Attack', 
                                       'Defense', 'SpAtk', 'SpDef', 'Speed', 'Height', 'Weight']
                        df = df[columns_order]
                        # Display the results count
                        st.write(f"Found {len(pokemon_list)} Pokemon:")
                        
                        # Calculate dynamic height (35 pixels per row including header)
                        row_height = 35
                        dynamic_height = (len(pokemon_list) + 2) * row_height  # Add one extra row for buffer
                        
                        # Container with custom width
                        with st.container():
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
            
