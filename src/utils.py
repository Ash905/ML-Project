import os
import sys

import numpy as np 
import pandas as pd
try:
    import dill
except Exception:
    dill = None
import pickle
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

from src.exception import CustomException

def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)

    except Exception as e:
        raise CustomException(e, sys)
    
def evaluate_models(X_train, y_train, X_test, y_test, models, params, cv=3, scoring=None, n_jobs=-1):
    """
    Evaluate multiple models using GridSearchCV and return a detailed report.

    Args:
        X_train, y_train, X_test, y_test: training and test data
        models: dict of name -> estimator
        params: dict of name -> param grid for GridSearchCV
        cv: cross-validation folds
        scoring: scoring string or callable passed to GridSearchCV
        n_jobs: parallel jobs for GridSearchCV

    Returns:
        report: dict mapping model name -> dict with 'train_score', 'test_score', 'best_params'
    """
    try:
        report = {}
        param = params

        for name, model in models.items():
            param_grid = params.get(name, {})

            if param_grid:
                gs = GridSearchCV(model, param_grid, cv=cv, scoring=scoring, n_jobs=n_jobs, refit=True)
                gs.fit(X_train, y_train)
                best_model = gs.best_estimator_
                best_params = gs.best_params_
            else:
                # If no param grid provided, just fit the model as-is
                best_model = model
                best_model.fit(X_train, y_train)
                best_params = {}

            # Predictions
            y_train_pred = best_model.predict(X_train)
            y_test_pred = best_model.predict(X_test)

            # Scores
            train_model_score = r2_score(y_train, y_train_pred)
            test_model_score = r2_score(y_test, y_test_pred)

            report[name] = {
                "train_score": float(train_model_score),
                "test_score": float(test_model_score),
                "best_params": best_params,
            }

        return report

    except Exception as e:
        raise CustomException(e, sys)
    
def load_object(file_path):
    try:
        with open(file_path, "rb") as file_obj:
            return pickle.load(file_obj)

    except Exception as e:
        raise CustomException(e, sys)