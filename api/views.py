from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import StockPredictionSerializer
from rest_framework import status
from rest_framework.response import Response
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os
from django.conf import settings
from .utils import save_plot

# ── Pure-numpy LSTM inference (no tensorflow / onnxruntime needed) ──────────

WEIGHTS_PATH = os.path.join(settings.BASE_DIR, 'stock_prediction_weights.npz')
_W = np.load(WEIGHTS_PATH)


def _sigmoid(x):
    return 1.0 / (1.0 + np.exp(-np.clip(x, -500, 500)))


def _tanh(x):
    return np.tanh(x)


def _lstm_step(x_t, h_prev, c_prev, W_i, W_h, b):
    """Single LSTM time-step (Keras gate order: i, f, c, o)."""
    z = x_t @ W_i + h_prev @ W_h + b
    units = h_prev.shape[-1]
    i = _sigmoid(z[:, :units])
    f = _sigmoid(z[:, units:2*units])
    c_cand = _tanh(z[:, 2*units:3*units])
    o = _sigmoid(z[:, 3*units:])
    c_new = f * c_prev + i * c_cand
    h_new = o * _tanh(c_new)
    return h_new, c_new


def _lstm_forward(x, W_i, W_h, b, return_sequences=False):
    """Run LSTM over a 3-D input (batch, timesteps, features)."""
    batch, timesteps, _ = x.shape
    units = b.shape[0] // 4
    h = np.zeros((batch, units), dtype=np.float64)
    c = np.zeros((batch, units), dtype=np.float64)
    if return_sequences:
        outputs = np.zeros((batch, timesteps, units), dtype=np.float64)
    for t in range(timesteps):
        h, c = _lstm_step(x[:, t, :], h, c, W_i, W_h, b)
        if return_sequences:
            outputs[:, t, :] = h
    return outputs if return_sequences else h


def _predict(x_input):
    """Feed-forward through the whole model: LSTM→LSTM→Dense→Dense."""
    x = x_input.astype(np.float64)
    # LSTM 1 (return_sequences=True, 128 units)
    x = _lstm_forward(x, _W['lstm_w0'], _W['lstm_w1'], _W['lstm_w2'], return_sequences=True)
    # LSTM 2 (return_sequences=False, 64 units)
    x = _lstm_forward(x, _W['lstm_1_w0'], _W['lstm_1_w1'], _W['lstm_1_w2'], return_sequences=False)
    # Dense 1 (64 → 25)
    x = x @ _W['dense_w0'] + _W['dense_w1']
    # Dense 2 (25 → 1)
    x = x @ _W['dense_1_w0'] + _W['dense_1_w1']
    return x


class SimpleMinMaxScaler:
    """Lightweight MinMaxScaler replacement (avoids scikit-learn + scipy ~70MB)."""
    def __init__(self, feature_range=(0, 1)):
        self.feature_range = feature_range
        self.min_ = None
        self.scale_ = None

    def fit_transform(self, data):
        self.min_ = data.min(axis=0)
        data_range = data.max(axis=0) - self.min_
        data_range[data_range == 0] = 1  # avoid division by zero
        self.scale_ = (self.feature_range[1] - self.feature_range[0]) / data_range
        return (data - self.min_) * self.scale_ + self.feature_range[0]

    def inverse_transform(self, data):
        return (data - self.feature_range[0]) / self.scale_ + self.min_


def _mean_squared_error(y_true, y_pred):
    return float(np.mean((y_true - y_pred) ** 2))


def _r2_score(y_true, y_pred):
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    return float(1 - ss_res / ss_tot) if ss_tot != 0 else 0.0


