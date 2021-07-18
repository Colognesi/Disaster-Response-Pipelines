# Disaster Response Pipelines

## Summary 

Project carried out with the intention of instantiating a machine learning model to predict the type of response needed based on the written message.<br>
For the prediction, we extract values from words that are used in the news (and from blogposts) in cases of natural disasters, and with these values, we created a machine learning model to predict the type of help that a given message needs.

### Project Structure
~~~
app {
  templates {
    go.html
    master.html
  }
  run.py
}</code>

Data {
  Loaded {
    DisasterResponse.db
    ML_model.pickle
  }
  raw {
    categories.csv
    messages.csv
  }
}

Models {
  train_classifier.py
}

Notebooks {
  .ipynb_checkpoints {
      ETL Pipeline Preparation-checkpoint.ipynb
      ML Pipeline Preparation-checkpoint.ipynb
  }
  ETL Pipeline Preparation.ipynb
  ML Pipeline Preparation.ipynb
}

.gitignore
README.md
requirements.txt
~~~

## Where the Data come from?
All the data used on this project has been provided by: [**FigureEight**](https://appen.com/) in Partnership with [Udacity](https://www.udacity.com/)

## Used Libs

### Wrangling and visualization
json <br>
Plotly <br>
Pandas <br>
Flask <br>
Pickle <br>
Sqlalchemy <br>
Sys <br>
Numpy <br>

### Machine Learning
Nltk.stem <br>
Nltk.tokenize <br>
Sklearn.pipeline <br>
Sklearn.feature_extraction.text <br>
Sklearn.multioutput <br>
Sklearn.ensemble <br>
Sklearn.model_selection <br>
Sklearn.metrics <br>

### Validation Metrics
Classification_Report (Accuracy, Recall, F1-Score)

