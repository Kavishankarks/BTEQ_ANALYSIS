import streamlit as st

class PreProcessData :
    def __init__(self,df) -> None:
        self.actual_columns  = ['jcl', 'control_card', 'sql_liness', 'sql_number', 'query_type',
       'parse_status', 'table_mode', 'target_table', 'dependent_tables',
       'pipelineid', 'import_status', 'metadata_build',
       'metadata_build_status', 'error']
        self.actual_columns_next = [ 'file_name', 'sql_liness', 'sql_number', 'query_type',
       'parse_status', 'table_mode', 'target_table', 'dependent_tables',
       'pipelineid', 'import_status', 'metadata_build',
       'metadata_build_status', 'error'
        ]
        self.current_columns = df.columns
        self.df = df

    def update_columns_names(self) :
        if (len(self.df.columns) == 15) :
            self.df = self.df.drop(self.df.columns[-1], axis=1)
            self.current_columns = self.df.columns
        if(len(self.current_columns)== len(self.actual_columns) ):
            try :
                self.df = self.df.rename(columns = dict(zip(self.current_columns, self.actual_columns)))
            except :
                st.exception("Column count mismatch")
        else :
            # if "file" in self.df.columns :

            try :
                self.df = self.df.rename(columns = dict(zip(self.current_columns, self.actual_columns_next)))
            except :
                st.exception("Column count mismatch")

        if("file_name" in self.df.columns) :
                self.df[["jcl","control_card"]] = self.df["file_name"].str.rsplit('/',n=1,expand=True)
                self.df.drop("file_name", axis=1, inplace=True)
                self.df.insert(0, 'control_card', self.df.pop('control_card'))
                self.df.insert(0, 'jcl', self.df.pop('jcl'))
        return self.df

    def replace_nan_with_na(self):
        self.df.fillna("NA",inplace=True)