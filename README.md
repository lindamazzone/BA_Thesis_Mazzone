# BachelorThesis-Mazzone

This GitHub repository includes all code used in the Bachelor Thesis. This includes scripts used for data extraction, filtering and modeling but also the one used to generate graphs and tables.
All scripts were written by me, Linda Mazzone, as part of my Bachelor's thesis in Computational Linguistics, with the exception of "VoxCommunis_lexicon_countphonemes.py", which originates from the VoxCommunis project (written by Ishu Sutharsan) and was only adapted by me in a few places.


## How to run:

## 1 - Missing documentation files
Python script to generate the missing documentation files:
* **VoxCommunis_lexicon_countphonemes.py**

To get the result the following files/folders are needed:
* **lexicon**: The lexicon folder downloaded from https://huggingface.co/datasets/pacscilab/VoxCommunis/tree/main/lexicons

Output files/folders of the python script:
* **overviewlexicons**: the folder with the created lexicons


## 2 - Filtering
### 2.1 - Filter the original csv files
Python script to generate the filtered csv files:
* **filter_csv.py**

To get the result the following files/folders are needed:
* **vxc_data**: Original csv files downloaded from xxxxxxx
* **speaker_files**: files with all the speaker information from https://huggingface.co/datasets/pacscilab/VoxCommunis/tree/main/speaker_files
* **vxc-speaker-scores4.txt**: file with the data to calculate the similarity score.

Output files/folders of the python script:
* **filtered_csv**: folder with the filtered csv files

### 2.2 - Get Standard Deviation and vowel count/inventory 
#### 2.2.1 - For the Full inventory
Python script to generate the standard deviation, the vowel count and the vowel inventory of each langauge:
* **get_std_full_inventory.py**

To get the result the following files/folders are needed:
* **vxc_data**: folder with the original csv files downloaded from xxxxxxx
* *3vxc-documentation**: folder with the documentation files to get the inventory and vowel count
  - Downloaded from https://github.com/pacscilab/voxcommunis/tree/main/vxc-documentation
  For the languages without a documentation file I created them (see 1) and added them to the folder while for italian the inforamtion was directly sourced from the original csv file:
  - **vxc_data/it_v17_dur_f0_formants.csv**: original csv file for Italian to get the vowel inventory and count (file is needed to run the script)
* **filtered_csv**: folder created in 2.1

Output files/folders of the python script:
* **stats_output_full_inventory**: folder with the csv with the new information
* **vowel_inventory_summary_full_inventory.csv**: A summarizing csv table with the following information vowel inventory, the number of vowels and weather it has schwa or not for each language

#### 2.2.2 - For the Full inventory
Python script to generate the standard deviation, the vowel count and the vowel inventory of each langauge:
* **get_std_base_inventory.py**

To get the result the following files/folders are needed:
* **vxc_data**: folder with the original csv files downloaded from xxxxxxx
* **vxc-documentation**: folder with the documentation files to get the inventory and vowel count
  - Downloaded from https://github.com/pacscilab/voxcommunis/tree/main/vxc-documentation
  For the languages without a documentation file I created them (see 1) and added them to the folder while for italian the inforamtion was directly sourced from the original csv file:
  - **vxc_data/it_v17_dur_f0_formants.csv**: original csv file for Italian to get the vowel inventory and count (file is needed to run the script)
* **filtered_csv**: folder created in 2.1

Output files/folders of the python script:
* **stats_output_base_inventory**: folder with the csv with the new information
* **vowel_inventory_summary_base_inventory**.csv: A summarizing csv table with the following information vowel inventory, the number of vowels and weather it has schwa or not for each language

### 2.3 - Create a merged summary table
Python script to get a complete csv summary table of the standard deviation, the vowel count and the vowel inventory of each langauge::
* **vowel_inventory_complete.py**

To get the result the following files/folders are needed:
* **stats_output_full_inventory** and **stats_output_base_inventory**: folders generated in 2.2
* **vowel_inventory_summary_full_inventory.csv** and **vowel_inventory_summary_base_inventory.csv** : csv files generated in 2.2

### 2.4 - Quantitative values 
Python script to get quantitative values about the vowels studied in the Thesis:
* **count_vowel_studied.py**

To get the result the following files/folders are needed:
* **filtered_csv**: folder with filtered csv files created in 2.1

Output:
* The results are directly printed in the terminal.

### 2.5 - Vowel Inventory Image
Script to get a visual representation of the the expectation of vowel dispersion based on the Vowel Dispersion Theory:
* **vowel_inventory_ellipses.py**

No other files are needed

Output files/folders of the python script:
* **vowel_inventory_ellipses_3.png**: Representation of the expectation of a three vowel inventory
* **vowel_inventory_ellipses_12.png**: Representation of the expectation of a 12 vowel inventory


## 3 - Linear Regression Models
### 3.1 Linear regression model for the full inventory
Script to get the linear regression model and two scatter plots:
* **model_mixed_regression_full_inventory.py**

To get the result the following files/folders are needed:
* **stats_output_full_inventory**: folder with the csv files generated in 2.2

Output files/folders of the python script:
* **model_results_f1_full.csv**: csv table with the results of the model for the standard deviation of F1
* **model_results_f1_full.csv**: csv table with the results of the model for the standard deviation of F2
* **F1_std_full_inventory.png**: scatterplot with the representation of the model results for he standard deviation of F1
* **F1_std_full_inventory.png**: scatterplot with the representation of the model results for the standard deviation of F2

### 3.2 Linear regression model for the base inventory
Script to get the linear regression model and two scatter plots:
* **model_mixed_regression_base_inventory.py**

To get the result the following files/folders are needed:
* **stats_output_base_inventory**: folder with the csv files generated in 2.2

Output files/folders of the python script:
* **model_results_f1_base.csv**: csv table with the results of the model for the standard deviation of F1
* **model_results_f1_base.csv**: csv table with the results of the model for the standard deviation of F2
* **F1_std_base_inventory.png**: scatterplot with the representation of the model results for he standard deviation of F1
* **F1_std_base_inventory.png**: scatterplot with the representation of the model results for the standard deviation of F2









