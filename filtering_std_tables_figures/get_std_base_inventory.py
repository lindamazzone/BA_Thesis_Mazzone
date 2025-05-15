# Author: Linda Mazzone
# Bachelor Thesis – Computational Linguistics: A Large-Scale, Cross-Linguistic Investigation of Vowel Dispersion
# University of Zurich
# Spring Semester 2025
# Description: Script to get the speaker and vowel-specific F1 and F2 standard deviations of each language as well as
# the vowel count for each language (for the base inventory)
# Note: This script was written as part of my Bachelor's thesis in Computational Linguistics.

import pandas as pd
import os
from bs4 import BeautifulSoup
import re



# Define folder
filtered_folder = 'filtered_csv'
output_folder = 'std_output_base_inventory'
original_folder = 'vxc_data'
info_folder = 'vxc-documentation'
schwa = ["ə", "ə̃", "əː", "ə́", "ə̀", "ə̃", "ʷə"]
has_schwa = None
vowel_count = None
found_html_file = False
it_file_path = "vxc_data/it_v17_dur_f0_formants.csv"

languages_with_no_file = {}
lang_list = []
big_vowel_set = set()

#semplified vowels
ipa_vowels = {
    "i": ['i', 'iː', 'iː̃', 'ĩ', 'ï', 'i̤', 'i̥', 'i̯','ĩ', 'ˈiː'],
    "y": ['y', 'yː', 'ỹ'],
    "ɨ": ['ɨ', 'ɨ̞'],
    "ʉ": ['ʉ', 'ʉː'],
    "ɯ": ['ɯ', 'ɯː', 'ɯːː', 'ɯː̃', 'ɯ̃', 'ɯ̥'],
    "u": ['u', 'uː', 'ũ', 'ũː', 'ü', 'ṳ', 'u̯', 'ü', 'ũ'],
    "ɪ": ['ɪ', 'ɪː', 'ɪ̀', 'ɪ̃', 'ɪ̯ˑ'],
    "ʏ": ['ʏ', 'ʏ̈', 'ʏ̫ː'],
    "ʊ": ['ʊ', 'ʊː', 'ʊ̀', 'ʊ̃', 'ʊ̃ˑ', 'ʊ̯', 'ʊ̯ˑ', 'ʲʊ'],
    "e": ['e', 'eː', 'eːː', 'eː̃', 'ẽ', 'ë', 'e̤', 'ʲe', 'ẽ'],
    "ø": ['ø', 'øː'],
    "ɘ": ['ɘ'],
    "ɵ": ['ɵ'],
    "ɤ": ['ɤ', 'ɤː'],
    "o": ['o', 'oː', 'oːː', 'oː̃', 'õ', 'ö', 'o̤', 'õ', 'ʷo'],
    "ə": ['ə', 'əː', 'ə̀', 'ə́', 'ə̃', 'ɚ', 'ʷə'],
    "ɛ": ['ɛ', 'ɛː', 'ɛ̀ː', 'ɛ́', 'ɛ́ː', 'ɛ̃', 'ɛ̈', 'ʲɛ'],
    "œ": ['œ', 'œː'],
    "ɜ": ['ɜ'],
    "ɞ": ['ɞ'],
    "ʌ": ['ʌ'],
    "ɔ": ['ɔ', 'ɔː', 'ɔ̀ː', 'ɔ́', 'ɔ́ː', 'ɔ̃', 'ɔ̃ʲ', 'ɔ̃ː', 'ɔ̃ˑ', 'ɔ̈', 'ɔ̋', 'ɔ̤'],
    "æ": ['æ', 'æː'],
    "ɐ": ['ɐ', 'ɐˤː', 'ɐ̀', 'ɐ́', 'ɐ̃'],
    "a": ['a', 'aː', 'aːː', 'aː̃', 'ã', 'ãː', 'a̤', 'a̯', 'ã', 'ʲa', 'ʷa'],
    "ɶ": ['ɶ'],
    "ɑ": ['ɑ', 'ɑː', 'ɑ̃', 'ɑ̈', 'ʲɑ', 'ʷɑ'],
    "ɒ": ['ɒ', 'ɒ̃']
}

vowel_inventory_summary = {}


# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)
a_vowels = ['a', 'aː', 'aːː', 'aː̃', 'ã', 'ãː', 'a̤', 'a̯', 'ʲa', 'ʷa', 'ã', 'æ', 'æː', 'ɐ', 'ɐˤː', 'ɐ̀', 'ɐ́',
            'ɐ̃', 'ɑ', 'ɑː', 'ɑ̃', 'ɑ̈', 'ʲɑ', 'ʷɑ']
