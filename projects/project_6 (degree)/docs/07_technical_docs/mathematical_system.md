# Проект системы (математическое обеспечение) Stets Home

## 1. Общие сведения

### 1.1 Наименование системы
**Полное наименование:** Математическое обеспечение системы управления умным домом Stets Home  
**Краткое наименование:** Stets Home Mathematical System  
**Код проекта:** STETS-HOME-MATH-001

### 1.2 Назначение математического обеспечения
Математическое обеспечение определяет алгоритмы, модели и методы обработки данных для системы управления умным домом, включая:
- Алгоритмы управления устройствами
- Математические модели энергопотребления
- Методы прогнозирования и оптимизации
- Алгоритмы обнаружения аномалий
- Методы машинного обучения для персонализации

### 1.3 Принципы математического обеспечения
- **Точность:** Высокая точность вычислений и прогнозов
- **Эффективность:** Оптимальные алгоритмы с минимальной сложностью
- **Адаптивность:** Способность к обучению и адаптации
- **Надежность:** Стабильная работа в различных условиях
- **Масштабируемость:** Возможность обработки больших объемов данных

## 2. Математические модели

### 2.1 Модель энергопотребления

#### 2.1.1 Базовая модель энергопотребления
Энергопотребление устройства в момент времени t описывается функцией:

```
P(t) = P_base + P_usage(t) + P_overhead(t)
```

Где:
- `P_base` - базовое энергопотребление в режиме ожидания
- `P_usage(t)` - энергопотребление при активном использовании
- `P_overhead(t)` - дополнительные потери энергии

#### 2.1.2 Модель для умных лампочек
```python
class SmartBulbEnergyModel:
    def __init__(self, base_power=0.5, max_power=10.0):
        self.base_power = base_power  # Вт в режиме ожидания
        self.max_power = max_power    # Максимальная мощность
        
    def calculate_power_consumption(self, brightness, color_temp, status):
        """
        Расчет энергопотребления умной лампочки
        
        Args:
            brightness: Яркость (0-100%)
            color_temp: Цветовая температура (2700K-6500K)
            status: Статус устройства (on/off)
        
        Returns:
            float: Потребляемая мощность в ваттах
        """
        if status == 'off':
            return self.base_power
        
        # Базовое потребление при включении
        power = self.base_power
        
        # Потребление от яркости (квадратичная зависимость)
        brightness_factor = (brightness / 100) ** 2
        power += brightness_factor * (self.max_power - self.base_power)
        
        # Потребление от цветовой температуры
        # Холодный свет требует больше энергии
        temp_factor = (color_temp - 2700) / (6500 - 2700)
        power += temp_factor * 0.5  # Дополнительно до 0.5 Вт
        
        return min(power, self.max_power)
    
    def calculate_daily_consumption(self, usage_pattern):
        """
        Расчет дневного энергопотребления
        
        Args:
            usage_pattern: Словарь с данными об использовании по часам
        
        Returns:
            float: Общее потребление за день в кВт⋅ч
        """
        total_consumption = 0
        
        for hour, data in usage_pattern.items():
            power = self.calculate_power_consumption(
                data['brightness'],
                data['color_temp'],
                data['status']
            )
            total_consumption += power / 1000  # Переводим в кВт⋅ч
        
        return total_consumption
```

#### 2.1.3 Модель для умных розеток
```python
class SmartSocketEnergyModel:
    def __init__(self, standby_power=0.1):
        self.standby_power = standby_power  # Потребление в режиме ожидания
        
    def calculate_power_consumption(self, connected_device_power, status, energy_saving_mode):
        """
        Расчет энергопотребления умной розетки
        
        Args:
            connected_device_power: Мощность подключенного устройства
            status: Статус розетки (on/off)
            energy_saving_mode: Режим энергосбережения
        
        Returns:
            float: Потребляемая мощность в ваттах
        """
        if status == 'off':
            return self.standby_power
        
        if energy_saving_mode:
            # В режиме энергосбережения розетка отключается при низкой нагрузке
            if connected_device_power < 1.0:  # Менее 1 Вт
                return self.standby_power
        
        # Основное потребление + потери
        efficiency = 0.95  # КПД розетки
        return (connected_device_power / efficiency) + self.standby_power
```

### 2.2 Модель прогнозирования энергопотребления

#### 2.2.1 Временные ряды для прогнозирования
```python
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from scipy import stats

class EnergyForecastingModel:
    def __init__(self, window_size=24, forecast_horizon=24):
        self.window_size = window_size  # Размер окна для анализа
        self.forecast_horizon = forecast_horizon  # Горизонт прогноза
        self.model = None
        self.feature_scaler = None
        
    def prepare_features(self, historical_data):
        """
        Подготовка признаков для модели
        
        Args:
            historical_data: Исторические данные энергопотребления
        
        Returns:
            np.array: Матрица признаков
        """
        features = []
        
        for i in range(len(historical_data) - self.window_size):
            window = historical_data[i:i + self.window_size]
            
            # Базовые статистики
            mean_consumption = np.mean(window)
            std_consumption = np.std(window)
            max_consumption = np.max(window)
            min_consumption = np.min(window)
            
            # Тренд
            trend = np.polyfit(range(len(window)), window, 1)[0]
            
            # Сезонность (для часовых данных)
            hour_of_day = i % 24
            day_of_week = (i // 24) % 7
            
            # Лаговые признаки
            lag_1 = window[-1] if len(window) > 0 else 0
            lag_24 = window[-24] if len(window) >= 24 else 0
            
            feature_vector = [
                mean_consumption, std_consumption, max_consumption, min_consumption,
                trend, hour_of_day, day_of_week, lag_1, lag_24
            ]
            
            features.append(feature_vector)
        
        return np.array(features)
    
    def train_model(self, historical_data):
        """
        Обучение модели прогнозирования
        
        Args:
            historical_data: Исторические данные энергопотребления
        """
        X = self.prepare_features(historical_data)
        y = historical_data[self.window_size:]
        
        # Нормализация признаков
        from sklearn.preprocessing import StandardScaler
        self.feature_scaler = StandardScaler()
        X_scaled = self.feature_scaler.fit_transform(X)
        
        # Обучение модели
        self.model = LinearRegression()
        self.model.fit(X_scaled, y)
        
        return self.model.score(X_scaled, y)  # R² score
    
    def predict(self, recent_data):
        """
        Прогнозирование энергопотребления
        
        Args:
            recent_data: Последние данные для прогноза
        
        Returns:
            np.array: Прогноз энергопотребления
        """
        if len(recent_data) < self.window_size:
            raise ValueError(f"Недостаточно данных. Требуется минимум {self.window_size} точек")
        
        predictions = []
        current_data = recent_data.copy()
        
        for _ in range(self.forecast_horizon):
            # Подготовка признаков для текущего окна
            window = current_data[-self.window_size:]
            features = self.prepare_features(window.reshape(1, -1))
            
            # Нормализация
            features_scaled = self.feature_scaler.transform(features)
            
            # Прогноз
            prediction = self.model.predict(features_scaled)[0]
            predictions.append(prediction)
            
            # Обновление данных для следующего прогноза
            current_data = np.append(current_data, prediction)
        
        return np.array(predictions)
```

