import sys
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV
import pickle


def load_data(database_filepath):
    '''
    input: database_filepath
    Output: X, Y

    custom function to load data from the database,
    creates an engine with: sqlalchemy create_engine,
    converts to a DataFrame,
    Extract X and Y and returns it.
    '''

    engine = create_engine('sqlite:///{}'.format(database_filepath))

    df = pd.read_sql_table('Disaster', engine)

    X = df['message']
    Y = df.iloc[: ,3:]
    return X, Y

def tokenize(text):
    '''
    Input: Text
    Output: clean_tokens

    Custom method created for tokenizing text data,
    After the input, tokenize text words, lemmatize it and returns clean tokens
    '''

    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()
    
    clean_tokens = []
    for tok in tokens:
        clean_tok = lemmatizer.lemmatize(tok).lower().strip()
        clean_tokens.append(clean_tok)

    return clean_tokens


def build_model():
    '''
    Input: None
    Output: CV

    Custom function created for instantiating a model with a pipeline.
    tokenizer equals to the tokenize function.
    Pipeline receives: CountVectorizer, TfidfTransformer and MultiOutputClassifier
    MultiOutputClassifier receives a RandomForestClassifier to prediction.

    parameters = {
    'clf__estimator__criterion':['gini', 'entropy'],
    'clf__estimator__n_estimators':[50,100]
    }  
    '''
    # Creating pipeline
    pipeline = Pipeline([
                ('vect', CountVectorizer(tokenizer = tokenize)),
                ('tfidf', TfidfTransformer()),
                ('clf', MultiOutputClassifier(RandomForestClassifier()))
            ])

    # I'm not using more parameters for it could take a long time to finish the fit.
    parameters = {
    'clf__estimator__criterion':['gini', 'entropy'],
    'clf__estimator__n_estimators':[50,100]
    }

    # creating a cv object for best parameters.
    cv = GridSearchCV(pipeline, param_grid = parameters, n_jobs = -1, verbose = 2, cv = 2)

    return cv

def evaluate_model(model, X_test, Y_test):
    '''
    Input: model, X_test, Y_test

    Output: Classification report for each cathegory predicted.
    '''
    categories = Y_test.columns.tolist()
    y_pred = model.predict(X_test)
    y_pred = pd.DataFrame(y_pred, columns=categories)

    for i, var in enumerate(Y_test.columns):
        print(var)
        print(classification_report(Y_test.iloc[:, i], y_pred.iloc[:, i], zero_division = 0))


def save_model(model, model_filepath):
    '''
    Input: model, model_filepath
    Output: None

    Saves the trained model on it's defined filepath using pickle
    '''

    with open(model_filepath, 'wb') as picklepath:
        pickle.dump(model, picklepath)
        picklepath.close()


def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, Y = load_data(database_filepath)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
        
        print('Building model...')
        model = build_model()
        
        print('Training model...')
        model.fit(X_train, Y_train)
        
        print('Evaluating model...')
        evaluate_model(model, X_test, Y_test)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database '\
              'as the first argument and the filepath of the pickle file to '\
              'save the model to as the second argument. \n\nExample: python '\
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()