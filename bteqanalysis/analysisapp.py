import pandas as pd
import streamlit as st
import numpy as np
from pages.summary import Summary
from pages.documentation import display_docs 

from util.preprocess import PreProcessData
from util.utilities import Utils
from util.sqlquery import SqlQuery
from util.mappingfileprep import JiraMappingHelper
# st.title("Analyzing BTEQ Run: A Comprehensive Evaluation of Results ")


st.set_page_config(
    page_title="IWX BTEQ Run Analysis",
    page_icon="./assets/IWX_transp.png",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "# Tool to analyse the BTEQ Run report "
    }
)

with st.sidebar:
    select_screen = st.sidebar.selectbox("Option", ("BTEQ Run Analysis","Compare two BteqRun Reports","Error Level Analysis","Documentation"))


uploaded_file = st.file_uploader("Choose a file")

    
if select_screen == "BTEQ Run Analysis" :
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        preprocess = PreProcessData(df)
        df = preprocess.update_columns_names()
        preprocess.replace_nan_with_na()
        st.title("Run report")
        st.write(df)

        summary = Summary(df)
        summary.buildSummary()

        sql_run = st.checkbox("Run SQL Queries")
        if sql_run :
            SqlQuery.sql_query_editor(df)
        st.header("Aggregated Errors")
        exclude_table =st.checkbox("Exclude table not found")
        if st.button("Get Aggregated Error") :
            query = "select distinct error from report"
            if exclude_table :
                query = query + " where error not like \"%Cant Find any table with%\" "
            res = SqlQuery.sql_query(df,query)
            st.write("Total unique errors : ",len(res))
            st.write(res)

            
        utils = Utils(df)
        st.header("Classified Error")
        utils.error_display()
        utils.keyword_error()
        utils.search_target_table()
        s = st.checkbox("List errors")
        if st.button("Get table analysis") :
            utils.get_table_completed(s)
        if st.button("Get JCL analysis") :
            utils.get_jcl_completed(s)
        uploaded_jira_mapping = st.file_uploader("Chose Jira Mapping ")
        if st.button("Get All Tables Not Found"):
            utils.get_table_not_found()
        if uploaded_jira_mapping is not None :
                df_jira = pd.read_csv(uploaded_jira_mapping)
                # df_jira.columns = df_jira.columns.str.lower().str.replace(' ', '_')
                jiramap = JiraMappingHelper(df_jira)
                df_jira = jiramap.update_column_names()
                df_jira["error"] = df_jira["error"].str.replace('""',"")
                dff = df[df["target_table"] != None]
                dff.fillna("NA",inplace=True)
                dff["error"] = dff["error"].str.replace('""',"")
                cnt =0
                for i in df_jira["error"] :
                    cnt += 1
                    try :
                        error_df = dff[dff["error"] == i]
                        if(not error_df.empty):
                            st.write(df_jira["jira_id"][cnt])
                            st.write(error_df)
                    except Exception as e :
                        st.exception(f'unknown exception {e}') 
        # st.write("sd")


elif(select_screen=="Compare two BteqRun Reports") :
     if uploaded_file is not None:
        st.write("Compare two Bteq")
        uploaded_file_second = st.file_uploader("Choose a compare file")
        df1 = pd.read_csv(uploaded_file)
        if uploaded_file_second :
            df2 = pd.read_csv(uploaded_file_second)

            #preprocess both files
            preprocess_df1 = PreProcessData(df1)
            df1 = preprocess_df1.updateColumnsNames()
            preprocess_df1.replace_nan_with_na()
            
            preprocess_df2 = PreProcessData(df2)
            df2 = preprocess_df2.updateColumnsNames()
            preprocess_df2.replace_nan_with_na()

            if(len(df1) == len(df2)) :
                if df1.equals(df2):
                    st.write("The two DataFrames are identical.")
                else :
                    st.write("Comparing the Run files")
            else :
                st.write("Not able to compare because of missmatch in file sizes")

elif select_screen == "Error Level Analysis" :
     if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write('Original DataFrame:')
        st.write(df.columns)

        # Allow the user to edit the dataframe
        edited_df = st.experimental_data_editor(df) # 👈 An editable dataframe
        st.write(edited_df)
        # favorite_command = edited_df.loc[edited_df["rating"].idxmax()]["command"]
        # st.markdown(f"Your favorite command is **{favorite_command}** 🎈")
        

elif select_screen == "Documentation" :
    display_docs()