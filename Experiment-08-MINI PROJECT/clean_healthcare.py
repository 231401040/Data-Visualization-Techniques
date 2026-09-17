import pandas as pd

df = pd.read_csv("healthcare_dataset.csv")
health = df.copy()

# 1. Fill missing categorical values
for col in ["Medical Condition", "Admission Type", "Insurance Provider",
            "Hospital", "Doctor", "Medication", "Test Results",
            "Gender", "Blood Type"]:
    health[col] = health[col].fillna("Unknown")

# 2. Clean the money column (dataset contains some negative values)
health["Billing Amount"] = health["Billing Amount"].fillna(0).abs().round(2)

# 3. Convert dates
health["Date of Admission"] = pd.to_datetime(health["Date of Admission"], errors="coerce")
health["Discharge Date"] = pd.to_datetime(health["Discharge Date"], errors="coerce")

# 4. Derive length of stay in days
health["Length of Stay"] = (health["Discharge Date"] - health["Date of Admission"]).dt.days
health = health[health["Length of Stay"] >= 0]

# 5. Derive an age group band
def age_band(a):
    if a <= 18: return "0-18"
    elif a <= 40: return "19-40"
    elif a <= 60: return "41-60"
    else: return "60+"

health["Age Group"] = health["Age"].apply(age_band)

# 6. Remove duplicates
health.drop_duplicates(inplace=True)

# 7. Standardise column names
health.columns = (health.columns
                  .str.lower()
                  .str.strip()
                  .str.replace(" ", "_"))

# 8. Report and export
print("Original Shape:", df.shape)
print("Cleaned Shape:", health.shape)
print("\nDataset Preview:")
print(health.head())
print("\nDataset Information:")
print(health.info())

health.to_csv("healthcare_clean.csv", index=False)
print("\nSaved healthcare_clean.csv")