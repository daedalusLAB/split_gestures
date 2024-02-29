import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
import cv2
import os
#from mediapipe.framework.formats import landmark_pb2
import argparse

def create_recognizer(model_asset_path):
    base_options = python.BaseOptions(model_asset_path=model_asset_path)
    options = vision.GestureRecognizerOptions(base_options=base_options)
    recognizer = vision.GestureRecognizer.create_from_options(options)
    return recognizer

def get_frames(video_path):
    cap = cv2.VideoCapture(video_path)
    frames = []
    index = 0
    fps = cap.get(cv2.CAP_PROP_FPS)
    while cap.isOpened():
        ret, frame = cap.read()
        index += 1
        if index % 6 == 0:
            timestamp = cap.get(cv2.CAP_PROP_POS_MSEC)
            timestamp = int(timestamp)
            if not ret:
                break
            if frame.shape[0] > 600:
                frame = cv2.resize(frame, (800, 600))
            frames.append((timestamp, frame))
    cap.release()
    return frames

def recognize_gestures(recognizer, frames, tmp_file_name, num_consecutive):
    found_gestures = {}
    last_gesture = None
    consecutive_count = 0
    for timestamp, frame in frames:
        cv2.imwrite(tmp_file_name, frame)
        image = mp.Image.create_from_file(tmp_file_name)
        recognition_result = recognizer.recognize(image)
        if len(recognition_result.gestures) > 0:
            # # print all the gestures recognized and their scores
            # for gesture in recognition_result.gestures[0]:
            #     print(f"Gesture: {gesture}")

            top_gesture = recognition_result.gestures[0][0]
            if top_gesture.score > 0.7 and top_gesture.category_name != "none" and top_gesture.category_name != "":
                if last_gesture == top_gesture.category_name:
                    consecutive_count += 1
                    if consecutive_count >= num_consecutive:
                        if top_gesture.category_name in found_gestures:
                            found_gestures[top_gesture.category_name].append(timestamp)
                        else:
                            found_gestures[top_gesture.category_name] = [timestamp]
                else:
                    last_gesture = top_gesture.category_name
                    consecutive_count = 1
        else:
            last_gesture = None
            consecutive_count = 0
        os.remove(tmp_file_name)
    return found_gestures

def process_gestures(found_gestures):
    gesture_timestamps = {}
    for gesture, timestamps in found_gestures.items():
        gesture_timestamps[gesture] = []    
        gesture_timestamps[gesture].append(timestamps[0])
        tmp_timestamp = timestamps[0]
        for i in range(1, len(timestamps)):
            if (i+1 < len(timestamps)) and (timestamps[i+1] - timestamps[i] > 1000):
                    continue
            elif timestamps[i] - tmp_timestamp > 1000:
                gesture_timestamps[gesture].append(timestamps[i])
            tmp_timestamp = timestamps[i]
    return gesture_timestamps

def ms_to_time(ms):
    hours = int(ms / (1000*60*60))
    minutes = int((ms % (1000*60*60)) / (1000*60))
    seconds = int(((ms % (1000*60*60)) % (1000*60)) / 1000)
    rest = int(((ms % (1000*60*60)) % (1000*60)) % 1000)
    return f"{hours}:{minutes}:{seconds}.{rest}"

def create_gesture_videos(video_path, video_name, gesture_timestamps, output_path):
    for gesture, timestamps in gesture_timestamps.items():
        for timestamp in timestamps:
            print(f"Creating video for gesture: {gesture} at timestamp: {timestamp} to {output_path}/{video_name}_{gesture}_{timestamp}.mp4")
            if timestamp - 2000 < 0:
                os.system(f"ffmpeg -i {video_path} -t 4  {output_path}/{video_name}_{gesture}_{timestamp}.mp4 -y > /dev/null 2>&1")
            else:
                os.system(f"ffmpeg -ss {ms_to_time(timestamp-1000)} -i {video_path} -t 4  {output_path}/{video_name}_{gesture}_{timestamp}.mp4 -y  > /dev/null 2>&1 ")

def main():
    parser = argparse.ArgumentParser(description='Split gestures from a video')
    parser.add_argument('--input', type=str, help='Path to the videos folder')
    parser.add_argument('--model', type=str, help='Path to the model')
    parser.add_argument('--output', type=str, help='Path to the output folder')
    parser.add_argument('--nconsecutive', type=int, help='Number of consecutive frames to consider a gesture', default=3)

    args = parser.parse_args()    

    # create output folder if it does not exist
    if not os.path.exists(args.output):
        os.makedirs(args.output)
    
    # check if the input folder exists
    if not os.path.exists(args.input):
        print(f"Error: The input folder does not exist")
        return
    
    # check if the model file exists
    if not os.path.exists(args.model):
        print(f"Error: The model file does not exist")
        return
    

    videos_path = args.input
    model_path = args.model
    output_path = args.output

    recognizer = create_recognizer(model_path)
    # loop through the videos in the videos_path
    for video in os.listdir(videos_path):
        print(f"Processing video: {video}")
        video_path = os.path.join(videos_path, video)
        video_name = os.path.splitext(os.path.basename(video_path))[0]
        tmp_file_name = f"/tmp/tmp_{np.random.randint(1000000000)}.jpg"
        frames = get_frames(video_path)
        found_gestures = recognize_gestures(recognizer, frames, tmp_file_name, args.nconsecutive)
        gesture_timestamps = process_gestures(found_gestures)
        create_gesture_videos(video_path, video_name, gesture_timestamps, output_path)


if __name__ == "__main__":
    main()
