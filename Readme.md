# Split Gestures with MediaPipe

This project uses the MediaPipe library to recognize and split gestures from a video using a machine learning model. A gesture is recognized only if it is found a specified number of consecutive times.

## Project Structure

- `split_gestures/`: The main package that contains the gesture recognition and splitting code.
  - `split_gestures.py`: The script that handles gesture recognition and splitting.

## Setup

1. Clone the repository:
    ```
    git clone https://github.com/yourusername/split-gestures-with-mediapipe.git
    ```
2. Install the package:
    ```
    pip install ./split-gestures-with-mediapipe
    ```

## Usage

Run the script with the following command:

```
python -m split_gestures.split_gestures --input_dir INPUT_DIR --model_path MODEL_PATH --output_dir OUTPUT_DIR --num_consecutive NUM_CONSECUTIVE
```
