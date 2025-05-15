# Author: Linda Mazzone
# Bachelor Thesis – Computational Linguistics: A Large-Scale, Cross-Linguistic Investigation of Vowel Dispersion
# University of Zurich
# Spring Semester 2025
# Description: Script to get a .csv of the complete vowel inventory of each language (full + base inventory)
# Note: This script was written as part of my Bachelor's thesis in Computational Linguistics.

import pandas as pd
import os
import numpy as np


input_folder = '../std/std_output_full_inventory'

speaker = {}
vowels = {}
file_count = 0
# Loop through each filtered file
for file_name in os.listdir(input_folder):
    if file_name.endswith('.csv'):
        file_path = os.path.join(input_folder, file_name)
        df = pd.read_csv(file_path)
        if df.empty:
            continue
        if df.shape[0] < 20:
            continue
        file_count += 1

        unique_speakers = df['speaker_id'].unique()
        language = df['language'].unique()
        language = language[0]
        num_unique_speakers = len(unique_speakers)

        speaker[language] = num_unique_speakers

        vowels_unique = list(df['vowel'].unique())
        vowels[language] = vowels_unique


max_item = max(speaker.items(), key=lambda item: item[1])
min_item = min(speaker.items(), key=lambda item: item[1])

print(max_item)
print(min_item)

all_v = {}
for k, v in vowels.items():
    for element in v:
        if element in all_v:
            all_v[element] += 1
        else:
            all_v[element] = 1
speaker_counts = [v for v in speaker.values()]

speaker_median = np.median(speaker_counts)
speaker_mean = np.mean(speaker_counts)
print(speaker_median, speaker_mean)
print(len(speaker))

print(speaker)
print(vowels)


print(all_v)


print(file_count)

input_folder = '../std/std_output_full_inventory'

speaker = {}
vowels = {}
file_count = 0
language_vowel_counts = {}

for file_name in os.listdir(input_folder):
    if file_name.endswith('.csv'):
        file_path = os.path.join(input_folder, file_name)
        df = pd.read_csv(file_path)
        if df.empty or df.shape[0] < 20:
            continue
        file_count += 1

        language = df['language'].iloc[0]
        unique_speakers = df['speaker_id'].nunique()
        speaker[language] = unique_speakers

        vowel_list = df['vowel'].dropna().tolist()
        vowels[language] = list(set(vowel_list))


# Load your vowel inventory CSV
vowel_df = pd.read_csv("vowel_inventory_summary_base_inventory.csv")

# Load the other data file (make sure 'language' column exists in both)
all_vowel_df = pd.read_csv("vowel_inventory_summary_full_inventory.csv")

# Merge on 'language'
merged_df = pd.merge(vowel_df, all_vowel_df, on='language', how='left')
merged_df = merged_df.sort_values(by='language')  # Ascending (default)
merged_df = merged_df.drop(columns=['has_schwa_x'])
merged_df = merged_df.rename(columns={'has_schwa_y': 'has_schwa'})

speaker_df = pd.DataFrame((speaker.items()), columns=['language', 'number_of_speakers'])
vowel_df = pd.DataFrame([(k, ', '.join(sorted(v))) for k, v in vowels.items()], columns=['language', 'studied_vowels'])


merged_df['language'] = merged_df['language'].str.lower()
speaker_df['language'] = speaker_df['language'].str.lower()
vowel_df['language'] = vowel_df['language'].str.lower()

# Merge with the original DataFrame
merged_df = merged_df.merge(speaker_df, on='language', how='left')
merged_df = merged_df.merge(vowel_df, on='language', how='left')
# count = 0
# for l in merged_df.language.unique():
#     if l not in vowels.keys():
#         print(l)
#         count += 1

# print(count)
merged_df = merged_df.dropna(subset=['number_of_speakers'])

# Save the new merged file
merged_df.to_csv('vowel_inventory_complete_summary.csv', index=False)

print("Merged CSV saved")
