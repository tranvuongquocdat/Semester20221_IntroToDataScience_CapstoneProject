from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

def eval_baseline(X_train, X_test, y_train, y_test, model = RandomForestRegressor(n_estimators = 300, verbose = 1, random_state = 42)): 
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    r2 = r2_score(preds, y_test)
    return r2

