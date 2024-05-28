import streamlit as st
import main
import clean_data

st.header("Youtube scraper!!")

HANDLES = [
    "etoileshowlive333",
    "dinanaladouceofficielle1762",
    # "kelbulmag5655",
    # "RDCComediensCongolaisTV",
    # "jeremieshabaniofficiel3323",
    # "RDCCINEMATV",
    # "CongofranceCFTv1",
    # "lepeupleparletv",
    # "majorbisadiditv9874",
    # "bellevuetv2706",
    # "BRAVOCINE",
    # "rdcongo83",
    # "kevinesydneyofficiel2833",
    # "kintheatre",
    # "canalcongoofficiel9601",
]

if "y_key" not in st.session_state:
    st.session_state['y_key'] = None

if 'handles' not in st.session_state:
    st.session_state['handles'] = HANDLES

y_key = st.text_input("Youtube API Key", type='password')
if y_key:
    st.session_state['y_key'] = y_key
    
def convert_df(df):
    return df.to_csv().encode("utf-8")

def download_layout(df):
    csv = convert_df(df)
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name="result.csv",
        mime="text/csv",
    )
  
def add_handles():
    with st.form("Add new handle", clear_on_submit=True):
        new_h = st.text_input("Add a handle")
        if st.form_submit_button("Submit"):
            if new_h:
                st.session_state['handles'].append(new_h) 
    
def main_page():
    add_handles()
    number_of_days_to_scrape = st.number_input("Number of Days to scrape")
    if st.button("Start!"):
        if st.session_state['y_key']:
            with st.spinner():
                df = main.engine(st.session_state['y_key'], int(number_of_days_to_scrape), st.session_state['handles'])
                df.to_csv('sample2.csv', index=False)
                new_df = clean_data.main(df)
                download_layout(new_df)
            st.success("Done!")
        else:
            st.error("Your API Key is missing")
    
main_page()
        