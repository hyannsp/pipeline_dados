from mongo import _Mongo  
import pandas as pd


# Optado por criar uma classe que herda do mongo para conseguir ter uma manipulação dos dataframes em conjunto com os dados em nuvem

class MongoDataFrame(_Mongo):
    def __init__(self, uri, db_name, collection_name):
        super().__init__(uri, db_name, collection_name)
        self.dfs = {}
    
    def load_to_dataframe(self, query={}, name=None):
        try:
            if not name:
                name = f"dataFrame_{len(self.dfs)}"
            documents = self.find_many(query)
            self.dfs[name] = pd.DataFrame(documents)
            
            if '_id' in self.dfs[name].columns:
                self.dfs[name]['_id'] = self.dfs[name]['_id'].astype(str)

            print(f"Loaded {len(self.dfs[name])} documents into DataFrame '{name}'")
        except Exception as e:
            print(f"Error loading DataFrame '{name}': {e}")
            self.dfs[name] = pd.DataFrame()

    def format_date_columns(self, name, columns_name, date_format="%m/%d/%Y", final_format="%Y-%m-%d"):
        if name not in self.dfs or self.dfs[name].empty:
            print(f"DataFrame '{name}' is empty. Nothing to process.")
            return
    
        valid_columns = [col for col in columns_name if col in self.dfs[name].columns]
        if not valid_columns:
            print(f"None of the specified columns exist in DataFrame '{name}'")
            return

        try:
            for col in valid_columns:
                self.dfs[name][col] = pd.to_datetime(self.dfs[name][col], format=date_format).dt.strftime(final_format)
            print(f"Formatted columns {valid_columns} in DataFrame '{name}'")
        except Exception as e:
            print(f"Error formatting columns {valid_columns} in '{name}': {e}")

    def save_to_csv(self, name, file_path):
        if name not in self.dfs or self.dfs[name].empty:
            print(f"DataFrame '{name}' is empty. Nothing to save.")
            return
        
        try:
            self.dfs[name].to_csv(file_path, index=False)
            print(f"DataFrame '{name}' saved as {file_path}")
        except Exception as e:
            print(f"Error saving DataFrame '{name}': {e}")

    def df_to_list(self, name):
        if name not in self.dfs or self.dfs[name].empty:
            print(f"DataFrame '{name}' is empty. Nothing to save.")
            return
        
        return [tuple(row) for i, row in self.dfs[name].iterrows()]