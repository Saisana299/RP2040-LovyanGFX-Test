#include <Arduino.h>
#include <Wire.h>
#include <LGFXRP2040.h>

LGFXRP2040 display;

void loop1();

void setup() {
    pinMode(LED_BUILTIN, OUTPUT);

    Serial2.setTX(8);
    Serial2.setRX(9);
    Serial2.begin(1000000);

    display.init();
    display.fillScreen(TFT_BLACK);

    multicore_launch_core1(loop1);
}

void loop() {}

void loop1() {
    if (Serial2.available() > 0) {
        String data = Serial2.readStringUntil('\n'); // 改行までのデータを受信
        const uint16_t maxSize = 8192;
        uint8_t bitmap[maxSize];
        uint16_t count = 0;

        char *ptr = strtok(const_cast<char*>(data.c_str()), ",");
        while (ptr != nullptr && count < maxSize) {
            // コロンがあるかどうかを確認してRLEエンコーディングを検出
            char *colonPtr = strchr(ptr, ':');
            if (colonPtr != nullptr) {
                uint8_t value = atoi(ptr);
                uint16_t repeatCount = atoi(colonPtr + 1);
                
                // RLEエンコーディングを展開
                for (uint16_t i = 0; i < repeatCount && count < maxSize; ++i) {
                    bitmap[count++] = (value == 1) ? 255 : value;
                }
            } else {
                // 非RLEデータ
                bitmap[count++] = (atoi(ptr) == 1) ? 255 : atoi(ptr);
            }

            ptr = strtok(nullptr, ",");
        }
        
        // データを表示
        display.pushImage(0, 0, 128, 64, bitmap);
        display.display();
    }
}