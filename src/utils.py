#A generic code to operate in whole program file like  extracting database form mongo db 
import os
import sys
import numpy as np
import pandas as pd
import dill
from sklearn.metrics import r2_score

from src.exception import CustomException

def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)
        
        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, 'wb') as file_obj:
            dill.dump(obj, file_obj)    

    except Exception as e:
        raise CustomException(e, sys)
    
def evaluate_models(X_train, y_train, X_test, y_test, models):
    try:
        report = {}
        for i in range(len(models)):
            model = list(models.values())[i] # Training the data on each and every model

            model.fit(X_train, y_train)  # Trrainign the model 

            y_train_pred  = model.predict(X_train)  # Predicting the training data

            y_test_pred = model.predict(X_test)  # Predicting the test data

            train_model_score = r2_score(y_train, y_train_pred)  # Evaluating the model on training data

            test_model_score = r2_score(y_test, y_test_pred) # Evlauting the model on test data
            

            report[list(models.keys())[i]] = test_model_score

        return report 
    
    except Exception as e:
        raise CustomException(e, sys)





