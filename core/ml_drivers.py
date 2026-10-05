"""
ML Drivers Analyzer — Local Machine Learning Engine for QueryMind
Provides Feature Importance & Drivers Analysis using Random Forest models.
Context-aware: Automatically processes Numeric, Categorical, and Text columns.
100% local — NO Gemini API dependency.
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer

def _build_dataframe(columns, rows):
    """Convert query result rows/columns into a pandas DataFrame."""
    df = pd.DataFrame(rows, columns=columns)
    # Convert obvious date strings to datetime if possible, but keep simple
    for col in df.columns:
        if df[col].dtype == object:
            try:
                # If a column is purely datetime, pandas might convert it
                dt_series = pd.to_datetime(df[col], errors='ignore')
                if pd.api.types.is_datetime64_any_dtype(dt_series):
                    df[col + '_year'] = dt_series.dt.year
                    df[col + '_month'] = dt_series.dt.month
                    df[col + '_day'] = dt_series.dt.day
                    df = df.drop(columns=[col])
            except Exception:
                pass
    return df


def _classify_columns(df):
    """
    Classify columns into numeric, categorical, and text buckets.
    """
    numeric_cols = []
    categorical_cols = []
    text_cols = []
    
    for col in df.columns:
        # Drop columns with zero variance (useless for ML)
        if df[col].nunique() <= 1:
            continue
            
        # Drop unique ID columns
        if df[col].nunique() == len(df):
            if str(col).lower() in ['id', 'uuid', 'guid'] or str(col).lower().endswith('_id'):
                continue
                
        if pd.api.types.is_numeric_dtype(df[col]):
            numeric_cols.append(col)
        else:
            # It's a string/object column
            # If low cardinality (< 20 unique values or < 20% of rows), treat as Categorical
            if df[col].nunique() < 20 or (df[col].nunique() / len(df) < 0.2):
                categorical_cols.append(col)
            else:
                text_cols.append(col)
                
    return numeric_cols, categorical_cols, text_cols


def analyze_drivers(columns, rows, target_column):
    """
    Analyzes what drives a target column using Random Forest Feature Importances.
    """
    if not rows:
        return {"success": False, "error": "No data to analyze."}

    if target_column not in columns:
        return {"success": False, "error": f"Target column '{target_column}' not found in data."}

    try:
        df = _build_dataframe(columns, rows)
        
        # Drop rows where the target column is missing
        df = df.dropna(subset=[target_column])
        if len(df) < 10:
            return {"success": False, "error": "Not enough valid data rows to analyze drivers (need at least 10)."}

        # Separate Target (y) from Features (X)
        y_raw = df[target_column]
        X = df.drop(columns=[target_column])
        
        # Determine if target is regression or classification
        is_regression = pd.api.types.is_numeric_dtype(y_raw)
        
        if is_regression:
            y = y_raw.values
        else:
            # Classification
            le = LabelEncoder()
            y = le.fit_transform(y_raw)
            # If there's only 1 class, we can't do ML
            if len(le.classes_) < 2:
                return {"success": False, "error": f"Target column '{target_column}' has only 1 unique value."}

        numeric_cols, categorical_cols, text_cols = _classify_columns(X)

        if len(numeric_cols) + len(categorical_cols) + len(text_cols) == 0:
            return {
                "success": False,
                "error": "No valid feature columns found to analyze against the target."
            }

        # Build transformations
        transformers = []
        
        if numeric_cols:
            numeric_transformer = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='median')),
                ('scaler', StandardScaler())
            ])
            transformers.append(('num', numeric_transformer, numeric_cols))
            
        if categorical_cols:
            categorical_transformer = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
            ])
            transformers.append(('cat', categorical_transformer, categorical_cols))
            
        for t_col in text_cols:
            X[t_col] = X[t_col].fillna('')
            text_transformer = TfidfVectorizer(max_features=20, stop_words='english')
            transformers.append((f'text_{t_col}', text_transformer, t_col))

        preprocessor = ColumnTransformer(transformers=transformers, remainder='drop')
        
        # Fit & Transform Features
        X_processed = preprocessor.fit_transform(X)
        if hasattr(X_processed, 'toarray'):
            X_processed = X_processed.toarray()

        # Extract feature names
        feature_names = []
        if numeric_cols:
            feature_names.extend(numeric_cols)
        if categorical_cols:
            # Get OneHotEncoder from the pipeline
            cat_encoder = preprocessor.named_transformers_['cat'].named_steps['onehot']
            cat_features = cat_encoder.get_feature_names_out(categorical_cols)
            feature_names.extend(cat_features)
        for t_col in text_cols:
            tfidf = preprocessor.named_transformers_[f'text_{t_col}']
            tfidf_features = tfidf.get_feature_names_out()
            feature_names.extend([f"{t_col} (keyword: {w})" for w in tfidf_features])

        # Train Model
        n_samples = len(X_processed)
        min_samples_leaf = 1 if n_samples < 50 else 3
        
        if is_regression:
            model = RandomForestRegressor(n_estimators=100, random_state=42, min_samples_leaf=min_samples_leaf)
        else:
            model = RandomForestClassifier(n_estimators=100, random_state=42, min_samples_leaf=min_samples_leaf)
            
        model.fit(X_processed, y)
        
        # Extract Importances
        importances = model.feature_importances_
        
        # Aggregate importances by base column if possible
        # e.g. status_completed, status_pending -> status
        aggregated_importances = {}
        for fname, imp in zip(feature_names, importances):
            # For categorical features from onehot, they look like "status_completed"
            # For tfidf, they look like "name (keyword: macbook)"
            # For numeric, they look like "price"
            base_col = fname
            if '_' in fname and fname.split('_')[0] in categorical_cols:
                base_col = fname.split('_')[0]
            elif ' (keyword:' in fname:
                base_col = fname.split(' (keyword:')[0]
                
            if base_col not in aggregated_importances:
                aggregated_importances[base_col] = 0.0
            aggregated_importances[base_col] += imp

        # Sort and Normalize
        total_imp = sum(aggregated_importances.values())
        if total_imp == 0:
             return {"success": False, "error": "Model could not find any meaningful patterns."}
             
        drivers_list = []
        for col, imp in aggregated_importances.items():
            percentage = (imp / total_imp) * 100
            if percentage > 1.0: # Only include features that contribute more than 1%
                drivers_list.append({
                    "column": col,
                    "importance_percent": round(percentage, 1)
                })
                
        # Sort by importance descending
        drivers_list.sort(key=lambda x: x["importance_percent"], reverse=True)

        return {
            "success": True,
            "target_column": target_column,
            "model_type": "RandomForestRegressor" if is_regression else "RandomForestClassifier",
            "total_rows_analyzed": len(df),
            "drivers": drivers_list[:10] # Return top 10
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        return {
            "success": False,
            "error": f"Driver analysis failed: {str(e)}"
        }
