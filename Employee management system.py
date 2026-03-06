import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("employees.csv")

print("Initial Dataset:")
print(df)

# Check duplicates
duplicates = df.duplicated().sum()
print("\nNumber of duplicate records:", duplicates)

# Remove duplicates
df = df.drop_duplicates()

# Check missing values
print("\nMissing Values Before Handling:")
print(df.isnull().sum())

# Fill missing Salary & Experience with median
df["Salary"] = df["Salary"].fillna(df["Salary"].median())
df["Experience"] = df["Experience"].fillna(df["Experience"].median())

# Fill missing Department with mode
df["Department"] = df["Department"].fillna(df["Department"].mode()[0])

print("\nMissing Values After Handling:")
print(df.isnull().sum())

# Create correlation matrix
correlation = df[["Experience", "Salary", "Age"]].corr()

# Create one figure with two plots
fig, axes = plt.subplots(1, 2, figsize=(12,5))

# ---------------- Box Plot ----------------
axes[0].boxplot(df["Salary"])
axes[0].set_title("Box Plot of Salary")
axes[0].set_ylabel("Salary")

# ---------------- Heatmap ----------------
cax = axes[1].imshow(correlation)
axes[1].set_title("Correlation Heatmap")

axes[1].set_xticks(range(len(correlation.columns)))
axes[1].set_xticklabels(correlation.columns)

axes[1].set_yticks(range(len(correlation.columns)))
axes[1].set_yticklabels(correlation.columns)

# Add correlation values inside heatmap
for i in range(len(correlation.columns)):
    for j in range(len(correlation.columns)):
        axes[1].text(j, i, round(correlation.iloc[i, j], 2),
                     ha="center", va="center", color="black")

# Color bar
fig.colorbar(cax)

plt.tight_layout()
plt.show()

print("\nCorrelation Matrix:")
print(correlation)
