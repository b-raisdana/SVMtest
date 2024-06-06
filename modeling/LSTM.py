import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import LSTM, Dense
from keras.utils import to_categorical
from PreProcessInterLogin import pre_process_inter_login

df = pre_process_inter_login()

# Normalizing the features
scaler = MinMaxScaler()
scaled_features = scaler.fit_transform(df[['user', 'Login Time', 'device']])

# Creating sequences
sequence_length = 3  # Example sequence length
sequences = []
labels = []

for i in range(len(scaled_features) - sequence_length):
    sequences.append(scaled_features[i:i + sequence_length])
    labels.append(scaled_features[i + sequence_length])

sequences = np.array(sequences)
labels = np.array(labels)

# Splitting the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(sequences, labels, test_size=0.2, random_state=42)

# Building the LSTM model
model = Sequential()
model.add(LSTM(50, activation='relu', input_shape=(sequence_length, 3)))
model.add(Dense(3))  # Adjust the output layer based on your specific use case

model.compile(optimizer='adam', loss='mse')

# Training the model
model.fit(X_train, y_train, epochs=200, verbose=1, validation_split=0.2)

# Evaluate the model
loss = model.evaluate(X_test, y_test, verbose=0)
print(f'Test Loss: {loss}')

# Making predictions
predictions = model.predict(X_test)

# For categorization, you might need to define categories and use a different output layer setup
