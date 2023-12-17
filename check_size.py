# import cv2
# import os

# def check_video_sizes(video_dir, num_videos=5):
#     video_files = [f for f in os.listdir(video_dir) if f.endswith('.avi')]

#     for i, video_file in enumerate(video_files[:num_videos]):
#         video_path = os.path.join(video_dir, video_file)

#         # Open the video file
#         cap = cv2.VideoCapture(video_path)

#         if not cap.isOpened():
#             print(f"Error opening video file: {video_file}")
#             continue

#         # Get video dimensions
#         width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#         height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

#         print(f"Video {i + 1}: {video_file}, Dimensions: {width}x{height}")

#         # Release the video capture object
#         cap.release()

# if __name__ == "__main__":
#     video_directory = "./"
#     check_video_sizes(video_directory)

import cv2
import os

def check_video_size(video_path):
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Error opening video file: {video_path}")
        return

    # Get video dimensions
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    print(f"Video Dimensions: {width}x{height}")

    # Release the video capture object
    cap.release()

if __name__ == "__main__":
    # Provide the path to the specific video file "vid.avi"
    specific_video_path = "./vid.avi"

    # Check the size of the specific video file
    check_video_size(specific_video_path)
