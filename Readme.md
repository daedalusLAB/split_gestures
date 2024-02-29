# Split Gestures with MediaPipe

This project uses the MediaPipe library to recognize and split gestures from a video using a machine learning model. A gesture is recognized only if it is found a specified number of consecutive times.

## Installation

```
pip install git+https://https://github.com/daedalusLAB/split_gestures.git
```

## Usage

Run the script with the following command:

```
python -m split_gestures.split_gestures --input_dir INPUT_DIR --model_path MODEL_PATH --output_dir OUTPUT_DIR --num_consecutive NUM_CONSECUTIVE
```
