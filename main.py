import cv2
import os

# bg_subtractor = cv2.createBackgroundSubtractorMOG2()

def extract_side(input_path, output_path, side):
    cap = cv2.VideoCapture(input_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Define the positions for top, middle, and bottom sections
    positions = [(0, 0, width, height//3), (0, height//3, width, 2*height//3), (0, 2*height//3, width, height)]

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, positions[side][3]-positions[side][1]))

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        section = frame[positions[side][1]:positions[side][3], positions[side][0]:positions[side][2]]
        out.write(section)

    cap.release()
    out.release()
    cv2.destroyAllWindows()

def detect_mouse_presence(frame, prev_frame):
    # Convert frames to grayscale for difference calculation
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_prev_frame = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

    # Compute absolute difference between frames
    frame_diff = cv2.absdiff(gray_prev_frame, gray_frame)

    # Threshold the difference image
    threshold = 30
    _, thresholded_diff = cv2.threshold(frame_diff, threshold, 255, cv2.THRESH_BINARY)

    # Count non-zero pixels in the thresholded image
    nonzero_count = cv2.countNonZero(thresholded_diff)

    # If there's significant motion, consider the mouse present
    # we have to adjust this threshold according to the videos
    return nonzero_count > 500

def trim_video(input_path, output_path):
    cap = cv2.VideoCapture(input_path)
    fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Initialize variables for trimming
    start_frame = None
    end_frame = None

    # Read the first frame
    ret, prev_frame = cap.read()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if detect_mouse_presence(frame, prev_frame):
            if start_frame is None:
                start_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
            end_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))

        prev_frame = frame

    cap.release()

    # Trim video
    cap = cv2.VideoCapture(input_path)
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    while start_frame <= end_frame:
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)
        start_frame += 1

    cap.release()
    out.release()
    cv2.destroyAllWindows()

def main():
    input_dir = r'D:\DKE\LIN Hiwi\PythonProject\inputvideosT2'
    output_dir = r'D:\DKE\LIN Hiwi\PythonProject\outputvideosT2'
    trimmed_dir = r'D:\DKE\LIN Hiwi\PythonProject\trimmedvideosT2'

    # Create the trimmed videos folder if it doesn't exist
    os.makedirs(trimmed_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.endswith(".mp4"):
            input_path = os.path.join(input_dir, filename)
            base_name = os.path.splitext(filename)[0]

            # Trim the video
            trimmed_path = os.path.join(trimmed_dir, f'{base_name}_trimmed.mp4')
            trim_video(input_path, trimmed_path)

            # Process the trimmed video
            for i in range(3):
                side_name = ['top', 'middle', 'bottom'][i]
                output_path = os.path.join(output_dir, f'{base_name}_{side_name}.mp4')
                extract_side(trimmed_path, output_path, i)
if __name__ == '__main__':
    main()

