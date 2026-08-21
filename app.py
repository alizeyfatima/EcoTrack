import streamlit as st
from weather import get_weather
import pandas as pd
import plotly.express as px

# PAGE CONFIGURATION
st.set_page_config(
    page_title="EcoTrack",
    page_icon="🌱",
    layout="wide"
)

st.markdown("""
<style>

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

.stApp {
    background-color: #0E1117;
}

p, label, .stMarkdown {
    color: #E8E8E8;
}

h1 {
    text-align: center !important;
    font-size: 3.2rem !important;
    font-weight: 700 !important;
}

h2, h3 {
    color: #FFFFFF;
}

h2 {
    margin-top: 2rem !important;
}

h3 {
    margin-top: 1rem !important;
}

</style>
""", unsafe_allow_html=True)

# TITLE
st.markdown(
    "<h1>🌱 EcoTrack</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align:center; font-size:20px;'>"
    "Smart Home Electricity Tracker & Bill Forecaster"
    "</p>",
    unsafe_allow_html=True
)

st.markdown(
    """
    <p style="text-align:center; font-size:18px;">
    Monitor your household electricity consumption,
    understand where your energy is going, and forecast
    your next electricity bill using historical usage and weather data.
    </p>
    """,
    unsafe_allow_html=True
)
st.divider()

# -----------------------------
# WEATHER
# -----------------------------

st.header("🌤️ Local Weather")

city = st.text_input(
    "Enter your city",
    value="Karachi"
)

temperature = None
humidity = None
description = None

if city:

    temperature, humidity, description = get_weather(city)

    if temperature is not None:

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Temperature",
                f"{temperature} °C"
            )

        with col2:
            st.metric(
                "Humidity",
                f"{humidity}%"
            )

        with col3:
            st.metric(
                "Condition",
                description.title()
            )

    else:
        st.error("Unable to retrieve weather information.")


# -----------------------------
# APPLIANCES
# -----------------------------

st.header("🔌 Add Your Appliances")

num_appliances = st.number_input(
    "Number of appliances",
    min_value=1,
    max_value=20,
    value=3,
    step=1
)

appliances = []

for i in range(num_appliances):

    st.subheader(f"Appliance {i + 1}")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

       name_input = st.text_input(
        "Appliance Name",
        key=f"name_{i}"
       )

       name = name_input.strip().title()

      # Keep common abbreviations uppercase
       if name.lower() == "ac":
        name = "AC"

       elif name.lower() == "tv":
        name = "TV"

       elif name.lower() == "led":
        name = "LED"

    with col2:
        power = st.number_input(
            "Power (Watts)",
            min_value=0,
            value=100,
            step=50,
            key=f"power_{i}"
        )

    with col3:
        hours = st.number_input(
            "Hours / Day",
            min_value=0,
            max_value=24,
            value=5,
            step=1,
            key=f"hours_{i}"
        )

    with col4:
        days = st.number_input(
            "Days / Month",
            min_value=1,
            max_value=31,
            value=30,
            step=1,
            key=f"days_{i}"
        )

    # Convert watts to kilowatts
    power_kw = power / 1000

    # Monthly electricity consumption
    monthly_usage = power_kw * hours * days

    appliance = {
        "name": name,
        "power": power,
        "hours": hours,
        "days": days,
        "usage": monthly_usage
    }

    appliances.append(appliance)


# -----------------------------
# CALCULATIONS
# -----------------------------

total_usage = sum(
    appliance["usage"]
    for appliance in appliances
)

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


current_bill = calculate_bill(total_usage)

# -----------------------------
# KEY PERFORMANCE INDICATORS
# -----------------------------

st.header("📊 Current Energy Overview")


# Find highest consuming appliance

if appliances:

    highest_appliance = max(
        appliances,
        key=lambda appliance: appliance["usage"]
    )

else:

    highest_appliance = None


# Create three columns

col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "⚡ Total Monthly Usage",
        f"{total_usage:.2f} kWh"
    )


with col2:

    st.metric(
        "💰 Estimated Current Bill",
        f"Rs. {current_bill:,.2f}"
    )


with col3:

    if highest_appliance:

        st.metric(
            "🔥 Highest Consumer",
            highest_appliance["name"]
        )

# -----------------------------
# BILL AT A GLANCE
# -----------------------------

st.header("💰 Bill at a Glance")

bill_col1, bill_col2 = st.columns(2)


with bill_col1:

    st.metric(
        "Estimated Current Bill",
        f"Rs. {current_bill:,.2f}"
    )


