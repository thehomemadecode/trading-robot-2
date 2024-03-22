import pandas as pd
import pandas_ta as ta

# Örnek veri oluşturma
data = {
    'close': [3437.00,3441.22,3433.01,3436.67,3434.12,3433.00,3405.19,3416.08,3415.86,3410.00]
}

# Pandas DataFrame oluşturma
df = pd.DataFrame(data)

# Basit Hareketli Ortalama (SMA) hesaplama
df.ta.sma(length=5, append=True)

# Üstel Hareketli Ortalama (EMA) hesaplama
df.ta.ema(length=5, append=True)

# Göstergeyi DataFrame'e eklemek için
print(df)
print("results: 3483.9985 results: 3435.94 results: 3448.0867")





