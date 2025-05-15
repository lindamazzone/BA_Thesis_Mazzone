# Author: Linda Mazzone
# Bachelor Thesis – Computational Linguistics: A Large-Scale, Cross-Linguistic Investigation of Vowel Dispersion
# University of Zurich
# Spring Semester 2025
# Description: Script to filter the original VoxCommunis Corpus
# Note: This script was written as part of my Bachelor's thesis in Computational Linguistics.

import os
import pandas as pd
list_vowels = set()



def filter(file_name, threshold_ms, threshold_ms_utt, threshold_speaker, threshold_vowel_instances, input_folder, speaker_info_folder, output_folder):

    #1 Filter aiu
    if file_name.endswith('.csv'):  # Process only .csv files
        input_file = os.path.join(input_folder, file_name)  # Full path of the input file
        output_file = os.path.join(output_folder, file_name.replace('.csv', '_filtered.csv'))

        # Load the CSV file
        df = pd.read_csv(input_file)


        print(f"Original rows: {len(df)}")
        # print(df.seg.unique())
        # print(df.seg.value_counts())
        print(file_name)


        # Define vowel categories
        a_vowels = ['a', 'aː', 'aːː', 'aː̃', 'ã', 'ãː', 'a̤', 'a̯', 'ʲa', 'ʷa', 'ã', 'æ', 'æː', 'ɐ', 'ɐˤː', 'ɐ̀', 'ɐ́',
                  'ɐ̃', 'ɑ', 'ɑː', 'ɑ̃', 'ɑ̈', 'ʲɑ', 'ʷɑ']
        i_vowels = ['i', 'iː', 'iː̃', 'ĩ', 'ï', 'i̤', 'i̥', 'i̯', 'ĩ', 'ˈiː', 'ɨ', 'ɨ̞', 'ɪ', 'ɪ̀', 'ɪ̃', 'ɪ̯ˑ', 'ʏ',
                  'ʏ̈', 'ʏ̫ː']
        u_vowels = ['u', 'uː', 'ũ', 'ũː', 'ü', 'ṳ', 'u̯', 'ü', 'ũ', 'ʉ', 'ʉː', 'ɯ', 'ɯː', 'ɯːː', 'ɯː̃', 'ɯ̃', 'ɯ̥', 'ʊ',
                  'ʊː', 'ʊ̀', 'ʊ̃', 'ʊ̃ˑ', 'ʊ̯', 'ʊ̯ˑ', 'ʲʊ']


        def get_most_frequent_vowel(vowels):
            filtered_seg = df[df['seg'].isin(vowels)]['seg']
            if not filtered_seg.empty:
                mode_result = filtered_seg.mode()
                if not mode_result.empty:
                    return mode_result.iloc[0]
            return None  # Return None if no vowel is found

        # Identify most frequent vowel in each category
        most_frequent_a = get_most_frequent_vowel(a_vowels)
        most_frequent_i = get_most_frequent_vowel(i_vowels)
        most_frequent_u = get_most_frequent_vowel(u_vowels)

        print(f"Most frequent a vowel: {most_frequent_a}")
        print(f"Most frequent i vowel: {most_frequent_i}")
        print(f"Most frequent u vowel: {most_frequent_u}")

        # Filter rows to keep only the most frequent vowels
        filtered_df_aiu = df[
            (df['seg'] == most_frequent_a) |
            (df['seg'] == most_frequent_i) |
            (df['seg'] == most_frequent_u)
        ]

        print(f"Filtered rows only a i u: {len(filtered_df_aiu)}")

        ####################################################################################################################################
        #2 filter lenght(ms)
        filtered_df_ms = filtered_df_aiu[filtered_df_aiu['seg_dur'] >= threshold_ms]
        print(f"Filtered rows lenght: {len(filtered_df_ms)}")

        ####################################################################################################################################
        #3 filter utterance duration(ms)
        filtered_df_ms = filtered_df_ms[filtered_df_ms['utt_dur'] >= threshold_ms_utt]
        print(f"Filtered rows utterance: {len(filtered_df_ms)}")


        ####################################################################################################################################
        #4 filter speaker
        lang_short = file_name.split('_')[0]

        # Find the corresponding speaker info file in the speaker info folder
        speaker_info_files = [
            f for f in os.listdir(speaker_info_folder)
            if f.startswith(lang_short) and f.endswith('.tsv')
        ]
        # print(speaker_info_files)

        # Load the speaker info file (assuming there's only one match per language short)
        speaker_info_file = os.path.join(speaker_info_folder, speaker_info_files[0])
        speaker_info_df = pd.read_csv(speaker_info_file, sep='\t', low_memory=False)

        # Ensure 'path' in speaker info file matches 'file_id' in original file
        speaker_info_df['file_id'] = speaker_info_df['path'].str.replace('.mp3', '', regex=False)

        # Merge speaker information into the original dataframe
        filtered_df_spkr_merged = filtered_df_ms.merge(speaker_info_df[['file_id', 'speaker_id']], on='file_id', how='left')

        # Count occurrences of each speaker_id
        speaker_counts = filtered_df_spkr_merged['speaker_id'].value_counts()
        # print(f"speaker counts: {speaker_counts}")

        # Filter speakers based on the threshold
        speakers_to_include = speaker_counts[speaker_counts > threshold_speaker].index

        # Filter rows based on the speakers to include
        filtered_df_spkr = filtered_df_spkr_merged[filtered_df_spkr_merged['speaker_id'].isin(speakers_to_include)]
        print(f"Filtered rows speaker: {len(filtered_df_spkr)}")


        ####################################################################################################################################
        # 5 filter std/mean
        # Step 1: Compute mean and std for F1 and F2 by speaker and segment
        stats = filtered_df_spkr.groupby(['seg', 'speaker_id'])[['F1', 'F2']].agg(['mean', 'std']).reset_index()

        # Flatten multi-level column names
        stats.columns = ['seg', 'speaker_id', 'F1_mean', 'F1_std', 'F2_mean', 'F2_std']

        # Step 2: Merge stats back to the original dataframe
        filtered_df_spkr = filtered_df_spkr.merge(stats, on=['speaker_id', 'seg'])

        # Step 3: Calculate upper and lower bounds for F1 and F2
        filtered_df_spkr['F1_upper_bound'] = filtered_df_spkr['F1_mean'] + 2.5 * filtered_df_spkr['F1_std']
        filtered_df_spkr['F1_lower_bound'] = filtered_df_spkr['F1_mean'] - 2.5 * filtered_df_spkr['F1_std']
        filtered_df_spkr['F2_upper_bound'] = filtered_df_spkr['F2_mean'] + 2.5 * filtered_df_spkr['F2_std']
        filtered_df_spkr['F2_lower_bound'] = filtered_df_spkr['F2_mean'] - 2.5 * filtered_df_spkr['F2_std']

        # Step 4: Filter rows where F1 and F2 are both within bounds
        df_spkr = filtered_df_spkr[
            (filtered_df_spkr['F1'] > filtered_df_spkr['F1_lower_bound']) &
            (filtered_df_spkr['F1'] < filtered_df_spkr['F1_upper_bound']) &
            (filtered_df_spkr['F2'] > filtered_df_spkr['F2_lower_bound']) &
            (filtered_df_spkr['F2'] < filtered_df_spkr['F2_upper_bound'])
            ]

        # Step 5: Group by speaker and vowel, count occurrences
        vowel_counts_per_speaker = (
            df_spkr.groupby(['speaker_id', 'seg'])
            .size()
            .unstack(fill_value=0)
        )

        # Ensure all vowel columns are present, even if zero
        for vowel in [most_frequent_a, most_frequent_i, most_frequent_u]:
            if vowel not in vowel_counts_per_speaker.columns:
                vowel_counts_per_speaker[vowel] = 0

        # Step 6: Filter speakers who have at least `threshold` occurrences for all vowels
        qualified_speakers = vowel_counts_per_speaker[
            (vowel_counts_per_speaker[most_frequent_a] >= threshold_vowel_instances) &
            (vowel_counts_per_speaker[most_frequent_i] >= threshold_vowel_instances) &
            (vowel_counts_per_speaker[most_frequent_u] >= threshold_vowel_instances)
            ].index

        # Step 7: Keep only rows for those qualified speakers
        df_spkr = df_spkr[df_spkr['speaker_id'].isin(qualified_speakers)]

        # Step 8: Drop unnecessary columns before saving
        df_spkr = df_spkr.drop(columns=[
            'F1_mean', 'F1_std', 'F2_mean', 'F2_std',
            'F1_upper_bound', 'F1_lower_bound',
            'F2_upper_bound', 'F2_lower_bound'
        ])

        print(f"Filtered rows std/mean (F1 & F2): {len(df_spkr)}")

        ####################################################################################################################################
        # 6 filter similarity score

        # Path to the similarity scores txt file
        similarity_score_file = 'vxc-speaker-scores4.txt'

        # Read the txt file (assuming it's tab-separated and has at least 3 columns)
        similarity_df = pd.read_csv(similarity_score_file, sep=' ', header=None, names=['text_file', 'enrolment_file', 'score'])
        # Remove the '.wav' extension from 'text_file' so it matches 'file_id'
        similarity_df['text_file'] = similarity_df['text_file'].str.replace('.wav', '', regex=False)

        # Filter for scores greater than 0.3
        similarity_df_filtered = similarity_df[similarity_df['score'] > 0.3]

        # Extract just the file names that pass the threshold
        valid_file_names = similarity_df_filtered['text_file'].unique()

        # Filter df_spkr based on these valid file names
        df_spkr = df_spkr[df_spkr['file_id'].isin(valid_file_names)]


        print(f"Filtered rows similarity score: {len(df_spkr)}")
        ####################################################################################################################################


        # Save the filtered DataFrame to a new CSV file
        df_spkr.to_csv(output_file, index=False)

        print(f"{lang_short} filtered file created: {output_file}")

input_folder = 'vxc_data'
output_folder0 = 'filtered_csv'
input_speaker_info = 'speaker_files'
os.makedirs(output_folder0, exist_ok=True)  # Ensure the output folder exists
for file in os.listdir(input_folder):
    filter(file, 50, 500,20, 20, input_folder, input_speaker_info, output_folder0)


