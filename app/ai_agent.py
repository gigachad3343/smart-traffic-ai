print("AI Agent loaded from:", __file__)

from google import genai

# ==========================================
# Gemini Client
# ==========================================

import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# ==========================================
# Helper Functions
# ==========================================

def busiest_road(traffic):
    return max(traffic["roads"], key=traffic["roads"].get)


def least_busy_road(traffic):
    return min(traffic["roads"], key=traffic["roads"].get)


def local_ai(question, traffic):

    q = question.lower().strip()

    # ======================================
    # Greetings
    # ======================================

    if q in [
        "hi",
        "hello",
        "hey",
        "good morning",
        "good evening"
    ]:

        return (
            "Hello! I'm your Smart Traffic AI Assistant. "
            "Ask me anything about the live traffic."
        )

    # ======================================
    # Total Vehicles
    # ======================================

    if (
        "vehicle" in q
        or "total vehicles" in q
        or "vehicle count" in q
    ):

        return (
            f"There are currently "
            f"{traffic['count']} vehicles detected."
        )

    # ======================================
    # Cars
    # ======================================

    if "car" in q and "road" not in q:

        return (
            f"There are currently "
            f"{traffic['types']['car']} cars."
        )

    # ======================================
    # Motorcycles
    # ======================================

    if "bike" in q or "motorcycle" in q:

        return (
            f"There are currently "
            f"{traffic['types']['motorcycle']} motorcycles."
        )

    # ======================================
    # Buses
    # ======================================

    if "bus" in q:

        return (
            f"There are currently "
            f"{traffic['types']['bus']} buses."
        )

    # ======================================
    # Trucks
    # ======================================

    if "truck" in q:

        return (
            f"There are currently "
            f"{traffic['types']['truck']} trucks."
        )

    # ======================================
    # Road Counts
    # ======================================

    if "road a" in q:
        return f"Road A currently has {traffic['roads']['A']} vehicles."

    if "road b" in q:
        return f"Road B currently has {traffic['roads']['B']} vehicles."

    if "road c" in q:
        return f"Road C currently has {traffic['roads']['C']} vehicles."

    if "road d" in q:
        return f"Road D currently has {traffic['roads']['D']} vehicles."

    # ======================================
    # Road Vehicle Type (Not Supported Yet)
    # ======================================

    if (
        ("car" in q or "bus" in q or "truck" in q or "bike" in q or "motorcycle" in q)
        and "road" in q
    ):

        return (
            "The current version can count the total number of vehicles on each road, "
            "but vehicle-type counting for individual roads is still under development."
        )

    # ======================================
    # Green Signal
    # ======================================

    if "green" in q:

        road = traffic["green_road"]

        return (
            f"Road {road} currently has the green signal because "
            f"it has the highest traffic flow."
        )

    # ======================================
    # Traffic Density
    # ======================================

    if "density" in q or "traffic" in q:

        return (
            f"Current traffic density is {traffic['density']}. "
            f"The signal timer is {traffic['signal_time']} seconds."
        )

    # ======================================
    # Signal Timer
    # ======================================

    if "signal" in q or "timer" in q:

        return (
            f"The current signal timer is "
            f"{traffic['signal_time']} seconds."
        )

    # ======================================
    # Busiest Road
    # ======================================

    if "busiest" in q or "most traffic" in q:

        road = busiest_road(traffic)

        return (
            f"Road {road} currently has the highest traffic "
            f"with {traffic['roads'][road]} vehicles."
        )

    # ======================================
    # Least Busy Road
    # ======================================

    if (
        "least" in q
        or "empty" in q
        or "lowest traffic" in q
    ):

        road = least_busy_road(traffic)

        return (
            f"Road {road} currently has the lowest traffic "
            f"with {traffic['roads'][road]} vehicles."
        )

    # ======================================
    # Compare Roads
    # ======================================

    if "compare" in q:

        roads = []

        for r in ["a", "b", "c", "d"]:
            if f"road {r}" in q:
                roads.append(r.upper())

        if len(roads) == 2:

            r1, r2 = roads

            c1 = traffic["roads"][r1]
            c2 = traffic["roads"][r2]

            if c1 > c2:
                return (
                    f"Road {r1} has more traffic ({c1} vehicles) "
                    f"than Road {r2} ({c2} vehicles)."
                )

            elif c2 > c1:
                return (
                    f"Road {r2} has more traffic ({c2} vehicles) "
                    f"than Road {r1} ({c1} vehicles)."
                )

            else:
                return (
                    f"Road {r1} and Road {r2} both have "
                    f"{c1} vehicles."
                )

        return "Please specify two roads, for example: Compare Road A and Road C."

    # ======================================
    # Traffic Report
    # ======================================

    if (
        "report" in q
        or "summary" in q
        or "status" in q
    ):

        return (
            "===== LIVE TRAFFIC REPORT =====\n\n"
            f"Total Vehicles : {traffic['count']}\n"
            f"Cars : {traffic['types']['car']}\n"
            f"Motorcycles : {traffic['types']['motorcycle']}\n"
            f"Buses : {traffic['types']['bus']}\n"
            f"Trucks : {traffic['types']['truck']}\n\n"
            f"Traffic Density : {traffic['density']}\n"
            f"Signal Timer : {traffic['signal_time']} seconds\n"
            f"Green Road : {traffic['green_road']}\n\n"
            f"Road A : {traffic['roads']['A']}\n"
            f"Road B : {traffic['roads']['B']}\n"
            f"Road C : {traffic['roads']['C']}\n"
            f"Road D : {traffic['roads']['D']}"
        )

    # ======================================
    # Best Route
    # ======================================

    if (
        "best route" in q
        or "which road should i use" in q
        or "best road" in q
    ):

        road = least_busy_road(traffic)

        return (
            f"I recommend using Road {road} because "
            f"it currently has the lowest traffic."
        )

    # ======================================
    # Emergency Vehicles
    # ======================================

    if (
        "ambulance" in q
        or "emergency" in q
        or "fire truck" in q
        or "police" in q
    ):

        return (
            "Emergency vehicles should receive immediate priority. "
            "The smart traffic controller can extend the green signal "
            "to reduce response time."
        )
    
    # ======================================
    # Unsupported Features
    # ======================================

    if (
        "black" in q
        or "white" in q
        or "blue" in q
        or "red" in q
        or "green car" in q
        or "yellow" in q
        or "colour" in q
        or "color" in q
    ):

        return (
            "The current AI model detects vehicle types only. "
            "Vehicle color recognition is not available."
        )

    if (
        "toyota" in q
        or "honda" in q
        or "suzuki" in q
        or "kia" in q
        or "hyundai" in q
        or "brand" in q
    ):

        return (
            "Vehicle brand recognition is not available "
            "in the current system."
        )

    if (
        "speed" in q
        or "fastest" in q
        or "km/h" in q
    ):

        return (
            "Vehicle speed estimation is not implemented "
            "in the current version."
        )

    if (
        "number plate" in q
        or "license plate" in q
        or "registration" in q
    ):

        return (
            "License plate recognition is not enabled "
            "in this project."
        )

    # ======================================
    # Default Answer
    # ======================================

    return (
        "I can answer questions about:\n\n"
        "• Total vehicles\n"
        "• Cars, buses, trucks and motorcycles\n"
        "• Traffic density\n"
        "• Signal timer\n"
        "• Green signal road\n"
        "• Road A, B, C and D vehicle counts\n"
        "• Traffic reports\n"
        "• Road comparison\n"
        "• Best route recommendation"
    )


# ==========================================
# Main AI Function
# ==========================================

def ask_ai(question, traffic):

    prompt = f"""
You are an AI Smart Traffic Control Assistant.

Current Traffic Data

Total Vehicles: {traffic['count']}
Traffic Density: {traffic['density']}
Signal Timer: {traffic['signal_time']}
Green Road: {traffic['green_road']}

Road A: {traffic['roads']['A']}
Road B: {traffic['roads']['B']}
Road C: {traffic['roads']['C']}
Road D: {traffic['roads']['D']}

Cars: {traffic['types']['car']}
Motorcycles: {traffic['types']['motorcycle']}
Buses: {traffic['types']['bus']}
Trucks: {traffic['types']['truck']}

User Question:
{question}

Answer professionally in less than 60 words.
"""

    # Try Gemini first
    try:

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        if response.text:
            return response.text

    except Exception:
        pass

    # Automatic Local AI Fallback
    return local_ai(question, traffic)