#### 2.2.2 Сезонная декомпозиция
```python
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.holtwinters import ExponentialSmoothing

class SeasonalEnergyModel:
    def __init__(self):
        self.decomposition = None
        self.seasonal_model = None
        
    def decompose_time_series(self, data, period=24):
        """
        Декомпозиция временного ряда на компоненты
        
        Args:
            data: Временной ряд энергопотребления
            period: Период сезонности (24 часа для дневных циклов)
        
        Returns:
            dict: Компоненты декомпозиции
        """
        self.decomposition = seasonal_decompose(
            data, 
            model='additive', 
            period=period
        )
        
        return {
            'trend': self.decomposition.trend,
            'seasonal': self.decomposition.seasonal,
            'residual': self.decomposition.resid,
            'observed': self.decomposition.observed
        }
    
    def fit_seasonal_model(self, data):
        """
        Обучение сезонной модели Хольта-Винтерса
        
        Args:
            data: Временной ряд энергопотребления
        """
        self.seasonal_model = ExponentialSmoothing(
            data,
            trend='add',
            seasonal='add',
            seasonal_periods=24
        ).fit()
        
        return self.seasonal_model
    
    def forecast_seasonal(self, steps=24):
        """
        Прогнозирование с учетом сезонности
        
        Args:
            steps: Количество шагов прогноза
        
        Returns:
            np.array: Прогноз с доверительными интервалами
        """
        if self.seasonal_model is None:
            raise ValueError("Модель не обучена")
        
        forecast = self.seasonal_model.forecast(steps)
        confidence_intervals = self.seasonal_model.forecast_intervals(steps)
        
        return {
            'forecast': forecast,
            'lower_bound': confidence_intervals['lower'],
            'upper_bound': confidence_intervals['upper']
        }
```

### 2.3 Модель оптимизации сценариев

#### 2.3.1 Задача оптимизации энергопотребления
```python
from scipy.optimize import minimize
import cvxpy as cp

class ScenarioOptimizationModel:
    def __init__(self, devices, time_horizon=24):
        self.devices = devices
        self.time_horizon = time_horizon
        self.device_power_models = {}
        
        # Инициализация моделей энергопотребления для каждого устройства
        for device in devices:
            if device.type == 'light_bulb':
                self.device_power_models[device.id] = SmartBulbEnergyModel()
            elif device.type == 'smart_socket':
                self.device_power_models[device.id] = SmartSocketEnergyModel()
    
    def optimize_energy_consumption(self, user_preferences, constraints):
        """
        Оптимизация энергопотребления с учетом предпочтений пользователя
        
        Args:
            user_preferences: Предпочтения пользователя
            constraints: Ограничения системы
        
        Returns:
            dict: Оптимальные настройки устройств
        """
        # Определение переменных оптимизации
        device_variables = {}
        
        for device in self.devices:
            device_vars = {}
            for t in range(self.time_horizon):
                if device.type == 'light_bulb':
                    device_vars[f'brightness_{t}'] = cp.Variable(
                        bounds=(0, 100), 
                        name=f'brightness_{device.id}_{t}'
                    )
                    device_vars[f'status_{t}'] = cp.Variable(
                        boolean=True, 
                        name=f'status_{device.id}_{t}'
                    )
                elif device.type == 'smart_socket':
                    device_vars[f'status_{t}'] = cp.Variable(
                        boolean=True, 
                        name=f'status_{device.id}_{t}'
                    )
                    device_vars[f'energy_saving_{t}'] = cp.Variable(
                        boolean=True, 
                        name=f'energy_saving_{device.id}_{t}'
                    )
            
            device_variables[device.id] = device_vars
        
        # Целевая функция: минимизация общего энергопотребления
        total_consumption = 0
        
        for device in self.devices:
            for t in range(self.time_horizon):
                if device.type == 'light_bulb':
                    brightness = device_variables[device.id][f'brightness_{t}']
                    status = device_variables[device.id][f'status_{t}']
                    
                    # Аппроксимация энергопотребления как квадратичной функции
                    power = self.device_power_models[device.id].base_power + \
                           cp.square(brightness / 100) * \
                           (self.device_power_models[device.id].max_power - 
                            self.device_power_models[device.id].base_power)
                    
                    total_consumption += power * status
                
                elif device.type == 'smart_socket':
                    status = device_variables[device.id][f'status_{t}']
                    energy_saving = device_variables[device.id][f'energy_saving_{t}']
                    
                    # Упрощенная модель энергопотребления розетки
                    power = self.device_power_models[device.id].standby_power + \
                           10 * status * (1 - 0.1 * energy_saving)  # 10 Вт при включении
                    
                    total_consumption += power
        
        # Ограничения
        constraints_list = []
        
        # Ограничения комфорта пользователя
        for device in self.devices:
            if device.type == 'light_bulb':
                for t in range(self.time_horizon):
                    # Минимальная яркость в активные часы
                    if t in user_preferences.get('active_hours', []):
                        constraints_list.append(
                            device_variables[device.id][f'brightness_{t}'] >= 30
                        )
                    
                    # Максимальная яркость ночью
                    if t in user_preferences.get('sleep_hours', []):
                        constraints_list.append(
                            device_variables[device.id][f'brightness_{t}'] <= 10
                        )
        
        # Ограничения энергопотребления
        max_daily_consumption = constraints.get('max_daily_consumption', 50)  # кВт⋅ч
        constraints_list.append(total_consumption <= max_daily_consumption * 1000)  # Вт
        
        # Решение задачи оптимизации
        problem = cp.Problem(cp.Minimize(total_consumption), constraints_list)
        problem.solve(verbose=True)
        
        if problem.status == cp.OPTIMAL:
            # Извлечение оптимальных значений
            optimal_settings = {}
            for device in self.devices:
                optimal_settings[device.id] = {}
                for t in range(self.time_horizon):
                    if device.type == 'light_bulb':
                        optimal_settings[device.id][t] = {
                            'brightness': device_variables[device.id][f'brightness_{t}'].value,
                            'status': bool(device_variables[device.id][f'status_{t}'].value)
                        }
                    elif device.type == 'smart_socket':
                        optimal_settings[device.id][t] = {
                            'status': bool(device_variables[device.id][f'status_{t}'].value),
                            'energy_saving': bool(device_variables[device.id][f'energy_saving_{t}'].value)
                        }
            
            return {
                'optimal_settings': optimal_settings,
                'total_consumption': total_consumption.value,
                'savings': self.calculate_savings(optimal_settings)
            }
        else:
            raise ValueError(f"Оптимизация не удалась: {problem.status}")
    
    def calculate_savings(self, optimal_settings):
        """
        Расчет экономии от оптимизации
        
        Args:
            optimal_settings: Оптимальные настройки устройств
        
        Returns:
            dict: Информация об экономии
        """
        # Расчет базового потребления (без оптимизации)
        baseline_consumption = 0
        for device in self.devices:
            if device.type == 'light_bulb':
                baseline_consumption += self.device_power_models[device.id].max_power * 12  # 12 часов в день
            elif device.type == 'smart_socket':
                baseline_consumption += 10 * 16  # 10 Вт, 16 часов в день
        
        # Расчет оптимизированного потребления
        optimized_consumption = 0
        for device_id, settings in optimal_settings.items():
            for t, setting in settings.items():
                if device_id in self.device_power_models:
                    if 'brightness' in setting:
                        power = self.device_power_models[device_id].calculate_power_consumption(
                            setting['brightness'], 3000, 'on' if setting['status'] else 'off'
                        )
                    else:
                        power = self.device_power_models[device_id].standby_power + \
                               10 * setting['status'] * (1 - 0.1 * setting['energy_saving'])
                    optimized_consumption += power
        
        savings_percentage = (baseline_consumption - optimized_consumption) / baseline_consumption * 100
        
        return {
            'baseline_consumption': baseline_consumption,
            'optimized_consumption': optimized_consumption,
            'savings_kwh': (baseline_consumption - optimized_consumption) / 1000,
            'savings_percentage': savings_percentage
        }
```

