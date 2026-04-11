from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import KNNImputer
import pandas as pd
import numpy as np

def dataSetPreprocessing(dataSetFrame):
    # Separate target variable 'Default_Status' from features
    X = dataSetFrame.drop('Default_Status', axis=1, errors='ignore')
    if 'Default_Status' in dataSetFrame.columns:
        y = dataSetFrame['Default_Status']
    else:
        y = None
        
    # get categorical columns
    categorical_cols = X.select_dtypes(include=['object', 'category']).columns
    numerical_cols = X.select_dtypes(exclude=['object', 'category']).columns

    numerical_transformer = MinMaxScaler()
    categorical_transformer = Pipeline(steps=[
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    imputer = Pipeline(steps=[
        ('imputer', KNNImputer(n_neighbors=5))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numerical_transformer, numerical_cols),
            ('cat', categorical_transformer, categorical_cols)
        ])

    preProcessingPipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('imputer', imputer)
    ])

    # applying preprocessing to the dataset
    X_processed = preProcessingPipeline.fit_transform(X)
    
    if len(categorical_cols) > 0:
        onehot_feature_names = preProcessingPipeline.named_steps['preprocessor'].named_transformers_['cat'].named_steps['onehot'].get_feature_names_out(categorical_cols)
    else:
        onehot_feature_names = []
        
    processed_feature_names = list(numerical_cols) + list(onehot_feature_names)

    # make it back to a DF
    X_processed_df = pd.DataFrame(X_processed, columns=processed_feature_names)
    
    if y is not None:
        return X_processed_df, pd.DataFrame(y), preProcessingPipeline, processed_feature_names
    return X_processed_df, None, preProcessingPipeline, processed_feature_names

def correlationAnalysis(df, y_target, num_features=10):
    # Combine processed features and the target variable
    data_for_correlation = df.copy()
    data_for_correlation['Default_Status'] = y_target

    # Calculate the correlation matrix
    correlation_matrix = data_for_correlation.corr()
    print(f"Top {num_features} features most correlated with 'Default_Status':\n")
    top_correlated_features = correlation_matrix['Default_Status'].sort_values(ascending=False).head(num_features + 1).iloc[1:] # Exclude self-correlation
    return top_correlated_features

def dervieSubsetFeatures(df):
    epsilon = 1e-9 # A small value to prevent division by zero
    
    if 'Monthly_Expenses' in df.columns and 'Annual_Income' in df.columns:
        df['FOIR_Score'] = df['Monthly_Expenses'] / (df['Annual_Income'] / 12 + epsilon)
        
    if 'Annual_Income' in df.columns and 'Dependents' in df.columns:
        df['Financial_Burden'] = df['Annual_Income'] / (df['Dependents'] + 1 + epsilon)
        
    if 'FICO_Score' in df.columns and 'Debt_to_Income_Ratio' in df.columns and 'Credit_Utilization' in df.columns:
        df['Lending_Score'] = 0.3 * df['FICO_Score'] - 0.2 * df['Debt_to_Income_Ratio'] - 0.1 * df['Credit_Utilization']
        
    if 'Debt_to_Income_Ratio' in df.columns and 'Credit_Utilization' in df.columns:
        df['Credit_Stress'] = df['Debt_to_Income_Ratio'] * df['Credit_Utilization']
        
    return df
