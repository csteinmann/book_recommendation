"""
Compress and Clean the initial csv file survey_response.csv which contained all demographic and answer data of the survey.
The data is split based on the rotation_state. After that, all columns of each dataframe, where all entries are empty
are removed. After that the columns are renamed to match (solves issue of having answers for questions 1 ... 144 instead
of  1 ... 24. Then all these compressed and summarised dataframes are saved individually into a csv file
"""

import pandas as pd

df = pd.read_csv('../data/survey_response_raw.csv')


# Get unique rotation_state values
unique_rotation_states = df['rotation_state'].unique()

# Create a dictionary to store the separate dataframes
dfs_by_rotation_state = {}

desired_columns = ['SurveyResponseID', 'rotation_state', 'age_group', 'gender', 'reading_platform', 'book_frequency', 'genre', 'sessionId', 'answer_to_1', 'answer_to_2', 'answer_to_3', 'answer_to_4', 'answer_to_5', 'answer_to_6', 'answer_to_7', 'answer_to_8', 'answer_to_9', 'answer_to_10', 'answer_to_11', 'answer_to_12', 'answer_to_13', 'answer_to_14', 'answer_to_15', 'answer_to_16', 'answer_to_17', 'answer_to_18', 'answer_to_19', 'answer_to_20', 'answer_to_21', 'answer_to_22', 'answer_to_23', 'answer_to_24']

# Split the dataframe based on rotation_state and store in the dictionary
for rotation_state in unique_rotation_states:
    dfs_by_rotation_state[rotation_state] = df[df['rotation_state'] == rotation_state]

# Remove columns with all NaN values from each dataframe
for rotation_state, dataframe in dfs_by_rotation_state.items():
    # drop question column where there is no answer
    dfs_by_rotation_state[rotation_state] = dataframe.dropna(axis=1, how='all')
    # rename columns to be uniform
    dfs_by_rotation_state[rotation_state].columns = desired_columns
    # Remove rows, where the attention check question was falsely answered
    dfs_by_rotation_state[rotation_state] = dfs_by_rotation_state[rotation_state].loc[dfs_by_rotation_state[rotation_state]['answer_to_14'] == 'About the same']

    csv_file_path = f'../data/survey_response_{rotation_state}.csv'
    dfs_by_rotation_state[rotation_state].to_csv(csv_file_path, index=False)

# Concatenate all dataframes in dfs_by_rotation_state
final_dataframe = pd.concat(dfs_by_rotation_state.values(), ignore_index=True)

# Save the concatenated dataframe to a CSV file
final_dataframe.to_csv('../data/survey_response.csv', index=False)

# Mapping
replace_mapping = {
    'Bit more A than B': 'Bit more B than A',
    'Bit more B than A': 'Bit more A than B',
    'Much more A than B': 'Much more B than A',
    'Much more B than A': 'Much more A than B'
}

# for II v. UU UUII is changed to match the squence of IIUU
for col in dfs_by_rotation_state['UUII'].columns:
    if col.startswith('answer_to_'):
        dfs_by_rotation_state['UUII'][col] = dfs_by_rotation_state['UUII'][col].replace(replace_mapping)
df_IIvUU = pd.concat([dfs_by_rotation_state['IIUU'], dfs_by_rotation_state['UUII']], ignore_index=True)
df_IIvUU.to_csv('../data/IIvUU.csv', index=False)

# for II v. ALS ALSII is changed to match the squence of IIALS
for col in dfs_by_rotation_state['ALSII'].columns:
    if col.startswith('answer_to_'):
        dfs_by_rotation_state['ALSII'][col] = dfs_by_rotation_state['ALSII'][col].replace(replace_mapping)
df_IIvALS = pd.concat([dfs_by_rotation_state['IIALS'], dfs_by_rotation_state['ALSII']], ignore_index=True)
df_IIvALS.to_csv('../data/IIvALS.csv', index=False)

# for ALS v. UU UUALS is changed to match the sequence of UUALS
for col in dfs_by_rotation_state['UUALS'].columns:
    if col.startswith('answer_to_'):
        dfs_by_rotation_state['UUALS'][col] = dfs_by_rotation_state['UUALS'][col].replace(replace_mapping)
df_ALSvUU = pd.concat([dfs_by_rotation_state['ALSUU'], dfs_by_rotation_state['UUALS']], ignore_index=True)
df_ALSvUU.to_csv('../data/ALSvUU.csv', index=False)

