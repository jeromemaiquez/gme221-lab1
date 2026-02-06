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