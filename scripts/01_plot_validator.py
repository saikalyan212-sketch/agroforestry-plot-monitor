from google.colab import files
import geopandas as gpd
import pandas as pd
import fiona

# Enable KML driver support
fiona.drvsupport.supported_drivers['KML'] = 'rw'

# Upload your file interactively
print("Please upload your KML file:")
uploaded = files.upload()
kml_filename = list(uploaded.keys())[0]  # Automatically grabs the uploaded filename

# Run the validation script using the uploaded file
def validate_agroforestry_plots(kml_path, output_excel_path):
    print("Reading KML file...")
    gdf = gpd.read_file(kml_path, driver='KML')

    name_col = 'Name' if 'Name' in gdf.columns else gdf.columns[0]

    # Reproject to UTM Zone 44N for accurate area calculation in hectares
    gdf_proj = gdf.to_crs(epsg=32644)
    gdf['area_ha'] = gdf_proj.geometry.area / 10000.0

    results = []

    print("Running validation checks...")
    for idx, row in gdf.iterrows():
        plot_name = row.get(name_col, f"Plot_{idx}")
        geom = row['geometry']
        proj_geom = gdf_proj.loc[idx, 'geometry']
        area = row['area_ha']

        is_valid = geom.is_valid
        centroid = geom.centroid
        is_in_district = (77.0 <= centroid.x <= 79.0) and (16.0 <= centroid.y <= 17.5)

        results.append({
            'Plot_Name': plot_name,
            'Area_Hectares': round(area, 2),
            'Valid_Geometry': 'PASS' if is_valid else 'FAIL (Twisted/Invalid Shape)',
            'Within_District': 'PASS' if is_in_district else 'FAIL (Outlier - Outside District)',
            'Geometry_Obj': proj_geom
        })

    df_results = pd.DataFrame(results)

    overlaps = []
    duplicates = []

    for i in range(len(df_results)):
        g1 = df_results.loc[i, 'Geometry_Obj']
        name1 = df_results.loc[i, 'Plot_Name']

        is_overlap = 'PASS'
        is_duplicate = 'PASS'

        for j in range(len(df_results)):
            if i == j:
                continue
            g2 = df_results.loc[j, 'Geometry_Obj']
            name2 = df_results.loc[j, 'Plot_Name']

            if g1.equals(g2) or g1.equals_exact(g2, tolerance=1e-3):
                is_duplicate = f'FAIL (Duplicate of {name2})'

            if g1.overlaps(g2) or (g1.intersects(g2) and g1.intersection(g2).area > 1.0):
                is_overlap = f'FAIL (Overlaps with {name2})'

        overlaps.append(is_overlap)
        duplicates.append(is_duplicate)

    df_results['Overlap_Check'] = overlaps
    df_results['Duplicate_Check'] = duplicates

    df_results['Final_Status'] = df_results.apply(
        lambda r: 'FAIL' if any('FAIL' in str(val) for val in [r['Valid_Geometry'], r['Within_District'], r['Overlap_Check'], r['Duplicate_Check']]) else 'PASS',
        axis=1
    )

    export_df = df_results.drop(columns=['Geometry_Obj'])
    export_df.to_excel(output_excel_path, index=False)

    print(f"\nValidation complete! Results saved to '{output_excel_path}'.")
    display(export_df[['Plot_Name', 'Area_Hectares', 'Final_Status']])

# Execute the function
validate_agroforestry_plots(kml_filename, 'plot_validation_results.xlsx')

# Download the Excel file back to your computer automatically
files.download('plot_validation_results.xlsx')