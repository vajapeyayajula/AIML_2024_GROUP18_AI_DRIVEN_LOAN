import pandas as pd
import os
from typing import List, Dict, Any
from src.ml_project.entity.config_entity import LoanApplication
from src.ml_project.components.data_processing import dataSetPreprocessing, dervieSubsetFeatures
from sklearn.linear_model import LogisticRegression

class PredictionPipeline:
    def __init__(self):
        # Load the dataset
        dataset_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "dataset.csv")
        self.model = LogisticRegression(max_iter=1000)
        self.pipeline = None
        self.feature_names = None
        self.col_defaults = {}  # per-column fill values derived from training
        
        if os.path.exists(dataset_path):
            df_train = pd.read_csv(dataset_path)
            df_derived = dervieSubsetFeatures(df_train.copy())
            X_processed, y, self.pipeline, self.feature_names = dataSetPreprocessing(df_derived)
            
            # Pre-compute per-column defaults from the training-derived frame
            for col in self.pipeline.feature_names_in_:
                if col in df_derived.columns:
                    if pd.api.types.is_numeric_dtype(df_derived[col]):
                        self.col_defaults[col] = float(df_derived[col].median())
                    else:
                        self.col_defaults[col] = str(df_derived[col].mode()[0])
                else:
                    self.col_defaults[col] = 0.0
            
            # fit a logistic regression model on the training data
            self.model.fit(X_processed.fillna(0), y.values.ravel())
        else:
            print(f"Dataset not found at {dataset_path}")

    def predict(self, applications: List[LoanApplication]) -> List[Dict[str, Any]]:
        # Convert Pydantic models to DataFrame
        data = [app.model_dump() for app in applications]
        df = pd.DataFrame(data)
        
        # Derive subset features as per original logic
        df_derived = dervieSubsetFeatures(df.copy())
        
        # Fill any columns the pipeline expects but weren't provided,
        # using training-set defaults so the encoder never sees unknown values.
        for col in self.pipeline.feature_names_in_:
            if col not in df_derived.columns:
                df_derived[col] = self.col_defaults.get(col, 0.0)
        
        X = df_derived[self.pipeline.feature_names_in_]
        
        X_trans = self.pipeline.transform(X)
        X_processed = pd.DataFrame(X_trans, columns=self.feature_names)
        
        # Predict using model
        predictions = self.model.predict(X_processed.fillna(0))
        
        results = []
        for i, pred in enumerate(predictions):
            results.append({
                "application_index": i,
                "prediction": "Approved" if pred == 1 else "Rejected"
            })
            
        return results
