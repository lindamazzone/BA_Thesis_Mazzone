# Bachelor Thesis – Computational Linguistics: A Large-Scale, Cross-Linguistic Investigation of Vowel Dispersion
# University of Zurich
# Spring Semester 2025
# Description: Script to get formant values
# Author: Miao Zhang
# Note: This script was written by Miao Zhang and kindly made available for this thesis.


import pandas as pd
pd.options.mode.copy_on_write = True
import os, logging, argparse, time, re
from praatio import textgrid
import parselmouth as psm
import numpy as np
from concurrent.futures import ProcessPoolExecutor, as_completed

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

# List of IPA vowel symbols
target_vowels = [
    'i', 'y', 'ɨ', 'ʉ', 'ɯ', 'u', 'ɪ', 'ʏ', 'ʊ', # High vowels
    'e', 'ø', 'ɘ', 'ɵ', 'ɤ', 'o', # Mid-high vowels
    'ɹ̩', 'ɻ̩', # Mandarin apical vowels
    'ə', # Schwa
    'ɛ', 'œ', 'ɜ', 'ɞ', 'ʌ', 'ɔ', # Mid-low vowels
    'a', 'ɶ', 'ɑ', 'ɒ', 'æ', 'ɐ', # Low vowels
]

# Helper function to check if a label contains any IPA vowel symbol
def contains_vowel(label):
    return any(vowel in label for vowel in target_vowels)

# Define a function to identify monophthongs
def is_monophthong(label):
    # Remove stress markers at the beginning if they exist
    if label.startswith("'") or label.startswith("ˈ｜ˌ"):
        label = label[1:]  # Remove the stress marker for further checks

    # Strip away IPA tone labels or any Arabic numbers
    label = re.sub(r"[˥˦˧˨˩0-9]", "", label)

    # Check if it's a monophthong without stress or with the long vowel marker
    true_mono = len(label) == 1 or (len(label) == 2 and (label[1] == 'ː' or label[1] == ':'))
    return true_mono

