import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("All_Diets.csv")


numeric_cols = ['Protein(g)', 'Carbs(g)', 'Fat(g)']
df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())

avg_macros = df.groupby('Diet_type')[numeric_cols].mean().reset_index()

top_protein = (df.sort_values('Protein(g)', ascending=False)
               .groupby('Diet_type')
               .head(5))

diet_protein_totals = df.groupby('Diet_type')['Protein(g)'].mean()
highest_protein_diet = diet_protein_totals.idxmax()
print("Highest protein diet type:", highest_protein_diet)

most_common_cuisines = (df.groupby(['Diet_type', 'Cuisine_type'])
                          .size()
                          .reset_index(name='count'))
most_common_cuisines = (most_common_cuisines
                        .sort_values(['Diet_type', 'count'], ascending=[True, False]))
print(most_common_cuisines.groupby('Diet_type').head(3))

df['Protein_to_Carbs_ratio'] = df['Protein(g)'] / df['Carbs(g)']
df['Carbs_to_Fat_ratio'] = df['Carbs(g)'] / df['Fat(g)']


# Bar chart
plt.figure(figsize=(10, 5))
sns.barplot(data=avg_macros, x='Diet_type', y='Protein(g)')
plt.xticks(rotation=45)
plt.title('Average Protein by Diet Type')
plt.tight_layout()
plt.show()

# Bar chart
avg_macros_melt = avg_macros.melt(id_vars='Diet_type',
                                  value_vars=numeric_cols,
                                  var_name='Macronutrient',
                                  value_name='Average')
plt.figure(figsize=(10, 5))
sns.barplot(data=avg_macros_melt, x='Diet_type', y='Average', hue='Macronutrient')
plt.xticks(rotation=45)
plt.title('Average Macros by Diet Type')
plt.tight_layout()
plt.show()

# Heatmap
heatmap_data = avg_macros.set_index('Diet_type')
plt.figure(figsize=(8, 6))
sns.heatmap(heatmap_data, annot=True, cmap='viridis')
plt.title('Average Macronutrients per Diet Type')
plt.tight_layout()
plt.show()

# Scatter
plt.figure(figsize=(10, 6))
sns.scatterplot(data=top_protein,
                x='Protein(g)',
                y='Carbs(g)',
                hue='Cuisine_type',
                style='Diet_type')
plt.title('Top 5 Protein-Rich Recipes per Diet Type')
plt.tight_layout()
plt.show()