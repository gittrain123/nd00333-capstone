from sklearn.linear_model import LogisticRegression
import argparse
import os
import numpy as np
from sklearn.metrics import mean_squared_error
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
from azureml.core.run import Run
from azureml.data.dataset_factory import TabularDatasetFactory
from azureml.core import Workspace, Dataset

def main():
    # Add arguments to script
    parser = argparse.ArgumentParser()

    parser.add_argument('--C', type=float, default=1.0, help="Inverse of regularization strength. Smaller values cause stronger regularization")
    parser.add_argument('--max_iter', type=int, default=100, help="Maximum number of iterations to converge")

    args = parser.parse_args()

    run = Run.get_context()

    run.log("Regularization Strength:", np.float(args.C))
    run.log("Max iterations:", np.int(args.max_iter))

    # TODO: Create TabularDataset using TabularDatasetFactory
    # Data is located at:
    # "https://automlsamplenotebookdata.blob.core.windows.net/automl-sample-notebook-data/bankmarketing_train.csv"
    url =  "https://raw.githubusercontent.com/gittrain123/nd00333-capstone/master/starter_file/forest_fire_cleaned.csv"
 
    data = Dataset.Tabular.from_delimited_files(path=url)
    df = data.to_pandas_dataframe()
    y = df["Classes_mapped"]
    x = df.drop(["Classes_mapped"], axis =1)

    x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.3, random_state=0)

    model = LogisticRegression(C=args.C, max_iter=args.max_iter).fit(x_train, y_train)

    accuracy = model.score(x_test, y_test)
    joblib.dump(value=model,filename='outputs/model.pkl')
    run.upload_file(name='model.pkl', path_or_stream='outputs/model.pkl')
    run.log("Accuracy", np.float(accuracy))

if __name__ == '__main__':
    main()