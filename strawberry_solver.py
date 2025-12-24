import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def main():
    print("Strawberry Problem Solver")
    print("-------------------------")
    
    try:
        costprice = float(input("Enter cost price (e.g., 60): "))
        sellprice = float(input("Enter selling price (e.g., 90): "))
        salvageprice = float(input("Enter salvage price (e.g., 30): "))
    except ValueError:
        print("Invalid input. Using defaults from notebook: 60, 90, 30")
        costprice = 60.0
        sellprice = 90.0
        salvageprice = 30.0

    # Hardcoded data from the notebook's output to replace missing Excel file
    data = {
        'Demand': [12, 13, 14, 15],
        'No. of Days': [12, 24, 36, 48]
    }
    table = pd.DataFrame(data)

    # Calculate Probability
    total_days = table['No. of Days'].sum()
    table['Probability'] = table['No. of Days'] / total_days

    # Order quantities from 12 to 15 (range(12, 16))
    order_quantity = [x for x in range(12, 16)]

    # Calculate Payoffs for each order quantity
    # Payoff = (Sold * SellingPrice) - (Ordered * CostPrice) + (Leftover * SalvagePrice)
    
    for y in order_quantity:
        table[str(y)] = None # Create column for this order quantity (using string for column name mostly, but notebook used int)
        # Notebook used int `y` as column name effectively.
        
        column_values = []
        for x in range(len(table)):
            demand = table.loc[x, 'Demand']
            
            if y > demand:
                # We ordered more than demand. 
                # Sold = demand
                # Leftover = y - demand
                payoff = (demand * sellprice) - (y * costprice) + ((y - demand) * salvageprice)
            else:
                # Demand >= ordered. We sold everything we ordered.
                # Sold = y
                # Leftover = 0
                payoff = y * (sellprice - costprice)
            
            column_values.append(payoff)
        
        table[y] = column_values

    print("\nPayoff Table:")
    print(table)

    # Calculate Expected Payoffs
    expected_payoffs_data = []
    
    for z in order_quantity:
        expected_val = (table['Probability'] * table[z]).sum()
        expected_payoffs_data.append(expected_val)
        
    expected_payoffs = pd.DataFrame(
        data=expected_payoffs_data, 
        index=order_quantity, 
        columns=["Expected Payoff"]
    )

    print("\nExpected Payoffs:")
    print(expected_payoffs)

    # Find Optimal
    max_profit = expected_payoffs["Expected Payoff"].max()
    optimal_qty = expected_payoffs["Expected Payoff"].idxmax()

    print(f"\nThe maximum expected profit = {max_profit}")
    print(f"The optimum number of boxes for maximum profit = {optimal_qty}")

    # Plotting
    try:
        x_axis = order_quantity
        y_axis = expected_payoffs["Expected Payoff"]
        plt.figure(figsize=(10, 6))
        plt.plot(x_axis, y_axis, label="Expected Profit", color='red', marker='o')
        plt.xlabel('Order Quantity')
        plt.ylabel('Expected Payoff')
        plt.title('Order Quantity vs Expected Payoff')
        plt.legend()
        plt.grid(True)
        
        # Save plot to file instead of showing it (better for script execution)
        output_plot = 'strawberry_payoff_plot.png'
        plt.savefig(output_plot)
        print(f"\nPlot saved to {output_plot}")
    except Exception as e:
        print(f"Could not generate plot: {e}")

if __name__ == "__main__":
    main()
