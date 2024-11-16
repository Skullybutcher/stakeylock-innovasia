import time

class TrafficLightController:
    def __init__(self):
        self.directions = {'North': 0, 'South': 0, 'East': 0, 'West': 0}
        self.red_count = {'North': 0, 'South': 0, 'East': 0, 'West': 0}
        self.signal_changes = 0
        self.traffic_signal = [0, 0, 0, 0]  # Array to represent traffic signals [North, East, South, West]

    def update_vehicle_count(self, counts):
        # Update vehicle counts from external input
        self.directions = counts

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

        # Print the current status before delay
        self.print_status()

        # Keep the green signal for 5 seconds
        #time.sleep(5)

        # Reset red counts for the prioritized direction
        for direction in self.red_count:
            if direction == priority:
                self.red_count[direction] = 0  # Reset red count for this direction
            else:
                self.red_count[direction] += 1  # Increment red count for other directions

        # Increment signal changes
        self.signal_changes += 1

    def print_status(self):
        print("Current vehicle counts:", self.directions)
        print("Red counts:", self.red_count)
        print("Signal changes:", self.signal_changes)
        print("Traffic signal (1=Green, 0=Red):", self.traffic_signal)
