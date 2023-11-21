#include <Arduino.h>
#include <Wire.h>
#include <LGFXRP2040.h>
#include <debug.h>

// debug 関連
#define DEBUG_MODE 0 //0 or 1
Debug debug(DEBUG_MODE, Serial2, 8, 9, 115200);

LGFXRP2040 display;

void setup() {
    pinMode(LED_BUILTIN, OUTPUT);

    Serial2.setTX(8);
    Serial2.setRX(9);
    Serial2.begin(1000000);

    debug.init();

    display.init();
    display.fillScreen(TFT_BLACK);
}

void loop() {
    if (Serial2.available() > 0) {
        String data = Serial2.readStringUntil('\n'); // 改行までのデータを受信
        const int maxSize = 8192; // 適切なサイズに変更
        uint8_t bitmap[maxSize];
        int count = 0;

        char *ptr = strtok(const_cast<char*>(data.c_str()), ",");
        while (ptr != nullptr && count < maxSize) {
            // コロンがあるかどうかを確認してRLEエンコーディングを検出
            char *colonPtr = strchr(ptr, ':');
            if (colonPtr != nullptr) {
                int value = atoi(ptr);
                int repeatCount = atoi(colonPtr + 1);
                
                // RLEエンコーディングを展開
                for (int i = 0; i < repeatCount && count < maxSize; ++i) {
                    bitmap[count++] = value;
                }
            } else {
                // 非RLEデータ
                bitmap[count++] = atoi(ptr);
            }

            ptr = strtok(nullptr, ",");
        }
        
        // データを表示またはさらなる処理を行う
        display.writePixels(bitmap, count);
        display.display();
    }
}