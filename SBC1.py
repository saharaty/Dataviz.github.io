import pandas as pd
import json

df = pd.read_json("output.json")
df = df[df['state'] == 'hawaii']

tree_counts = df['common_name'].value_counts()

top_tree_types = tree_counts.head(5).index
df['common_name'] = df['common_name'].apply(lambda x: x if x in top_tree_types else 'Other')

grouped_df = df.groupby(["city", "common_name"]).size().reset_index(name='count')

sorted_df = grouped_df.sort_values(by=['common_name', 'count'], ascending=[False, False])

json_data = sorted_df.to_dict(orient='records')

with open('tree_species_abundance.json', 'w') as json_file:
    json.dump(json_data, json_file, indent=4)
