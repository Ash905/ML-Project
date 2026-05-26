# Model training utilities
import os
import sys
from dataclasses import dataclass

from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor,
)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from src.exception import CustomException
from src.logger import logging
from src.utils import evaluate_models, save_object


@dataclass
class ModelTrainerConfig:
    trained_model_file_path: str = os.path.join("artifacts", "model.pkl")


class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def _get_catboost_model(self):
        """Attempt to import and return a CatBoostRegressor instance, or None if unavailable."""
        try:
            from catboost import CatBoostRegressor

            return CatBoostRegressor(verbose=False)
        except Exception:
            logging.warning("CatBoost not available; skipping CatBoost model.")
            return None

    def initiate_model_trainer(self, train_array, test_array):
        try:
            logging.info("Splitting training and test input data")
            X_train, y_train = train_array[:, :-1], train_array[:, -1]
            X_test, y_test = test_array[:, :-1], test_array[:, -1]

            models = {
                "Random Forest": RandomForestRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "Linear Regression": LinearRegression(),
                "K-Neighbors Regressor": KNeighborsRegressor(),
                "XGBRegressor": XGBRegressor(),
                "AdaBoost Regressor": AdaBoostRegressor(),
            }

            cat_model = self._get_catboost_model()
            if cat_model is not None:
                models["CatBoosting Regressor"] = cat_model

            model_report = evaluate_models(
                X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test, models=models
            )

            # select best model by test score  ->> 0.8804332983749565
            best_model_name = max(model_report, key=model_report.get)
            best_model_score = model_report[best_model_name]
            best_model = models[best_model_name]

            if best_model_score < 0.6:
                raise CustomException("No best model found with score >= 0.6")

            logging.info(
                f"Best model: {best_model_name} with r2 score: {best_model_score}"
            )

            save_object(file_path=self.model_trainer_config.trained_model_file_path, obj=best_model)

            y_pred = best_model.predict(X_test)
            final_r2 = r2_score(y_test, y_pred)
            return final_r2

        except Exception as e:
            raise CustomException(e, sys)

