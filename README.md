# GmE 221 - Laboratory Exercise 1

## Overview
This laboratory sets up a spatial analysis environment using Python and PostGIS and performs a parcel-landuse overlay analysis.

## Environment Setup
- Python 3.x
- PostgreSQL with PostGIS
- GeoPandas, SQLAlchemy, psycopg2

## How to Run
1. Activate the virtual environment
2. Run `main.py` to test the database connection
3. Run `overlay.py` to compute landuse percentages

## Outputs
- PostGIS table: `parcel_landuse_percentage`
- Visualization in QGIS

## Reflections - Part D
The successful execution of `main.py` shows that Python can be used to connect to a PostGIS-enabled database and access spatial data. This is done by constructing a query in Python and sending this query to PostGIS, upon which a table is returned (containing the rows and columns satisfying this query). Down the line, these queries will also contain GIS algorithms implemented in PostGIS. This means that Python can be used as the "orchestrator" or "manager", while PostGIS can be used as the powerful "engine" running the spatial computations themselves in the backend. In a way, Python is used to operationalize _spatial intent_ and manage _computational execution_ performed by PostGIS.

## Reflection - Part E
The successful execution of `overlay.py` hints at the real power of the Python-PostGIS connection: This connection not only allows access to data stored in a PostGIS-enabled database, but also execution of spatial algorithms. Once again, this computation was spelled out using Python (by writing a SQL query as a Python string), and then sent to the PostGIS "engine" for execution. 

## Reflection - Part F
In this exercise, QGIS was used not to run the algorithms themselves (which it may do so slowly at large scales), but only to view the results of the computation performed by PostGIS. This already represents a simple tech stack GIS professionals can use to clearly and quickly translate spatial intent to computational execution: orchestrating the workflow in Python, running the heavy GIS algorithms in PostGIS, and post-processing checking in QGIS.

At first, it was puzzling to see parcel-landuse intersections that overlapped with each other. This is because I was expecting the landuse layer itself to have no overlaps, i.e. that each location only had 1 landuse type. However, upon checking the landuse layer itself (by adding it to QGIS directly from the database), I was able to verify that certain locations had more than one land use. For example, the western portion of the study area was a residential area, but also part of the "buffer area". With this information, I'd say there weren't any parcels with unexpected values.

When calculating distances and areas, it is important to ensure the correct CRS, adequate geometric quality, and the appropriate scale. Areas and distances are only meaningful with a geometric/planar CRS (not the default CRS of EPSG:4326, which is geographic and assumes a 3D Earth). Moreover, the quality of the geometry digitization matters. Oversimplified geometries might have larger or smaller areas than expected. The quality of digitization is related to the scale at which the digitization is performed. In choosing the appropriate scale, a tradeoff exists between accuracy and file size/storage. The correct scale balances these two in relation to the study purpose.