## 3. Алгоритмы машинного обучения

### 3.1 Обнаружение аномалий

#### 3.1.1 Изолирующий лес (Isolation Forest)
```python
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import numpy as np

class AnomalyDetectionModel:
    def __init__(self, contamination=0.1):
        self.model = IsolationForest(
            contamination=contamination,
            random_state=42,
            n_estimators=100
        )
        self.scaler = StandardScaler()
        self.is_trained = False
        
    def prepare_features(self, device_data):
        """
        Подготовка признаков для обнаружения аномалий
        
        Args:
            device_data: Данные устройства
        
        Returns:
            np.array: Матрица признаков
        """
        features = []
        
        for data_point in device_data:
            feature_vector = [
                data_point['energy_consumption'],
                data_point['temperature'],
                data_point['brightness'] if 'brightness' in data_point else 0,
                data_point['uptime'],
                data_point['response_time'],
                data_point['error_count']
            ]
            features.append(feature_vector)
        
        return np.array(features)
    
    def train(self, normal_data):
        """
        Обучение модели на нормальных данных
        
        Args:
            normal_data: Данные нормальной работы устройств
        """
        features = self.prepare_features(normal_data)
        features_scaled = self.scaler.fit_transform(features)
        
        self.model.fit(features_scaled)
        self.is_trained = True
        
        return self.model.score_samples(features_scaled)
    
    def detect_anomalies(self, test_data):
        """
        Обнаружение аномалий в новых данных
        
        Args:
            test_data: Данные для проверки
        
        Returns:
            dict: Результаты обнаружения аномалий
        """
        if not self.is_trained:
            raise ValueError("Модель не обучена")
        
        features = self.prepare_features(test_data)
        features_scaled = self.scaler.transform(features)
        
        # Предсказание аномалий
        anomaly_scores = self.model.score_samples(features_scaled)
        anomaly_predictions = self.model.predict(features_scaled)
        
        # Определение аномалий (score < threshold)
        threshold = np.percentile(anomaly_scores, 10)  # Нижние 10% считаются аномальными
        anomalies = anomaly_scores < threshold
        
        return {
            'anomaly_scores': anomaly_scores,
            'anomaly_predictions': anomaly_predictions,
            'anomalies': anomalies,
            'threshold': threshold,
            'anomaly_count': np.sum(anomalies)
        }
    
    def explain_anomaly(self, anomaly_data):
        """
        Объяснение причин аномалии
        
        Args:
            anomaly_data: Данные аномального события
        
        Returns:
            dict: Объяснение аномалии
        """
        features = self.prepare_features([anomaly_data])[0]
        feature_names = [
            'energy_consumption', 'temperature', 'brightness', 
            'uptime', 'response_time', 'error_count'
        ]
        
        # Анализ отклонений от нормальных значений
        explanations = []
        
        for i, (feature, name) in enumerate(zip(features, feature_names)):
            # Получаем нормальные значения из обучающих данных
            normal_values = self.scaler.inverse_transform(
                self.scaler.transform(self.prepare_features([anomaly_data]))
            )[0]
            
            # Вычисляем z-score
            z_score = (feature - np.mean(normal_values)) / np.std(normal_values)
            
            if abs(z_score) > 2:  # Значительное отклонение
                explanations.append({
                    'feature': name,
                    'value': feature,
                    'z_score': z_score,
                    'severity': 'high' if abs(z_score) > 3 else 'medium'
                })
        
        return {
            'explanations': explanations,
            'overall_severity': max([abs(exp['z_score']) for exp in explanations]) if explanations else 0
        }
```

