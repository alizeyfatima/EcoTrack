from weather import get_weather

print("------ ECOTRACK -------")
print("Home Electricity Tracker")

# Storing appliances
appliances = []



#number of appliances
num_appliances = int(
    input("Enter the number of appliances you want to track: ")
)

#getting appliance information
for i in range(num_appliances):

    print(f"\nAppliance {i + 1}:")

    appliance_name = input("Enter the appliance name: ")

    power_watts = float(
        input("Enter the power consumption in watts: ")
    )

    hours_per_day = float(
        input("Enter the number of hours used per day: ")
    )

    days_per_month = float(
        input("Enter the number of days used per month: ")
    )


    # Convert watts to kilowatts
    power_kw = power_watts / 1000


    # Calculate monthly energy consumption
    monthly_usage = (
        power_kw
        * hours_per_day
        * days_per_month
    )


    # Store appliance information
    appliance = {
        "name": appliance_name,
        "power": power_watts,
        "hours": hours_per_day,
        "days": days_per_month,
        "usage": monthly_usage
    }

    appliances.append(appliance)

#calculate total monthly usage
total_usage = sum(
    appliance["usage"]
    for appliance in appliances
)


#electricity bill calculation
def calculate_bill(usage):

    if usage <= 100:

        bill = usage * 20

    elif usage <= 200:

        bill = (
            (100 * 20)
            + ((usage - 100) * 25)
        )

    elif usage <= 300:

        bill = (
            (100 * 20)
            + (100 * 25)
            + ((usage - 200) * 30)
        )

    else:

        bill = (
            (100 * 20)
            + (100 * 25)
            + (100 * 30)
            + ((usage - 300) * 40)
        )

    return bill


#current estimated bill
current_bill = calculate_bill(total_usage)

#historical electricity usage
historical_usage = []

print("\nEnter your previous monthly electricity usage.")

for i in range(3):

    usage = float(
        input(f"Month {i + 1} usage (kWh): ")
    )

    historical_usage.append(usage)


historical_average = (
    sum(historical_usage)
    / len(historical_usage)
)


print(
    "\nHistorical Average:",
    round(historical_average, 2),
    "kWh"
)

#baseline usage
baseline_usage = (
    historical_average
    + total_usage
) / 2

#get weather information
city = input("\nEnter your city: ")

temperature, humidity, description = get_weather(city)


if temperature is None:

    print(
        "Weather data unavailable. "
        "Using 25°C as default."
    )

    temperature = 25


#weather effect
if temperature >= 35:

    weather_factor = 1.15

elif temperature >= 30:

    weather_factor = 1.08

elif temperature >= 25:

    weather_factor = 1.03

else:

    weather_factor = 0.98

#next month prediction
predicted_usage = (
    baseline_usage
    * weather_factor
)


# Calculate predicted bill
predicted_bill = calculate_bill(
    predicted_usage
)

#display results
print("\n====================================")
print("        APPLIANCE BREAKDOWN")
print("====================================")


for appliance in appliances:

    usage = appliance["usage"]

    if total_usage > 0:

        percentage = (
            usage / total_usage
        ) * 100

    else:

        percentage = 0


    print(
        appliance["name"],
        "-",
        round(usage, 2),
        "kWh",
        "-",
        round(percentage, 1),
        "%"
    )


#find highest consuming appliance
highest_appliance = max(
    appliances,
    key=lambda appliance: appliance["usage"]
)

#current results
print("------------------------------------")

print(
    "TOTAL USAGE:",
    round(total_usage, 2),
    "kWh"
)

print(
    "Highest Consumer:",
    highest_appliance["name"]
)

print(
    "Consumption:",
    round(highest_appliance["usage"], 2),
    "kWh"
)

print(
    "Estimated Monthly Bill: Rs.",
    round(current_bill, 2)
)


#next month forecast
print(
    "\n========== NEXT MONTH FORECAST =========="
)

print("City:", city)

print(
    "Temperature:",
    temperature,
    "°C"
)

print(
    "Humidity:",
    humidity,
    "%"
)

print(
    "Weather:",
    description
)

print(
    "Historical Average:",
    round(historical_average, 2),
    "kWh"
)

print(
    "Baseline Usage:",
    round(baseline_usage, 2),
    "kWh"
)

print(
    "Predicted Usage:",
    round(predicted_usage, 2),
    "kWh"
)

print(
    "Predicted Bill: Rs.",
    round(predicted_bill, 2)
)

print("==========================================")


