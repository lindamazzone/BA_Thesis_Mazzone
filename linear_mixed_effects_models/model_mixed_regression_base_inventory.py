# Author: Linda Mazzone
# Bachelor Thesis – Computational Linguistics: A Large-Scale, Cross-Linguistic Investigation of Vowel Dispersion
# University of Zurich
# Spring Semester 2025
# Description: Script to get the mixed regression model of the base vowel inventory as well as representative tables
# and graphs
# Note: This script was written as part of my Bachelor's thesis in Computational Linguistics.

import pandas as pd
import statsmodels.formula.api as smf
import os
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import linregress



# Path to your stats_output folder
std_data = '../std/std_output_base_inventory'

# Empty list to collect dataframes
all_dfs = []
results = {}

# Read all files and combine into one dataframe
for file_name in os.listdir(std_data):
    if file_name.endswith('.csv'):
        file_path = os.path.join(std_data, file_name)
        df = pd.read_csv(file_path)
        if df.empty:
            continue
        if df.shape[0] < 20:
            continue
        all_dfs.append(df)

data = pd.concat( all_dfs, ignore_index=True)
data = data.dropna()

model_columns_F1 = ['F1_std', 'number_of_vowels', 'has_schwa', 'vowel_contrast1', 'vowel_contrast2', 'language']
clean_data_F1 = data.dropna(subset=model_columns_F1)

model_columns_F2 = ['F2_std', 'number_of_vowels', 'has_schwa', 'vowel_contrast1', 'vowel_contrast2', 'language']
clean_data_F2 = data.dropna(subset=model_columns_F2)



formula_F1 = 'F1_std ~ number_of_vowels + has_schwa + vowel_contrast1 + vowel_contrast2'
formula_F2 = 'F2_std ~ number_of_vowels + has_schwa + vowel_contrast1 + vowel_contrast2'


md_F1 = smf.mixedlm(formula_F1, clean_data_F1, groups=clean_data_F1['language'])
md_F2 = smf.mixedlm(formula_F2, clean_data_F2, groups=clean_data_F2['language'])


mdf_F1 = md_F1.fit()
# mdf2 = md.fit(method="lbfgs")
mdf_F2 = md_F2.fit(method="cg")


# mdf2 = md.fit(method="lbfgs")


print("Summary for F1")
# Summary output
print(mdf_F1.summary())

# Define new names for predictors
name_map = {
    'Intercept': 'Intercept',
    'number_of_vowels': 'Number of vowels',
    'has_schwa': 'Has schwa',
    'vowel_contrast1': 'Vowel contrast 1',
    'vowel_contrast2': 'Vowel contrast 2',
    'Group Var': 'Group Var'
}

# Apply the mapping

results_df_F1 = pd.DataFrame({
    'Predictor': mdf_F1.params.index,
    'Estimate': mdf_F1.params.values,
    'Std. Error': mdf_F1.bse.values,
    'p-value': mdf_F1.pvalues.values,
    'CI Lower': mdf_F1.conf_int()[0].values,
    'CI Upper': mdf_F1.conf_int()[1].values
})

# Round for clarity
results_df_F1['p-value'] = results_df_F1['p-value'].apply(lambda x: "< 0.0001" if 0 <= x < 0.0001 else round(x, 3))
results_df_F1 = results_df_F1.round(3)
results_df_F1['Predictor'] = results_df_F1['Predictor'].replace(name_map)


# print(results_df_F1)
results_df_F1.to_csv('model_results_f1_base.csv', index=False)


print("________________________________________________________________________")
print("Summary for F2")

# Summary output
print(mdf_F2.summary())
# print(mdf2.summary())



results_df_F2 = pd.DataFrame({
    'Predictor': mdf_F2.params.index,
    'Estimate': mdf_F2.params.values,
    'Std. Error': mdf_F2.bse.values,
    'p-value': mdf_F2.pvalues.values,
    'CI Lower': mdf_F2.conf_int()[0].values,
    'CI Upper': mdf_F2.conf_int()[1].values
})

# Round for clarity
results_df_F2['p-value'] = results_df_F2['p-value'].apply(lambda x: "< 0.0001" if 0 <= x < 0.0001 else round(x, 3))

results_df_F2 = results_df_F2.round(3)
results_df_F2['Predictor'] = results_df_F1['Predictor'].replace(name_map)

# print(results_df_F2)
results_df_F2.to_csv('model_results_f2_base.csv', index=False)




# Group by language to get mean F1/F2_std and vowel counts
summary = data.groupby('language').agg({
    'F1_std': 'mean',
    'F2_std': 'mean',
    'number_of_vowels': 'first',
    'has_schwa': 'first'
}).reset_index()


sns.set(style="whitegrid", font_scale=1.1)

def plot_scatter(x, y, data, title, xlabel, ylabel, filename):
    slope, intercept, r_value, p_value, std_err = linregress(data[x], data[y])
    plt.figure(figsize=(8,6))
    sns.regplot(x=x, y=y, data=data, scatter_kws={'s': 60}, line_kws={'color': 'red'})
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.savefig(filename, dpi=300)  # Save with high resolution
    plt.show()
    print(f"{title} — Slope: {slope:.3f}, p-value: {p_value:.3f}, R²: {r_value**2:.3f}")


# 1. F1_std vs number_of_vowels
plot_scatter(
    x='number_of_vowels',
    y='F1_std',
    data=summary,
    title='Standard Deviation of F1 vs Number of Vowels (Base Inventory)',
    xlabel='Number of Vowels',
    ylabel='F1 Standard Deviation (Hz)',
    filename='F1_std_base_inventory'
)


# 2. F2_std vs number_of_vowels
plot_scatter(
    x='number_of_vowels',
    y='F2_std',
    data=summary,
    title='Standard Deviation of F2 vs Number of Vowels (Base Inventory)',
    xlabel='Number of Vowels',
    ylabel='F2 Standard Deviation (Hz)',
    filename='F2_std_base_inventory'
)