#### 3.1.2 LSTM для обнаружения аномалий во временных рядах
```python
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam

class LSTMAutoencoder:
    def __init__(self, sequence_length=24, features=6):
        self.sequence_length = sequence_length
        self.features = features
        self.model = None
        self.scaler = StandardScaler()
        
    def build_model(self):
        """
        Построение модели LSTM автокодировщика
        """
        model = Sequential([
            # Энкодер
            LSTM(64, return_sequences=True, input_shape=(self.sequence_length, self.features)),
            Dropout(0.2),
            LSTM(32, return_sequences=False),
            Dropout(0.2),
            
            # Боттleneck
            Dense(16, activation='relu'),
            
            # Декодер
            Dense(32, activation='relu'),
            LSTM(32, return_sequences=True),
            Dropout(0.2),
            LSTM(64, return_sequences=True),
            Dropout(0.2),
            Dense(self.features, activation='linear')
        ])
        
        model.compile(
            optimizer=Adam(learning_rate=0.001),
            loss='mse',
            metrics=['mae']
        )
        
        self.model = model
        return model
    
    def prepare_sequences(self, data):
        """
        Подготовка последовательностей для обучения
        
        Args:
            data: Временной ряд данных
        
        Returns:
            np.array: Матрица последовательностей
        """
        sequences = []
        
        for i in range(len(data) - self.sequence_length + 1):
            sequence = data[i:i + self.sequence_length]
            sequences.append(sequence)
        
        return np.array(sequences)
    
    def train(self, normal_data, epochs=100, batch_size=32):
        """
        Обучение модели на нормальных данных
        
        Args:
            normal_data: Нормальные данные для обучения
            epochs: Количество эпох
            batch_size: Размер батча
        """
        # Нормализация данных
        data_scaled = self.scaler.fit_transform(normal_data)
        
        # Подготовка последовательностей
        sequences = self.prepare_sequences(data_scaled)
        
        # Обучение модели
        if self.model is None:
            self.build_model()
        
        history = self.model.fit(
            sequences, sequences,  # Автокодировщик: вход = выход
            epochs=epochs,
            batch_size=batch_size,
            validation_split=0.2,
            verbose=1
        )
        
        return history
    
    def detect_anomalies(self, test_data, threshold_percentile=95):
        """
        Обнаружение аномалий с помощью автокодировщика
        
        Args:
            test_data: Данные для тестирования
            threshold_percentile: Процентиль для определения порога
        
        Returns:
            dict: Результаты обнаружения аномалий
        """
        if self.model is None:
            raise ValueError("Модель не обучена")
        
        # Нормализация тестовых данных
        test_scaled = self.scaler.transform(test_data)
        
        # Подготовка последовательностей
        sequences = self.prepare_sequences(test_scaled)
        
        # Предсказание
        reconstructed = self.model.predict(sequences)
        
        # Вычисление ошибки реконструкции
        mse = np.mean(np.square(sequences - reconstructed), axis=(1, 2))
        
        # Определение порога
        threshold = np.percentile(mse, threshold_percentile)
        
        # Обнаружение аномалий
        anomalies = mse > threshold
        
        return {
            'mse_scores': mse,
            'threshold': threshold,
            'anomalies': anomalies,
            'anomaly_count': np.sum(anomalies),
            'reconstructed_data': reconstructed
        }
```

### 3.2 Персонализация пользовательского опыта

#### 3.2.1 Система рекомендаций на основе коллаборативной фильтрации
```python
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import NMF
import pandas as pd

class UserRecommendationSystem:
    def __init__(self, n_factors=50):
        self.n_factors = n_factors
        self.user_item_matrix = None
        self.user_similarity_matrix = None
        self.item_similarity_matrix = None
        self.nmf_model = None
        
    def build_user_item_matrix(self, user_interactions):
        """
        Построение матрицы пользователь-элемент
        
        Args:
            user_interactions: Данные взаимодействий пользователей
        """
        # Создание матрицы взаимодействий
        df = pd.DataFrame(user_interactions)
        
        # Создание pivot table
        self.user_item_matrix = df.pivot_table(
            index='user_id',
            columns='item_id',
            values='rating',
            fill_value=0
        )
        
        return self.user_item_matrix
    
    def calculate_user_similarity(self):
        """
        Расчет схожести пользователей
        """
        if self.user_item_matrix is None:
            raise ValueError("Матрица пользователь-элемент не построена")
        
        self.user_similarity_matrix = cosine_similarity(self.user_item_matrix)
        return self.user_similarity_matrix
    
    def calculate_item_similarity(self):
        """
        Расчет схожести элементов
        """
        if self.user_item_matrix is None:
            raise ValueError("Матрица пользователь-элемент не построена")
        
        self.item_similarity_matrix = cosine_similarity(self.user_item_matrix.T)
        return self.item_similarity_matrix
    
    def train_nmf_model(self):
        """
        Обучение модели NMF для рекомендаций
        """
        if self.user_item_matrix is None:
            raise ValueError("Матрица пользователь-элемент не построена")
        
        self.nmf_model = NMF(n_components=self.n_factors, random_state=42)
        self.nmf_model.fit(self.user_item_matrix)
        
        return self.nmf_model
    
    def get_user_recommendations(self, user_id, n_recommendations=10):
        """
        Получение рекомендаций для пользователя
        
        Args:
            user_id: ID пользователя
            n_recommendations: Количество рекомендаций
        
        Returns:
            list: Список рекомендованных элементов
        """
        if self.nmf_model is None:
            raise ValueError("NMF модель не обучена")
        
        # Получение профиля пользователя
        user_profile = self.user_item_matrix.loc[user_id].values
        
        # Предсказание оценок
        user_factors = self.nmf_model.transform(user_profile.reshape(1, -1))
        predicted_ratings = self.nmf_model.inverse_transform(user_factors)[0]
        
        # Получение элементов, которые пользователь еще не оценивал
        unrated_items = self.user_item_matrix.columns[
            self.user_item_matrix.loc[user_id] == 0
        ]
        
        # Сортировка по предсказанным оценкам
        recommendations = []
        for item_id in unrated_items:
            item_index = self.user_item_matrix.columns.get_loc(item_id)
            predicted_rating = predicted_ratings[item_index]
            recommendations.append((item_id, predicted_rating))
        
        # Сортировка по убыванию оценок
        recommendations.sort(key=lambda x: x[1], reverse=True)
        
        return recommendations[:n_recommendations]
    
    def get_similar_users(self, user_id, n_similar=5):
        """
        Получение похожих пользователей
        
        Args:
            user_id: ID пользователя
            n_similar: Количество похожих пользователей
        
        Returns:
            list: Список похожих пользователей
        """
        if self.user_similarity_matrix is None:
            self.calculate_user_similarity()
        
        user_index = self.user_item_matrix.index.get_loc(user_id)
        similarities = self.user_similarity_matrix[user_index]
        
        # Получение индексов похожих пользователей
        similar_indices = np.argsort(similarities)[::-1][1:n_similar+1]  # Исключаем самого пользователя
        
        similar_users = []
        for idx in similar_indices:
            similar_user_id = self.user_item_matrix.index[idx]
            similarity_score = similarities[idx]
            similar_users.append((similar_user_id, similarity_score))
        
        return similar_users
```

