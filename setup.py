from setuptools import setup, find_packages

setup(
    name='split-gestures',
    version='0.1.0',
    description='A tool to recognize and split gestures from a video using MediaPipe',
    author='Raúl Sánchez',
    author_email='raul@um.es',
    url='https://github.com/raulkite/split-gestures-with-mediapipe',
    packages=find_packages(),
    install_requires=[
        'mediapipe',
        'opencv-python',
        'numpy',
        'argparse',
        'gdown'
    ],
    entry_points={
        'console_scripts': [
            'split_gestures=split_gestures:main'
        ]
    }
)