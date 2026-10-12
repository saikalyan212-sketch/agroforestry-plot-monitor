\# Agroforestry Plot Boundary Checker \& Land-Use Change Monitor



An automated GIS and remote sensing pipeline designed to validate incoming agroforestry farm plot boundaries, run quality-assurance geometric checks, and quantify long-term canopy greening using multi-temporal satellite imagery.



!\[Plot Validation Map](visuals/maps/plot\_validation\_status\_map.png)



\---



\## 📌 Project Overview

\* \*\*Target Area:\*\* Mahabubnagar District, Telangana, India

\* \*\*Primary Objective:\*\* Eliminate erroneous field boundary submissions and monitor parcel-level vegetation trajectory (2018–2025) across valid agroforestry plots.

\* \*\*Core Technologies:\*\* Python (`GeoPandas`, `Shapely`), Google Earth Engine (Sentinel-2 Harmonized, Dynamic World), QGIS 3.x, Excel.



\---



\## 🛠️ Automated QA/QC Validation Pipeline

Incoming raw KML vector files often contain digitization errors, boundary disputes, or GPS logging inaccuracies. The automated Python script (`01\_plot\_validator.py`) inspects boundaries against 5 key rules:



1\. \*\*Topology \& Geometry Validity:\*\* Catches self-intersecting lines and twisted "figure-eight" boundaries using Shapely.

2\. \*\*Administrative Boundary Compliance:\*\* Flags coordinates lying outside the designated district bounding box.

3\. \*\*Parcel Overlap Detection:\*\* Detects boundary encroachment and shared acreage between plots.

4\. \*\*Duplicate Geometry Check:\*\* Eliminates identical records submitted under multiple IDs.

5\. \*\*Projected Area Calculation:\*\* Reprojects coordinates into \*\*UTM Zone 44N (EPSG:32644)\*\* to deliver accurate surface areas in hectares.



\### Validation Summary

\* \*\*Total Digitized Plots Evaluated:\*\* 14

\* \*\*Approved Parcels:\*\* 6 (Plots 4, 5, 6, 7, 9, 10)

\* \*\*Flagged / Rejected Parcels:\*\* 4 (Outlier boundary, twisted geometry, duplicate entry, boundary overlap)



\---



\## 🛰️ Temporal Remote Sensing \& Canopy Monitoring (2018–2025)

For all validated parcels, satellite time series were extracted to quantify agroforestry adoption and growth:



1\. \*\*Peak Monsoon NDVI Trajectory:\*\* Annual composite median NDVI (July 1 – October 31) derived from Sentinel-2 Surface Reflectance at 10 m resolution.

2\. \*\*Land Cover Proportions:\*\* Dynamic World 10 m LULC classification tracking relative shifts between tree canopy, seasonal crops, and bare soil.



!\[NDVI Greening Chart](visuals/charts/ndvi\_trend\_selected\_plots.png)



\---



\## 📊 Consolidated Results Table



| Plot ID | Area (ha) | Baseline NDVI (2018) | Current NDVI (2025) | Net NDVI Change | Primary Land Cover Shift | Status |

| :--- | :--- | :--- | :--- | :--- | :--- | :--- |

| \*\*Plot 4\*\* | 16.42 | 0.421 | 0.612 | +0.191 | Crop to Agroforestry Canopy | Verified |

| \*\*Plot 5\*\* | 4.85 | 0.380 | 0.540 | +0.160 | Bare Soil to Mixed Tree Cover | Verified |

| \*\*Plot 6\*\* | 2.91 | 0.450 | 0.510 | +0.060 | Stable Existing Tree Border | Verified |

| \*\*Plot 7\*\* | 15.10 | 0.395 | 0.589 | +0.194 | Significant Canopy Expansion | Verified |

| \*\*Plot 9\*\* | 12.05 | 0.410 | 0.495 | +0.085 | Mixed Silvo-pastoral / Crop | Verified |

| \*\*Plot 10\*\* | 7.63 | 0.365 | 0.528 | +0.163 | Young Tree Plantation Growth | Verified |



\---



\## ⚠️ Synthetic Data Disclaimer

The vector parcel boundaries included in `data/raw/MBNR\_Plots.kml` are synthetic geometries digitized manually for demonstration, testing, and portfolio purposes. They do not represent proprietary landowner data or active cadastral records in Mahabubnagar.



\---



\## 🚀 How to Replicate



1\. Clone this repository:

&#x20;  ```bash

&#x20;  git clone \[https://github.com/your-username/agroforestry-plot-monitor.git](https://github.com/your-username/agroforestry-plot-monitor.git)

&#x20;  cd agroforestry-plot-monitor

&#x20;  ```

2\. Install required packages:

&#x20;  ```bash

&#x20;  pip install -r requirements.txt

&#x20;  ```

3\. Run boundary validation:

&#x20;  ```bash

&#x20;  python scripts/01\_plot\_validator.py

&#x20;  ```

4\. Authenticate Earth Engine and generate temporal indices:

&#x20;  ```bash

&#x20;  python scripts/02\_gee\_ndvi\_timeseries.py

&#x20;  ```