with bill_col2:

    if highest_appliance and total_usage > 0:

        highest_percentage = (
            highest_appliance["usage"]
            / total_usage
        ) * 100

        st.metric(
            "Largest Energy Consumer",
            highest_appliance["name"],
            f"{highest_percentage:.1f}% of usage"
        )
        
st.subheader("Potential Savings")

if highest_appliance and highest_appliance["usage"] > 0:

    potential_saving_usage = (
        highest_appliance["usage"] * 0.10
    )

    potential_saving_bill = calculate_bill(
        max(
            total_usage - potential_saving_usage,
            0
        )
    )

    estimated_saving = (
        current_bill - potential_saving_bill
    )

    st.metric(
        "💚 Estimated Monthly Saving",
        f"Rs. {estimated_saving:,.2f}",
        "If top appliance usage is reduced by 10%"
    )

# -----------------------------
# APPLIANCE BREAKDOWN
# -----------------------------

st.header("🔌 Appliance Breakdown")

breakdown_data = []

for appliance in appliances:

    if total_usage > 0:
        percentage = (
            appliance["usage"] / total_usage
        ) * 100
    else:
        percentage = 0

    breakdown_data.append({
        "Appliance": appliance["name"],
        "Power (W)": appliance["power"],
        "Hours / Day": appliance["hours"],
        "Monthly Usage (kWh)": round(appliance["usage"], 2),
        "Usage Share (%)": round(percentage, 1)
    })


breakdown_df = pd.DataFrame(breakdown_data)

st.dataframe(
    breakdown_df,
    use_container_width=True,
    hide_index=True
)


# -----------------------------
# CHARTS
# -----------------------------

import pandas as pd
import matplotlib.pyplot as plt

st.header("📈 Energy Consumption Charts")

# Create data for charts
chart_data = pd.DataFrame({
    "Appliance": [
        a["name"] if a["name"] else f"Appliance {i + 1}"
        for i, a in enumerate(appliances)
    ],
    "Usage": [a["usage"] for a in appliances]
})

chart_col1, chart_col2 = st.columns(2)
with chart_col1:

    st.subheader("⚡ Electricity Consumption")
    
    bar_fig = px.bar(
    chart_data,
    x="Appliance",
    y="Usage",
    text="Usage",
    color="Appliance",
    color_discrete_sequence=[
        "#2E7D32",
        "#43A047",
        "#66BB6A",
        "#81C784",
        "#A5D6A7",
        "#26A69A",
        "#00897B"
    ]
 )

    bar_fig.update_traces(
    texttemplate="%{text:.1f} kWh",
    textposition="outside"
    )

    bar_fig.update_layout(
    showlegend=False,
    xaxis_title="Appliance",
    yaxis_title="Monthly Usage (kWh)",

    plot_bgcolor="#0E1117",
    paper_bgcolor="#0E1117",

    font=dict(
        color="#FFFFFF"
    ),

    xaxis=dict(
        color="#FFFFFF",
        gridcolor="#252A34"
    ),

    yaxis=dict(
        color="#FFFFFF",
        gridcolor="#252A34"
    ),

    margin=dict(
        t=40,
        l=20,
        r=20,
        b=20
    )
  )
    st.plotly_chart(
    bar_fig,
    use_container_width=True
    )
 

with chart_col2:

    st.subheader("🥧 Energy Distribution")

    pie_fig = px.pie(
    chart_data,
    names="Appliance",
    values="Usage",
    hole=0.45,
    color_discrete_sequence=[
        "#2E7D32",
        "#43A047",
        "#66BB6A",
        "#81C784",
        "#A5D6A7",
        "#26A69A",
        "#00897B"
    ]
    )

    pie_fig.update_traces(
    textposition="inside",
    textinfo="percent+label"
    )

    pie_fig.update_layout(
    showlegend=True,

    plot_bgcolor="#0E1117",
    paper_bgcolor="#0E1117",

    font=dict(
        color="#FFFFFF"
    ),

    legend=dict(
        font=dict(
            color="#FFFFFF"
        )
    ),

    margin=dict(
        t=30,
        l=20,
        r=20,
        b=20
    )
 )

    st.plotly_chart(
    pie_fig,
    use_container_width=True
    )

# -----------------------------
# NEXT MONTH FORECAST
# -----------------------------

st.header("🔮 Next Month Forecast")

# Ask for historical electricity usage
st.subheader("Historical Electricity Usage")

historical_usage = []

for i in range(3):

    usage = st.number_input(
        f"Month {i + 1} usage (kWh)",
        min_value=0,
        value=500,
        key=f"history_{i}"
    )

    historical_usage.append(usage)


# Calculate historical average
historical_average = (
    sum(historical_usage) / len(historical_usage)
)


