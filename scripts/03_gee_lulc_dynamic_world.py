import ee
import pandas as pd
from google.colab import files

# Define Project ID established in previous cells
PROJECT_ID = 'steam-hour-493717-i3'

# Initialize Earth Engine
try:
    ee.Initialize(project=PROJECT_ID)
except Exception:
    ee.Authenticate()
    ee.Initialize(project=PROJECT_ID)

# Coordinates for selected plots
selected_plots = {
    'Plot4': [[77.98487435142356, 16.75457290594678], [77.99012027269562, 16.7404018580078], [77.99832272146543, 16.75351924617443], [77.99404780804478, 16.75796344612128], [77.98487435142356, 16.75457290594678]],
    'Plot5': [[78.00835046508159, 16.74239328210136], [78.01104101548414, 16.74098856685968], [78.0160625021972, 16.74157074320585], [78.01777502078552, 16.74461848894421], [78.00957189397755, 16.74473827044434], [78.00835046508159, 16.74239328210136]],
    'Plot6': [[77.99733576648987, 16.73582639942359], [77.99867968069657, 16.72972040258868], [78.00210892333689, 16.73019086759409], [78.00235408889219, 16.73371273753379], [78.00027285261922, 16.73230616924524], [78.00015108222344, 16.73477143006452], [77.99733576648987, 16.73582639942359]],
    'Plot7': [[77.9760646224653, 16.73841400298689], [77.97728011542338, 16.73278830998727], [77.98216341556503, 16.72656994775528], [77.99145716103236, 16.72644151603579], [77.99231947399754, 16.73489121403104], [77.9805847665949, 16.73747554880105], [77.9760646224653, 16.73841400298689]],
    'Plot9': [[77.96132825388192, 16.73152653346157], [77.96490595364045, 16.72070460643297], [77.9743174648538, 16.72292296812536], [77.97275407287434, 16.7316160308243], [77.96132825388192, 16.73152653346157]],
    'Plot10': [[77.99332002686535, 16.77327524457403], [77.99589704657423, 16.76459774344642], [78.00137884861174, 16.76755733312756], [77.99881354714734, 16.77071246808508], [77.9971048790583, 16.77421428963936], [77.99624923881552, 16.77129310736423], [77.99332002686535, 16.77327524457403]]
}

target_years = [2018, 2021, 2025]
lulc_records = []

print("Extracting Dynamic World land-use mix...")
for plot_name, coords in selected_plots.items():
    geom = ee.Geometry.Polygon([coords])

    for yr in target_years:
        start_date = f'{yr}-07-01'
        end_date = f'{yr}-11-30'

        # Load Dynamic World collection and compute the mode of the 'label' band
        dw = (ee.ImageCollection("GOOGLE/DYNAMICWORLD/V1")
              .filterBounds(geom)
              .filterDate(start_date, end_date)
              .select('label'))

        mode_label = dw.reduce(ee.Reducer.mode())

        # Calculate pixel count per class (1: Trees, 4: Crops, 7: Bare)
        stats = mode_label.reduceRegion(
            reducer=ee.Reducer.frequencyHistogram(),
            geometry=geom,
            scale=10,
            maxPixels=1e9
        ).get('label_mode').getInfo()

        counts = stats if stats else {}
        total = sum(counts.values()) if counts else 1

        tree_pct = round((counts.get('1', 0) / total) * 100, 1)
        crops_pct = round((counts.get('4', 0) / total) * 100, 1)
        bare_pct = round((counts.get('7', 0) / total) * 100, 1)

        lulc_records.append({
            'Plot_Name': plot_name,
            'Year': yr,
            'Tree_Cover_%': tree_pct,
            'Crops_%': crops_pct,
            'Bare_%': bare_pct
        })

df_lulc = pd.DataFrame(lulc_records)
display(df_lulc.pivot(index='Plot_Name', columns='Year', values=['Tree_Cover_%', 'Crops_%']))

df_lulc.to_excel('LULC_DynamicWorld_Selected_Plots.xlsx', index=False)
files.download('LULC_DynamicWorld_Selected_Plots.xlsx')