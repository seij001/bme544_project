import cv2
import os

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier("haarcascade_eye.xml")

def process_frame(frame, out_left_eye_mp4, out_right_eye_mp4, out_left_eye_avi, out_right_eye_avi):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # Initialize variables to store left and right eye images outside the loop
    left_eye_roi = None
    right_eye_roi = None

    # Process each detected face
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]

        # Detect eyes in the face region
        eyes = eye_cascade.detectMultiScale(roi_gray)

        # Sort eyes based on x-coordinate
        eyes = sorted(eyes, key=lambda eye: eye[0])

        # Process each detected eye
        for i, (ex, ey, ew, eh) in enumerate(eyes):
            eye_roi = roi_color[ey:ey + eh, ex:ex + ew]

            # Save left eye
            if i == 0:
                left_eye_roi = eye_roi
            # Save right eye
            elif i == 1:
                right_eye_roi = eye_roi

    # Write frames outside the inner loop
    out_left_eye_mp4.write(left_eye_roi) if left_eye_roi is not None else out_left_eye_mp4.write(frame)
    out_right_eye_mp4.write(right_eye_roi) if right_eye_roi is not None else out_right_eye_mp4.write(frame)
    out_left_eye_avi.write(left_eye_roi) if left_eye_roi is not None else out_left_eye_avi.write(frame)
    out_right_eye_avi.write(right_eye_roi) if right_eye_roi is not None else out_right_eye_avi.write(frame)

    return frame

def process_video(video_path, subject_name):
    # Output file names with subject name
    # output_path_left_eye_mp4 = f"output_{subject_name}_left_eye.mp4"
    # output_path_left_eye_avi = f"output_{subject_name}_left_eye.avi"
    # output_path_right_eye_mp4 = f"output_{subject_name}_right_eye.mp4"
    # output_path_right_eye_avi = f"output_{subject_name}_right_eye.avi"
    output_path_left_eye_mp4 = os.path.join(output_directory, f"output_{subject_name}_left_eye.mp4")
    output_path_left_eye_avi = os.path.join(output_directory, f"output_{subject_name}_left_eye.avi")
    output_path_right_eye_mp4 = os.path.join(output_directory, f"output_{subject_name}_right_eye.mp4")
    output_path_right_eye_avi = os.path.join(output_directory, f"output_{subject_name}_right_eye.avi")

    # VideoWriter objects for left and right eyes in MP4 format
    fourcc_mp4 = cv2.VideoWriter_fourcc(*'mp4v')
    out_left_eye_mp4 = cv2.VideoWriter(output_path_left_eye_mp4, fourcc_mp4, 20.0, (80, 80))  # Update frame size if needed
    out_right_eye_mp4 = cv2.VideoWriter(output_path_right_eye_mp4, fourcc_mp4, 20.0, (80, 80))  # Update frame size if needed

    # VideoWriter objects for left and right eyes in AVI format
    fourcc_avi = cv2.VideoWriter_fourcc(*'XVID')
    out_left_eye_avi = cv2.VideoWriter(output_path_left_eye_avi, fourcc_avi, 20.0, (80, 80))  # Update frame size if needed
    out_right_eye_avi = cv2.VideoWriter(output_path_right_eye_avi, fourcc_avi, 20.0, (80, 80))  # Update frame size if needed

    # Open video capture
    cap = cv2.VideoCapture(video_path)

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        result_frame = process_frame(frame, out_left_eye_mp4, out_right_eye_mp4, out_left_eye_avi, out_right_eye_avi)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()

    # Release VideoWriter objects
    out_left_eye_mp4.release()
    out_right_eye_mp4.release()
    out_left_eye_avi.release()
    out_right_eye_avi.release()

if __name__ == "__main__":
    dataset_directory = "../UBFC_DATASET/DATASET_2" #change dataset number
    output_directory = "dataset_2_roi"  # specify the output directory
    os.makedirs(output_directory, exist_ok=True)  # create output directory if not exists
    
    for subject_folder in os.listdir(dataset_directory):
        subject_path = os.path.join(dataset_directory, subject_folder)
        if os.path.isdir(subject_path):
            video_files = [f for f in os.listdir(subject_path) if f.endswith('.avi')]
            if len(video_files) == 1:
                video_path = os.path.join(subject_path, video_files[0])
                process_video(video_path, subject_folder)
