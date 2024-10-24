import os, sys
from osgeo import ogr, osr, gdal
from pyearth.toolbox.analysis.extract.clip_vector_by_polygon import clip_vector_by_polygon_file


sFilename_vector_in='/compyfs/liao313/04model/pyhexwatershed/arctic/pyhexwatershed20240601003/hexwatershed/mpas_flow_direction.geojson'
sFilename_polygon_in='/compyfs/liao313/04model/pyhexwatershed/arctic/pyhexwatershed20240601003/hexwatershed/mpas_flow_direction_yukon_delta.geojson'
sFilename_vector_out='/compyfs/liao313/04model/pyhexwatershed/arctic/pyhexwatershed20240601003/hexwatershed/mpas_flow_direction_yukon.geojson'

#create a polygon file using the corner points

dLon_min = -165.2
dLon_max = -163
dLat_min = 62.1
dLat_max = 63.3

aExtent = [dLon_min, dLon_max, dLat_min, dLat_max]
# Create a spatial reference object (optional, set to WGS84 here)
pSpatialRef = osr.SpatialReference()
pSpatialRef.ImportFromEPSG(4326)

# Create a new GeoJSON pDriver
pDriver = ogr.GetDriverByName("GeoJSON")

# Create a new GeoJSON pDataSource
if os.path.exists(sFilename_polygon_in):
    pDriver.DeleteDataSource(sFilename_polygon_in)

pDataSource = pDriver.CreateDataSource(sFilename_polygon_in)

# Create a new empty pLayer
pLayer = pDataSource.CreateLayer("delta", pSpatialRef, ogr.wkbPolygon)

# Create a new polygon geometry
ring = ogr.Geometry(ogr.wkbLinearRing)
ring.AddPoint(dLon_min, dLat_min)
ring.AddPoint(dLon_max, dLat_min)
ring.AddPoint(dLon_max, dLat_max)
ring.AddPoint(dLon_min, dLat_max)
ring.AddPoint(dLon_min, dLat_min)  # Close the ring

pPolygon = ogr.Geometry(ogr.wkbPolygon)
pPolygon.AddGeometry(ring)

# Create a new pFeature
pFeature = ogr.Feature(pLayer.GetLayerDefn())
pFeature.SetGeometry(pPolygon)
# Add the pFeature to the pLayer
pLayer.CreateFeature(pFeature)
# Clean up

pLayer = None
pDataSource = None
pFeature = None


clip_vector_by_polygon_file(sFilename_vector_in, sFilename_polygon_in, sFilename_vector_out)
print('The vector file is clipped by the polygon file!')




