import kagglehub


# Download latest version
#path = kagglehub.dataset_download("drsourcecode/reddit-post-title-nsfw-or-sfw")


# yall i stole the next part from the intro of a kaggle file yay

# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 20GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder

# get the dataset that i stole from kaggle 
df = pd.read_csv("kaggle_reddit-nsfw-classification-data.csv")

# there's missing values 
df = df.dropna(subset=['title'])  # Remove rows with NaN in the 'title' column

# preprocessing 
df['title'] = df['title'].str.lower().str.replace('[^a-zA-Z\\s]', '', regex=True)


# handle the target values (is_nsfw -> 1, false -> 0)
label_encoder = LabelEncoder()
df['is_nsfw'] = label_encoder.fit_transform(df['is_nsfw'])

# split to test, train 
X = df['title']
y = df['is_nsfw']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# vectorization using TF-IDF (something made by somebody way smarter than me)
vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# model training
model = LogisticRegression(max_iter=1000)
model.fit(X_train_tfidf, y_train)

# predict and evaluate 
y_pred = model.predict(X_test_tfidf)
print(f'Accuracy: {accuracy_score(y_test, y_pred)}')
print(f'Classification Report:{classification_report(y_test, y_pred)}')


# Function to predict if input text is NSFW or SFW
def predict_nsfw(input_text):
    # Preprocess the input text (convert to lowercase and remove unwanted characters)
    # Updated code to avoid SyntaxWarning by using raw string notation
    input_text = input_text.lower().replace(r'[^a-zA-Z\s]', '')

    
    # Vectorize the input text using the same vectorizer
    input_tfidf = vectorizer.transform([input_text])
    
    # Make prediction
    prediction = model.predict(input_tfidf)
    
    # Convert prediction back to label (0 = SFW, 1 = NSFW)
    if prediction == 1:
        return "NSFW"
    else:
        return "SFW"


print(predict_nsfw("I like dick"))