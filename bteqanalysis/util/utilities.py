import re
import streamlit as st


class Utils :
    def __init__(self,df):
        self.df = df

    def keyword_error(self):
        text_input = st.text_input("Search Error")
        if text_input and st.button("Submit") :
            dff =self.df[self.df["error"] != None]
            errors = dff[dff["error"].str.contains(text_input,case=False)]
            st.write(errors)

    def search_target_table(self):
        unique_tables = {}
        for i in self.df["target_table"]:
            if i  not in unique_tables and type(i) == str:
                unique_tables[i] = 1
        selected_table = st.selectbox("Select table",unique_tables.keys())
        if st.button("Search table"):
            dff = self.df[self.df["target_table"] != None]

            target_table = dff[dff["target_table"].str.contains(selected_table,case=False)]
            metadata, parser , sqlimport = self.get_individual_table(target_table)
            st.write(target_table)
            st.write("\t\tParser Error",parser)
            st.write("\t\tSQL Import Error",sqlimport)
            st.write("\t\tMetadata Error",metadata)



    def extractSchemaTable(self,text):
        if(type(text) != str or "Cant" not in text) :
            return None
        pattern = r"schema:\s*(\w+)\s+and\s+table\s+name:\s*(\w+)"
        match = re.search(pattern, text)
        if match:
            return "Schema : " + match.group(1) + " Table : " + match.group(2)
        else :
            return None

    def get_table_not_found(self):
        errors = self.df[self.df["import_status"]=="Failed"]
        tables_count = 0
        for i in errors["error"]:
            res = self.extractSchemaTable(i)
            if(res):
                tables_count += 1
                st.write(res)
        st.write("Total table count : ",tables_count)

    def get_individual_table(self, target_table):
        return (target_table["metadata_build_status"] == "failed").sum() , (target_table["parse_status"] == "Failed").sum(), (target_table["import_status"] == "Failed").sum()

    def get_table_completed(self,list_error):
        unique_tables = {}
        for i in self.df["target_table"]:
            if i  not in unique_tables and type(i) == str:
                unique_tables[i] = 1
        dff = self.df[self.df["target_table"] != None]
        dff.fillna("NA",inplace=True)
        fully_completed =0
        cnt = 1
        for i in unique_tables.keys():
            target_table = dff[dff["target_table"] == i]
            metadata, parser , sqlimport = self.get_individual_table(target_table)
            if (metadata ==0 and parser ==0 and sqlimport ==0):
                st.write(str(cnt) + ". Table Name : " + i + " Total SQL's :  " + str(len(target_table))  + " Completed ✅ " )
                fully_completed += 1
            else :
                st.write(str(cnt) + ". Table Name : " + i )
                col1, col2, col3, col4, col5 = st.columns(5)
                col2.metric("Total SQL's ",len(target_table))
                col3.metric("Parser Error",parser)
                col4.metric("SQL Import Error",sqlimport)
                col5.metric("Metadata Error",metadata)
                if list_error:
                    st.write(target_table)
            cnt += 1
        st.subheader("Fully completed : " + str(fully_completed) + " out of : " + str(cnt))

    def get_jcl_completed(self,list_error):
        # compare_with_last = st.selectbox("Compare with last",("Yes","No"))
        # if compare_with_last == "Yes" :
        #     upload_last_file = st.file_uploader("Chosse last run report")
        #     last_run_self.df= pd.read_csv(upload_last_file)
        #     st.write(last_run_self.df)
        # else :
        unique_jcls = {}
        for i in self.df["jcl"]:
            if i  not in unique_jcls and type(i) == str:
                unique_jcls[i] = 1
        # st.write(unique_jcls.keys())
        # st.write(len(unique_jcls))
        dff = self.df[self.df["jcl"] != None]
        dff.fillna("NA",inplace=True)
        fully_completed =0
        cnt = 1
        for i in unique_jcls.keys():
            target_jcl = dff[dff["jcl"] == i]
            metadata, parser , sqlimport = self.get_individual_table(target_jcl)
            if (metadata ==0 and parser ==0 and sqlimport ==0):
                st.subheader(str(cnt) + ". Table Name : " + i  + " Completed ✅ " )
                cola1, cola2 = st.columns(2)
                cola1.metric(" Total SQL's :  " , str(len(target_jcl)) )
                fully_completed += 1
            else :
                total_failed = metadata + parser + sqlimport
                st.subheader(str(cnt) + ". JCL : " + i )
                col1, col2, col3, col4, col5 = st.columns(5)
                col2.metric("Total SQL's ",len(target_jcl))
                col3.metric("Parser Error",parser)
                col4.metric("SQL Import Error",sqlimport)
                col5.metric("Metadata Error",metadata)
                if list_error:
                    st.write(target_jcl)
            cnt += 1
        st.subheader("Fully completed : " + str(fully_completed) + " out of : " + str(cnt))

    def error_display(self):
        tab1, tab2, tab3 = st.tabs(["Parser error","SQL Import error", "Metadata build error"])

        with tab1 :
            import_error = self.df[self.df["parse_status"]=="Failed"]
            st.write(import_error)
        with tab2 :
            parser_error = self.df[self.df["import_status"]=="Failed"]
            st.write(parser_error)
        with tab3:
            metadata_error = self.df[self.df["metadata_build_status"]=="failed"]
            st.write(metadata_error)