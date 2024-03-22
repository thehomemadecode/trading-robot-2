#include <stdio.h>

#define PERIOD 5 // Periyot say�s�

float calculateEMA(float currentPrice, float previousEMA) {
    float k = 2.0 / (PERIOD + 1);
    return (currentPrice * k) + (previousEMA * (1 - k));
}

int main() {
    float prices[] = {3437.00,3441.22,3433.01,3436.67,3434.12,3433.00,3405.19,3416.08,3415.86,3410.00};
    float ema = prices[0]; // �lk EMA de�eri, ba�lang�� de�eri olarak ilk fiyat al�n�r.

    printf("EMA0: %.2f\n", ema); // Ba�lang�� de�eri yazd�r�l�r.

    // Di�er fiyatlar �zerinden EMA hesaplan�r ve yazd�r�l�r.
    for (int i = 1; i < sizeof(prices) / sizeof(prices[0]); i++) {
        ema = calculateEMA(prices[i], ema);
        printf("EMA%d: %.2f\n", i, ema);
    }

    return 0;
}

//results: 3425.0167 results: 3410.0 results: 3421.723
