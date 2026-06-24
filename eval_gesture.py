import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import confusion_matrix, accuracy_score

train_df = pd.read_csv(r"C:\Users\marti\.gemini\antigravity-ide\brain\f16046aa-3f54-4622-8a4b-93ed96d40a4b\scratch\train_emg.csv")
test_df = pd.read_csv(r"C:\Users\marti\.gemini\antigravity-ide\brain\f16046aa-3f54-4622-8a4b-93ed96d40a4b\scratch\test_emg.csv")
preds = pd.read_csv("predictions.csv", header=None).values.flatten()

le = LabelEncoder()
le.fit(train_df['class'])

y_true_str = test_df['class'].values
y_pred_str = le.inverse_transform(preds.astype(int))

def get_gesture(label):
    return label.split('_', 1)[1]

y_true_ges = [get_gesture(x) for x in y_true_str]
y_pred_ges = [get_gesture(x) for x in y_pred_str]

acc = accuracy_score(y_true_ges, y_pred_ges)
print(f"Gesture Disambiguation Accuracy: {acc*100:.2f}%")

cm = confusion_matrix(y_true_ges, y_pred_ges)
labels = sorted(list(set(y_true_ges)))

print("\nConfusion Matrix (Gestures only):")
df_cm = pd.DataFrame(cm, index=labels, columns=labels)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
print(df_cm)
