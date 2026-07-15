from ultralytics import YOLO
import cv2
import time

# ==========================================
# Load YOLO Model
# ==========================================

model = YOLO("yolo11n.pt")

# ==========================================
# Video Path
# ==========================================

VIDEO_PATH = "video/videostraffic.mp4"

# ==========================================
# Vehicle Classes
# ==========================================

VEHICLE_CLASSES = [
    "car",
    "motorcycle",
    "bus",
    "truck"
]

# ==========================================
# Global Variables
# ==========================================

vehicle_count = 0

traffic_density = "LOW"

signal_time = 30

green_road = "A"

road_counts = {
    "A": 0,
    "B": 0,
    "C": 0,
    "D": 0
}

vehicle_types = {
    "car": 0,
    "motorcycle": 0,
    "bus": 0,
    "truck": 0
}

road_vehicle_types = {
    "A": {
        "car": 0,
        "motorcycle": 0,
        "bus": 0,
        "truck": 0
    },
    "B": {
        "car": 0,
        "motorcycle": 0,
        "bus": 0,
        "truck": 0
    },
    "C": {
        "car": 0,
        "motorcycle": 0,
        "bus": 0,
        "truck": 0
    },
    "D": {
        "car": 0,
        "motorcycle": 0,
        "bus": 0,
        "truck": 0
    }
}

counted_ids = set()

# ==========================================
# Generate Frames
# ==========================================

def generate_frames():

    global vehicle_count
    global traffic_density
    global signal_time
    global green_road
    global road_counts
    global vehicle_types
    global road_vehicle_types
    global counted_ids

    cap = cv2.VideoCapture(VIDEO_PATH)

    if not cap.isOpened():
        print("ERROR: Cannot open video.")
        return

    while True:

        success, frame = cap.read()

        if not success:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            counted_ids.clear()
            continue

        line_y = 250

        current_vehicles = 0

        # Reset current frame values

        for r in road_counts:
            road_counts[r] = 0

        for t in vehicle_types:
            vehicle_types[t] = 0

        for r in road_vehicle_types:
            for t in road_vehicle_types[r]:
                road_vehicle_types[r][t] = 0

            # ==========================================
        # YOLO + ByteTrack Detection
        # ==========================================

        results = model.track(
            frame,
            persist=True,
            tracker="bytetrack.yaml",
            verbose=False
        )

        if (
            results
            and len(results) > 0
            and results[0].boxes is not None
            and results[0].boxes.id is not None
        ):

            boxes = results[0].boxes.xyxy.cpu().numpy()
            ids = results[0].boxes.id.int().cpu().tolist()
            classes = results[0].boxes.cls.int().cpu().tolist()

            frame_width = frame.shape[1]

            for box, track_id, cls in zip(boxes, ids, classes):

                class_name = model.names[cls]

                if class_name not in VEHICLE_CLASSES:
                    continue

                current_vehicles += 1

                vehicle_types[class_name] += 1

                x1, y1, x2, y2 = map(int, box)

                center_x = (x1 + x2) // 2
                center_y = (y1 + y2) // 2

                # -----------------------------
                # Detect Road
                # -----------------------------

                if center_x < frame_width * 0.25:
                    road = "A"

                elif center_x < frame_width * 0.50:
                    road = "B"

                elif center_x < frame_width * 0.75:
                    road = "C"

                else:
                    road = "D"

                road_counts[road] += 1
                road_vehicle_types[road][class_name] += 1

                # -----------------------------
                # Count only once
                # -----------------------------

                if center_y > line_y and track_id not in counted_ids:

                    counted_ids.add(track_id)
                    vehicle_count += 1

                # -----------------------------
                # Draw Bounding Box
                # -----------------------------

                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    frame,
                    f"{class_name} {track_id}",
                    (x1, y1 - 8),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    2
                )

                cv2.circle(
                    frame,
                    (center_x, center_y),
                    4,
                    (0, 0, 255),
                    -1
                )
    
            # ==========================================
        # Traffic Density
        # ==========================================

        if current_vehicles <= 5:
            traffic_density = "LOW"
            signal_time = 15

        elif current_vehicles <= 15:
            traffic_density = "MEDIUM"
            signal_time = 30

        else:
            traffic_density = "HIGH"
            signal_time = 45

        # ==========================================
        # Smart Green Road
        # ==========================================

        green_road = max(road_counts, key=road_counts.get)

        # ==========================================
        # Draw Counting Line
        # ==========================================

        h, w = frame.shape[:2]

        cv2.line(frame, (0, line_y), (w, line_y), (255, 0, 0), 3)

        # Road Dividers

        cv2.line(frame, (w // 4, 0), (w // 4, h), (255, 255, 255), 2)
        cv2.line(frame, (w // 2, 0), (w // 2, h), (255, 255, 255), 2)
        cv2.line(frame, (3 * w // 4, 0), (3 * w // 4, h), (255, 255, 255), 2)

        # ==========================================
        # Dashboard
        # ==========================================

        info = [

            f"Vehicles : {vehicle_count}",
            f"Density : {traffic_density}",
            f"Signal : {signal_time}s",
            f"Green Road : {green_road}",

            f"A : {road_counts['A']}",
            f"B : {road_counts['B']}",
            f"C : {road_counts['C']}",
            f"D : {road_counts['D']}",

            f"Cars : {vehicle_types['car']}",
            f"Bikes : {vehicle_types['motorcycle']}",
            f"Buses : {vehicle_types['bus']}",
            f"Trucks : {vehicle_types['truck']}"
        ]

        y = 30

        for text in info:

            cv2.putText(
                frame,
                text,
                (20, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.65,
                (255, 255, 255),
                2
            )

            y += 28

        # ==========================================
        # Encode Frame
        # ==========================================

        ret, buffer = cv2.imencode(".jpg", frame)

        if not ret:
            continue

        frame = buffer.tobytes()

        time.sleep(0.03)

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n'
            + frame +
            b'\r\n'
        )

    cap.release()

    # ==========================================
# API Functions
# ==========================================

def get_vehicle_count():
    return vehicle_count


def get_traffic_density():
    return traffic_density


def get_signal_time():
    return signal_time


def get_green_road():
    return green_road


def get_road_counts():
    return road_counts.copy()


def get_vehicle_types():
    return vehicle_types.copy()


def get_road_vehicle_types():
    return road_vehicle_types.copy()


def get_all_data():

    return {
        "count": vehicle_count,
        "density": traffic_density,
        "signal_time": signal_time,
        "green_road": green_road,
        "roads": road_counts.copy(),
        "types": vehicle_types.copy(),
        "road_types": road_vehicle_types.copy()
    }


def get_total_cars():
    return vehicle_types["car"]


def get_total_bikes():
    return vehicle_types["motorcycle"]


def get_total_buses():
    return vehicle_types["bus"]


def get_total_trucks():
    return vehicle_types["truck"]


def get_busiest_road():
    return max(road_counts, key=road_counts.get)


def get_least_busy_road():
    return min(road_counts, key=road_counts.get)


def get_vehicle_summary():

    return {
        "cars": vehicle_types["car"],
        "motorcycles": vehicle_types["motorcycle"],
        "buses": vehicle_types["bus"],
        "trucks": vehicle_types["truck"],
        "total": vehicle_count
    }


def traffic_report():

    return {
        "total_vehicles": vehicle_count,
        "density": traffic_density,
        "signal_time": signal_time,
        "green_road": green_road,
        "road_counts": road_counts.copy(),
        "vehicle_types": vehicle_types.copy(),
        "road_vehicle_types": road_vehicle_types.copy()
    }