#### 3.2.2 Модель предсказания предпочтений пользователя
```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

class UserPreferenceModel:
    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=100,
            random_state=42,
            max_depth=10
        )
        self.label_encoders = {}
        self.feature_names = []
        
    def prepare_features(self, user_data, device_data, context_data):
        """
        Подготовка признаков для модели предпочтений
        
        Args:
            user_data: Данные пользователя
            device_data: Данные устройства
            context_data: Контекстные данные
        
        Returns:
            np.array: Матрица признаков
        """
        features = []
        
        # Признаки пользователя
        user_features = [
            user_data['age'],
            user_data['occupation_encoded'],
            user_data['home_type_encoded'],
            user_data['family_size'],
            user_data['has_children']
        ]
        
        # Признаки устройства
        device_features = [
            device_data['device_type_encoded'],
            device_data['room_type_encoded'],
            device_data['power_rating'],
            device_data['age_months']
        ]
        
        # Контекстные признаки
        context_features = [
            context_data['hour_of_day'],
            context_data['day_of_week'],
            context_data['season_encoded'],
            context_data['temperature'],
            context_data['weather_encoded']
        ]
        
        # Временные признаки
        time_features = [
            np.sin(2 * np.pi * context_data['hour_of_day'] / 24),  # Циклическое кодирование времени
            np.cos(2 * np.pi * context_data['hour_of_day'] / 24),
            np.sin(2 * np.pi * context_data['day_of_week'] / 7),
            np.cos(2 * np.pi * context_data['day_of_week'] / 7)
        ]
        
        feature_vector = user_features + device_features + context_features + time_features
        features.append(feature_vector)
        
        return np.array(features)
    
    def encode_categorical_features(self, data):
        """
        Кодирование категориальных признаков
        
        Args:
            data: Данные с категориальными признаками
        
        Returns:
            dict: Закодированные данные
        """
        encoded_data = data.copy()
        
        categorical_columns = ['occupation', 'home_type', 'device_type', 'room_type', 'season', 'weather']
        
        for column in categorical_columns:
            if column in data.columns:
                if column not in self.label_encoders:
                    self.label_encoders[column] = LabelEncoder()
                    encoded_data[f'{column}_encoded'] = self.label_encoders[column].fit_transform(data[column])
                else:
                    encoded_data[f'{column}_encoded'] = self.label_encoders[column].transform(data[column])
        
        return encoded_data
    
    def train(self, training_data):
        """
        Обучение модели предпочтений
        
        Args:
            training_data: Данные для обучения
        """
        # Подготовка данных
        encoded_data = self.encode_categorical_features(training_data)
        
        # Подготовка признаков и целевой переменной
        X = []
        y = []
        
        for _, row in encoded_data.iterrows():
            features = self.prepare_features(row, row, row)
            X.append(features[0])
            y.append(row['preference'])  # Целевая переменная
        
        X = np.array(X)
        y = np.array(y)
        
        # Обучение модели
        self.model.fit(X, y)
        
        # Сохранение названий признаков
        self.feature_names = [
            'age', 'occupation', 'home_type', 'family_size', 'has_children',
            'device_type', 'room_type', 'power_rating', 'age_months',
            'hour_of_day', 'day_of_week', 'season', 'temperature', 'weather',
            'hour_sin', 'hour_cos', 'day_sin', 'day_cos'
        ]
        
        return self.model.score(X, y)
    
    def predict_preference(self, user_data, device_data, context_data):
        """
        Предсказание предпочтения пользователя
        
        Args:
            user_data: Данные пользователя
            device_data: Данные устройства
            context_data: Контекстные данные
        
        Returns:
            dict: Предсказание предпочтения
        """
        # Подготовка данных
        combined_data = {**user_data, **device_data, **context_data}
        encoded_data = self.encode_categorical_features(pd.DataFrame([combined_data]))
        
        # Подготовка признаков
        features = self.prepare_features(encoded_data.iloc[0], encoded_data.iloc[0], encoded_data.iloc[0])
        
        # Предсказание
        prediction = self.model.predict(features)[0]
        prediction_proba = self.model.predict_proba(features)[0]
        
        return {
            'preference': prediction,
            'confidence': max(prediction_proba),
            'probabilities': dict(zip(self.model.classes_, prediction_proba))
        }
    
    def get_feature_importance(self):
        """
        Получение важности признаков
        
        Returns:
            dict: Важность признаков
        """
        if self.model is None:
            raise ValueError("Модель не обучена")
        
        importance = self.model.feature_importances_
        
        return dict(zip(self.feature_names, importance))
```

## 4. Алгоритмы оптимизации

### 4.1 Генетический алгоритм для оптимизации сценариев

