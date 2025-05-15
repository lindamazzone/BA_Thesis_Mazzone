# Author: Linda Mazzone
# Bachelor Thesis – Computational Linguistics: A Large-Scale, Cross-Linguistic Investigation of Vowel Dispersion
# University of Zurich
# Spring Semester 2025
# Description: Script to get quantitative values about the vowels studied in the Thesis
# Note: This script was written as part of my Bachelor's thesis in Computational Linguistics.

import os
import pandas as pd

a_vowels = ['a', 'aː', 'aːː', 'aː̃', 'ã', 'ãː', 'a̤', 'a̯', 'ʲa', 'ʷa', 'ã', 'æ', 'æː', 'ɐ', 'ɐˤː', 'ɐ̀', 'ɐ́',
            'ɐ̃', 'ɑ', 'ɑː', 'ɑ̃', 'ɑ̈', 'ʲɑ', 'ʷɑ']
i_vowels = ['i', 'iː', 'iː̃', 'ĩ', 'ï', 'i̤', 'i̥', 'i̯', 'ĩ', 'ˈiː', 'ɨ', 'ɨ̞', 'ɪ', 'ɪ̀', 'ɪ̃', 'ɪ̯ˑ', 'ʏ',
            'ʏ̈', 'ʏ̫ː']
u_vowels = ['u', 'uː', 'ũ', 'ũː', 'ü', 'ṳ', 'u̯', 'ü', 'ũ', 'ʉ', 'ʉː', 'ɯ', 'ɯː', 'ɯːː', 'ɯː̃', 'ɯ̃', 'ɯ̥', 'ʊ',
            'ʊː', 'ʊ̀', 'ʊ̃', 'ʊ̃ˑ', 'ʊ̯', 'ʊ̯ˑ', 'ʲʊ']

def filter(file_name, input_folder):


    #1 Filter aiu
    if file_name.endswith('.csv'):  # Process only .csv files
        input_file = os.path.join(input_folder, file_name)  # Full path of the input file

        # Load the CSV file
        df = pd.read_csv(input_file)
        count = len(df)
        value_counts = df['seg'].value_counts()

        existing_a_vowels = [v for v in a_vowels if v in value_counts]
        existing_i_vowels = [v for v in i_vowels if v in value_counts]
        existing_u_vowels = [v for v in u_vowels if v in value_counts]

        # Sum counts for only those vowels that appear
        filtered_totala = value_counts[existing_a_vowels].sum()
        filtered_totali = value_counts[existing_i_vowels].sum()
        filtered_totalu = value_counts[existing_u_vowels].sum()


    return count, filtered_totala, filtered_totali, filtered_totalu

count = 0
count_a = 0
count_i = 0
count_u = 0
for file in os.listdir("../filtering/filtered_csv"):
    x, a, i, u = filter(file, "../filtering/filtered_csv")
    count = count + x
    count_a = count_a + a
    count_i = count_i + i
    count_u = count_u + u


print("count=", count)
print("a=", count_a)
print("i=", count_i)
print("u=", count_u)

total = count_a + count_i + count_u
print(total)
