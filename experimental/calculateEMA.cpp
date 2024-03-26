#include <stdio.h>

#define PERIOD 5

float calculateEMA(float currentPrice, float previousEMA) {
    float k = 2.0 / (PERIOD + 1);
    return (currentPrice * k) + (previousEMA * (1 - k));
}

int main() {
    float prices[] = {3437.00,3441.22,3433.01,3436.67,3434.12,3433.00,3405.19,3416.08,3415.86,3410.00};
    float ema = prices[0];

    printf("EMA0: %.2f\n", ema);

    
    for (int i = 1; i < sizeof(prices) / sizeof(prices[0]); i++) {
        ema = calculateEMA(prices[i], ema);
        printf("EMA%d: %.2f\n", i, ema);
    }

    return 0;
}