```python
import random
from typing import List, Tuple, Callable

class GeneticAlgorithmOptimizer:
    def __init__(self, 
                 population_size=100,
                 mutation_rate=0.1,
                 crossover_rate=0.8,
                 generations=100):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.generations = generations
        
    def create_individual(self, scenario_template):
        """
        Создание индивидуального решения (сценария)
        
        Args:
            scenario_template: Шаблон сценария
        
        Returns:
            dict: Индивидуальное решение
        """
        individual = {
            'actions': [],
            'schedule': {},
            'fitness': 0
        }
        
        # Генерация случайных действий
        num_actions = random.randint(1, len(scenario_template['available_devices']))
        selected_devices = random.sample(
            scenario_template['available_devices'], 
            num_actions
        )
        
        for device in selected_devices:
            action = {
                'device_id': device['id'],
                'action_type': random.choice(['turn_on', 'turn_off', 'set_brightness']),
                'parameters': self.generate_random_parameters(device)
            }
            individual['actions'].append(action)
        
        # Генерация случайного расписания
        individual['schedule'] = self.generate_random_schedule()
        
        return individual
    
    def generate_random_parameters(self, device):
        """
        Генерация случайных параметров для устройства
        
        Args:
            device: Данные устройства
        
        Returns:
            dict: Случайные параметры
        """
        parameters = {}
        
        if device['type'] == 'light_bulb':
            parameters['brightness'] = random.randint(10, 100)
            parameters['color_temp'] = random.randint(2700, 6500)
        elif device['type'] == 'smart_socket':
            parameters['power_limit'] = random.uniform(0.5, 1.0)
        
        return parameters
    
    def generate_random_schedule(self):
        """
        Генерация случайного расписания
        
        Returns:
            dict: Случайное расписание
        """
        schedule = {}
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        
        for day in days:
            schedule[day] = random.choice([True, False])
        
        schedule['start_time'] = random.randint(0, 23)
        schedule['end_time'] = random.randint(schedule['start_time'], 23)
        
        return schedule
    
    def calculate_fitness(self, individual, fitness_function):
        """
        Расчет приспособленности индивидуума
        
        Args:
            individual: Индивидуальное решение
            fitness_function: Функция оценки приспособленности
        
        Returns:
            float: Значение приспособленности
        """
        return fitness_function(individual)
    
    def selection(self, population):
        """
        Селекция родителей для следующего поколения
        
        Args:
            population: Популяция индивидуумов
        
        Returns:
            list: Выбранные родители
        """
        # Турнирная селекция
        parents = []
        
        for _ in range(self.population_size):
            # Выбор случайных кандидатов
            candidates = random.sample(population, 3)
            # Выбор лучшего кандидата
            best_candidate = max(candidates, key=lambda x: x['fitness'])
            parents.append(best_candidate)
        
        return parents
    
    def crossover(self, parent1, parent2):
        """
        Скрещивание двух родителей
        
        Args:
            parent1: Первый родитель
            parent2: Второй родитель
        
        Returns:
            tuple: Два потомка
        """
        if random.random() > self.crossover_rate:
            return parent1.copy(), parent2.copy()
        
        # Одноточечное скрещивание для действий
        actions1 = parent1['actions']
        actions2 = parent2['actions']
        
        if len(actions1) > 1 and len(actions2) > 1:
            crossover_point = random.randint(1, min(len(actions1), len(actions2)) - 1)
            
            child1_actions = actions1[:crossover_point] + actions2[crossover_point:]
            child2_actions = actions2[:crossover_point] + actions1[crossover_point:]
        else:
            child1_actions = actions1.copy()
            child2_actions = actions2.copy()
        
        # Скрещивание расписания
        child1_schedule = parent1['schedule'].copy()
        child2_schedule = parent2['schedule'].copy()
        
        # Обмен дней недели
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        for day in days:
            if random.random() < 0.5:
                child1_schedule[day] = parent2['schedule'][day]
                child2_schedule[day] = parent1['schedule'][day]
        
        # Создание потомков
        child1 = {
            'actions': child1_actions,
            'schedule': child1_schedule,
            'fitness': 0
        }
        
        child2 = {
            'actions': child2_actions,
            'schedule': child2_schedule,
            'fitness': 0
        }
        
        return child1, child2
    
    def mutation(self, individual, scenario_template):
        """
        Мутация индивидуума
        
        Args:
            individual: Индивидуальное решение
            scenario_template: Шаблон сценария
        """
        if random.random() > self.mutation_rate:
            return
        
        # Мутация действий
        if individual['actions'] and random.random() < 0.5:
            action = random.choice(individual['actions'])
            
            if action['action_type'] == 'set_brightness':
                action['parameters']['brightness'] = random.randint(10, 100)
            elif action['action_type'] == 'set_color_temp':
                action['parameters']['color_temp'] = random.randint(2700, 6500)
        
        # Мутация расписания
        if random.random() < 0.5:
            days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
            day = random.choice(days)
            individual['schedule'][day] = not individual['schedule'][day]
        
        # Мутация времени
        if random.random() < 0.3:
            individual['schedule']['start_time'] = random.randint(0, 23)
            individual['schedule']['end_time'] = random.randint(
                individual['schedule']['start_time'], 23
            )
    
    def optimize_scenario(self, scenario_template, fitness_function):
        """
        Оптимизация сценария с помощью генетического алгоритма
        
        Args:
            scenario_template: Шаблон сценария
            fitness_function: Функция оценки приспособленности
        
        Returns:
            dict: Оптимальное решение
        """
        # Создание начальной популяции
        population = []
        for _ in range(self.population_size):
            individual = self.create_individual(scenario_template)
            individual['fitness'] = self.calculate_fitness(individual, fitness_function)
            population.append(individual)
        
        # Эволюция
        for generation in range(self.generations):
            # Сортировка по приспособленности
            population.sort(key=lambda x: x['fitness'], reverse=True)
            
            # Выбор родителей
            parents = self.selection(population)
            
            # Создание нового поколения
            new_population = []
            
            # Элитизм - сохранение лучших индивидуумов
            elite_size = self.population_size // 10
            new_population.extend(population[:elite_size])
            
            # Скрещивание и мутация
            while len(new_population) < self.population_size:
                parent1, parent2 = random.sample(parents, 2)
                child1, child2 = self.crossover(parent1, parent2)
                
                self.mutation(child1, scenario_template)
                self.mutation(child2, scenario_template)
                
                child1['fitness'] = self.calculate_fitness(child1, fitness_function)
                child2['fitness'] = self.calculate_fitness(child2, fitness_function)
                
                new_population.extend([child1, child2])
            
            population = new_population[:self.population_size]
            
            # Логирование прогресса
            best_fitness = max(individual['fitness'] for individual in population)
            avg_fitness = sum(individual['fitness'] for individual in population) / len(population)
            
            if generation % 10 == 0:
                print(f"Generation {generation}: Best = {best_fitness:.4f}, Avg = {avg_fitness:.4f}")
        
        # Возврат лучшего решения
        population.sort(key=lambda x: x['fitness'], reverse=True)
        return population[0]
```

### 4.2 Симплекс-метод для линейного программирования

```python
import numpy as np
from scipy.optimize import linprog

class LinearProgrammingOptimizer:
    def __init__(self):
        self.solution = None
        self.objective_value = None
        
    def optimize_energy_distribution(self, devices, constraints, preferences):
        """
        Оптимизация распределения энергии между устройствами
        
        Args:
            devices: Список устройств
            constraints: Ограничения системы
            preferences: Предпочтения пользователя
        
        Returns:
            dict: Оптимальное решение
        """
        # Количество переменных (по одной для каждого устройства)
        n_devices = len(devices)
        
        # Коэффициенты целевой функции (минимизация общего потребления)
        c = np.array([device.power_rating for device in devices])
        
        # Матрица ограничений
        A_ub = []  # Неравенства
        b_ub = []  # Правая часть неравенств
        
        A_eq = []  # Равенства
        b_eq = []  # Правая часть равенств
        
        # Ограничение на максимальное потребление
        A_ub.append([1] * n_devices)
        b_ub.append(constraints['max_total_power'])
        
        # Ограничения на минимальное потребление для каждого устройства
        for i, device in enumerate(devices):
            constraint = [0] * n_devices
            constraint[i] = 1
            A_ub.append(constraint)
            b_ub.append(device.max_power)
            
            # Ограничение снизу
            constraint_lower = [0] * n_devices
            constraint_lower[i] = -1
            A_ub.append(constraint_lower)
            b_ub.append(-device.min_power)
        
        # Ограничения комфорта пользователя
        for preference in preferences:
            if preference['type'] == 'min_brightness':
                device_idx = next(i for i, d in enumerate(devices) if d.id == preference['device_id'])
                constraint = [0] * n_devices
                constraint[device_idx] = -1
                A_ub.append(constraint)
                b_ub.append(-preference['min_value'])
        
        # Решение задачи линейного программирования
        result = linprog(
            c=c,
            A_ub=A_ub,
            b_ub=b_ub,
            A_eq=A_eq,
            b_eq=b_eq,
            bounds=[(0, None)] * n_devices,
            method='highs'
        )
        
        if result.success:
            self.solution = result.x
            self.objective_value = result.fun
            
            # Формирование результата
            optimal_settings = {}
            for i, device in enumerate(devices):
                optimal_settings[device.id] = {
                    'power': self.solution[i],
                    'efficiency': self.solution[i] / device.power_rating,
                    'savings': device.power_rating - self.solution[i]
                }
            
            return {
                'success': True,
                'optimal_settings': optimal_settings,
                'total_power': self.objective_value,
                'total_savings': sum(device.power_rating for device in devices) - self.objective_value,
                'savings_percentage': (sum(device.power_rating for device in devices) - self.objective_value) / 
                                    sum(device.power_rating for device in devices) * 100
            }
        else:
            return {
                'success': False,
                'error': result.message,
                'optimal_settings': None
            }
    
    def optimize_scenario_timing(self, scenarios, time_slots, constraints):
        """
        Оптимизация времени выполнения сценариев
        
        Args:
            scenarios: Список сценариев
            time_slots: Доступные временные слоты
            constraints: Ограничения системы
        
        Returns:
            dict: Оптимальное расписание
        """
        n_scenarios = len(scenarios)
        n_slots = len(time_slots)
        
        # Переменные: x[i][j] = 1, если сценарий i выполняется в слоте j
        n_vars = n_scenarios * n_slots
        
        # Целевая функция: минимизация конфликтов и максимизация эффективности
        c = np.zeros(n_vars)
        
        for i, scenario in enumerate(scenarios):
            for j, slot in enumerate(time_slots):
                # Штраф за выполнение в неоптимальное время
                time_penalty = abs(slot.hour - scenario.preferred_hour) / 24
                c[i * n_slots + j] = time_penalty
        
        # Ограничения
        A_eq = []
        b_eq = []
        
        # Каждый сценарий должен быть выполнен ровно один раз
        for i in range(n_scenarios):
            constraint = [0] * n_vars
            for j in range(n_slots):
                constraint[i * n_slots + j] = 1
            A_eq.append(constraint)
            b_eq.append(1)
        
        # Ограничения на мощность в каждом слоте
        A_ub = []
        b_ub = []
        
        for j in range(n_slots):
            constraint = [0] * n_vars
            for i in range(n_scenarios):
                constraint[i * n_slots + j] = scenarios[i].power_consumption
            A_ub.append(constraint)
            b_ub.append(constraints['max_power_per_slot'])
        
        # Решение задачи
        result = linprog(
            c=c,
            A_eq=A_eq,
            b_eq=b_eq,
            A_ub=A_ub,
            b_ub=b_ub,
            bounds=[(0, 1)] * n_vars,
            method='highs'
        )
        
        if result.success:
            # Формирование расписания
            schedule = {}
            for i, scenario in enumerate(scenarios):
                for j, slot in enumerate(time_slots):
                    if result.x[i * n_slots + j] > 0.5:  # Пороговое значение
                        schedule[scenario.id] = {
                            'time_slot': slot,
                            'power_consumption': scenario.power_consumption
                        }
                        break
            
            return {
                'success': True,
                'schedule': schedule,
                'total_conflicts': result.fun,
                'utilization': sum(s['power_consumption'] for s in schedule.values()) / 
                             (constraints['max_power_per_slot'] * n_slots) * 100
            }
        else:
            return {
                'success': False,
                'error': result.message,
                'schedule': None
            }
```

