# ImageProcessing

This project utilizes the OpenCV library for video editing.

## Features

1. **Video Input**: Videos are sourced from the `Input` folder.

2. **Motion Detection**: The program trims the videos by detecting motion. Motion is primarily defined by mouse appearance.

3. **Video Cropping**: After detecting motion, the program further processes the videos by cropping them into three equal quarters from the top, center, and bottom.

## Usage

1. Place the videos you want to process in the `Input` folder.

2. Run the program.

## Requirements

- OpenCV library

## How to Install

Clone the repository and ensure you have OpenCV installed.

```bash
pip install opencv-python-headless
