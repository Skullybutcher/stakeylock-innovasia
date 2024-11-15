import time
import random

class TrafficLightController:
    def __init__(self):
        self.directions = {'North': 0, 'South': 0, 'East': 0, 'West': 0}
        self.red_count = {'North': 0, 'South': 0, 'East': 0, 'West': 0}
        self.signal_changes = 0
        self.traffic_signal = [0, 0, 0, 0]  # Array to represent traffic signals [North, East, South, West]

    def update_vehicle_count(self):
        # Simulating vehicle counts with random numbers for demonstration
        self.directions['North'] = random.randint(0, 10)
        self.directions['South'] = random.randint(0, 10)
        self.directions['East'] = random.randint(0, 10)
        self.directions['West'] = random.randint(0, 10)

    def get_priority_direction(self):
        return max(self.directions, key=self.directions.get)

    def change_signal(self):
        # Reset traffic signal array
        self.traffic_signal = [0, 0, 0, 0]

        priority = self.get_priority_direction()
        print(f"Allowing traffic from {priority}")

        # Set the traffic signal for the prioritized direction to green
        if priority == 'North':
            self.traffic_signal[0] = 1  # North
        elif priority == 'East':
            self.traffic_signal[1] = 1  # East
        elif priority == 'South':
            self.traffic_signal[2] = 1  # South
        elif priority == 'West':
            self.traffic_signal[3] = 1  # West

        # Reset red counts for the prioritized direction
        for direction in self.red_count:
            if direction == priority:
                self.red_count[direction] = 0  # Reset red count for this direction
            else:
                self.red_count[direction] += 1  # Increment red count for other directions

        # Increment signal changes
        self.signal_changes += 1

        # Check if any direction has been red for 5 changes
        for direction, count in self.red_count.items():
            if count >= 5:
                print(f"{direction} has been red for too long, allowing it to go next.")
                self.red_count[direction] = 0  # Reset red count for that direction

        # Print the current status
        self.print_status()

    def print_status(self):
        print("Current vehicle counts:", self.directions)
        print("Red counts:", self.red_count)
        print("Signal changes:", self.signal_changes)
        print("Traffic signal (1=Green, 0=Red):", self.traffic_signal)

    def run(self):
        while True:
            self.update_vehicle_count()  # Update vehicle counts
            self.change_signal()  # Change the traffic signal based on the counts
            time.sleep(5)  # Wait for a specified time before the next update (e.g., 5 seconds)

# Example usage
traffic_light_controller = TrafficLightController()
traffic_light_controller.run()