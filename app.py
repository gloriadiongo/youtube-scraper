import streamlit as st
import main
import clean_data
import pandas as pd
import io

st.header("Youtube scraper!!")

HANDLES = [
   "silabisaluofficiel3524",
"bellevuetv2706",
"kevinesydneyofficiel2833",
"lardytv911",
"canalcongoofficiel9601",
"kintheatre",
"RDCComediensCongolaisTV",
"GraceLuzoloMatondo",
"aidagladisofficiel2503",
"Jeremieshabani",
"Films243officiel",
"adailungatv",
"dinanaladouceofficielle1762",
"leketvofficielle2952",
"cardozokanduofficiel9443",
"omarikabongo7242",
"filmdramatique",
"gueshospoontv",
"ifokurenatetv7666",
"pierrotndombasitv5288",
"Films243officiel",
"exaucepapamunokotv8770",
"Fannymasudi-0fficielle11",
"michecomofficiel",
"esepelisa",
"bosskekeofficiel",
"batistatvofficiel7913",
"mimikabeyaofficieltv"
]

if "y_key" not in st.session_state:
    st.session_state['y_key'] = None

if 'handles' not in st.session_state:
    st.session_state['handles'] = HANDLES

y_key = st.text_input("Youtube API Key", type='password')
if y_key:
    st.session_state['y_key'] = y_key

def download_layout(df: pd.DataFrame):
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        # Write each dataframe to a different worksheet.
        df.to_excel(writer, sheet_name='Sheet1', index=False)
        writer.close()
        download2 = st.download_button(
            label="Download data as Excel",
            data=buffer,
            file_name='result.xlsx',
            mime='application/vnd.ms-excel'
        )

def add_handles():
    with st.form("Add new handle", clear_on_submit=True):
        new_h = st.text_input("Add a handle")
        if st.form_submit_button("Submit"):
            if new_h:
                st.session_state['handles'].append(new_h)

def remove_handles():
    with st.form("Remove handle", clear_on_submit=True):
        new_h = st.text_input("Remove handle")
        if st.form_submit_button("Submit"):
            if new_h:
                st.session_state['handles'].remove(new_h)

def show_handle():
    with st.expander("show handle"):
        st.write(st.session_state['handles'])
           
def main_page():
    add_handles()
    remove_handles()
    show_handle()
    number_of_days_to_scrape = st.number_input("Number of Days to scrape")
    if st.button("Start!"):
        if st.session_state['y_key']:
            with st.spinner():
                df = main.engine(st.session_state['y_key'], int(number_of_days_to_scrape), st.session_state['handles'])
                new_df = clean_data.main(df)
                download_layout(new_df)
            st.success("Done!")
        else:
            st.error("Your API Key is missing")
    
main_page()
        
