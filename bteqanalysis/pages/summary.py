import streamlit as st
class Summary :
    def __init__(self,df):
        self.df = df
        
    def get_metadata_completed(self):
        return (self.df["metadata_build_status"] == "completed").sum()
    
    def get_metadata_failed(self):
        return (self.df["metadata_build_status"] == "failed").sum()
    
    def get_parse_completed(self):
        return (self.df["parse_status"] == "Success").sum()
    
    def get_parse_failed(self):
        return (self.df["parse_status"] == "Failed").sum()
        
    def get_import_completed(self):
        return (self.df["import_status"] == "Success").sum()
    
    def get_import_failed(self):
        return (self.df["import_status"] == "Failed").sum()
    
    def buildSummary(self):
        st.write("Summary")
        col1, col2, col3, col4= st.columns(4)
        col1.metric("Total SQL's : ",len(self.df))
        col2.metric("Parsing Completed",self.get_parse_completed())
        col3.metric("SQL Import Completed",self.get_import_completed())
        col4.metric("Metadata build Completed",self.get_metadata_completed())
        col2.metric("Parsing Failed : " ,self.get_parse_failed())
        col3.metric("SQL Import Failed : ", self.get_import_failed())
        col4.metric("Metadata build failed : ", self.get_metadata_failed())