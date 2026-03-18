import yfinance as yf
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')  # Явно указываем бэкенд
import matplotlib.pyplot as plt

# 1. СКАЧИВАЕМ ДАННЫЕ
# Скачиваем историю цены Биткоина за 2 года
print("Скачиваем данные...")
data = yf.download("BTC-USD", start="2022-01-01", end="2024-01-01")

# 2. СОЗДАЕМ ИНДИКАТОРЫ
# Быстрая скользящая средняя (за 50 дней)
data['SMA_50'] = data['Close'].rolling(window=50).mean()
# Медленная скользящая средняя (за 200 дней)
data['SMA_200'] = data['Close'].rolling(window=200).mean()

# 3. ГЕНЕРИРУЕМ СИГНАЛЫ
# Создаем колонку 'Signal', по умолчанию 0 (ничего не делаем)
data['Signal'] = 0

# Если Быстрая > Медленной -> Ставим 1 (Покупать)
data.loc[data['SMA_50'] > data['SMA_200'], 'Signal'] = 1

# 4. БЭКТЕСТ (ПРОВЕРКА НА ИСТОРИИ)
# Считаем доходность самой монеты (просто держали и ждали)
data['Market_Return'] = data['Close'].pct_change()

# Считаем доходность нашей стратегии
# Мы покупаем, когда Signal = 1. Значит, завтра мы получаем доходность рынка.
# .shift(1) нужен, чтобы мы не знали будущее (мы покупаем сегодня, а прибыль получаем завтра)
data['Strategy_Return'] = data['Signal'].shift(1) * data['Market_Return']

# 5. РЕЗУЛЬТАТЫ
# Считаем накопленный процент роста
market_cum = (1 + data['Market_Return']).cumprod()
strategy_cum = (1 + data['Strategy_Return']).cumprod()

print(f"Если бы просто держали Биткоин: {market_cum.iloc[-1]:.2f}x")
print(f"Если бы использовали нашего робота: {strategy_cum.iloc[-1]:.2f}x")

# 6. РИСУЕМ ГРАФИК
plt.figure(figsize=(12, 6))
plt.plot(strategy_cum, label='Наш Робот', color='green')
plt.plot(market_cum, label='Просто Биткоин', color='gray', linestyle='--')
plt.title('Бэк тест: Робот против Рынка')
plt.legend()
plt.grid(True)
plt.show()