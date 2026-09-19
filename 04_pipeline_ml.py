"""Pipeline reproduzivel da Parte 2 do CP4.

Pode receber o DataFrame retornado pelo Oracle ou ler o CSV para teste local.
O holdout fica separado antes do tuning. Imputacao e one-hot ficam dentro do
Pipeline, portanto usam apenas os dados de treino durante o ajuste.
"""

from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeClassifier


RANDOM_STATE = 42
DATA_PATH = Path(__file__).with_name("data.csv")


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    result.columns = [str(column).upper() for column in result.columns]
    return result


def build_features(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    data = normalize_columns(df)
    data["DT_CUSTOMER"] = pd.to_datetime(data["DT_CUSTOMER"], errors="coerce")

    # Features criadas antes do split, sem usar RESPONSE.
    data["AGE_AT_2014"] = 2014 - data["YEAR_BIRTH"]
    data["TOTAL_CHILDREN"] = data["KIDHOME"] + data["TEENHOME"]
    spend_columns = [
        "MNTWINES", "MNTFRUITS", "MNTMEATPRODUCTS",
        "MNTFISHPRODUCTS", "MNTSWEETPRODUCTS", "MNTGOLDPRODS",
    ]
    purchase_columns = [
        "NUMDEALSPURCHASES", "NUMWEBPURCHASES",
        "NUMCATALOGPURCHASES", "NUMSTOREPURCHASES",
    ]
    campaign_columns = [
        "ACCEPTEDCMP1", "ACCEPTEDCMP2", "ACCEPTEDCMP3",
        "ACCEPTEDCMP4", "ACCEPTEDCMP5",
    ]
    data["TOTAL_SPEND"] = data[spend_columns].sum(axis=1)
    data["TOTAL_PURCHASES"] = data[purchase_columns].sum(axis=1)
    data["CAMPAIGNS_ACCEPTED"] = data[campaign_columns].sum(axis=1)
    data["WEB_PURCHASE_SHARE"] = (
        data["NUMWEBPURCHASES"] / data["TOTAL_PURCHASES"].replace(0, 1)
    )
    data["CUSTOMER_TENURE_DAYS"] = (
        pd.Timestamp("2014-06-30") - data["DT_CUSTOMER"]
    ).dt.days

    y = data.pop("RESPONSE").astype(int)
    X = data.drop(
        columns=["ID", "YEAR_BIRTH", "DT_CUSTOMER", "Z_COSTCONTACT", "Z_REVENUE"]
    )
    return X, y


def make_preprocessor(X: pd.DataFrame) -> ColumnTransformer:
    numeric_columns = X.select_dtypes(include="number").columns.tolist()
    categorical_columns = X.select_dtypes(exclude="number").columns.tolist()

    numeric = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
    ])
    categorical = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore")),
    ])
    return ColumnTransformer([
        ("numeric", numeric, numeric_columns),
        ("categorical", categorical, categorical_columns),
    ])


def evaluate(name: str, model: Pipeline, X_test: pd.DataFrame, y_test: pd.Series) -> dict:
    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)[:, 1]
    metrics = {
        "model": name,
        "precision": precision_score(y_test, predictions, zero_division=0),
        "recall": recall_score(y_test, predictions, zero_division=0),
        "f1": f1_score(y_test, predictions, zero_division=0),
        "roc_auc": roc_auc_score(y_test, probabilities),
    }
    print(pd.Series(metrics).to_string())
    return metrics


def run(df: pd.DataFrame) -> pd.DataFrame:
    X, y = build_features(df)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, stratify=y, random_state=RANDOM_STATE
    )

    reference = Pipeline([
        ("preprocessor", make_preprocessor(X_train)),
        ("model", DecisionTreeClassifier(random_state=RANDOM_STATE)),
    ])
    reference.fit(X_train, y_train)
    results = [evaluate("reference", reference, X_test, y_test)]

    tuned = Pipeline([
        ("preprocessor", make_preprocessor(X_train)),
        ("model", DecisionTreeClassifier(random_state=RANDOM_STATE)),
    ])
    search = GridSearchCV(
        tuned,
        param_grid={
            "model__criterion": ["gini", "entropy", "log_loss"],
            "model__max_depth": [3, 5, 8, None],
            "model__min_samples_leaf": [1, 5, 10, 20],
            "model__class_weight": [None, "balanced"],
        },
        scoring="roc_auc",
        cv=5,
        n_jobs=-1,
        refit=True,
    )
    search.fit(X_train, y_train)
    print("best_params")
    print(search.best_params_)
    results.append(evaluate("tuned", search.best_estimator_, X_test, y_test))
    return pd.DataFrame(results)


if __name__ == "__main__":
    source = Path(r"C:\Users\israel.toledo\Downloads\data.csv")
    metrics = run(pd.read_csv(source))
    print("\nmetricas finais")
    print(metrics.to_string(index=False))

