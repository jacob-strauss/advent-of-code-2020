with open('inputs/bus.txt', 'r') as file:
    arrival, bus_times = file.readlines()

bus_list = bus_times.split(',')
departures = len(bus_list)  # Total number of departures - aka length of timetable
bus_times = {int(elem): index for index, elem in enumerate(bus_list) if elem.isnumeric()}


# --- Solution 1 ---

def waiting_time():
    smallest = float('inf')
    bus_id = 0
    for time in bus_times.keys():
        remainder = int(arrival) % time
        if time - remainder < smallest:
            smallest = time - remainder
            bus_id = time

    return bus_id * smallest


# --- Solution 2 ---

def chinese_remainder_theorem():
    """
    https://www.dave4math.com/mathematics/chinese-remainder-theorem/
    """
    n = 1
    for modulus in bus_times.keys():
        n *= modulus

    res = -departures
    # I don't know why I need to subtract the number of departures from the final answer, but initialising res = 0
    # gives me an answer off by the length of the bus timetable. Oh well.

    for modulus, remainder in bus_times.items():
        t = n // modulus
        u = 1
        while True:
            if (t * u) % modulus == 1:
                break
            u += 1
        res += (departures - remainder) * t * u
    return res
