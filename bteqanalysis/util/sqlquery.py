import streamlit as st
from streamlit_ace import st_ace
import pandasql as psql
import pandas as pd

class SqlQuery :

    def sql_query_editor(report) :
        st.title("SQL asQuery Editor")
        st.write("Table name is : report")
        st.write("report columns : ",str(report.columns.values).replace("' '",","))
        mapping_check = st.checkbox("Add mapping file")
        if mapping_check :
             mapping_file  = st.file_uploader("Choose a mapping file")
             if mapping_file is not None :
                  mapping = pd.read_csv(mapping_file)
                  st.write("Mapping table name is : mapping")
                  st.write("columns : ",str(mapping.columns.values))

        sql_codes = """SELECT *
FROM report"""
        
        sql_code = st_ace(
                value=sql_codes,
                language="sql",
                theme="twilight",
                height=250,
                font_size=14,
                auto_update=True,
                wrap=True,
                keybinding="sublime"
            )
            # Display the SQL code
        st.write("SQL code:")
        st.code(sql_code, language="sql")
            # sql_query = st.text_area('Enter SQL query:')
        if st.button("Submit"):
                try:
                    result = psql.sqldf(sql_code)
                    # Display the results
                    st.title("SQL Query Results")
                    st.write(result)
                    csv_data = result.to_csv(index=False)
                    st.download_button('Download CSV', data=csv_data, file_name='data.csv', mime='text/csv')
                    # Add a download button for Excel file
                    # excel_data = result.to_excel(index=False)
                    # st.download_button('Download Excel', data=excel_data, file_name='data.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

                    # Add a download button for JSON file
                    json_data = result.to_json()
                    st.download_button('Download JSON', data=json_data, file_name='data.json', mime='application/json')
                except Exception as e:
                    st.write('Invalid SQL query',e)
    

    def sql_query(report,query) :
         try:
              res = psql.sqldf(query)
              return res
         except Exception as e:
              return ("Error while executing ",e)