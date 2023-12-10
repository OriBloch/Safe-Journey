import pandas as pd

# 7,728,394 items
file_path = "./accidents/US_Accidents_March23.csv"


def data_selection_by_state(state):
    df = pd.read_csv(file_path)
    new_file_name = "./accidents/selected_data_" + f"{state}.csv"
    state_df = df[df['State'] == state]
    state_df.to_csv(new_file_name, index=False)


def get_accidents(number_of_accidents, state):  # returns all the accidents in tuple form [lat, lon, datetime]
    accidents_list = []
    file_path = "./accidents/selected_data_" + f"{state}.csv"
    df = pd.read_csv(file_path, nrows=number_of_accidents)
    selected_columns = ['Start_Lat', 'Start_Lng', 'Start_Time', 'State']

    for i in range(number_of_accidents):
        lat, lon, timestamp_str, state = df[selected_columns].iloc[i]
        timestamp_dt = pd.to_datetime(timestamp_str)
        result_tuple = (lat, lon, timestamp_dt, state)
        accidents_list.append(result_tuple)
    return accidents_list


def get_length_dataset():  # data_selection_by_state("CO")
    df = pd.read_csv("./accidents/selected_data_CO.csv")
    num_data = len(df)
    return num_data
