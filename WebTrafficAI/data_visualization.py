import matplotlib.pyplot as plt
import seaborn as sns

def visualize_data(df):
    sns.pairplot(df)
    plt.show()

def visualize_predictions(y_test, y_pred, model_name):
    plt.figure(figsize=(10, 6))
    plt.plot(y_test.values, label='Actual')
    plt.plot(y_pred, label='Predicted', linestyle='--')
    plt.title(f'{model_name} - Actual vs Predicted')
    plt.legend()
    plt.show()
