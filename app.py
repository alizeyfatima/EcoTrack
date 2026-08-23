import streamlit as st
from weather import get_weather
from ml_forecast import predict_consumption
import pandas as pd
import plotly.express as px
from datetime import date

# PAGE CONFIGURATION
st.set_page_config(
    page_title="EcoTrack",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)


# -----------------------------
# CUSTOM STYLING
# -----------------------------

st.markdown("""
<style>

    /* Main background */
    .stApp {
        background-color: #0E1117;
    }

    /* Main content spacing */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 4rem;
        max-width: 1400px;
    }

    /* Main headings */
    h1 {
        font-size: 3.2rem !important;
        font-weight: 700 !important;
        text-align: center;
        margin-bottom: 0.2rem !important;
    }

    h2 {
        font-size: 1.8rem !important;
        font-weight: 600 !important;
        margin-top: 2rem !important;
    }

    h3 {
        font-size: 1.3rem !important;
        font-weight: 600 !important;
    }

    /* Text */
    p, label, .stMarkdown {
        color: #E8E8E8;
    }

    /* Metric cards */
    [data-testid="stMetric"] {
        background-color: #161B22;
        border: 1px solid #30363D;
        padding: 1.2rem;
        border-radius: 12px;
    }

    [data-testid="stMetricLabel"] {
        color: #A8B3C2 !important;
    }

    [data-testid="stMetricValue"] {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 8px;
        border: 1px solid #2E7D32;
        padding: 0.5rem 1.2rem;
        font-weight: 600;
    }

    /* Input boxes */
    .stTextInput input,
    .stNumberInput input {
        border-radius: 8px;
    }

    /* Dividers */
    hr {
        border-color: #30363D;
    }
        /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #11161D;
        border-right: 1px solid #30363D;
    }

    [data-testid="stSidebar"] h2 {
        color: #FFFFFF !important;
    }

    [data-testid="stSidebar"] p {
        color: #A8B3C2 !important;
    }

</style>
""", unsafe_allow_html=True)

# -----------------------------
# SIDEBAR
# -----------------------------

with st.sidebar:

    st.markdown("## 🌱 EcoTrack")

    st.caption("Smart Energy Dashboard")

    st.divider()

    st.markdown("### 📍 Dashboard")

    st.markdown("""
    **Sections**
    
    🌤️ Weather  
    🔌 Appliances  
    📊 Energy Overview  
    📈 Analytics  
    🔮 Forecast  
    🤖 AI Prediction  
    💡 Insights
    """)

    st.divider()

    st.markdown("### ℹ️ About")

    st.caption(
        "EcoTrack helps households monitor electricity "
        "consumption, estimate bills, and forecast future usage."
    )

    st.caption("Built with Streamlit • Python • Machine Learning")

# -----------------------------
# HEADER
# -----------------------------

st.markdown(
    "<h1>🌱 EcoTrack</h1>",
    unsafe_allow_html=True
)