# Helper function to process a single TextGrid file
def process_textgrid_file(lang_code, tg_file, tg_dir, snd_dir):
    results = []
    tg_path = os.path.join(tg_dir, tg_file)
    tg_name = os.path.basename(tg_file)
    file_id, _ = os.path.splitext(tg_name)
    snd_name = file_id + '.mp3'
    snd_file = os.path.join(snd_dir, snd_name)

    failed_intervals = 0
    processed_intervals = 0
    total_duration = 0
    total_intervals = 0
    non_spn_intervals = []

    if not os.path.exists(snd_file):
        logging.warning(f"Sound file {snd_file} does not exist. Skipping.")
        return results, failed_intervals, processed_intervals

    try:
        tg = textgrid.openTextgrid(tg_path, includeEmptyIntervals=True)
        word_tier = tg.getTier(tg.tierNames[0]) # Get the word tier
        seg_tier = tg.getTier(tg.tierNames[1]) # Get the segment tier

        n_wd_intv = len(word_tier)

        # Skip any recordings that have only one or two words
        if n_wd_intv > 4:

            # Get the total duration and number of non-'spn' intervals
            utterance_start = next(start for start, _, label in seg_tier.entries if label)
            utterance_end = max(stop for _, stop, label in reversed(seg_tier.entries) if label)
            utterance_duration = utterance_end - utterance_start

            # Get the total duration and number of non-'spn' intervals
            for start, stop, label in seg_tier.entries:
                if label and label != 'spn':
                    intv_dur = stop - start
                    total_duration += intv_dur
                    total_intervals += 1
                    non_spn_intervals.append((start, stop, label))

            # Read the sound file
            snd = psm.Sound(snd_file)

            # Get the pitch object
            pitch = snd.to_pitch_ac(time_step=None, pitch_floor=75.0, pitch_ceiling=500.0)
            f0s = pitch.selected_array["frequency"]
            times = pitch.xs()

            # Calculate the mean F0 of the entire recording
            valid_f0s = f0s[f0s > 0]
            mean_f0_recording = np.mean(valid_f0s) if valid_f0s.size > 0 else np.nan

            # Get the formant object
            if mean_f0_recording <= 160:
                mean_pitch_range = 'low'
                formants = snd.to_formant_burg(time_step = None, 
                                            window_length = 0.04, 
                                            maximum_formant = 4000,
                                            max_number_of_formants = 4)
            else:
                mean_pitch_range = 'high'
                formants = snd.to_formant_burg(time_step = None, 
                                            window_length = 0.025,
                                            maximum_formant = 5500,
                                            max_number_of_formants = 5)

            for i in range(len(seg_tier.entries)):
                start, stop, label = seg_tier.entries[i]
                if contains_vowel(label) and is_monophthong(label) and label:
                    intv_dur = round((stop - start) * 1000)
                    if intv_dur >= 30:

                        prev_label = seg_tier.entries[i - 1][2] if i > 0 else 'NA'
                        next_label = seg_tier.entries[i + 1][2] if i < len(seg_tier.entries) - 1 else 'NA'

                        word_info = None
                        for word_idx, (word_start, word_stop, word_label) in enumerate(word_tier.entries):
                            if word_start <= start and word_stop >= stop:
                                word_info = (word_label, round((word_stop - word_start) * 1000), word_idx, word_start, word_stop)
                                break
            
                        if not word_info:
                            logging.warning(f"No matching word found for segment {label} at interval {i}.")
                            continue

                        word_label, word_dur, word_idx, word_start, word_stop = word_info
                        
                        # Determine the position within the utterance
                        start_percentage = round((start - utterance_start) / utterance_duration, 2)

                        # Get the utterance position
                        utt_pos = ''
                        if start == word_start or (i > 0 and not any(contains_vowel(seg_tier.entries[j][2]) for j in range(i) if seg_tier.entries[j][0] >= word_start)):
                            if word_idx == 1: # the first word in an utterance
                                utt_pos = 'utt-initial'
                            else:
                                utt_pos = 'word-initial'
                        if stop == word_stop or (i > 0 and not any(contains_vowel(seg_tier.entries[j][2]) for j in range(i+1, len(seg_tier.entries)) if seg_tier.entries[j][0] <= word_stop)):
                            if word_idx == len(word_tier.entries) - 1:
                                utt_pos = 'utt-final'
                            else:
                                utt_pos = 'word-final'
                        if not utt_pos:
                            utt_pos = 'word-medial'
                        
                        # Check if the vowel is preceded by any consonants in a word
                        preceded_by_consonants = any(
                            not contains_vowel(seg_tier.entries[j][2]) 
                            for j in range(i) if seg_tier.entries[j][0] >= word_start and seg_tier.entries[j][1] <= start
                            )
                        
                        # Check if the vowel is followed by any consonants in a word
                        followed_by_consonants = any(
                            not contains_vowel(seg_tier.entries[j][2])
                            for j in range(i + 1, len(seg_tier.entries)) if seg_tier.entries[j][0] > stop and seg_tier.entries[j][1] <= word_stop
                        )

                        mid_start = start + (stop - start) * 0.45
                        mid_stop = stop - (stop - start) * 0.45
                        mid_indices = np.where(np.logical_and(times >= mid_start, times <= mid_stop))
                        target_f0s = f0s[mid_indices]
                        valid_target_f0s = target_f0s[target_f0s > 0]

                        f1_vals = []
                        f2_vals = []
                        for time in times[mid_indices]:
                            f1_value = formants.get_value_at_time(1, time)
                            f2_value = formants.get_value_at_time(2, time)
                            if f1_value is not None and not np.isnan(f1_value):
                                f1_vals.append(f1_value)
                            if f2_value is not None and not np.isnan(f2_value):
                                f2_vals.append(f2_value)
                        
                        # Calculate mean F0 for the entire vowel segment
                        segment_indices = np.where(np.logical_and(times >= start, times <= stop))
                        segment_f0s = f0s[segment_indices]
                        valid_segment_f0s = segment_f0s[segment_f0s > 0]
                        mean_segment_f0 = np.nan if valid_segment_f0s.size == 0 else round(np.mean(valid_segment_f0s))

                        # Calculate mean F0 for the first 10% of the vowel segment
                        first_10_stop = start + (stop - start) * 0.1
                        first_10_indices = np.where(np.logical_and(times >= start, times <= first_10_stop))
                        first_10_f0s = f0s[first_10_indices]
                        valid_first_10_f0s = first_10_f0s[first_10_f0s > 0]
                        mean_first_10_f0 = np.nan if valid_first_10_f0s.size == 0 else round(np.mean(valid_first_10_f0s))

                        if valid_target_f0s.size > 0 and f1_vals and f2_vals:
                            mean_f0 = np.nan if valid_target_f0s.size == 0 else round(np.mean(valid_target_f0s))
                            mean_f1 = np.nan if not f1_vals else round(np.nanmean(f1_vals))
                            mean_f2 = np.nan if not f2_vals else round(np.nanmean(f2_vals))

                            results.append([lang_code, file_id, mean_pitch_range, prev_label, label, i, next_label, preceded_by_consonants, followed_by_consonants, start, stop, intv_dur, mean_f0, mean_first_10_f0, mean_segment_f0, mean_f1, mean_f2, 
                            word_label, word_start, word_stop, word_dur, round(total_duration*1000), total_intervals, start_percentage, utt_pos])
                            processed_intervals += 1
                        else:
                            failed_intervals += 1
                    else:
                        failed_intervals += 1
        #else:
        #    print(f'Skipping {tg_file}: the utterance contains less than three words.')

    except Exception as e:
        logging.error(f"Error processing {tg_file}: {e}")

    return results, failed_intervals, processed_intervals

