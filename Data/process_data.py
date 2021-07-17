import sys
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

def load_data(messages_filepath, categories_filepath):
    '''
    Input: messages_filepath, categories_filepath
    Output: df

    Receives both messages and categories csv's filepaths and converts on a DataFrame
    '''

    messages = pd.read_csv(messages_filepath)
    categories = pd.read_csv(categories_filepath)

    df = messages.merge(categories, on = ['id'])

    return df


def clean_data(df):
    '''
    Input: DF
    Output: DF

    Receives DF and clean its data
    '''

    # Get the categories column, and splits by ";"
    categories = df['categories'].str.split(';', expand = True)
    # Get the first row of categories
    row = categories.iloc[1, :]
    # defines the first row as column names
    category_colnames = row.apply(lambda x: x[: -2])
    categories.columns = category_colnames

    # Gets from every row, the last caracter and converts it to INT
    for column in categories:
        categories[column] = categories[column].str[-1:]
    
    categories[column] = categories[column].astype('int64')

    # drops the old categories to replace with the new/cleaned categories
    df.drop('categories', axis = 1, inplace = True)
    df = pd.concat([df, categories], axis = 1, join = 'inner')

    # drops duplicates(rows) and original(column)
    df.drop_duplicates(subset = ['message', 'original'], inplace = True)
    df.drop('original', axis = 1, inplace = True)

    return df

def save_data(df, database_filename):
    '''
    input: df
    output: None

    saves the df on a sqlite database, 
    table name = Disaster
    '''
    engine = create_engine('sqlite:///{}'.format(database_filename))
    df.to_sql('Disaster', engine, index=False, if_exists = 'replace')  


def main():
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)
        
        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)
        
        print('Cleaned data saved to database!')
    
    else:
        print('Please provide the filepaths of the messages and categories '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'DisasterResponse.db')


if __name__ == '__main__':
    main()