# Lab2.py
# Exploratory Data Analysis for WorldEnergy.csv

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# =====================================================
# 1. Load Dataset
# =====================================================

file_name = "WorldEnergy.csv"

if not os.path.exists(file_name):
    print("Error: WorldEnergy.csv not found.")
    print("Please make sure WorldEnergy.csv and Lab2.py are in the same folder.")
    exit()

df = pd.read_csv(file_name)

print("Dataset loaded successfully.")
print("Dataset shape:", df.shape)

print("\nFirst 5 rows:")
print(df.head())

print("\nColumn names:")
print(df.columns.tolist())

print("\nDataset information:")
print(df.info())

print("\nMissing values:")
print(df.isnull().sum().sort_values(ascending=False).head(20))

print("\nDescriptive statistics:")
print(df.describe())


# =====================================================
# 2. Create Folder for Graphs
# =====================================================

output_folder = "eda_graphs"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

sns.set_theme(style="whitegrid")


# =====================================================
# 3. Basic Data Cleaning
# =====================================================

# Remove rows without country or year
df = df.dropna(subset=["country", "year"])

# Convert year to integer
df["year"] = pd.to_numeric(df["year"], errors="coerce")
df = df.dropna(subset=["year"])
df["year"] = df["year"].astype(int)

# Use data after 1965 for clearer modern energy trends
modern_df = df[df["year"] >= 1965]


# =====================================================
# 4. Graph 1: World Primary Energy Consumption Trend
# =====================================================

if "primary_energy_consumption" in df.columns:
    world_df = modern_df[modern_df["country"] == "World"].copy()

    world_df["primary_energy_consumption"] = pd.to_numeric(
        world_df["primary_energy_consumption"],
        errors="coerce"
    )

    world_df = world_df.dropna(subset=["primary_energy_consumption"])

    if not world_df.empty:
        plt.figure(figsize=(10, 6))
        plt.plot(
            world_df["year"],
            world_df["primary_energy_consumption"],
            marker="o",
            linewidth=2
        )

        plt.title("World Primary Energy Consumption Trend")
        plt.xlabel("Year")
        plt.ylabel("Primary Energy Consumption")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(output_folder + "/01_world_primary_energy_trend.png", dpi=300)
        plt.show()

        print("Graph 1 saved successfully.")
    else:
        print("Graph 1 skipped: no world primary energy consumption data.")
else:
    print("Graph 1 skipped: primary_energy_consumption column not found.")


# =====================================================
# 5. Graph 2: Top 10 Countries by Primary Energy Consumption
# =====================================================

if "primary_energy_consumption" in df.columns:
    temp_df = df[["country", "year", "primary_energy_consumption"]].copy()

    temp_df["primary_energy_consumption"] = pd.to_numeric(
        temp_df["primary_energy_consumption"],
        errors="coerce"
    )

    temp_df = temp_df.dropna(subset=["primary_energy_consumption"])
    temp_df = temp_df[temp_df["primary_energy_consumption"] > 0]

    exclude_names = [
        "World",
        "Asia",
        "Europe",
        "Africa",
        "North America",
        "South America",
        "Oceania",
        "European Union (27)",
        "High-income countries",
        "Upper-middle-income countries",
        "Lower-middle-income countries",
        "Low-income countries"
    ]

    temp_df = temp_df[~temp_df["country"].isin(exclude_names)]

    if not temp_df.empty:
        latest_valid_year = temp_df["year"].max()
        latest_df = temp_df[temp_df["year"] == latest_valid_year]

        top10 = latest_df.sort_values(
            by="primary_energy_consumption",
            ascending=False
        ).head(10)

        plt.figure(figsize=(10, 6))
        sns.barplot(
            data=top10,
            x="primary_energy_consumption",
            y="country"
        )

        plt.title("Top 10 Countries by Primary Energy Consumption in " + str(latest_valid_year))
        plt.xlabel("Primary Energy Consumption")
        plt.ylabel("Country")
        plt.tight_layout()
        plt.savefig(output_folder + "/02_top10_energy_consumption.png", dpi=300)
        plt.show()

        print("Graph 2 saved successfully.")
    else:
        print("Graph 2 skipped: no valid country energy consumption data.")
else:
    print("Graph 2 skipped: primary_energy_consumption column not found.")


# =====================================================
# 6. Graph 3: World Energy Mix
# =====================================================

energy_mix_cols = [
    "coal_consumption",
    "oil_consumption",
    "gas_consumption",
    "nuclear_consumption",
    "hydro_consumption",
    "wind_consumption",
    "solar_consumption",
    "biofuel_consumption"
]

available_mix_cols = [col for col in energy_mix_cols if col in df.columns]

if len(available_mix_cols) > 0:
    world_mix_df = df[df["country"] == "World"].copy()

    for col in available_mix_cols:
        world_mix_df[col] = pd.to_numeric(world_mix_df[col], errors="coerce")

    world_mix_df = world_mix_df.dropna(subset=available_mix_cols, how="all")

    if not world_mix_df.empty:
        latest_world_year = world_mix_df["year"].max()
        latest_world = world_mix_df[world_mix_df["year"] == latest_world_year]

        mix_values = latest_world[available_mix_cols].iloc[0].dropna()
        mix_values = mix_values[mix_values > 0]

        if mix_values.sum() > 0:
            labels = [
                name.replace("_consumption", "").title()
                for name in mix_values.index
            ]

            plt.figure(figsize=(9, 9))
            plt.pie(
                mix_values,
                labels=labels,
                autopct="%1.1f%%",
                startangle=140
            )

            plt.title("World Energy Mix in " + str(latest_world_year))
            plt.tight_layout()
            plt.savefig(output_folder + "/03_world_energy_mix.png", dpi=300)
            plt.show()

            print("Graph 3 saved successfully.")
        else:
            print("Graph 3 skipped: energy mix values are not positive.")
    else:
        print("Graph 3 skipped: no world energy mix data.")
