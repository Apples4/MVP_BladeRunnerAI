#!/usr/bin/python3

import pandas as pd
import os


def update_main(new_detection_path: str, maindata_path: str):
    """
    This function updates the number of detection of the system

    params:
        new_detection_path: is a path to a CSV of new detections
        maindata_path: path to csv main detections
    output:
        updated main csv
    """
    if new_detection_path is None or not isinstance(new_detection_path, str):
        print("Provide link to new_data.csv")

    if maindata_path is None or not isinstance(maindata_path, str):
        print("Provide link to main_data.csv")
    
    """
    Entering pathway of cvs's
    """
    df_main = pd.read_csv(maindata_path)
    df_new = pd.read_csv(new_detection_path)

    """
    Operations of the data frame
    """
    if not df_new.empty:
        " Set 'class_name' as index for easy operation"
        df_main.set_index('class_name', inplace=True)
        df_new.set_index('class_name', inplace=True)

        "Count the number of occurrences of each class in df_new"
        df_new_counts = df_new.index.value_counts()

        "Find the intersection of the 'class_name' in both dataframes"
        common_classes = df_main.index.intersection(df_new_counts.index)

        "Increment the count in df_main for the common classes"
        df_main.loc[common_classes, 'counts'] += df_new_counts.loc[common_classes]

        "Find new classes that are in df_new but not in df_main"
        new_classes = df_new_counts.index.difference(df_main.index)

        "Add new classes to df_main"
        df_main = pd.concat([df_main, pd.DataFrame({'class_name': new_classes,
                                                    'counts': df_new_counts.loc[new_classes]})])

        "Reset the index"
        df_main.reset_index(drop=True, inplace=True)
        "saving tthe csv file and deleting the new data"
        df_main.to_csv(maindata_path, index=False)
    else:
        print("df_new is empty. Please check your date.")
