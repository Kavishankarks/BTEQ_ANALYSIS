import streamlit as st
class JiraMappingHelper :
    def __init__(self,df_mapping) -> None :
        self.actual_columns = ["jira_id","error"]
        self.current_columns = df_mapping.columns
        self.df_mapping = df_mapping

    def update_column_names(self) :
        if(len(self.current_columns)== len(self.actual_columns) ):
            try :
                self.df_mapping = self.df_mapping.rename(columns = dict(zip(self.current_columns, self.actual_columns)))
            except :
                st.exception("Column count mismatch")
        return self.df_mapping