else:
    print("Graph 3 skipped: energy mix columns not found.")


# =====================================================
# 7. Graph 4: Renewable Electricity Share Comparison
# =====================================================

selected_countries = [
    "China",
    "United States",
    "India",
    "Malaysia",
    "Germany"
]

if "renewables_share_elec" in df.columns:
    renewable_df = modern_df[
        modern_df["country"].isin(selected_countries)
    ].copy()

    renewable_df["renewables_share_elec"] = pd.to_numeric(
        renewable_df["renewables_share_elec"],
        errors="coerce"
    )

    renewable_df = renewable_df.dropna(subset=["renewables_share_elec"])

    if not renewable_df.empty:
        plt.figure(figsize=(10, 6))

        for country in selected_countries:
            country_data = renewable_df[renewable_df["country"] == country]

            if not country_data.empty:
                plt.plot(
                    country_data["year"],
                    country_data["renewables_share_elec"],
                    marker="o",
                    linewidth=2,
                    label=country
                )

        plt.title("Renewable Share of Electricity Generation")
        plt.xlabel("Year")
        plt.ylabel("Renewables Share of Electricity (%)")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(output_folder + "/04_renewable_electricity_share.png", dpi=300)
        plt.show()

        print("Graph 4 saved successfully.")
    else:
        print("Graph 4 skipped: no renewable electricity share data.")
else:
    print("Graph 4 skipped: renewables_share_elec column not found.")


# =====================================================
# 8. Graph 5: GDP vs Primary Energy Consumption
# =====================================================

required_cols = [
    "country",
    "year",
    "gdp",
    "primary_energy_consumption",
    "population"
]

if all(col in df.columns for col in required_cols):
    scatter_df = df[required_cols].copy()

    scatter_df["gdp"] = pd.to_numeric(scatter_df["gdp"], errors="coerce")
    scatter_df["primary_energy_consumption"] = pd.to_numeric(
        scatter_df["primary_energy_consumption"],
        errors="coerce"
    )
    scatter_df["population"] = pd.to_numeric(
        scatter_df["population"],
        errors="coerce"
    )

    scatter_df = scatter_df.dropna(
        subset=["gdp", "primary_energy_consumption", "population"]
    )

    # Log scale only works with positive values
    scatter_df = scatter_df[
        (scatter_df["gdp"] > 0) &
        (scatter_df["primary_energy_consumption"] > 0) &
        (scatter_df["population"] > 0)
    ]

    exclude_names = [
        "World",
        "Asia",
        "Europe",
        "Africa",
        "North America",
        "South America",
        "Oceania",
        "European Union (27)",
        "High-income countries",
        "Upper-middle-income countries",
        "Lower-middle-income countries",
        "Low-income countries"
    ]

    scatter_df = scatter_df[~scatter_df["country"].isin(exclude_names)]

    if not scatter_df.empty:
        latest_valid_year = scatter_df["year"].max()
        scatter_latest = scatter_df[scatter_df["year"] == latest_valid_year]

        if not scatter_latest.empty:
            plt.figure(figsize=(10, 6))
            sns.scatterplot(
                data=scatter_latest,
                x="gdp",
                y="primary_energy_consumption",
                size="population",
                sizes=(20, 400),
                alpha=0.6
            )

            plt.xscale("log")
            plt.yscale("log")

            plt.title("GDP vs Primary Energy Consumption in " + str(latest_valid_year))
            plt.xlabel("GDP, log scale")
            plt.ylabel("Primary Energy Consumption, log scale")
            plt.tight_layout()
            plt.savefig(output_folder + "/05_gdp_vs_energy_consumption.png", dpi=300)
            plt.show()

            print("Graph 5 saved successfully.")
        else:
            print("Graph 5 skipped: latest valid year has no data.")
    else:
        print("Graph 5 skipped: no positive GDP and energy consumption data.")
else:
    print("Graph 5 skipped: required columns not found.")


# =====================================================
# 9. Graph 6: Correlation Heatmap
# =====================================================

corr_cols = [
    "population",
    "gdp",
    "primary_energy_consumption",
    "fossil_fuel_consumption",
    "renewables_consumption",
    "electricity_generation",
    "energy_per_capita",
    "carbon_intensity_elec"
]

available_corr_cols = [col for col in corr_cols if col in df.columns]

if len(available_corr_cols) >= 2:
    corr_df = df[available_corr_cols].copy()

    for col in available_corr_cols:
        corr_df[col] = pd.to_numeric(corr_df[col], errors="coerce")

    corr_df = corr_df.dropna()

    if len(corr_df) > 1:
        plt.figure(figsize=(10, 7))
        sns.heatmap(
            corr_df.corr(),
            annot=True,
            cmap="coolwarm",
            fmt=".2f"
        )

        plt.title("Correlation Heatmap of Energy Variables")
        plt.tight_layout()
        plt.savefig(output_folder + "/06_correlation_heatmap.png", dpi=300)
        plt.show()

        print("Graph 6 saved successfully.")
    else:
        print("Graph 6 skipped: not enough complete data for correlation.")
else:
    print("Graph 6 skipped: not enough correlation columns found.")


# =====================================================
# 10. Finish
# =====================================================

print("\nEDA completed.")
print("All available graphs have been saved in the folder:", output_folder)