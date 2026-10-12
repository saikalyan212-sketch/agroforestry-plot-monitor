import ee
import pandas as pd
import matplotlib.pyplot as plt
from google.colab import files

# Define Project ID established in previous cells
PROJECT_ID = 'steam-hour-493717-i3'

# 1. Initialize Google Earth Engine
try:
    ee.Initialize(project=PROJECT_ID)
except Exception:
    ee.Authenticate()
    ee.Initialize(project=PROJECT_ID)

print("Earth Engine authenticated and initialized successfully!")

# 2. Coordinates for selected valid plots (Plots 4, 5, 6, 7, 9, and 10)
selected_plots = {
    'Plot4': [[77.98487435142356, 16.75457290594678], [77.99012027269562, 16.7404018580078], [77.99832272146543, 16.75351924617443], [77.99404780804478, 16.75796344612128], [77.98487435142356, 16.75457290594678]],
    'Plot5': [[78.00835046508159, 16.74239328210136], [78.01104101548414, 16.74098856685968], [78.0160625021972, 16.74157074320585], [78.01777502078552, 16.74461848894421], [78.00957189397755, 16.74473827044434], [78.00835046508159, 16.74239328210136]],
    'Plot6': [[77.99733576648987, 16.73582639942359], [77.99867968069657, 16.72972040258868], [78.00210892333689, 16.73019086759409], [78.00235408889219, 16.73371273753379], [78.00027285261922, 16.73230616924524], [78.00015108222344, 16.73477143006452], [77.99733576648987, 16.73582639942359]],
    'Plot7': [[77.9760646224653, 16.73841400298689], [77.97728011542338, 16.73278830998727], [77.98216341556503, 16.72656994775528], [77.99145716103236, 16.72644151603579], [77.99231947399754, 16.73489121403104], [77.9805847665949, 16.73747554880105], [77.9760646224653, 16.73841400298689]],
    'Plot9': [[77.96132825388192, 16.73152653346157], [77.96490595364045, 16.72070460643297], [77.9743174648538, 16.72292296812536], [77.97275407287434, 16.7316160308243], [77.96132825388192, 16.73152653346157]],
    'Plot10': [[77.99332002686535, 16.77327524457403], [77.99589704657423, 16.76459774344642], [78.00137884861174, 16.76755733312756], [77.99881354714734, 16.77071246808508], [77.9971048790583, 16.77421428963936], [77.99624923881552, 16.77129310736423], [77.99332002686535, 16.77327524457403]]
}

# 3. Time Series extraction (Monsoon/Kharif season: July 1 to October 31)
years = list(range(2018, 2026))
table_rows = []

print("Extracting annual NDVI profiles for the 6 selected plots...")
for plot_name, coords in selected_plots.items():
    geom = ee.Geometry.Polygon([coords])
    row_data = {'Plot_Name': plot_name}

    for year in years:
        start_date = f'{year}-07-01'
        end_date = f'{year}-10-31'

        # Filter Sentinel-2 collection
        s2 = (ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
              .filterBounds(geom)
              .filterDate(start_date, end_date)
              .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 25)))

        # Band math: (B8 - B4) / (B8 + B4)
        def calc_ndvi(img):
            return img.normalizedDifference(['B8', 'B4']).rename('NDVI')

        ndvi_col = s2.map(calc_ndvi)
        stats = ndvi_col.mean().reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=geom,
            scale=10,
            maxPixels=1e9
        )

        # Use client-side getInfo() on the entire stats dictionary to check keys safely
        stats_info = stats.getInfo() or {}
        mean_val = stats_info.get('NDVI', None)

        row_data[str(year)] = round(mean_val, 3) if mean_val is not None else 0.0

    row_data['Net_Change'] = round(row_data['2025'] - row_data['2018'], 3)
    table_rows.append(row_data)
    print(f"  Processed {plot_name} complete.")

# 4. Tabular Summary Display & Excel Export
df_ndvi = pd.DataFrame(table_rows)
print("\n" + "="*80)
print("ANNUAL MEAN NDVI SUMMARY (2018 - 2025) FOR SELECTED PLOTS")
print("="*80)
display(df_ndvi)

output_excel = 'NDVI_Selected_Plots_2018_2025.xlsx'
df_ndvi.to_excel(output_excel, index=False)
print(f"\nTable exported to: {output_excel}")

# 5. Multi-line Time-Series Plot
plt.figure(figsize=(11, 5.5))
plot_years = [str(y) for y in years]

for idx, row in df_ndvi.iterrows():
    plt.plot(plot_years, row[plot_years], marker='o', linewidth=2.2, label=row['Plot_Name'])

plt.title('Vegetation Greening Index (NDVI) Trajectory (2018–2025)', fontsize=13, weight='bold', pad=12)
plt.xlabel('Year', fontsize=11, labelpad=8)
plt.ylabel('Mean NDVI (Peak Season)', fontsize=11, labelpad=8)
plt.ylim(0.0, 1.0)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(bbox_to_anchor=(1.02, 1), loc="upper left", title="Plots")
plt.tight_layout()

# Save image and download files
chart_filename = 'ndvi_trend_selected_plots.png'
plt.savefig(chart_filename, dpi=300)
plt.show()

files.download(output_excel)
files.download(chart_filename)