class StockPredictionAPIView(APIView):
    def post(self, request):
        serializer = StockPredictionSerializer(data=request.data)
        if serializer.is_valid():
            ticker = serializer.validated_data['ticker']

            # Fetch the data from yfinance
            now = datetime.now()
            start = datetime(now.year-10, now.month, now.day)
            end = now
            df = yf.download(ticker, start, end)
            if df.empty:
                return Response({"error": "No data found for the given ticker.",
                                 'status': status.HTTP_404_NOT_FOUND})
            df = df.reset_index()
            # Generate Basic Plot
            plt.switch_backend('AGG')
            plt.figure(figsize=(12, 5))
            plt.plot(df.Close, label='Closing Price')
            plt.title(f'Closing price of {ticker}')
            plt.xlabel('Days')
            plt.ylabel('Price')
            plt.legend()
            # Save the plot to a file
            plot_img_path = f'{ticker}_plot.png'
            plot_img = save_plot(plot_img_path)
            
            # 100 Days moving average
            ma100 = df.Close.rolling(100).mean()
            plt.switch_backend('AGG')
            plt.figure(figsize=(12, 5))
            plt.plot(df.Close, label='Closing Price')
            plt.plot(ma100, 'r', label='100 DMA')
            plt.title(f'100 Days Moving Average of {ticker}')
            plt.xlabel('Days')
            plt.ylabel('Price')
            plt.legend()
            plot_img_path = f'{ticker}_100_dma.png'
            plot_100_dma = save_plot(plot_img_path)

            # 200 Days moving average
            ma200 = df.Close.rolling(200).mean()
            plt.switch_backend('AGG')
            plt.figure(figsize=(12, 5))
            plt.plot(df.Close, label='Closing Price')
            plt.plot(ma100, 'r', label='100 DMA')
            plt.plot(ma200, 'g', label='200 DMA')
            plt.title(f'200 Days Moving Average of {ticker}')
            plt.xlabel('Days')
            plt.ylabel('Price')
            plt.legend()
            plot_img_path = f'{ticker}_200_dma.png'
            plot_200_dma = save_plot(plot_img_path)

            # Splitting data into Training & Testing datasets
            data_training = pd.DataFrame(df.Close[0:int(len(df)*0.7)])
            data_testing = pd.DataFrame(df.Close[int(len(df)*0.7): int(len(df))])

            # Scaling down the data between 0 and 1
            scaler = SimpleMinMaxScaler(feature_range=(0, 1))

            # Preparing Test Data
            past_100_days = data_training.tail(100)
            final_df = pd.concat([past_100_days, data_testing], ignore_index=True)
            input_data = scaler.fit_transform(final_df)

            x_test = []
            y_test = []
            for i in range(100, input_data.shape[0]):
                x_test.append(input_data[i-100: i])
                y_test.append(input_data[i, 0])
            x_test, y_test = np.array(x_test), np.array(y_test)

            # Making Predictions using pure numpy LSTM
            y_predicted = _predict(x_test)

            # Revert the scaled prices to original price
            y_predicted = scaler.inverse_transform(y_predicted.reshape(-1, 1)).flatten()
            y_test = scaler.inverse_transform(y_test.reshape(-1, 1)).flatten()

            # Plot the final prediction
            plt.switch_backend('AGG')
            plt.figure(figsize=(12, 5))
            plt.plot(y_test, 'b', label='Original Price')
            plt.plot(y_predicted, 'r', label='Predicted Price')
            plt.title(f'Final Prediction for {ticker}')
            plt.xlabel('Days')
            plt.ylabel('Price')
            plt.legend()
            plot_img_path = f'{ticker}_final_prediction.png'
            plot_prediction = save_plot(plot_img_path)

            # Model Evaluation
            mse = _mean_squared_error(y_test, y_predicted)
            rmse = float(np.sqrt(mse))
            r2 = _r2_score(y_test, y_predicted)


            return Response({
                'status': 'success',
                'plot_img': plot_img,
                'plot_100_dma': plot_100_dma,
                'plot_200_dma': plot_200_dma,
                'plot_prediction': plot_prediction,
                'mse': mse,
                'rmse': rmse,
                'r2': r2
                })