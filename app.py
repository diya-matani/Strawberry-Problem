import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Page Config
st.set_page_config(page_title="Strawberry Problem Solver", page_icon="🍓", layout="centered")

# Custom CSS for better styling
st.markdown("""
<style>
    .main_title {
        text-align: center;
        color: #D32F2F;
    }
    .stButton>button {
        width: 100%;
        background-color: #D32F2F;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1 class='main_title'>🍓 Strawberry Problem Solver</h1>", unsafe_allow_html=True)
st.markdown("Determine the optimum number of boxes of strawberries to purchase per day to maximize profits.")
st.divider()

# Sidebar for inputs (or top columns)
st.subheader("📝 Enter Price Details")
col1, col2, col3 = st.columns(3)

with col1:
    costprice = st.number_input("Cost Price", min_value=0.0, value=60.0, step=1.0)
with col2:
    sellprice = st.number_input("Selling Price", min_value=0.0, value=90.0, step=1.0)
with col3:
    salvageprice = st.number_input("Salvage Price", min_value=0.0, value=30.0, step=1.0)

if sellprice < costprice:
    st.error("⚠️ Selling Price should ideally be higher than Cost Price!")

st.divider()

# Main Logic
if st.button("Calculate Optimal Order"):
    # Hardcoded data from problem statement
    data = {
        'Demand': [12, 13, 14, 15],
        'No. of Days': [12, 24, 36, 48]
    }
    table = pd.DataFrame(data)

    # Calculate Probability
    total_days = table['No. of Days'].sum()
    table['Probability'] = table['No. of Days'] / total_days

    # Order quantities
    order_quantity = [x for x in range(12, 16)]
    
    # Calculate Payoffs
    for y in order_quantity:
        column_values = []
        for x in range(len(table)):
            demand = table.loc[x, 'Demand']
            if y > demand:
                # Ordered more than demand -> Unsold inventory
                payoff = (demand * sellprice) - (y * costprice) + ((y - demand) * salvageprice)
            else:
                # Demand >= Ordered -> Sold out
                payoff = y * (sellprice - costprice)
            column_values.append(payoff)
        table[f'Order {y}'] = column_values

    # Display Payoff Table
    st.subheader("📊 Payoff Table")
    st.dataframe(table.style.format(precision=2), use_container_width=True)

    # Calculate Expected Payoffs
    expected_payoffs_data = []
    for z in order_quantity:
        expected_val = (table['Probability'] * table[f'Order {z}']).sum()
        expected_payoffs_data.append(expected_val)
        
    expected_df = pd.DataFrame({
        "Order Quantity": order_quantity,
        "Expected Payoff": expected_payoffs_data
    })
    
    # Find Optimal
    max_profit = expected_df["Expected Payoff"].max()
    optimal_qty = expected_df.loc[expected_df["Expected Payoff"] == max_profit, "Order Quantity"].values[0]

    # Display Results
    st.subheader("🏆 Optimization Results")
    col_res1, col_res2 = st.columns(2)
    with col_res1:
        st.metric(label="Maximum Expected Profit", value=f"{max_profit:,.2f}")
    with col_res2:
        st.metric(label="Optimum Boxes to Order", value=f"{optimal_qty}")

    st.success(f"The retailer should purchase **{optimal_qty} boxes** per day to maximize profit.")

    # Plotting
    st.subheader("📈 Profit Analysis Chart")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(expected_df["Order Quantity"], expected_df["Expected Payoff"], 
            marker='o', color='#D32F2F', linestyle='-', linewidth=2, markersize=8)
    ax.set_title('Order Quantity vs Expected Payoff', fontsize=12)
    ax.set_xlabel('Order Quantity', fontsize=10)
    ax.set_ylabel('Expected Payoff', fontsize=10)
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Highlight optimal point
    ax.plot(optimal_qty, max_profit, marker='*', color='gold', markersize=15, markeredgecolor='black', label='Optimal Point')
    ax.legend()
    
    st.pyplot(fig)
else:
    st.info("Click the button above to calculate the results.")
