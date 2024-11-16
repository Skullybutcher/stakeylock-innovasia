import cv2
import time
from tracker import EuclideanDistTracker
from signal_change import TrafficLightController
from collections import defaultdict

# Initialize tracker and traffic light controller
tracker = EuclideanDistTracker()
traffic_light_controller = TrafficLightController()

# Open video
cap = cv2.VideoCapture("car_counting.mp4")

# Create object detector
object_detector = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40)

# Directions mapping
directions_map = {
    0: 'North',
    1: 'East',
    2: 'South',
    3: 'West'
}

# Initialize timing variables
last_signal_change_time = time.time()
signal_change_interval = 5  # Signal changes every 5 seconds

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Assume frame is divided into 4 regions for 4 directions
    height, width, _ = frame.shape
    regions = {
        'North': frame[:height//2, :width//2],
        'East': frame[:height//2, width//2:],
        'South': frame[height//2:, :width//2],
        'West': frame[height//2:, width//2:]
    }

    # Count vehicles in each region
    vehicle_counts = defaultdict(int)

    for i, (direction, roi) in enumerate(regions.items()):
        # Detect objects in ROI
        mask = object_detector.apply(roi)
        _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        detections = []

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 100:
                x, y, w, h = cv2.boundingRect(cnt)
                detections.append([x, y, w, h])

        boxes_ids = tracker.update(detections)
        vehicle_counts[direction] += len(boxes_ids)

    # Check if it's time to change the signal
    current_time = time.time()
    if current_time - last_signal_change_time >= signal_change_interval:
        # Update traffic light controller with current vehicle counts
        traffic_light_controller.update_vehicle_count(vehicle_counts)

        # Change the signal based on updated counts
        traffic_light_controller.change_signal()

        # Reset the timer
        last_signal_change_time = current_time

    # Display video
    for direction, roi in regions.items():
        cv2.imshow(f"{direction} ROI", roi)
    cv2.imshow("Frame", frame)

    key = cv2.waitKey(30)
    if key == 27:  # Press Esc to exit
        break

cap.release()
cv2.destroyAllWindows()
