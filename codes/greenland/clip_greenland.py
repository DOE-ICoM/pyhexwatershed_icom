import os, sys
from osgeo import ogr, osr, gdal
import cartopy.crs as ccrs
from pyearth.toolbox.analysis.extract.clip_vector_by_polygon import clip_vector_by_polygon_file
from pyearth.visual.map.vector.map_vector_polyline_data import map_vector_polyline_data

sFilename_vector_in='/compyfs/liao313/04model/pyhexwatershed/arctic/pyhexwatershed20240601004/hexwatershed/mpas_flow_direction.geojson'
sFilename_polygon_in='/people/liao313/data/hexwatershed/greenland/greenland.geojson'
sFilename_vector_out='/compyfs/liao313/04model/pyhexwatershed/arctic/pyhexwatershed20240601004/hexwatershed/mpas_flow_direction_greenland.geojson'

#create a polygon file using the corner points

clip_vector_by_polygon_file(sFilename_vector_in, sFilename_polygon_in, sFilename_vector_out)
print('The vector file is clipped by the polygon file!')


sTitle = 'Flow direction'
pProjection_data = ccrs.Geodetic()

sFilename_output_in = '/compyfs/liao313/04model/pyhexwatershed/arctic/pyhexwatershed20240601004/hexwatershed/flow_direction_greenland.png'
pProjection_map = ccrs.Orthographic(central_longitude=-41,  central_latitude=74, globe=None)
map_vector_polyline_data(1, sFilename_vector_out,
                             sFilename_output_in = sFilename_output_in,
                             iFlag_thickness_in= 1 ,
                             iDPI_in=300,
                             iFlag_zebra_in=1,
                             iSize_x_in=12,
                             iSize_y_in=12,
                             sTitle_in=sTitle,
                             sField_thickness_in = 'drainage_area', #use drainage area to scale the thickness
                             pProjection_map_in = pProjection_map,
                             pProjection_data_in = pProjection_data)




