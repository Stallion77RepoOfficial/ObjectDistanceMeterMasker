import numpy as np
import cv2
from collections import deque

# Constants
DEFAULT_FOCAL_LENGTH = 450  # Default focal length
DEFAULT_OBJECT_WIDTH = 4    # Default object width in cm
DEFAULT_MIN_AREA = 50       # Default minimum contour area
DEFAULT_MAX_AREA = 100000   # Default maximum contour area

# Initialize deque for smoothing distance measurements
distance_history = deque(maxlen=5)

# Function to calculate distance from the camera
def calculate_distance(rect_params, focal_length, object_width):
    pixel_width = rect_params[1][0]  # Width of the bounding box
    if pixel_width != 0:
        distance = (object_width * focal_length) / pixel_width  # Distance formula
    else:
        distance = 0
    return distance

# Function to detect the color of the object
def detect_color(mean_hue):
    h = mean_hue
    if (0 <= h < 10) or (160 <= h <= 180):
        return 'Red'
    elif 35 <= h < 85:
        return 'Green'
    elif 85 <= h < 130:
        return 'Blue'
    else:
        return 'Unknown'

# Function to display detected object information on the screen
def show_info(image, rect, distance, color_name):
    font = cv2.FONT_HERSHEY_SIMPLEX
    text = f'Distance: {distance:.2f} cm, Color: {color_name}'
    org = (int(rect[0][0]), int(rect[0][1]) - 10)
    cv2.putText(image, text, org, font, 0.6, (0, 255, 255), 2, cv2.LINE_AA)
    return image

# Callback function for trackbars
def empty(a):
    pass

