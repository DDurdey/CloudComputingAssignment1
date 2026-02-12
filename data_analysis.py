import os
import pandas as pd
import seaborn as sns

import matplotlib
matplotlib.use("Agg")  # headless backend for CI
import matplotlib.pyplot as plt

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load dataset
df = pd.read_csv("All_Diets.csv")

# Clean numeric columns
numeric_cols = ["Protein(g)", "Carbs(g)", "Fat(g)"]
df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")
df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean(numeric_only=True))

# Averages by diet
avg_macros = df.groupby("Diet_type")[numeric_cols].mean().reset_index()
avg_macros.to_csv(os.path.join(OUTPUT_DIR, "avg_macros_by_diet.csv"), index=False)

# Top 5 protein recipes per diet
top_protein = (
    df.sort_values("Protein(g)", ascending=False)
      .groupby("Diet_type", as_index=False)
      .head(5)
)
top_protein.to_csv(os.path.join(OUTPUT_DIR, "top_5_protein_recipes_by_diet.csv"), index=False)

# Diet with highest mean protein
diet_protein_means = df.groupby("Diet_type")["Protein(g)"].mean()
highest_protein_diet = diet_protein_means.idxmax()
with open(os.path.join(OUTPUT_DIR, "highest_protein_diet.txt"), "w", encoding="utf-8") as f:
    f.write(f"Highest protein diet type (by mean protein): {highest_protein_diet}\n")
print("Highest protein diet type:", highest_protein_diet)

# Most common cuisines (top 3) per diet
most_common_cuisines = (
    df.groupby(["Diet_type", "Cuisine_type"])
      .size()
      .reset_index(name="count")
      .sort_values(["Diet_type", "count"], ascending=[True, False])
)
top3_cuisines = most_common_cuisines.groupby("Diet_type").head(3)
top3_cuisines.to_csv(os.path.join(OUTPUT_DIR, "top_3_cuisines_by_diet.csv"), index=False)
print(top3_cuisines)

# Ratios
df["Protein_to_Carbs_ratio"] = df["Protein(g)"] / df["Carbs(g)"]
df["Carbs_to_Fat_ratio"] = df["Carbs(g)"] / df["Fat(g)"]
df[["Diet_type", "Recipe_name", "Cuisine_type", "Protein_to_Carbs_ratio", "Carbs_to_Fat_ratio"]].to_csv(
    os.path.join(OUTPUT_DIR, "recipe_ratios.csv"),
    index=False
)

# ---- Visualizations ----

# 1) Bar chart: average protein by diet
plt.figure(figsize=(12, 6))
sns.barplot(data=avg_macros, x="Diet_type", y="Protein(g)")
plt.xticks(rotation=45, ha="right")
plt.title("Average Protein by Diet Type")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "avg_protein_by_diet.png"), dpi=150)
plt.close()

# 2) Bar chart: avg macros by diet
avg_macros_melt = avg_macros.melt(
    id_vars="Diet_type",
    value_vars=numeric_cols,
    var_name="Macronutrient",
    value_name="Average"
)
plt.figure(figsize=(12, 6))
sns.barplot(data=avg_macros_melt, x="Diet_type", y="Average", hue="Macronutrient")
plt.xticks(rotation=45, ha="right")
plt.title("Average Macros by Diet Type")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "avg_macros_by_diet.png"), dpi=150)
plt.close()

# 3) Heatmap: avg macros per diet
heatmap_data = avg_macros.set_index("Diet_type")[numeric_cols]
plt.figure(figsize=(10, 6))
sns.heatmap(heatmap_data, annot=True, cmap="viridis")
plt.title("Average Macronutrients per Diet Type")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "avg_macros_heatmap.png"), dpi=150)
plt.close()

# 4) Scatter: top protein recipes
plt.figure(figsize=(12, 7))
sns.scatterplot(
    data=top_protein,
    x="Protein(g)",
    y="Carbs(g)",
    hue="Cuisine_type",
    style="Diet_type"
)
plt.title("Top 5 Protein-Rich Recipes per Diet Type")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "top5_protein_scatter.png"), dpi=150)
plt.close()

print(f"Done. Outputs saved to: {OUTPUT_DIR}/")