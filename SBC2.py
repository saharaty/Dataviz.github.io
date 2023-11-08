import pandas as pd
import json

df = pd.read_json("output.json")
df = df[df['state'] == 'hawaii']

tree_counts = df.groupby(['common_name', 'city']).size().reset_index(name='count')

top_tree_types = tree_counts.groupby('common_name')['count'].sum().nlargest(5).index
tree_counts['common_name'] = tree_counts['common_name'].apply(lambda x: x if x in top_tree_types else 'Other')

city_totals = df.groupby('city')['common_name'].count().reset_index(name='count')

data_dict = []

for tree_type in tree_counts['common_name'].unique():
    tree_data = tree_counts[tree_counts['common_name'] == tree_type][['city', 'count']].to_dict(orient='records')
    data_dict.append({"common_name": tree_type, "data": tree_data})

total_data = city_totals.to_dict(orient='records')
data_dict.append({"common_name": "Total", "data": total_data})

with open('tree_species_abundance_updated.json', 'w') as json_file:
    json.dump(data_dict, json_file, indent=4)