# Set up camera capture
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Create settings window with trackbars
cv2.namedWindow("Settings", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Settings", 500, 800)  # Increased size for settings window

# Function to create HSV trackbars
def create_hsv_trackbars(color_name, window_name="Settings"):
    cv2.createTrackbar(f"{color_name} Lower H", window_name, 0, 180, empty)
    cv2.createTrackbar(f"{color_name} Lower S", window_name, 50, 255, empty)
    cv2.createTrackbar(f"{color_name} Lower V", window_name, 50, 255, empty)
    cv2.createTrackbar(f"{color_name} Upper H", window_name, 10, 180, empty)
    cv2.createTrackbar(f"{color_name} Upper S", window_name, 255, 255, empty)
    cv2.createTrackbar(f"{color_name} Upper V", window_name, 255, 255, empty)

# Create HSV trackbars for Red, Green, and Blue
create_hsv_trackbars("Red")
create_hsv_trackbars("Green")
create_hsv_trackbars("Blue")

# Create additional trackbars for object width, focal length, min area, and max area
cv2.createTrackbar("Object Width (cm)", "Settings", DEFAULT_OBJECT_WIDTH, 100, empty)
cv2.createTrackbar("Focal Length", "Settings", DEFAULT_FOCAL_LENGTH, 2000, empty)
cv2.createTrackbar("Min Area", "Settings", DEFAULT_MIN_AREA, 10000, empty)
cv2.createTrackbar("Max Area", "Settings", DEFAULT_MAX_AREA, 500000, empty)

# Function to track objects based on their centroids
def track_object(prev_center, new_center, threshold=50):
    if prev_center is None:
        return new_center
    dist = np.linalg.norm(np.array(prev_center) - np.array(new_center))
    if dist < threshold:  # if the movement is small, continue tracking the same object
        return new_center
    return None  # If the movement is too large, consider it a new object

# Main loop for real-time processing
prev_center = None
while True:
    ret, frame = cap.read()

    if not ret:
        print("Kamera görüntüsü alınamadı.")
        break

    # Get current values from the sliders
    object_width = cv2.getTrackbarPos("Object Width (cm)", "Settings")
    focal_length = cv2.getTrackbarPos("Focal Length", "Settings")
    min_area = cv2.getTrackbarPos("Min Area", "Settings")
    max_area = cv2.getTrackbarPos("Max Area", "Settings")

    # Prevent division by zero and ensure object_width is positive
    if object_width <= 0:
        object_width = DEFAULT_OBJECT_WIDTH

    # Convert to HSV color space
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Red color mask (single range)
    red_lower_h = cv2.getTrackbarPos("Red Lower H", "Settings")
    red_lower_s = cv2.getTrackbarPos("Red Lower S", "Settings")
    red_lower_v = cv2.getTrackbarPos("Red Lower V", "Settings")
    red_upper_h = cv2.getTrackbarPos("Red Upper H", "Settings")
    red_upper_s = cv2.getTrackbarPos("Red Upper S", "Settings")
    red_upper_v = cv2.getTrackbarPos("Red Upper V", "Settings")

    red_mask = cv2.inRange(hsv_frame, 
                           np.array([red_lower_h, red_lower_s, red_lower_v]), 
                           np.array([red_upper_h, red_upper_s, red_upper_v]))

    # Green color mask
    green_lower_h = cv2.getTrackbarPos("Green Lower H", "Settings")
    green_lower_s = cv2.getTrackbarPos("Green Lower S", "Settings")
    green_lower_v = cv2.getTrackbarPos("Green Lower V", "Settings")
    green_upper_h = cv2.getTrackbarPos("Green Upper H", "Settings")
    green_upper_s = cv2.getTrackbarPos("Green Upper S", "Settings")
    green_upper_v = cv2.getTrackbarPos("Green Upper V", "Settings")

    green_mask = cv2.inRange(hsv_frame, 
                             np.array([green_lower_h, green_lower_s, green_lower_v]), 
                             np.array([green_upper_h, green_upper_s, green_upper_v]))

    # Blue color mask
    blue_lower_h = cv2.getTrackbarPos("Blue Lower H", "Settings")
    blue_lower_s = cv2.getTrackbarPos("Blue Lower S", "Settings")
    blue_lower_v = cv2.getTrackbarPos("Blue Lower V", "Settings")
    blue_upper_h = cv2.getTrackbarPos("Blue Upper H", "Settings")
    blue_upper_s = cv2.getTrackbarPos("Blue Upper S", "Settings")
    blue_upper_v = cv2.getTrackbarPos("Blue Upper V", "Settings")

    blue_mask = cv2.inRange(hsv_frame, 
                            np.array([blue_lower_h, blue_lower_s, blue_lower_v]), 
                            np.array([blue_upper_h, blue_upper_s, blue_upper_v]))

    # Reduce noise with morphological operations
    kernel = np.ones((15, 15), np.uint8)  # Increased kernel size for smoother results
    red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_CLOSE, kernel)
    green_mask = cv2.morphologyEx(green_mask, cv2.MORPH_CLOSE, kernel)
    blue_mask = cv2.morphologyEx(blue_mask, cv2.MORPH_CLOSE, kernel)

    # Combine all masks
    combined_mask = cv2.bitwise_or(red_mask, cv2.bitwise_or(green_mask, blue_mask))

    # Apply Gaussian Blur to reduce noise further
    combined_mask = cv2.GaussianBlur(combined_mask, (15, 15), 0)

    # Find contours
    contours, _ = cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Sort contours by area and filter
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    for cnt in contours:
        area = cv2.contourArea(cnt)

        if min_area < area < max_area:  # Filter contours by area
            # Get bounding box around the detected object
            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)
            box = np.int0(box)  # Avoid DeprecationWarning

            # Calculate distance from the camera
            distance = calculate_distance(rect, focal_length, object_width)
            distance_history.append(distance)
            smoothed_distance = np.mean(distance_history)

            # Get average color of the object (for classification)
            color_mask = np.zeros(hsv_frame.shape[:2], dtype=np.uint8)  # Single-channel mask
            cv2.drawContours(color_mask, [box], -1, 255, thickness=cv2.FILLED)

            # Use single-channel mask to get Hue values
            hue_values = hsv_frame[:, :, 0][color_mask == 255]
            mean_hue = np.mean(hue_values) if len(hue_values) > 0 else 0

            # Detect the color of the object
            color_name = detect_color(mean_hue)

            # Only proceed if the color is known
            if color_name != 'Unknown':
                # Track the object based on its centroid
                moments = cv2.moments(cnt)
                if moments["m00"] != 0:
                    center = (int(moments["m10"] / moments["m00"]), int(moments["m01"] / moments["m00"]))
                    prev_center = track_object(prev_center, center)

                if prev_center is not None:
                    # Draw the bounding box and show distance/color info
                    cv2.drawContours(frame, [box], -1, (255, 0, 0), 3)
                    frame = show_info(frame, rect, smoothed_distance, color_name)

                break  # Remove this if you want to detect multiple objects

    # Display the results
    cv2.imshow("Object Detection", frame)
    cv2.imshow("Masks", combined_mask)

    # Exit loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close windows
cap.release()
cv2.destroyAllWindows()
