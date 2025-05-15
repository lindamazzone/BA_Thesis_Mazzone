import os
from ipapy import is_valid_ipa

def phoneme_count(input_path, output_path, base_name):
    """This function opens the files, processes its content and saves it to another subfolder.
    it takes 3 arguments;
    - input path
    - output path
    - base name for naming the processed files.
    It calculates the phoneme frequencies and creates a new text file with the relevant information.
    """

    # create a set of vowels (some vowels still missing)
    vowels = {
        'a', 'e', 'i', 'o', 'u', 'ə', 'ɛ', 'ɪ', 'ɔ', 'ʊ', 'æ', 'ʌ', 'ɑ', 'ɒ',
        'ø', 'ɤ', 'œ', 'ɨ', 'ʉ', 'ɯ', 'ɘ', 'ɵ', 'ɜ', 'ɞ', 'ɝ', 'ɐ', 'ʲ', 'ɚ',
        'y', 'ø', 'ø̞', 'œ', 'œ̞', 'ʏ', 'ʏ̞', 'ʏ̈', 'ɥ', 'ɶ', 'ɞ̞', 'ɞ̈', 'ɘ̞',
        'ɘ̈', 'ɪ̈', 'ɪ̯', 'ʏ̯', 'y̯', 'ø̯', 'ʏ̯', 'ɜ̝', 'ɐ̝', 'ɪ̯', 'ʊ̯', 'ʏ̯',
        'ɯ̯', 'ɪ̯', 'iː', 'iˑ', 'yː', 'yˑ', 'eː', 'eˑ', 'øː', 'øˑ', 'ɛː', 'ɛˑ',
        'œː', 'œˑ', 'ɪː', 'ɪˑ', 'ʏː', 'ʏˑ', 'aː', 'aˑ', 'ɶː', 'ɶˑ', 'ɒː', 'ɒˑ',
        'ɔː', 'ɔˑ', 'oː', 'oˑ', 'uː', 'uˑ', 'ʊː', 'ʊˑ', 'əː', 'əˑ', 'ɜː', 'ɜˑ',
        'ɚː', 'ɚˑ', 'ɯː', 'ɯˑ', 'ɯ̃', 'ɤː', 'ɤˑ', 'ʌː', 'ʌˑ', 'ɐː', 'ɐˑ', 'ɨː', 'ɨˑ',
        'ʉː', 'ʉˑ', 'ɘː', 'ɘˑ', 'ɵː', 'ɵˑ', 'ɞː', 'ɞˑ', 'ɞ̈ː', 'ɞ̈ˑ', 'ɪ̈ː', 'ɪ̈ˑ',
        'ʏ̈ː', 'ʏ̈ˑ', 'ɪ̯ː', 'ɪ̯ˑ', 'ʏ̯ː', 'ʏ̯ˑ', 'ʊ̈ː', 'ʊ̈ˑ', 'ɯ̯ː', 'ɯ̯ˑ',
        'ɯ̈ː', 'ɯ̈ˑ', 'i̯ː', 'i̯ˑ', 'y̯ː', 'y̯ˑ', 'e̯ː', 'e̯ˑ', 'ø̯ː', 'ø̯ˑ', 'ɛ̯ː',
        'ɛ̯ˑ', 'œ̯ː', 'œ̯ˑ', 'ɪ̯ː', 'ɪ̯ˑ', 'ʏ̯ː', 'ʏ̯ˑ', 'a̯ː', 'a̯ˑ', 'ɶ̯ː',
        'ɶ̯ˑ', 'ɒ̯ː', 'ɒ̯ˑ', 'ɔ̯ː', 'ɔ̯ˑ', 'o̯ː', 'o̯ˑ', 'u̯ː', 'u̯ˑ', 'ʊ̯ː',
        'ʊ̯ˑ', 'ə̯ː', 'ə̯ˑ', 'ɜ̯ː', 'ɜ̯ˑ', 'ɚ̯ː', 'ɚ̯ˑ', 'ɯ̯ː', 'ɯ̯ˑ', 'ɤ̯ː',
        'ɤ̯ˑ', 'ʌ̯ː', 'ʌ̯ˑ', 'ɐ̯ː', 'ɐ̯ˑ', 'ɨ̯ː', 'ɨ̯ˑ', 'ʉ̯ː', 'ʉ̯ˑ', 'ɘ̯ː',
        'ɘ̯ˑ', 'ɵ̯ː', 'ɵ̯ˑ', 'ɞ̯ː', 'ɞ̯ˑ', 'ɞ̯̈ː', 'ɞ̯̈ˑ', 'ɪ̯̈ː', 'ɪ̯̈ˑ', 'ʏ̯̈ː',
        'ʏ̯̈ˑ', 'ãː', 'ũː', 'ũ', 'ẽ', 'ə̃', 'ã', 'æː', 'õ', 'ɔ̃', 'ɑ̃'}

    # create phonetic classification

    phonetic_classification = {
        # Stops
        'p': 'voiceless bilabial stop',
        'b': 'voiced bilabial stop',
        't': 'voiceless alveolar stop',
        'd': 'voiced alveolar stop',
        'k': 'voiceless velar stop',
        'g': 'voiced velar stop',
        'ɡ': 'voiced velar stop',
        'ʔ': 'glottal stop',
        'q': 'voiceless uvular stop',
        'ɢ': 'voiced uvular stop',
        'c': 'voiceless palatal stop',
        'ɟ': 'voiced palatal stop',
        'pʰ': 'aspirated bilabial stop',
        'tʰ': 'aspirated alveolar stop',
        'kʰ': 'aspirated velar stop',
        'bʰ': 'voiced aspirated bilabial stop',
        'dʰ': 'voiced aspirated alveolar stop',
        'ɡʰ': 'voiced aspirated velar stop',
        't̪': 'voiceless dental stop',
        'd̪': 'voiced dental stop',
        't̪ʰ': 'aspirated voiceless dental stop',
        'd̪̪ʰ': 'aspirated voiced dental stop',
        'ʈʰ': 'aspirated voiceless retroflex stop',
        'ʈ': 'voiceless retroflex stop',
        'ɖ': 'voiced retroflex stop',
        'ɖʰ': 'voiced aspirated retroflex stop',
        # Nasals
        'm': 'bilabial nasal',
        'ɱ': 'labiodental nasal',
        'n': 'alveolar nasal',
        'n̪': 'dental nasal',
        'ŋ': 'velar nasal',
        'ɲ': 'palatal nasal',
        'ɴ': 'uvular nasal',
        'ɳ': 'retroflex nasal',
        # Trills
        'ʙ': 'voiced bilabial trill',
        'r': 'voiced alveolar trill',
        'ʀ': 'voiced uvular trill',
        # Flaps
        'ⱱ': 'labiodental flap',
        'ɾ': 'alveolar flap',
        'ɽ': 'retroflex flap',
        # Fricatives
        'ɸ': 'voiceless bilabial fricative',
        'β': 'voiced bilabial fricative',
        'f': 'voiceless labiodental fricative',
        'v': 'voiced labiodental fricative',
        'θ': 'dental fricative',
        'ð': 'voiced dental fricative',
        's': 'voiceless alveolar fricative',
        'z': 'voiced alveolar fricative',
        'ʃ': 'voiceless postalveolar fricative',
        'ʒ': 'voiced postalveolar fricative',
        'ʂ': 'voiceless retroflex fricative',
        'ʐ': 'voiced retroflex fricative',
        'ç': 'voiceless palatal fricative',
        'ʝ': 'voiced palatal fricative',
        'x': 'voiceless velar fricative',
        'ɣ': 'voiced velar fricative',
        'χ': 'voiceless uvular fricative',
        'ʁ': 'voiced uvular fricative',
        'ħ': 'voiceless pharyngeal fricative',
        'ʕ': 'voiced pharyngeal fricative',
        'h': 'voiceless glottal fricative',
        'ɦ': 'voiced glottal fricative',
        # Affricates
        't͡ʃ': 'postalveolar affricate',
        'tʃ': 'postalveolar affricate',
        'd͡ʒ': 'voiced postalveolar affricate',
        'dʒ': 'voiced postalveolar affricate',
        'd͡ʒʰ': 'voiced postalveolar aspirated affricate',
        'dʒʰ': 'voiced postalveolar aspirated affricate',
        'ts': 'alveolar affricate',
        'dz': 'voiced alveolar affricate',
        'd͡z': 'voiced alveolar affricate',
        'dzʰ': 'voiced alveolar aspirated affricate',
        't͡s': 'alveolar affricate',
        'd͡z': 'voiced alveolar affricate',
        'dzʰ': 'voiced aspirated alveolar affricate',
        't͡ʃʰ': 'postalveolar aspirated affricate',
        'tʃʰ': 'postalveolar aspirated affricate',
        't͡sʰ': 'alveolar aspirated affricate',
        # Lateral Fricatives
        'ɬ': 'voiceless alveolar lateral fricative',
        'ɮ': 'voiced alveolar lateral fricative',
        # Approximants
        'ʋ': 'voiced labiodental approximant',
        'ɹ': 'alveolar approximant',
        'ɻ': 'retroflex approximant',
        'j': 'palatal approximant',
        'ɰ': 'velar approximant',
        # Lateral Approximants
        'l': 'alveolar lateral approximant',
        'l̪': 'dental lateral approximant',
        'ɭ': 'retroflex lateral approximant',
        'ʎ': 'palatal lateral approximant',
        'ʟ': 'velar lateral approximant',
        # Vowels (nasalized and long vowels missing still)
        'i': 'close front unrounded vowel',
        'y': 'close front rounded vowel',
        'ɨ': 'close central unrounded vowel',
        'ʉ': 'close central rounded vowel',
        'ɪ': 'near-close near-front unrounded vowel',
        'ʏ': 'near-close near-front rounded vowel',
        'e': 'close-mid front unrounded vowel',
        'ø': 'close-mid front rounded vowel',
        'ɘ': 'close-mid central unrounded vowel',
        'ɵ': 'close-mid central rounded vowel',
        'ɛ': 'open-mid front unrounded vowel',
        'œ': 'open-mid front rounded vowel',
        'æ': 'near-open front unrounded vowel',
        'a': 'open front unrounded vowel',
        'ɶ': 'open front rounded vowel',
        'ɜ': 'open-mid central unrounded vowel',
        'ɞ': 'open-mid central rounded vowel',
        'ə': 'mid-central vowel',
        'ɐ': 'near-open central vowel',
        'u': 'close back rounded vowel',
        'ɯ': 'close back unrounded vowel',
        'o': 'close-mid back rounded vowel',
        'ɤ': 'close-mid back unrounded vowel',
        'ɔ': 'open-mid back rounded vowel',
        'ɑ': 'open back unrounded vowel',
        'ɒ': 'open back rounded vowel',
        'a': 'open front unrounded vowel',
        'ã': 'open front nasalized unrounded vowel',
        'õ': 'close-mid back nasalized rounded vowel'
    }

    vowel_count = 0
    consonant_count = 0

    # open the lexicon files
    with open(input_path, 'r', encoding='utf-8') as file:

        # dictionary to keep track of phonemes
        phoneme_dictionary = {}
        vowel_dictionary = {}
        consonant_dictionary = {}

        # create list to only extract the second column from the text files (phonemes)
        list_col2 = []

        for line in file:
            columns = line.strip().split('\t')
            if len(columns) > 1:
                list_col2.append(columns[1])

        for word in list_col2:
            # split the word by whitespace
            split_phone = word.split()
            # print(split_phone)

            for phone in split_phone:
                if is_valid_ipa(phone):   # for Guarani and Maldivian (XPF languages), comment out this line of code (superscript letter could not be caught if this line was active)
                    if phone not in phoneme_dictionary:
                        phoneme_dictionary[phone] = 1
                    else:
                        phoneme_dictionary[phone] += 1

    # count the whole phoneme:
    total_inventory = sum(phoneme_dictionary.values())

    for phone, count in phoneme_dictionary.items():
        if phone in vowels:
            vowel_count += 1
            vowel_dictionary[phone] = count
        else:
            consonant_count += 1
            consonant_dictionary[phone] = count

    # create sorted dictionaries (descending values)
    sorted_vowels_dict = {k: v for k, v in sorted(vowel_dictionary.items(), key=lambda item: item[1], reverse=True)}
    sorted_consonants_dict = {k: v for k, v in sorted(consonant_dictionary.items(), key=lambda item: item[1], reverse=True)}
    ## sorted_fullinventory_dict = {k:v for k,v in sorted(phoneme_dictionary.items(), key=lambda item: item[1], reverse=True)}

    # write the phoneme type count into a new .txt file
    with open(output_path, 'w', encoding='utf-8') as output:
        output.write(f'LANGUAGE: {base_name}\n\n'
                     f'The phoneme inventory:\n\n'
                     f'{phoneme_dictionary}\n\n'
                     f'Total phonemes count: {total_inventory}\n\n'
                     f'Total vowels: {vowel_dictionary}\n\n'
                     f'Vowel count: {vowel_count}\n\n'
                     f'Total consonants: {consonant_dictionary}\n\n'
                     f'Consonant count: {consonant_count}\n\n')

        output.write(30 * '___' + str('\n'))
        output.write('<h4>Vowels frequency:</h4>\n')
        output.write('<p>')
        for phoneme in sorted_vowels_dict:
            output.write(f'\t{phoneme}: {sorted_vowels_dict[phoneme]}<br>\n')
        output.write(f'</p>\n')

        output.write(30 * '___' + str('\n\n'))
        output.write('<h4>Consonants frequency:</h4>\n')
        output.write('<p>')
        for phoneme in sorted_consonants_dict:
            output.write(f'\t{phoneme}: {sorted_consonants_dict[phoneme]}<br>\n')
        output.write(f'</p>\n')

        output.write(30 * '___' + str('\n\n'))
        output.write('Consonants with classification:\n')
        for phoneme in sorted_consonants_dict:
            classification = phonetic_classification.get(phoneme, 'Unknown classification')
            output.write(f'{phoneme}: {classification}\n')

        output.write(30 * '___' + str('\n\n'))
        output.write('Vowels with classification:\n')
        for vowel in sorted_vowels_dict:
            classification = phonetic_classification.get(vowel, 'Unknown classification')
            output.write(f'{vowel}: {classification}\n')


# open the files and process them one by one
def process_all_files(input_folder, output_folder):
    """
    This function processes all .txt files in the input_folder and saves the results to output_folder.
    """
    os.makedirs(output_folder, exist_ok=True)

    # read in text files
    for filename in os.listdir(input_folder):
        if filename.endswith('.txt'):
            input_path = os.path.join(input_folder, filename)
            base_name = os.path.splitext(filename)[0]
            output_path = os.path.join(output_folder, f"{base_name}_overview.txt")

            # pass the variables into the function
            phoneme_count(input_path, output_path, base_name)
            # print(f"Processed {input_path} and saved to {output_path}")


input_folder = 'lexicons'   # change the path
output_folder = 'overviewlexicons'  # change the path

process_all_files(input_folder, output_folder)