def parse_args():
    parser = argparse.ArgumentParser(description="Process TextGrid files for speech analysis.")
    parser.add_argument("commonvoice_dir", type=str, help="Path to the CommonVoice directory")
    parser.add_argument("lang_code", type=str, help="Language code")
    parser.add_argument("ver_num", type=str, help="Version number")
    parser.add_argument("output_dir", type=str, help="Directory to save the output CSV file")
    return parser.parse_args()

def main(commonvoice_dir, lang_code, ver_num, output_dir):
    # Record the start time
    start_time = time.time()

    # Define paths
    lang_dir = os.path.join(commonvoice_dir, f'{lang_code}_v{ver_num}')
    tg_dir = os.path.join(lang_dir, 'output')
    snd_dir = os.path.join(lang_dir, 'validated')
    output_csv = os.path.join(output_dir, f'{lang_code}_v{ver_num}_dur_f0_formants.csv')

    results = []
    total_failed_intervals = 0
    total_processed_intervals = 0

    # Using ProcessPoolExecutor for parallel processing
    max_workers = min(10, os.cpu_count() or 1)  # Adapt according to your CPU
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(process_textgrid_file, lang_code, tg_file.name, tg_dir, snd_dir): tg_file.name
            for tg_file in os.scandir(tg_dir) if tg_file.is_file() and tg_file.name.endswith('.TextGrid')
        }

        for future in as_completed(futures):
            try:
                res, failed_intervals, processed_intervals = future.result()
                if res:
                    results.extend(res)
                total_failed_intervals += failed_intervals
                total_processed_intervals += processed_intervals
            except Exception as e:
                logging.error(f"Error in future result: {e}")

    # Save results to CSV
    df = pd.DataFrame(results, columns=['lang_code', 'file_id', 'mean_pitch_range', 'prev_seg', 'seg', 'seg_intv', 'next_seg', 'preceded_by_cons', 'followed_by_cons', 'seg_start', 'seg_stop', 'seg_dur', 'F0_mid10', 'F0_first10', 'F0_seg_mean', 'F1', 'F2',
                                    'word', 'word_start', 'word_stop', 'word_dur', 'utt_dur', 'n_phone', 'utt_perc', 'utt_pos'])
    if not df.empty:
        df.to_csv(output_csv, index=False, na_rep='NaN')
        print(f"Results saved to {output_csv}")
    else:
        print("No valid results to save")

    # Report the number of processed and failed intervals
    print(f"Number of vowel intervals successfully processed: {total_processed_intervals}")
    print(f"Number of vowel intervals that failed to yield an F0 value: {total_failed_intervals}")

    # Record the end time
    end_time = time.time()
    runtime = end_time - start_time
    # Convert the elapsed time to hours, minutes, and seconds
    hours, rem = divmod(runtime, 3600)
    minutes, seconds = divmod(rem, 60)

    # Print the runtime
    print(f"Runtime: {int(hours):02}:{int(minutes):02}:{seconds:.2f}")

if __name__ == "__main__":
    args = parse_args()
    main(args.commonvoice_dir, args.lang_code, args.ver_num, args.output_dir)
