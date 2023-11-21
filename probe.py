import csv
import serial
import time

def run_length_encode(data):
    encoded_data = []
    current_count = 1

    for i in range(1, len(data)):
        if data[i] == data[i - 1]:
            current_count += 1
        else:
            encoded_data.append((data[i - 1], current_count))
            current_count = 1

    encoded_data.append((data[-1], current_count))
    return encoded_data

def send_data_to_serial(csv_file_path, serial_port):
    # シリアルポートの設定
    ser = serial.Serial(serial_port, 1000000, timeout=1)

    try:
        with open(csv_file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)

            # 1行目はヘッダーなどがある場合に読み飛ばす
            next(csv_reader, None)

            # Get all rows in a list
            all_rows = list(csv_reader)

            # フレームごとにデータをシリアルポートに送信
            i = 0
            start_time = time.perf_counter()
            while True:
                end_time = time.perf_counter()
                elapsed_time_milliseconds = (end_time - start_time) * 1000
                
                if elapsed_time_milliseconds < (1000/15):
                    continue
                    
                start_time = time.perf_counter()
            
                # Check if we have reached the end of the data
                if i >= len(all_rows):
                    break

                # 1フレーム分のデータ
                frame_data = list(map(int, all_rows[i]))

                # ランレングス圧縮
                compressed_data = run_length_encode(frame_data)

                # データの文字列化とシリアルポートへの送信
                data_str = ','.join(f'{value}:{count}' for value, count in compressed_data)
                data_str += '\n'  # 改行を追加
                ser.write(data_str.encode('utf-8'))

                # Increment i manually based on your requirements
                # For example, you can uncomment the line below to increment i by 2 each time
                i += 1

                # Add a delay if needed

    except KeyboardInterrupt:
        pass

    finally:
        ser.close()

# シリアルポートの設定（COMxはデバイス名に置き換えてください）
serial_port = 'COM12'

# CSVファイルのパスを設定
csv_file_path = 'output_data.csv'

# データをシリアルポートに送信
send_data_to_serial(csv_file_path, serial_port)
