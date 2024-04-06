import vitaldb
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt
import pandas as pd
import numpy as np

class VitalParser:
    """
    Класс для предобработки и визуализации сигналов из набора данных VitalDB.

    Attributes:
        track_names (list): Список названий сигналов для отслеживания.
        signal_number (int): Номер сигнала для обработки.
        samples (numpy.ndarray): Образцы сигналов из набора данных VitalDB.
        processed_data (pandas.DataFrame): Обработанные данные сигналов.

    Methods:
        preprocessing(): Выполняет предварительную обработку сигналов.
        filter_signal(raw, fs): Применяет фильтрацию к сигналу.
        normalization_signal(df_signals): Нормализует сигналы в диапазоне [0, 1] или [-1, 1].
        display_parameters(interval): Визуализирует обработанные сигналы в заданном интервале времени.
    """

    track_names = ['SNUADC/ECG_V5', 'BIS/EEG1_WAV', 'SNUADC/ART']

    def __init__(self, signal_number):
        self.signal_number = signal_number
        vf = vitaldb.VitalFile(1869, self.track_names)
        self.samples = vf.to_numpy(self.track_names, 1/100)
        self.processed_data = []


    def preprocessing(self):
        processed_signals = [[]]*len(self.samples.T)
        for i, signal in enumerate(self.samples.T):
            # processed_signals[i] = self.removing_artifacts(signal)
            print(signal)
            signal = signal[np.logical_not(np.isnan(signal))]
            print(signal)
            processed_signals[i] = self.filter_signal(signal, 100)
            # processed_signals[i] = self.normalization_signal(processed_signals[i])

        lens = [len(x) for x in processed_signals]
        maxlen = max(lens)

        for i in range(len(processed_signals)):
            processed_signals[i] = list(processed_signals[i]) + [np.nan]*(maxlen-len(processed_signals[i]))

        processed_signals = pd.DataFrame(np.array(processed_signals).T)

        processed_signals = self.normalization_signal(processed_signals)
        self.processed_data = processed_signals
        return processed_signals
    
    def filter_signal(self, raw, fs):
        nyq = 0.5 * fs
        normal_cutoff = 20/nyq
        b, a = butter(4, normal_cutoff, btype='high', analog=False)
        y = filtfilt(b, a, raw)

        normal_cutoff1 = 10/nyq
        b, a = butter(4, normal_cutoff1, btype='low', analog=False)
        y1 = filtfilt(b, a, y)
        return y1
    
    def removing_artifacts(self, raw):
        return
    
    def normalization_signal(self, df_signals):
        df_normalized = (df_signals - df_signals.min()) / (df_signals.max() - df_signals.min())
        return df_normalized
    
    def display_parameters(self, interval):
        fig, axs = plt.subplots(len(self.samples.T), 1, figsize=(10, 7))
        print(self.processed_data.columns)
        for i in range(len(self.samples.T)):
            axs[i].plot(self.processed_data[i][interval[0]:interval[1]])
        plt.tight_layout()
        plt.show()
        return
    