from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor
import tensorflow as tf
from sklearn.metrics import mean_squared_error

def hyperparameter_tuning(df, model_name):
    X = df[['Page Views', 'Clicks', 'Session Duration', 'Bounce Rate', 'IsWeekend', 'PageViews_per_Click', 'SessionDuration_per_PageView']]
    y = df['User Traffic']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    if model_name == 'Random Forest':
        param_grid = {
            'n_estimators': [100, 200, 300],
            'max_depth': [10, 20, 30]
        }
        model = RandomForestRegressor(random_state=42)
        grid_search = GridSearchCV(model, param_grid, cv=3, scoring='neg_mean_squared_error', verbose=1)
        grid_search.fit(X_train, y_train)
        best_params = grid_search.best_params_
        best_model = grid_search.best_estimator_
    elif model_name == 'TensorFlow Neural Network':
        best_params = {
            'layers': [64, 128],
            'epochs': [50, 100],
            'batch_size': [32, 64]
        }
        best_model = tf.keras.Sequential([
            tf.keras.layers.Dense(best_params['layers'][0], activation='relu', input_shape=(X_train.shape[1],)),
            tf.keras.layers.Dense(best_params['layers'][1], activation='relu'),
            tf.keras.layers.Dense(1)
        ])
        best_model.compile(optimizer='adam', loss='mse')
        best_model.fit(X_train, y_train, epochs=best_params['epochs'][0], batch_size=best_params['batch_size'][0], verbose=0)
    
    mse = mean_squared_error(y_test, best_model.predict(X_test).flatten())
    return best_params, mse
