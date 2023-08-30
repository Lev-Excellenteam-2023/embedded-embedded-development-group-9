import random

import cv2
import time
import math as m
import mediapipe as mp
from user import User

from consts import CAM_ALIGNMENT_OFFSET, NECK_INCLINATION_THRESHOLD, TORSO_INCLINATION_THRESHOLD, BAD_POSTURE_MIN


def calc_distance(x1, y1, x2, y2):
    dist = m.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return dist


def calc_angle(x1, y1, x2, y2):
    theta = m.acos((y2 - y1) * (-y1) / (m.sqrt(
        (x2 - x1) ** 2 + (y2 - y1) ** 2) * y1))
    degree = int(180 / m.pi) * theta
    return degree


def init_videowriter(video_capture):
    # Meta
    fps = int(video_capture.get(cv2.CAP_PROP_FPS))
    width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_size = (width, height)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    # Return video writer
    return cv2.VideoWriter('output.mp4', fourcc, fps, frame_size)


# Font type
font = cv2.FONT_HERSHEY_SIMPLEX

# Colors for image
blue = (255, 127, 0)
red = (50, 50, 255)
green = (127, 255, 0)
dark_blue = (127, 20, 0)
light_green = (127, 233, 100)
yellow = (0, 255, 255)
pink = (255, 0, 255)

bad_posture_messages = [
    "Hey there, it looks like your spine's on vacation. Can you please bring it back to work and sit straight?",
    "Are you trying out for the 'Leaning Tower of Pisa' impersonation contest? If not, let's straighten up!",
    "Hate to break it to you, but your chair isn't a hammock. Let's give the hammock vibes a break and sit properly.",
    "Rumor has it that the 'Couch Potato Olympics' are next week. Until then, let's work on sitting straight, champ.",
    "I hope you have a slouching permit, because the 'No Slouching Zone' is right here. Sit straight and stay legal!"
]

# Initialize mediapipe pose class
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()


