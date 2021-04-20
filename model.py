import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader as web
import datetime as dt
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM


class Model:
  def __init__(self):
    stk_data = pd.read_csv('stk_data.csv')
    self.data, self.test_data = train_test_split(
      stk_data, test_size=.2, shuffle=False)
    self.scaler = MinMaxScaler(feature_range=(0,1))
    self.scaled_data = self.scaler.fit_transform(
      self.data['Close'].values.reshape(-1,1))
    prediction_days = 60
    self.x_train = []
    self.y_train = []
    for x in range(prediction_days, len(self.scaled_data)):
      self.x_train.append(self.scaled_data[x-prediction_days:x, 0])
      self.y_train.append(self.scaled_data[x, 0])
    self.x_train, self.y_train = np.array(self.x_train), np.array(self.y_train)
    self.x_train = np.reshape(
      self.x_train, (self.x_train.shape[0], self.x_train.shape[1], 1))
    #test data preparation
    self.actual_prices = self.test_data['Close'].values
    self.total_dataset = pd.concat(
      (self.data['Close'], self.test_data['Close']), axis=0)
    self.model_inputs = self.total_dataset[
      len(self.total_dataset) - len(self.test_data) - prediction_days:].values
    self.model_inputs = self.model_inputs.reshape(-1,1)
    self.model_inputs = self.scaler.transform(self.model_inputs)
    self.x_test = []
    for x in range(prediction_days, len(self.model_inputs)):
      self.x_test.append(self.model_inputs[x-prediction_days:x, 0])
    self.x_test = np.array(self.x_test)
    self.x_test = np.reshape(
      self.x_test, (self.x_test.shape[0], self.x_test.shape[1], 1))
    return

  def create(self):
    self.model = Sequential()
    self.model.add(LSTM(units=50, return_sequences=True, input_shape=(
      self.x_train.shape[1], 1)))
    self.model.add(Dropout(0.2))
    self.model.add(LSTM(units=50, return_sequences=True))
    self.model.add(Dropout(0.2))
    self.model.add(LSTM(units=50))
    self.model.add(Dropout(0.2))
    self.model.add(Dense(units=1))
    self.model.compile(optimizer='adam', loss='mean_squared_error')
    self.model.fit(self.x_train, self.y_train, epochs=25, batch_size=32)
    return self.model
    
  def predict(self, model):
    self.model = model
    self.predicted_prices = self.model.predict(self.x_test)
    self.predicted_prices = self.scaler.inverse_transform(self.predicted_prices)

  def plotting(self):
    data = pd.DataFrame()
    data['Date'] = self.test_data['Date']
    data['actual'] = self.actual_prices
    data['prediction'] = self.predicted_prices
    trace1 = go.Scatter(x=data.Date, y=data.actual, text='actual prices')
    trace2 = go.Scatter(x=data.Date, y=data.prediction, text='predicted prices')
    figure = [trace1, trace2]
    fig = {'data':figure}
    return fig

  def results(self):
    prediction_days = 60
    self.real_data = [
      self.model_inputs[
        len(self.model_inputs)+1-prediction_days:len(self.model_inputs+1), 0]]
    self.real_data = np.array(self.real_data)
    self.real_data = np.reshape(
      self.real_data, (self.real_data.shape[0], self.real_data.shape[1], 1))
    prediction = self.model.predict(self.real_data)
    prediction = self.scaler.inverse_transform(prediction)
    r2 = round(r2_score(self.actual_prices, self.predicted_prices)*100)
    return {'r2': r2,'prediction': prediction[0][0]}
