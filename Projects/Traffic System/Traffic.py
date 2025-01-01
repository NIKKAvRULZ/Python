# Author: 
# Date: 
# Student ID: 

# Task A: Input Validation
def validate_date_input():
    while True:
        try:
            # Get date input from the user
            day = int(input("Enter the day (DD): "))
            if not (1 <= day <= 31):
                raise ValueError("Day must be between 1 and 31.")
            
            month = int(input("Enter the month (MM): "))
            if not (1 <= month <= 12):
                raise ValueError("Month must be between 1 and 12.")
            
            year = int(input("Enter the year (YYYY): "))
            if not (2000 <= year <= 2024):
                raise ValueError("Year must be between 2000 and 2024.")
            
            return f"traffic_data{day:02}{month:02}{year}.csv"
        except ValueError as e:
            print(f"Invalid input: {e}")


def validate_continue_input():
    while True:
        choice = input("\nDo you want to load another dataset? (Y/N): ").strip().upper()
        if choice in ("Y", "N"):
            return choice
        else:
            print("Invalid input. Please enter 'Y' or 'N'.")


# Task B: Processed Outcomes
def process_csv_data(file_path):
    try:
        # Open the file and read lines
        with open(file_path, "r") as file:
            rows = []
            headers = file.readline().strip().split(",")

            # Read rows and split them into dictionaries
            for line in file:
                row_values = line.strip().split(",")
                rows.append(dict(zip(headers, row_values)))
    except FileNotFoundError:
        print(f"File {file_path} does not exist.")
        return None

    required_columns = [
        "JunctionName", "Date", "timeOfDay", "travel_Direction_in", "travel_Direction_out",
        "Weather_Conditions", "JunctionSpeedLimit", "VehicleSpeed", "VehicleType", "elctricHybrid"
    ]
    
    if not all(col in headers for col in required_columns):
        print("CSV file does not have the required format.")
        return None

    # Data Processing Logic
    total_vehicles = len(rows)
    total_trucks = sum(1 for row in rows if row["VehicleType"] == "Truck")
    total_electric_vehicles = sum(1 for row in rows if row["elctricHybrid"].lower() == "true")
    two_wheeled = sum(1 for row in rows if row["VehicleType"] in ["Bike", "Motorbike", "Scooter"])
    buses_north = sum(
        1 for row in rows
        if row["JunctionName"] == "Elm Avenue/Rabbit Road" and 
           row["VehicleType"] == "Buss" and 
           row["travel_Direction_out"] == "N"
    )
    no_turn_vehicles = sum(1 for row in rows if row["travel_Direction_in"] == row["travel_Direction_out"])
    truck_percentage = round((total_trucks / total_vehicles) * 100)
    
    bicycles_per_hour = {}
    for row in rows:
        if row["VehicleType"] == "Bicycle":
            hour = int(row["timeOfDay"].split(":")[0])
            bicycles_per_hour[hour] = bicycles_per_hour.get(hour, 0) + 1
    average_bicycles_per_hour = round(sum(bicycles_per_hour.values()) / len(bicycles_per_hour)) if bicycles_per_hour else 0
    
    over_speed_vehicles = sum(
        1 for row in rows 
        if int(row["VehicleSpeed"]) > int(row["JunctionSpeedLimit"])
    )
    elm_avenue_vehicles = sum(1 for row in rows if row["JunctionName"] == "Elm Avenue/Rabbit Road")
    hanley_highway_vehicles = sum(1 for row in rows if row["JunctionName"] == "Hanley Highway/Westway")
    scooters_elm_avenue = sum(
        1 for row in rows 
        if row["JunctionName"] == "Elm Avenue/Rabbit Road" and row["VehicleType"] == "Scooter"
    )
    scooter_percentage = round((scooters_elm_avenue / elm_avenue_vehicles) * 100) if elm_avenue_vehicles else 0

    hanley_traffic = {}
    for row in rows:
        if row["JunctionName"] == "Hanley Highway/Westway":
            hour = int(row["timeOfDay"].split(":")[0])
            hanley_traffic[hour] = hanley_traffic.get(hour, 0) + 1
    max_traffic = max(hanley_traffic.values(), default=0)
    busiest_hours = [
        f"Between {hour}:00 and {hour + 1}:00" 
        for hour, count in hanley_traffic.items() if count == max_traffic
    ]

    rainy_hours = set(
        int(row["timeOfDay"].split(":")[0]) 
        for row in rows if row["Weather_Conditions"] == "Rain"
    )

    # Store Results
    outcomes = {
        "Total vehicles": total_vehicles,
        "Total trucks": total_trucks,
        "Total electric vehicles": total_electric_vehicles,
        "Two-wheeled vehicles": two_wheeled,
        "Buses heading north (Elm Avenue/Rabbit Road)": buses_north,
        "Vehicles going straight": no_turn_vehicles,
        "Percentage of trucks": truck_percentage,
        "Average bicycles per hour": average_bicycles_per_hour,
        "Vehicles over speed limit": over_speed_vehicles,
        "Vehicles at Elm Avenue/Rabbit Road": elm_avenue_vehicles,
        "Vehicles at Hanley Highway/Westway": hanley_highway_vehicles,
        "Percentage of scooters at Elm Avenue/Rabbit Road": scooter_percentage,
        "Peak hour traffic at Hanley Highway/Westway": max_traffic,
        "Peak hour(s) at Hanley Highway/Westway": busiest_hours,
        "Total hours of rain": len(rainy_hours),
    }

    return outcomes


def display_outcomes(outcomes):
    if outcomes:
        print("\nProcessed Outcomes:")
        for key, value in outcomes.items():
            print(f"{key}: {value}")


# Task C: Save Results to Text File
def save_results_to_file(outcomes, file_name="results.txt"):
    if outcomes:
        with open(file_name, "a") as file:
            file.write("Processed Outcomes:\n")
            for key, value in outcomes.items():
                file.write(f"{key}: {value}\n")
            file.write("\n")


# Main Function
def main():
    date = validate_date_input()
    file_path = date
    
    outcomes = process_csv_data(file_path)
    if outcomes:
        display_outcomes(outcomes)
        save_results_to_file(outcomes)
    

    if validate_continue_input() == "N":
        print("Exiting the program.")
        return
    else:
        main()


if __name__ == "__main__":
    main()