## 5. Статистические методы

### 5.1 Анализ временных рядов

```python
from statsmodels.tsa.stattools import adfuller, kpss
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.stats.diagnostic import acorr_ljungbox
import pandas as pd

class TimeSeriesAnalyzer:
    def __init__(self):
        self.stationarity_tests = {}
        self.arima_model = None
        
    def test_stationarity(self, time_series):
        """
        Тестирование стационарности временного ряда
        
        Args:
            time_series: Временной ряд
        
        Returns:
            dict: Результаты тестов стационарности
        """
        # Тест Дики-Фуллера
        adf_result = adfuller(time_series)
        
        # Тест KPSS
        kpss_result = kpss(time_series, regression='c')
        
        # Тест Льюнга-Бокса на автокорреляцию
        ljung_box_result = acorr_ljungbox(time_series, lags=10, return_df=True)
        
        results = {
            'adf': {
                'statistic': adf_result[0],
                'p_value': adf_result[1],
                'critical_values': adf_result[4],
                'is_stationary': adf_result[1] < 0.05
            },
            'kpss': {
                'statistic': kpss_result[0],
                'p_value': kpss_result[1],
                'critical_values': kpss_result[3],
                'is_stationary': kpss_result[1] > 0.05
            },
            'ljung_box': {
                'statistics': ljung_box_result['lb_stat'].tolist(),
                'p_values': ljung_box_result['lb_pvalue'].tolist(),
                'has_autocorrelation': any(ljung_box_result['lb_pvalue'] < 0.05)
            }
        }
        
        self.stationarity_tests = results
        return results
    
    def make_stationary(self, time_series, method='diff'):
        """
        Преобразование временного ряда в стационарный
        
        Args:
            time_series: Временной ряд
            method: Метод преобразования ('diff', 'log', 'box_cox')
        
        Returns:
            np.array: Стационарный временной ряд
        """
        if method == 'diff':
            return np.diff(time_series)
        elif method == 'log':
            return np.log(time_series + 1)  # +1 для избежания log(0)
        elif method == 'box_cox':
            from scipy.stats import boxcox
            return boxcox(time_series + 1)[0]
        else:
            raise ValueError(f"Неизвестный метод: {method}")
    
    def fit_arima_model(self, time_series, order=(1, 1, 1)):
        """
        Обучение модели ARIMA
        
        Args:
            time_series: Временной ряд
            order: Порядок модели (p, d, q)
        
        Returns:
            ARIMA: Обученная модель
        """
        self.arima_model = ARIMA(time_series, order=order)
        fitted_model = self.arima_model.fit()
        
        return fitted_model
    
    def forecast_arima(self, steps=24):
        """
        Прогнозирование с помощью модели ARIMA
        
        Args:
            steps: Количество шагов прогноза
        
        Returns:
            dict: Результаты прогнозирования
        """
        if self.arima_model is None:
            raise ValueError("Модель ARIMA не обучена")
        
        fitted_model = self.arima_model.fit()
        forecast = fitted_model.forecast(steps=steps)
        confidence_intervals = fitted_model.get_forecast(steps=steps).conf_int()
        
        return {
            'forecast': forecast,
            'lower_bound': confidence_intervals.iloc[:, 0],
            'upper_bound': confidence_intervals.iloc[:, 1],
            'model_summary': fitted_model.summary()
        }
    
    def calculate_forecast_accuracy(self, actual, forecast):
        """
        Расчет точности прогноза
        
        Args:
            actual: Фактические значения
            forecast: Прогнозируемые значения
        
        Returns:
            dict: Метрики точности
        """
        actual = np.array(actual)
        forecast = np.array(forecast)
        
        # Средняя абсолютная ошибка
        mae = np.mean(np.abs(actual - forecast))
        
        # Средняя квадратичная ошибка
        mse = np.mean((actual - forecast) ** 2)
        rmse = np.sqrt(mse)
        
        # Средняя абсолютная процентная ошибка
        mape = np.mean(np.abs((actual - forecast) / actual)) * 100
        
        # Коэффициент детерминации
        ss_res = np.sum((actual - forecast) ** 2)
        ss_tot = np.sum((actual - np.mean(actual)) ** 2)
        r2 = 1 - (ss_res / ss_tot)
        
        return {
            'mae': mae,
            'mse': mse,
            'rmse': rmse,
            'mape': mape,
            'r2': r2
        }
```

