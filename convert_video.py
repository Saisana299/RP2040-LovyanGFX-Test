import cv2
import numpy as np

def convert_to_binary(frame):
    # 128x64にリサイズ
    resized_frame = cv2.resize(frame, (128, 64))
    
    # グレースケールに変換
    gray_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)
    
    # 2値化（白=255、黒=0）
    _, binary_frame = cv2.threshold(gray_frame, 128, 255, cv2.THRESH_BINARY)
    
    return binary_frame.flatten()

def process_video(input_path, output_path, target_fps=15):
    # 動画の読み込み
    cap = cv2.VideoCapture(input_path)
    
    # 元のFPS
    original_fps = cap.get(cv2.CAP_PROP_FPS)
    
    # 出力FPS
    output_fps = target_fps
    
    # フレームごとの待ち時間
    frame_interval = int(original_fps / output_fps)
    
    # CSVファイルに書き込むデータ
    data = []
    
    # フレームを読み込み処理
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # フレームをXFPSでサンプリング
        if frame_count % frame_interval == 0:
            # フレームを白黒変換
            binary_frame = convert_to_binary(frame)
            
            # 1フレーム分のデータを1次元に変換して追加
            data.append(binary_frame)
        
        frame_count += 1
    
    # CSVに保存
    np.savetxt(output_path, data, delimiter=",", fmt="%d")

    # キャプチャの解放
    cap.release()

if __name__ == "__main__":
    input_video_path = "input_video.mp4"
    output_csv_path = "output_data.csv"
    
    process_video(input_video_path, output_csv_path)
