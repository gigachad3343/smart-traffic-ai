from ultralytics import YOLO
import cv2

# ==========================
# Load YOLO Model
# ==========================
model = YOLO("yolo11n.pt")

# ==========================
# Video Path
# ==========================
VIDEO_PATH = "video/videostraffic.mp4"

cap = cv2.VideoCapture(VIDEO_PATH)

# Check if video opened successfully
if not cap.isOpened():
    print("❌ ERROR: Could not open the video.")
    print("Please check that the video exists at:")
    print(VIDEO_PATH)
    exit()

print("✅ Video loaded successfully!")

# Vehicle classes we want to detect
vehicle_classes = ["car", "bus", "truck", "motorcycle"]

while True:

    success, frame = cap.read()

    # Stop when video ends
    if not success:
        print("✅ Video finished.")
        break

    # Run YOLO
    results = model(frame, verbose=False)

    vehicle_count = 0

    for result in results:

        for box in result.boxes:

            cls = int(box.cls[0])
            class_name = model.names[cls]

            if class_name in vehicle_classes:

                vehicle_count += 1

                x1, y1, x2, y2 = map(int, box.xyxy[0])
                confidence = float(box.conf[0])

                # Draw green rectangle
                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    2
                )

                # Vehicle label
                cv2.putText(
                    frame,
                    f"{class_name} {confidence:.2f}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2
                )

    # Display total vehicles
    cv2.putText(
        frame,
        f"Vehicles: {vehicle_count}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        3
    )

    cv2.imshow("Smart Traffic AI", frame)

    # Press Q to quit
    key = cv2.waitKey(1)
    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()