# Calculate baseline
baseline_usage = (
    historical_average + total_usage
) / 2


# -----------------------------
# WEATHER EFFECT
# -----------------------------

if temperature >= 35:

    weather_factor = 1.15

elif temperature >= 30:

    weather_factor = 1.08

elif temperature >= 25:

    weather_factor = 1.03

else:

    weather_factor = 0.98


# -----------------------------
# PREDICTION
# -----------------------------

predicted_usage = (
    baseline_usage * weather_factor
)

predicted_bill = calculate_bill(predicted_usage)

# -----------------------------
# FORECAST RESULTS
# -----------------------------

st.write(
    "EcoTrack combines your recent electricity usage, "
    "current appliance consumption, and weather conditions "
    "to estimate your electricity usage for next month."
)


# Forecast metrics
col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "📚 Historical Average",
        f"{historical_average:.2f} kWh"
    )


with col2:

    usage_change = (
        (predicted_usage - total_usage)
        / total_usage * 100
        if total_usage > 0
        else 0
    )

    st.metric(
        "⚡ Predicted Usage",
        f"{predicted_usage:.2f} kWh",
        f"{usage_change:+.1f}% vs current"
    )


with col3:

    bill_change = (
        predicted_bill - current_bill
    )

    st.metric(
        "💰 Predicted Bill",
        f"Rs. {predicted_bill:,.2f}",
        f"Rs. {bill_change:+,.2f}"
    )


# Forecast details
st.subheader("Forecast Details")

forecast_col1, forecast_col2 = st.columns(2)


with forecast_col1:

    st.write("**Current Usage:**")
    st.write(f"{total_usage:.2f} kWh")

    st.write("**Historical Average:**")
    st.write(f"{historical_average:.2f} kWh")

    st.write("**Baseline Usage:**")
    st.write(f"{baseline_usage:.2f} kWh")


with forecast_col2:

    st.write("**Expected Temperature:**")
    st.write(f"{temperature:.1f} °C")

    st.write("**Weather Condition:**")
    st.write(description.title())

    st.write("**Weather Adjustment:**")
    st.write(f"{(weather_factor - 1) * 100:+.0f}%")


# Forecast explanation
if predicted_usage > total_usage:

    st.warning(
        "⚠️ EcoTrack predicts higher electricity consumption "
        "next month. Hotter weather may increase cooling demand."
    )

elif predicted_usage < total_usage:

    st.success(
        "🌱 EcoTrack predicts lower electricity consumption "
        "next month based on current usage and weather conditions."
    )

else:

    st.info(
        "ℹ️ EcoTrack predicts electricity consumption "
        "to remain approximately the same next month."
    )
# -----------------------------
# ENERGY INSIGHTS
# -----------------------------

st.header("💡 Energy Insights")


if highest_appliance:

    highest_percentage = (
        highest_appliance["usage"]
        / total_usage * 100
        if total_usage > 0
        else 0
    )

    st.write(
        f"🔥 **{highest_appliance['name']}** is your highest "
        f"energy-consuming appliance, using "
        f"**{highest_appliance['usage']:.2f} kWh/month** "
        f"({highest_percentage:.1f}% of total consumption)."
    )


# Check for high consumption
if total_usage > 500:

    st.warning(
        "⚡ Your estimated household consumption is relatively high. "
        "Reducing usage of your highest-consuming appliances could "
        "significantly lower your electricity bill."
    )

elif total_usage > 300:

    st.info(
        "💡 Your household has moderate electricity consumption. "
        "Monitoring your largest appliances can help control costs."
    )

else:

    st.success(
        "🌱 Your estimated electricity consumption is relatively low. "
        "Continue monitoring your appliances to maintain efficient usage."
    )
    
# -----------------------------
# POTENTIAL SAVINGS
# -----------------------------

st.subheader("💰 Potential Savings")


if highest_appliance and highest_appliance["usage"] > 0:

    potential_saving_usage = (
        highest_appliance["usage"] * 0.10
    )

    potential_saving_bill = calculate_bill(
        max(total_usage - potential_saving_usage, 0)
    )

    estimated_saving = (
        current_bill - potential_saving_bill
    )

    st.metric(
        "Estimated Monthly Saving",
        f"Rs. {estimated_saving:,.2f}",
        "if top appliance usage is reduced by 10%"
    )

    st.caption(
        "This is an estimate intended to demonstrate the "
        "potential impact of reducing usage."
    )
    
# -----------------------------
# FORECAST EXPLANATION
# -----------------------------

st.info(
    f"EcoTrack estimates next month's electricity usage "
    f"using your current appliance consumption, "
    f"historical usage, and local weather conditions."
)