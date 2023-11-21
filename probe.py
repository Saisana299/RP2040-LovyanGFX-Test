import csv
import serial
import time

fps = 15

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

def compress_all_frames(csv_file_path):
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        # 1行目はヘッダーなどがある場合に読み飛ばす
        next(csv_reader, None)

        # Get all rows in a list
        all_rows = list(csv_reader)

        # 圧縮したデータを格納するリスト
        compressed_frames = []

        # 全てのフレームを圧縮
        for row in all_rows:
            frame_data = list(map(int, row))
            compressed_data = run_length_encode(frame_data)
            compressed_frames.append(compressed_data)

    return compressed_frames

def send_compressed_data_to_serial(compressed_frames, serial_port):
    # シリアルポートの設定
    ser = serial.Serial(serial_port, 1000000, timeout=1)

    try:
        # 全てのフレームをシリアルポートに送信
        i = 0
        start_time = time.perf_counter()
        while True:
            end_time = time.perf_counter()
            elapsed_time_milliseconds = (end_time - start_time) * 1000
            
            if elapsed_time_milliseconds < (1000/fps):
                continue
                
            start_time = time.perf_counter()
            
            if i >= len(compressed_frames):
                break
            
            data_str = ','.join(f'{value}:{count}' for value, count in compressed_frames[i])
            data_str += '\n'  # 改行を追加
            ser.write(data_str.encode('utf-8'))
            
            i += 1

    except KeyboardInterrupt:
        pass

    finally:
        ser.close()

# シリアルポートの設定（COMxはデバイス名に置き換えてください）
serial_port = 'COM12'

# CSVファイルのパスを設定
csv_file_path = 'output_data.csv'

# 全てのフレームを圧縮
compressed_frames = compress_all_frames(csv_file_path)

# 圧縮したデータをシリアルポートに送信
send_compressed_data_to_serial(compressed_frames, serial_port)
