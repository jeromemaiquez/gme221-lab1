# Description:
# This script establishes a connection to a PostGIS-enabled PostgreSQL database
# and verifies access by querying a spatial table.

import geopandas as gpd
from sqlalchemy import create_engine

# Database connection parameters
host = "localhost"
port = "5432"
dbname = "gme221"
user = "postgres"
password = "postgres"

# Create the connection string
conn_str = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"

# Create the database engine
engine = create_engine(conn_str)

# SQL queries to load the parcel and landuse layers from the PostGIS database
sql_parcel = """
SELECT parcel_pin, geom
FROM public.parcel
"""
sql_landuse = """
SELECT name, geom
FROM public.landuse
"""

# Load the data into GeoDataFrames
parcel = gpd.read_postgis(sql_parcel, engine, geom_col="geom")
landuse = gpd.read_postgis(sql_landuse, engine, geom_col="geom")
parcel = parcel.to_crs(epsg=3395)
landuse = landuse.to_crs(epsg=3395)

# SQL query for spatial overlay in PostGIS
sql_overlay = """
WITH overlay AS (
    SELECT
        p.parcel_pin,
        l.name,
        ST_Intersection(p.geom, l.geom) AS intersect_geom
    FROM public.parcel p
    JOIN public.landuse l
        ON ST_Intersects(p.geom, l.geom)
)
SELECT
    parcel_pin,
    name,
    ST_Transform(intersect_geom, 3395) AS intersect_geom,
    SUM(ST_Area(ST_Transform(intersect_geom, 3395))) AS landuse_area
FROM overlay
GROUP BY parcel_pin, name, intersect_geom
"""

# Fetch overlay results into GeoDataFrame and check results
overlay_result = gpd.read_postgis(sql_overlay, engine, geom_col="intersect_geom")
# print(overlay_result.head(10))

# Calculate total area of each parcel
parcel['total_area'] = parcel.geometry.area

# Merge overlay result with parcels to get total parcel area
overlay_result = overlay_result.merge(parcel[["parcel_pin", "total_area"]], on="parcel_pin")

# Calculate the percentage of each landuse type within each parcel
overlay_result["percentage"] = round((overlay_result["landuse_area"] / overlay_result["total_area"]) * 100, 2)

# Ensure the correct geometry is set
overlay_result = overlay_result.set_geometry("intersect_geom")

# Save the result to the PostGIS database as a new table
overlay_result.to_postgis("parcel_landuse_percentage", engine, if_exists="replace", index=True)