st.markdown(
    """
    <p style="
        text-align: center;
        font-size: 1.25rem;
        color: #A8B3C2;
        margin-top: 0;
    ">
        Smart Home Electricity Tracker & Bill Forecaster
    </p>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <p style="
        text-align: center;
        font-size: 1rem;
        color: #7D8590;
        max-width: 750px;
        margin: 0 auto 2rem auto;
    ">
        Monitor your household electricity consumption,
        understand your energy usage, and forecast your
        future electricity bill using usage and weather data.
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

st.caption(
    "Enter the appliances you use and their typical daily usage."
)

num_appliances = st.number_input(
    "Number of appliances",
    min_value=1,
    max_value=20,
    value=3,
    step=1
)

appliances = []

appliance_options = [
     "Air Conditioner",
     "Refrigerator",
     "Fan",
     "Television",
     "Washing Machine",
     "Microwave",
     "Electric Iron",
     "Water Heater",
     "Laptop",
     "Lights",
     "Other"
     ]
for i in range(num_appliances):

    with st.expander(
        f"🔌 Appliance {i + 1}",
        expanded=(i == 0)
    ):

        col1, col2, col3, col4 = st.columns(4)

        # Appliance name
        with col1:

            selected_appliance = st.selectbox(
                "Appliance",
                appliance_options,
                key=f"appliance_select_{i}"
            )

            if selected_appliance == "Other":

                name = st.text_input(
                    "Enter appliance name",
                    key=f"other_appliance_{i}"
                )

            else:

                name = selected_appliance

        # Power
        with col2:

            power = st.number_input(
                "Power (Watts)",
                min_value=0,
                value=100,
                step=50,
                key=f"power_{i}"
            )

        # Hours
        with col3:

            hours = st.number_input(
                "Hours / Day",
                min_value=0,
                max_value=24,
                value=5,
                step=1,
                key=f"hours_{i}"
            )

        # Days
        with col4:

            days = st.number_input(
                "Days / Month",
                min_value=1,
                max_value=31,
                value=30,
                step=1,
                key=f"days_{i}"
            )

        # Calculate monthly consumption
        power_kw = power / 1000

        monthly_usage = power_kw * hours * days

        appliance = {
            "name": name.strip().title(),
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
# ENERGY OVERVIEW
# -----------------------------

st.header("📊 Energy Overview")

# Find highest consuming appliance
if appliances:
    highest_appliance = max(
        appliances,
        key=lambda appliance: appliance["usage"]
    )
else:
    highest_appliance = None


# KPI cards
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="⚡ Monthly Consumption",
        value=f"{total_usage:,.1f} kWh",
        help="Estimated electricity consumption based on your appliances."
    )

with col2:
    st.metric(
        label="💰 Estimated Bill",
        value=f"Rs. {current_bill:,.0f}",
        help="Estimated monthly electricity bill."
    )

with col3:
    if highest_appliance:
        st.metric(
            label="🔥 Highest Consumer",
            value=highest_appliance["name"],
            help="Appliance responsible for the highest electricity usage."
        )
    else:
        st.metric(
            label="🔥 Highest Consumer",
            value="—"
        )


# Small summary underneath the cards
if highest_appliance and total_usage > 0:

    highest_percentage = (
        highest_appliance["usage"] / total_usage
    ) * 100

    st.caption(
        f"💡 {highest_appliance['name']} accounts for "
        f"**{highest_percentage:.1f}%** of your estimated monthly consumption."
    )
# -----------------------------
# APPLIANCE BREAKDOWN
# -----------------------------

st.header("🔌 Appliance Breakdown")

st.caption(
    "See how each appliance contributes to your household's monthly electricity consumption."
)

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
        "Days / Month": appliance["days"],
        "Monthly Usage (kWh)": appliance["usage"],
        "Usage Share (%)": percentage
    })


breakdown_df = pd.DataFrame(breakdown_data)

st.dataframe(
    breakdown_df,
    use_container_width=True,
    hide_index=True,
    column_config={
       "Appliance": st.column_config.TextColumn(
            "Appliance",
            width="medium"
        ),

        "Power (W)": st.column_config.NumberColumn(
            "Power",
            format="%d W"
        ),

        "Hours / Day": st.column_config.NumberColumn(
            "Hours / Day",
            format="%.0f"
        ),

        "Days / Month": st.column_config.NumberColumn(
            "Days / Month",
            format="%.0f"
        ),

        "Monthly Usage (kWh)": st.column_config.NumberColumn(
            "Monthly Usage",
            format="%.1f kWh"
        ),

        "Usage Share (%)": st.column_config.ProgressColumn(
            "Usage Share",
            format="%.1f%%",
            min_value=0,
            max_value=100
        )
    }
)


# -----------------------------
# CHARTS
# -----------------------------
st.header("📈 Energy Analytics")

st.caption(
    "Visualize which appliances are driving your electricity consumption."
)

# Create data for charts
chart_data = pd.DataFrame({
    "Appliance": [
        a["name"] if a["name"] else f"Appliance {i + 1}"
        for i, a in enumerate(appliances)
    ],
    "Usage": [a["usage"] for a in appliances]
})

chart_col1, chart_col2 = st.columns(2)

#bar chart
with chart_col1:

    st.subheader("⚡ Monthly Consumption")
    
    bar_fig = px.bar(
        chart_data,
        x="Appliance",
        y="Usage",
        text="Usage"
    )

    bar_fig.update_traces(
        texttemplate="%{text:.1f} kWh",
        textposition="outside",
        marker_color="#43A047",
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Usage: %{y:.1f} kWh"
            "<extra></extra>"
        )
    )

    bar_fig.update_layout(
        showlegend=False,

        xaxis_title=None,
        yaxis_title="Monthly Usage (kWh)",

        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",

        font=dict(
            color="#E8E8E8"
        ),

        xaxis=dict(
            showgrid=False
        ),

        yaxis=dict(
            gridcolor="#30363D"
        ),

        margin=dict(
            t=30,
            l=10,
            r=10,
            b=10
        )
    )

    st.plotly_chart(
        bar_fig,
        use_container_width=True
    )


# -----------------------------
# DONUT CHART
# -----------------------------

with chart_col2:

    st.subheader("🥧 Energy Distribution")

    pie_fig = px.pie(
        chart_data,
        names="Appliance",
        values="Usage",
        hole=0.55
    )

    pie_fig.update_traces(
        textposition="inside",
        textinfo="percent",
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Usage: %{value:.1f} kWh<br>"
            "Share: %{percent}"
            "<extra></extra>"
        )
    )

    pie_fig.update_layout(
        showlegend=True,

        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",

        font=dict(
            color="#E8E8E8"
        ),

        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.25,
            xanchor="center",
            x=0.5
        ),

        margin=dict(
            t=20,
            l=10,
            r=10,
            b=40
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

if temperature is None:

    weather_factor = 1.0
    
elif temperature >= 35:

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

st.header("🔮 Next Month Forecast")

st.caption(
    "Estimate your next month's electricity consumption and bill "
    "using recent usage and local weather conditions."
)


# -----------------------------
# FORECAST SUMMARY
# -----------------------------

forecast_col1, forecast_col2, forecast_col3 = st.columns(3)

with forecast_col1:
    st.metric(
        "📚 Historical Average",
        f"{historical_average:,.1f} kWh"
    )

with forecast_col2:

    usage_change = (
        (predicted_usage - total_usage) / total_usage * 100
        if total_usage > 0
        else 0
    )

    st.metric(
        "⚡ Predicted Usage",
        f"{predicted_usage:,.1f} kWh",
        f"{usage_change:+.1f}% vs current"
    )

with forecast_col3:

    bill_change = predicted_bill - current_bill

    st.metric(
        "💰 Predicted Bill",
        f"Rs. {predicted_bill:,.0f}",
        f"Rs. {bill_change:+,.0f}"
    )


# -----------------------------
# FORECAST DETAILS
# -----------------------------

st.subheader("📋 Forecast Details")

detail_col1, detail_col2 = st.columns(2)

with detail_col1:

    st.markdown("### ⚡ Usage")

    st.write(
        f"**Current Usage:** {total_usage:,.1f} kWh"
    )

    st.write(
        f"**Historical Average:** {historical_average:,.1f} kWh"
    )

    st.write(
        f"**Baseline Usage:** {baseline_usage:,.1f} kWh"
    )

with detail_col2:

    st.markdown("### 🌤️ Weather Impact")

    st.write(
        f"**Expected Temperature:** {temperature:.1f} °C"
    )

    st.write(
        f"**Weather Condition:** {description.title()}"
    )

    st.write(
        f"**Weather Adjustment:** "
        f"{(weather_factor - 1) * 100:+.0f}%"
    )


# -----------------------------
# FORECAST MESSAGE
# -----------------------------

if predicted_usage > total_usage:

    st.warning(
        "⚠️ **Higher consumption expected** — "
        "EcoTrack predicts increased electricity usage next month. "
        "Hotter weather may increase cooling demand."
    )

elif predicted_usage < total_usage:

    st.success(
        "🌱 **Lower consumption expected** — "
        "EcoTrack predicts electricity usage will decrease "
        "next month based on current usage and weather conditions."
    )

else:

    st.info(
        "ℹ️ **Stable consumption expected** — "
        "EcoTrack predicts electricity usage will remain "
        "approximately the same next month."
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
# -----------------------------
# MACHINE LEARNING FORECAST
# -----------------------------

st.header("🤖 AI Consumption Forecast")

st.caption(
    "Use the Random Forest model to estimate daily electricity"
    "consumption based on forecast weather conditions."
)

# -----------------------------
# MODEL INFORMATION
# -----------------------------

st.info(
    "🌱 **EcoTrack AI** uses a Random Forest regression model "
    "trained on historical electricity consumption and weather data."
)


# -----------------------------
# WEATHER INPUTS
# -----------------------------

st.subheader("🌤️ Forecast Weather Conditions")

ml_col1, ml_col2, ml_col3, ml_col4 = st.columns(4)

with ml_col1:

    ml_wind = st.number_input(
        "💨 Wind Speed",
        min_value=0.0,
        value=2.5,
        step=0.1
    )

with ml_col2:

    ml_rain = st.number_input(
        "🌧️ Precipitation",
        min_value=0.0,
        value=0.0,
        step=0.1
    )

with ml_col3:

    ml_max_temp = st.number_input(
        "🌡️ Maximum Temperature",
        value=35.0,
        step=0.5
    )

with ml_col4:

    ml_min_temp = st.number_input(
        "🌡️ Minimum Temperature",
        value=27.0,
        step=0.5
    )


# -----------------------------
# ML PREDICTION
# -----------------------------

ml_prediction = predict_consumption(
    str(date.today()),
    ml_wind,
    ml_rain,
    ml_max_temp,
    ml_min_temp
)


# -----------------------------
# PREDICTION RESULT
# -----------------------------

st.subheader("📊 AI Prediction")

prediction_col1, prediction_col2, prediction_col3 = st.columns(3)

with prediction_col1:

    st.metric(
        "🤖 Predicted Daily Consumption",
        f"{ml_prediction:.2f}"
    )

with prediction_col2:

    st.metric(
        "🌡️ Maximum Temperature",
        f"{ml_max_temp:.1f} °C"
    )

with prediction_col3:

    st.metric(
        "💨 Wind Speed",
        f"{ml_wind:.1f}"
    )


# -----------------------------
# MODEL SUMMARY
# -----------------------------

st.markdown("---")

summary_col1, summary_col2 = st.columns(2)

with summary_col1:

    st.markdown("### 🧠 Model")

    st.write("**Algorithm:** Random Forest Regression")

    st.write(
        "**Purpose:** Predict daily electricity consumption"
    )

with summary_col2:

    st.markdown("### 🌤️ Inputs")

    st.write(
        "**Weather:** Wind, precipitation, maximum temperature, "
        "and minimum temperature"
    )

    st.write(
        "**Output:** Predicted electricity consumption"
    )


st.caption(
    "The ML prediction is an estimate generated by EcoTrack's "
    "Random Forest regression model."
)

# -----------------------------
# FOOTER
# -----------------------------

st.divider()

st.markdown(
    """
    <div style="
        text-align: center;
        color: #7D8590;
        padding: 1rem 0;
    ">
        <strong>🌱 EcoTrack</strong><br>
        Smart Home Electricity Tracker & Bill Forecaster<br>
        <small>Built with Python • Streamlit • Plotly • Machine Learning</small>
    </div>
    """,
    unsafe_allow_html=True
)