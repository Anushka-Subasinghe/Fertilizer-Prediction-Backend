import joblib
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import pandas as pd

# Load the dataset
data = pd.read_csv('Fertilizer Prediction.csv')

# Encoding categorical variables
le_soil = LabelEncoder()
le_crop = LabelEncoder()
le_fertilizer = LabelEncoder()

data['Soil Type'] = le_soil.fit_transform(data['Soil Type'])
data['Crop Type'] = le_crop.fit_transform(data['Crop Type'])
data['Fertilizer Name'] = le_fertilizer.fit_transform(data['Fertilizer Name'])

# Features and target variable
X = data.drop('Fertilizer Name', axis=1)  # Features
y = data['Fertilizer Name']  # Target

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the RandomForestClassifier
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Make predictions
y_pred = clf.predict(X_test)

# Evaluate the model
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

# Save the model and LabelEncoders
joblib.dump(clf, 'fertilizer_model.joblib')
joblib.dump(le_soil, 'soil_label_encoder.joblib')
joblib.dump(le_crop, 'crop_label_encoder.joblib')
joblib.dump(le_fertilizer, 'fertilizer_label_encoder.joblib')