def monitor(user: User) -> (bool, str):
    # For webcam input replace file name with 0
    file_name = 0
    cap = cv2.VideoCapture(file_name)

    # Video writer for video output
    video_output = init_videowriter(cap)
    time.sleep(5)

    # Capture frame from webcam
    success, original_image = cap.read()
    if not success:
        print("Null.Frames")
        return False, ''

    # Get webcam default frames per second
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Get the user bounding box
    x1, y1, x2, y2 = user.crop
    image = original_image[y1:y2, x1:x2]

    # Get height and width
    h, w = image.shape[:2]

    # Convert the BGR image to RGB.
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Process pose
    key_points = pose.process(image)

    # Convert the image back to BGR.
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Use lm and lm_pose as representative of the following methods.
    lm = key_points.pose_landmarks
    lm_pose = mp_pose.PoseLandmark
    if not lm:
        return False, ''

    # Get the landmark coordinates
    # Left shoulder.
    l_shldr_x = int(lm.landmark[lm_pose.LEFT_SHOULDER].x * w)
    l_shldr_y = int(lm.landmark[lm_pose.LEFT_SHOULDER].y * h)
    # Right shoulder
    r_shldr_x = int(lm.landmark[lm_pose.RIGHT_SHOULDER].x * w)
    r_shldr_y = int(lm.landmark[lm_pose.RIGHT_SHOULDER].y * h)
    # Left ear.
    l_ear_x = int(lm.landmark[lm_pose.LEFT_EAR].x * w)
    l_ear_y = int(lm.landmark[lm_pose.LEFT_EAR].y * h)
    # Left hip.
    l_hip_x = int(lm.landmark[lm_pose.LEFT_HIP].x * w)
    l_hip_y = int(lm.landmark[lm_pose.LEFT_HIP].y * h)

    # Calculate distance between left shoulder and right shoulder points
    offset = calc_distance(l_shldr_x, l_shldr_y, r_shldr_x, r_shldr_y)

    # This is to ensure the camera captures the person’s proper side view.
    # We are measuring the horizontal distance between the left and right shoulder points.
    # With correct alignment, the left and right points should almost coincide.
    if offset < CAM_ALIGNMENT_OFFSET:
        cv2.putText(image, str(int(offset)) + ' Aligned', (w - 150, 30), font, 0.9, green, 2)
    else:
        cv2.putText(image, str(int(offset)) + ' Not Aligned', (w - 150, 30), font, 0.9, red, 2)

    # Calculate angles
    neck_inclination = calc_angle(l_shldr_x, l_shldr_y, l_ear_x, l_ear_y)
    torso_inclination = calc_angle(l_hip_x, l_hip_y, l_shldr_x, l_shldr_y)

    # Draw landmarks
    cv2.circle(image, (l_shldr_x, l_shldr_y), 7, yellow, -1)
    cv2.circle(image, (l_ear_x, l_ear_y), 7, yellow, -1)

    # Let's take y - coordinate of P3 100px above x1,  for display elegance.
    # Although we are taking y = 0 while calculating angle between P1,P2,P3.
    cv2.circle(image, (l_shldr_x, l_shldr_y - 100), 7, yellow, -1)
    cv2.circle(image, (r_shldr_x, r_shldr_y), 7, pink, -1)
    cv2.circle(image, (l_hip_x, l_hip_y), 7, yellow, -1)

    # Similarly, here we are taking y - coordinate 100px above x1. Note that
    # you can take any value for y, not necessarily 100 or 200 pixels.
    cv2.circle(image, (l_hip_x, l_hip_y - 100), 7, yellow, -1)

    # Put text, Posture and angle inclination.
    angle_text_string = 'Neck : ' + str(int(neck_inclination)) + '  Torso : ' + str(int(torso_inclination))

    # Determine whether good posture or bad posture.
    # The threshold angles have been set based on intuition.
    if neck_inclination < NECK_INCLINATION_THRESHOLD and torso_inclination < TORSO_INCLINATION_THRESHOLD:
        user.bad_frames = min(0, user.bad_frames - 1)
        # user.good_frames += 1

        cv2.putText(image, angle_text_string, (10, 30), font, 0.9, light_green, 2)
        cv2.putText(image, str(int(neck_inclination)), (l_shldr_x + 10, l_shldr_y), font, 0.9, light_green, 2)
        cv2.putText(image, str(int(torso_inclination)), (l_hip_x + 10, l_hip_y), font, 0.9, light_green, 2)

        # Line landmarks from before
        cv2.line(image, (l_shldr_x, l_shldr_y), (l_ear_x, l_ear_y), green, 4)
        cv2.line(image, (l_shldr_x, l_shldr_y), (l_shldr_x, l_shldr_y - 100), green, 4)
        cv2.line(image, (l_hip_x, l_hip_y), (l_shldr_x, l_shldr_y), green, 4)
        cv2.line(image, (l_hip_x, l_hip_y), (l_hip_x, l_hip_y - 100), green, 4)

    else:
        # user.good_frames = min(0, user.good_frames - 1)
        user.bad_frames += 1

        cv2.putText(image, angle_text_string, (10, 30), font, 0.9, red, 2)
        cv2.putText(image, str(int(neck_inclination)), (l_shldr_x + 10, l_shldr_y), font, 0.9, red, 2)
        cv2.putText(image, str(int(torso_inclination)), (l_hip_x + 10, l_hip_y), font, 0.9, red, 2)

        # Line landmarks from before
        cv2.line(image, (l_shldr_x, l_shldr_y), (l_ear_x, l_ear_y), red, 4)
        cv2.line(image, (l_shldr_x, l_shldr_y), (l_shldr_x, l_shldr_y - 100), red, 4)
        cv2.line(image, (l_hip_x, l_hip_y), (l_shldr_x, l_shldr_y), red, 4)
        cv2.line(image, (l_hip_x, l_hip_y), (l_hip_x, l_hip_y - 100), red, 4)

    # # Calculate the time of remaining in a particular posture
    # good_time = (1 / fps) * good_frames
    # bad_time = (1 / fps) * bad_frames

    # # Pose time
    # if good_time > 0:
    #     time_string_good = 'Good Posture Time : ' + str(round(good_time, 1)) + 's'
    #     cv2.putText(image, time_string_good, (10, h - 20), font, 0.9, green, 2)
    # else:
    #     time_string_bad = 'Bad Posture Time : ' + str(round(bad_time, 1)) + 's'
    #     cv2.putText(image, time_string_bad, (10, h - 20), font, 0.9, red, 2)
    #
    # # If you stay in bad posture for more than 3 minutes (180s) send an alert
    # if bad_time > 180:
    #     send_notification()

    # # Save frames as output video
    # video_output.write(image)

    # Display captured frame and add to user frames
    cv2.imshow('MediaPipe Pose', image)
    user.user_frames.append(image)

    # if cv2.waitKey(5) & 0xFF == ord('q'):
    #     return
    cap.release()
    cv2.destroyAllWindows()

    if user.bad_frames > BAD_POSTURE_MIN:
        return True, bad_posture_messages[random.randint(0, 4)]
    else:
        return False, ''