i_vowels = ['i', 'iː', 'iː̃', 'ĩ', 'ï', 'i̤', 'i̥', 'i̯', 'ĩ', 'ˈiː', 'ɨ', 'ɨ̞', 'ɪ', 'ɪ̀', 'ɪ̃', 'ɪ̯ˑ', 'ʏ',
            'ʏ̈', 'ʏ̫ː']
u_vowels = ['u', 'uː', 'ũ', 'ũː', 'ü', 'ṳ', 'u̯', 'ü', 'ũ', 'ʉ', 'ʉː', 'ɯ', 'ɯː', 'ɯːː', 'ɯː̃', 'ɯ̃', 'ɯ̥', 'ʊ',
            'ʊː', 'ʊ̀', 'ʊ̃', 'ʊ̃ˑ', 'ʊ̯', 'ʊ̯ˑ', 'ʲʊ']

# Define vowel priority for sorting: low -> high front -> high back
def assign_vowel_priority(vowel):
    if vowel in a_vowels:
        return 1
    elif vowel in i_vowels:
        return 2
    elif vowel in u_vowels:
        return 3
    else:
        return None


# Loop through each filtered file
for file_name in os.listdir(filtered_folder):
    if file_name.endswith('.csv'):
        file_path = os.path.join(filtered_folder, file_name)
        df = pd.read_csv(file_path)

        print(f"Processing file: {file_name}")

        # Create a new speaker_id that combines lang_code and speaker_id
        df['speaker_id_full'] = df['lang_code'].str.lower() + '_' + df['speaker_id'].astype(str)

        df['language'] = df['lang_code'].str.lower()

        # Group by full speaker_id and vowel (seg)
        grouped = df.groupby(['speaker_id_full', 'seg'])

        # Calculate standard deviation for F1 and F2
        std_df = grouped[['F1', 'F2']].std().reset_index()

        # Extract language from speaker_id_full
        std_df['language'] = df['lang_code'].str.lower()

        # Check schwa existence in the original file
        original_file_name = file_name.replace('_filtered.csv', '.csv')
        original_file_path = os.path.join(original_folder, original_file_name)


        original_df = pd.read_csv(original_file_path)

        language = file_name.split('_')[0]


        #documentation file .html
        for file in os.listdir(info_folder):
            if file.startswith(f'{language}') and file.endswith('.html'):
                print(f"Documentation: {file}")
                languages_with_no_file[language] = file
                with open(os.path.join(info_folder, file), 'r') as f:
                    soup = BeautifulSoup(f, 'html.parser')

                    # vowel_count = soup.find(string=lambda t: 'Vowel count:' in t).split(':')[1].strip()
                    vowels = [line.split(':')[0].strip() for line in
                              soup.find('h4', string=lambda t: 'Vowels frequency' in t).find_next('p').text.strip().split('\n')]
                    vowel_count = len(vowels)
                    for vowel in vowels:
                        big_vowel_set.add(vowel)

                    base_vowels = []
                    for v in vowels:
                        for base, variants in ipa_vowels.items():
                            if v in variants:
                                if base not in base_vowels:
                                    base_vowels.append(base)
                                break
                    vowel_count_base = len(base_vowels)




                    print(f"Language: {language}")
                    print(f"Vowel count: {vowel_count}")
                    print(f"Vowels: {' '.join(vowels)}")
                    print(f"Vowel count: {len(base_vowels)}")
                    print(f"Vowels: {' '.join(base_vowels)}")

                    has_schwa = 1 if any(s in vowels for s in schwa) else -1
                    vowel_inventory_summary[language] = [vowel_count_base, base_vowels, has_schwa]


                break

        #documentation files .txt
        for file in os.listdir(info_folder):
            if file.startswith(f'{language}') and file.endswith('.txt') and language not in languages_with_no_file:
                languages_with_no_file[language] = file
                print(f"Documentation: {file}")
                with open(os.path.join(info_folder, file), 'r') as f:
                    content = f.read()

                # Find the vowels block
                vowels_section = re.search(r"Total vowels:\s*{([^}]*)}", content)

                vowel_entries = vowels_section.group(1).split(",")
                vowels = [entry.split(":")[0].strip().strip("'") for entry in vowel_entries]
                vowel_count = len(vowels)
                for vowel in vowels:
                    big_vowel_set.add(vowel)

                base_vowels = []
                for v in vowels:
                    for base, variants in ipa_vowels.items():
                        if v in variants:
                            if base not in base_vowels:
                                base_vowels.append(base)
                            break
                vowel_count_base = len(base_vowels)

                print(f"Language: {language}")
                print(f"Vowel count: {vowel_count}")
                print(f"Vowels: {' '.join(vowels)}")
                print(f"Vowel count: {len(base_vowels)}")
                print(f"Vowels: {' '.join(base_vowels)}")

                # Check for schwa presence
                has_schwa = 1 if any(s in vowels for s in schwa) else -1
                vowel_inventory_summary[language] = [vowel_count_base, base_vowels, has_schwa]


        #for italian since at the moment there is no documentation file (use the csv file to count them)
        if language == "it":
            df = pd.read_csv(it_file_path)

            # Check which column to look at
            column_name = 'seg'

            # Get all elements from the column
            elements = df[column_name].dropna().tolist()

            # Find unique vowels
            vowels = set(elements)
            vowel_count = len(vowels)

            base_vowels = []
            for v in vowels:
                for base, variants in ipa_vowels.items():
                    if v in variants:
                        if base not in base_vowels:
                            base_vowels.append(base)
                        break

            vowel_count_base = len(base_vowels)

            # Check if any schwa variants are present
            has_schwa = 1 if any(s in vowels for s in schwa) else -1
            vowel_inventory_summary[language] = [vowel_count_base, base_vowels, has_schwa]


            print(f"Language: {language}")
            print(f"Vowel count: {vowel_count}")
            print(f"Vowels: {' '.join(vowels)}")
            print(f"Vowels: {' '.join(vowels)}")
            print(f"Vowel count: {len(base_vowels)}")
            print(f"Vowels: {' '.join(base_vowels)}")

        # Add has_schwa column to std_df (same value for all rows in that language file)
        std_df['has_schwa'] = has_schwa
        std_df['number_of_vowels'] = vowel_count_base


        # Vowel contrast coding
        contrast1_map = {
                            v: -1 for v in a_vowels
                        } | {
                            v: 1 for v in i_vowels
                        } | {
                            v: 0 for v in u_vowels
                        }

        contrast2_map = {
                            v: -1 for v in a_vowels
                        } | {
                            v: 0 for v in i_vowels
                        } | {
                            v: 1 for v in u_vowels
                        }

        # Add the contrast codes based on the vowel
        std_df['vowel_contrast1'] = std_df['seg'].map(contrast1_map)
        std_df['vowel_contrast2'] = std_df['seg'].map(contrast2_map)

        # Rename
        std_df.rename(columns={
            'speaker_id_full': 'speaker_id',
            'seg': 'vowel',
            'F1': 'F1_std',
            'F2': 'F2_std',
        }, inplace=True)

        # Rearrange columns order
        std_df = std_df[['speaker_id', 'language', 'vowel', 'number_of_vowels', 'F1_std', 'F2_std', 'has_schwa', 'vowel_contrast1', 'vowel_contrast2']]

        # Rearrange columns order
        std_df = std_df[
            ['speaker_id', 'language', 'vowel', 'number_of_vowels', 'F1_std', 'F2_std', 'has_schwa', 'vowel_contrast1',
             'vowel_contrast2']]

        # Add sorting
        std_df['sort_priority'] = std_df['vowel'].apply(assign_vowel_priority)
        std_df = std_df.sort_values(by=['speaker_id', 'sort_priority']).reset_index(drop=True)
        std_df.drop(columns=['sort_priority'], inplace=True)

        # Save to a new CSV
        output_file = os.path.join(output_folder, f'{file_name}'.replace('_filtered.csv', '_std.csv'))
        std_df.to_csv(output_file, index=False)
print(sorted(big_vowel_set))

rows = []

for lang, data in  vowel_inventory_summary.items():
    number = int(data[0])
    base_vowels = sorted(list(data[1]))  # Convert set to list if needed and sort
    schwa = data[2]
    rows.append({
        'language': lang,
        'vowel_inventory': ', '.join(base_vowels),
        'number_of_vowels': number,
        'has_schwa': schwa
    })

# Create DataFrame and export to CSV
df = pd.DataFrame(rows)
df.to_csv('vowel_inventory_summary_base_inventory.csv', index=False)