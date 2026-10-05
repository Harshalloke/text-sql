"""
ML Analyzer — Local Machine Learning Engine for QueryMind
Provides anomaly detection using Isolation Forest & LocalOutlierFactor.
Context-aware: Automatically processes Numeric, Categorical, and Text columns.
100% local — NO Gemini API dependency.
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.preprocessing import StandardScaler, OneHotEncoder
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
                df[col] = pd.to_datetime(df[col])
                # We can extract useful numeric features from dates
                df[col + '_year'] = df[col].dt.year
                df[col + '_month'] = df[col].dt.month
                df[col + '_day'] = df[col].dt.day
                df = df.drop(columns=[col])
            except (ValueError, TypeError):
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
            
        # Drop unique ID columns (if every row is unique and it's an int/string)
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


def _generate_human_reason(row_series, col_stats, numeric_cols):
    """
    Generate numeric explanations. We keep the explanation purely numeric
    for simplicity, but the model's decision to flag it was context-aware.
    """
    reasons = []
    for col in numeric_cols:
        val = row_series.get(col)
        if val is None or pd.isna(val):
            continue
        stats = col_stats.get(col, {})
        mean = stats.get('mean', None)
        std = stats.get('std', None)
        q1 = stats.get('q1', None)
        q3 = stats.get('q3', None)
        iqr = stats.get('iqr', None)

        if mean is None or std is None:
            continue

        z = abs((val - mean) / std) if std > 0 else 0

        if q1 is not None and iqr is not None and iqr > 0:
            lower_fence = q1 - 1.5 * iqr
            upper_fence = q3 + 1.5 * iqr
        else:
            lower_fence = mean - 3 * std
            upper_fence = mean + 3 * std

        if val > upper_fence:
            ratio = round(val / mean, 1) if mean != 0 else None
            if ratio:
                reasons.append("{} is {}x higher than average ({})".format(col, ratio, round(mean, 2)))
            else:
                reasons.append("{} is far above the expected upper limit ({})".format(col, round(upper_fence, 2)))
        elif val < lower_fence:
            ratio = round(mean / val, 1) if val != 0 else None
            if ratio:
                reasons.append("{} is {}x lower than average ({})".format(col, ratio, round(mean, 2)))
            else:
                reasons.append("{} is far below the expected lower limit ({})".format(col, round(lower_fence, 2)))
        elif z > 2.5:
            direction = 'high' if val > mean else 'low'
            reasons.append("{} is unusually {} (z-score: {})".format(col, direction, round(z, 1)))

    return reasons[:3]


def detect_anomalies(columns, rows, table_name="data", contamination=0.1):
    """
    Context-Aware Anomaly Detection
    """
    if not rows:
        return {"success": False, "error": "No data to analyze. The table appears to be empty."}

    try:
        df = _build_dataframe(columns, rows)
        original_len = len(df)

        numeric_cols, categorical_cols, text_cols = _classify_columns(df)

        if len(numeric_cols) == 0:
            return {
                "success": False,
                "error": "No numeric columns found in this dataset. Anomaly detection requires at least one numeric feature."
            }

        # Build transformations
        transformers = []
        
        # 1. Numeric Transformation
        numeric_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())
        ])
        transformers.append(('num', numeric_transformer, numeric_cols))
        
        # 2. Categorical Transformation
        if categorical_cols:
            categorical_transformer = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
            ])
            transformers.append(('cat', categorical_transformer, categorical_cols))
            
        # 3. Text Transformation
        # TfidfVectorizer expects a 1D array, so we must add a separate transformer for each text column
        for t_col in text_cols:
            # Impute NaN with empty string first
            df[t_col] = df[t_col].fillna('')
            text_transformer = TfidfVectorizer(max_features=20, stop_words='english')
            transformers.append((f'text_{t_col}', text_transformer, t_col))

        preprocessor = ColumnTransformer(transformers=transformers, remainder='drop')
        
        # Transform the data into the final mathematical matrix
        X_scaled = preprocessor.fit_transform(df)
        if hasattr(X_scaled, 'toarray'):
            X_scaled = X_scaled.toarray()

        # Pre-compute column statistics for human explanations (only on numeric cols)
        col_stats = {}
        for col in numeric_cols:
            s = df[col].dropna()
            if len(s) == 0:
                continue
            q1 = s.quantile(0.25)
            q3 = s.quantile(0.75)
            col_stats[col] = {
                'mean': s.mean(),
                'std': s.std(),
                'median': s.median(),
                'q1': q1,
                'q3': q3,
                'iqr': q3 - q1
            }

        # ---- MODEL 1: Isolation Forest ----
        n_samples = len(df)
        safe_contamination = max(1 / n_samples, min(contamination, 0.5))

        iso_forest = IsolationForest(
            n_estimators=200,
            contamination=safe_contamination,
            random_state=42,
            n_jobs=-1
        )
        iso_scores = iso_forest.fit_predict(X_scaled)
        iso_raw_scores = iso_forest.decision_function(X_scaled)

        # ---- MODEL 2: Local Outlier Factor ----
        lof_scores = np.ones(n_samples)
        lof_raw = np.zeros(n_samples)
        # LOF can struggle with highly sparse data (like heavy text features), 
        # but with max_features=20 it should be okay. We require >= 5 samples.
        use_lof = n_samples >= 5
        if use_lof:
            n_neighbors = min(20, n_samples - 1)
            lof = LocalOutlierFactor(
                n_neighbors=n_neighbors,
                contamination=safe_contamination,
                n_jobs=-1
            )
            # Ensure X_scaled is contiguous array for LOF
            X_scaled_np = np.asarray(X_scaled)
            lof_scores = lof.fit_predict(X_scaled_np)
            lof_raw = -lof.negative_outlier_factor_

        # ---- Combine scores into 0-100 Anomaly Score ----
        iso_normalized = 1 - (iso_raw_scores - iso_raw_scores.min()) / \
                         (iso_raw_scores.max() - iso_raw_scores.min() + 1e-9)

        if use_lof:
            lof_normalized = (lof_raw - lof_raw.min()) / \
                             (lof_raw.max() - lof_raw.min() + 1e-9)
            combined = 0.60 * iso_normalized + 0.40 * lof_normalized
        else:
            combined = iso_normalized

        anomaly_scores_0_100 = (combined * 100).astype(int)
        anomaly_scores_0_100 = np.clip(anomaly_scores_0_100, 0, 100)

        is_anomaly = (iso_scores == -1)
        if use_lof:
            is_anomaly = is_anomaly | (lof_scores == -1)

        # ---- Build enriched result rows ----
        enriched_rows = []
        for i, row in enumerate(rows):
            # Pass original row dict for explanation, but use numeric_cols
            row_series = pd.Series(row)
            score = int(anomaly_scores_0_100[i])
            flagged = bool(is_anomaly[i])

            if flagged:
                reasons = _generate_human_reason(row_series, col_stats, numeric_cols)
                if not reasons:
                    # If it was flagged primarily due to context/text and the numbers are fine:
                    reasons = ["Contextual Anomaly: Unusual combination of text, categories, and numbers"]
            else:
                reasons = []

            enriched_rows.append(dict(
                list(row.items()) + [
                    ("_anomaly_score", score),
                    ("_is_anomaly", flagged),
                    ("_reasons", reasons)
                ]
            ))

        anomaly_count = int(is_anomaly.sum())
        normal_count = original_len - anomaly_count

        return {
            "success": True,
            "table_name": table_name,
            "total_rows": original_len,
            "anomaly_count": anomaly_count,
            "normal_count": normal_count,
            "numeric_cols_used": numeric_cols,
            "contamination_rate": round(anomaly_count / original_len * 100, 1),
            "rows": enriched_rows,
            "columns": columns,
            "summary": {
                "models_used": (
                    ["Isolation Forest (200 trees)", "Local Outlier Factor"]
                    if use_lof else
                    ["Isolation Forest (200 trees)"]
                ),
                "ensemble_weights": (
                    "60% IsolationForest + 40% LocalOutlierFactor"
                    if use_lof else "100% IsolationForest"
                ),
                "top_anomaly_score": int(anomaly_scores_0_100.max()),
                "avg_anomaly_score": int(anomaly_scores_0_100.mean()),
            }
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        return {
            "success": False,
            "error": "Anomaly detection failed: {}".format(str(e))
        }