### 5.2 Корреляционный анализ

```python
from scipy.stats import pearsonr, spearmanr, kendalltau
from scipy.stats import chi2_contingency
import pandas as pd

class CorrelationAnalyzer:
    def __init__(self):
        self.correlation_matrix = None
        self.significance_tests = {}
        
    def calculate_correlations(self, data, method='pearson'):
        """
        Расчет корреляций между переменными
        
        Args:
            data: DataFrame с данными
            method: Метод корреляции ('pearson', 'spearman', 'kendall')
        
        Returns:
            pd.DataFrame: Матрица корреляций
        """
        if method == 'pearson':
            self.correlation_matrix = data.corr(method='pearson')
        elif method == 'spearman':
            self.correlation_matrix = data.corr(method='spearman')
        elif method == 'kendall':
            self.correlation_matrix = data.corr(method='kendall')
        else:
            raise ValueError(f"Неизвестный метод: {method}")
        
        return self.correlation_matrix
    
    def test_correlation_significance(self, x, y, method='pearson'):
        """
        Тестирование значимости корреляции
        
        Args:
            x: Первая переменная
            y: Вторая переменная
            method: Метод корреляции
        
        Returns:
            dict: Результаты теста значимости
        """
        if method == 'pearson':
            correlation, p_value = pearsonr(x, y)
        elif method == 'spearman':
            correlation, p_value = spearmanr(x, y)
        elif method == 'kendall':
            correlation, p_value = kendalltau(x, y)
        else:
            raise ValueError(f"Неизвестный метод: {method}")
        
        return {
            'correlation': correlation,
            'p_value': p_value,
            'is_significant': p_value < 0.05,
            'strength': self.interpret_correlation_strength(abs(correlation))
        }
    
    def interpret_correlation_strength(self, correlation):
        """
        Интерпретация силы корреляции
        
        Args:
            correlation: Значение корреляции
        
        Returns:
            str: Интерпретация силы корреляции
        """
        if correlation < 0.1:
            return 'negligible'
        elif correlation < 0.3:
            return 'weak'
        elif correlation < 0.5:
            return 'moderate'
        elif correlation < 0.7:
            return 'strong'
        else:
            return 'very strong'
    
    def analyze_device_correlations(self, device_data):
        """
        Анализ корреляций между устройствами
        
        Args:
            device_data: Данные устройств
        
        Returns:
            dict: Результаты анализа корреляций
        """
        correlations = {}
        
        # Корреляция энергопотребления между устройствами
        power_data = device_data.pivot_table(
            index='timestamp',
            columns='device_id',
            values='power_consumption',
            fill_value=0
        )
        
        power_correlations = self.calculate_correlations(power_data)
        
        # Поиск сильно коррелированных устройств
        strong_correlations = []
        for i in range(len(power_correlations.columns)):
            for j in range(i+1, len(power_correlations.columns)):
                corr_value = power_correlations.iloc[i, j]
                if abs(corr_value) > 0.7:  # Сильная корреляция
                    strong_correlations.append({
                        'device1': power_correlations.columns[i],
                        'device2': power_correlations.columns[j],
                        'correlation': corr_value,
                        'strength': self.interpret_correlation_strength(abs(corr_value))
                    })
        
        correlations['power_correlations'] = power_correlations
        correlations['strong_correlations'] = strong_correlations
        
        return correlations
    
    def analyze_user_behavior_correlations(self, user_data):
        """
        Анализ корреляций в поведении пользователей
        
        Args:
            user_data: Данные пользователей
        
        Returns:
            dict: Результаты анализа корреляций
        """
        correlations = {}
        
        # Корреляция между временем использования и энергопотреблением
        time_energy_corr = self.test_correlation_significance(
            user_data['usage_hours'],
            user_data['energy_consumption']
        )
        
        # Корреляция между количеством устройств и общим потреблением
        devices_consumption_corr = self.test_correlation_significance(
            user_data['device_count'],
            user_data['total_consumption']
        )
        
        # Корреляция между активностью и эффективностью
        activity_efficiency_corr = self.test_correlation_significance(
            user_data['activity_score'],
            user_data['efficiency_score']
        )
        
        correlations['time_energy'] = time_energy_corr
        correlations['devices_consumption'] = devices_consumption_corr
        correlations['activity_efficiency'] = activity_efficiency_corr
        
        return correlations
```

## 6. Заключение

### 6.1 Ключевые особенности математического обеспечения

#### 6.1.1 Комплексность моделей
- **Многоуровневые модели:** От простых до сложных машинного обучения
- **Интегрированный подход:** Связь между различными математическими методами
- **Адаптивность:** Модели, способные к обучению и адаптации
- **Практичность:** Реальные алгоритмы для решения конкретных задач

#### 6.1.2 Эффективность алгоритмов
- **Оптимальная сложность:** O(n log n) для большинства алгоритмов
- **Масштабируемость:** Возможность обработки больших объемов данных
- **Точность:** Высокая точность прогнозов и оптимизации
- **Надежность:** Стабильная работа в различных условиях

#### 6.1.3 Инновационность подходов
- **Машинное обучение:** Современные методы ML для персонализации
- **Оптимизация:** Генетические алгоритмы и линейное программирование
- **Статистика:** Продвинутые методы анализа временных рядов
- **Аналитика:** Комплексный анализ данных и корреляций

### 6.2 Преимущества решения

#### 6.2.1 Для системы
- **Интеллектуальность:** Умные алгоритмы принятия решений
- **Эффективность:** Оптимизация ресурсов и энергопотребления
- **Надежность:** Стабильная работа математических моделей
- **Масштабируемость:** Возможность роста сложности системы

#### 6.2.2 Для пользователей
- **Персонализация:** Адаптация под индивидуальные потребности
- **Экономия:** Оптимизация энергопотребления и затрат
- **Удобство:** Автоматические рекомендации и оптимизация
- **Предсказуемость:** Прогнозы и предупреждения о проблемах

#### 6.2.3 Для бизнеса
- **Конкурентное преимущество:** Уникальные алгоритмы и модели
- **Операционная эффективность:** Автоматизация принятия решений
- **Инновационность:** Современные математические методы
- **Масштабируемость бизнеса:** Возможность роста без увеличения сложности

### 6.3 Следующие шаги

1. **Реализация базовых моделей:** Создание основных математических моделей
2. **Интеграция с системой:** Внедрение алгоритмов в программное обеспечение
3. **Тестирование и валидация:** Проверка точности и эффективности моделей
4. **Оптимизация производительности:** Улучшение скорости работы алгоритмов
5. **Расширение функциональности:** Добавление новых математических методов

---

**Дата создания:** [Текущая дата]  
**Версия:** 1.0  
**Статус:** Утвержден
