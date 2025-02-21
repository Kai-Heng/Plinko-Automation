import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
file_path = "Plinko_automation/plinko_multiplier_log.csv"
df = pd.read_csv(file_path)

# Convert multipliers to numeric values by removing '×' and converting to float
df['Multiplier'] = df['Multiplier'].str.replace('×', '', regex=True).astype(float)

# Identify losses and wins
df['Loss'] = df['Multiplier'] == 0.2  # Loss is when multiplier is 0.2
df['Win'] = df['Multiplier'] > 0.2    # Win is anything greater than 0.2

# Count consecutive losses before a win
loss_streaks = []
streak = 0

for multiplier in df['Multiplier']:
    if multiplier == 0.2:
        streak += 1
    else:
        if streak > 0:
            loss_streaks.append(streak)
        streak = 0

# If streak ended at the last bet, add it
if streak > 0:
    loss_streaks.append(streak)

# Display loss streak analysis
if loss_streaks:
    print(f"Average consecutive losses before a win: {sum(loss_streaks) / len(loss_streaks):.2f}")
    print(f"Max consecutive losses: {max(loss_streaks)}")
else:
    print("No loss streaks detected.")

# Plot loss streaks
plt.figure(figsize=(10, 5))
plt.hist(loss_streaks, bins=range(1, max(loss_streaks) + 2), edgecolor='black', alpha=0.7)
plt.xlabel("Consecutive Losses Before a Win")
plt.ylabel("Frequency")
plt.title("Distribution of Loss Streaks")
plt.xticks(range(1, max(loss_streaks) + 1))
plt.show()
