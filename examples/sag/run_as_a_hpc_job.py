
import os, sys, stat
from sre_constants import IN
from pathlib import Path
from os.path import realpath
import argparse
import cartopy.crs as ccrs

from pyhexwatershed.classes.pycase import hexwatershedcase
from pyhexwatershed.pyhexwatershed_read_model_configuration_file import pyhexwatershed_read_model_configuration_file


iFlag_create_job=1
iFlag_visualization =0

sMesh_type = 'mpas'
iCase_index = 1
dResolution_meter=5000
sDate='20221115'

aExtent_full = [-150.1,-146.3, 64.8,70.7]
dLongitude_outlet_degree=-148.36105
dLatitude_outlet_degree=69.29553
pProjection_map = ccrs.Orthographic(central_longitude=  dLongitude_outlet_degree, \
        central_latitude= dLatitude_outlet_degree, globe=None)

sPath = str( Path().resolve() )
iFlag_option = 1
sWorkspace_data = realpath( sPath +  '/data/sag' )
sWorkspace_input =  str(Path(sWorkspace_data)  /  'input')
sWorkspace_output=  '/compyfs/liao313/04model/pyhexwatershed/sag'




#generate a bash job script
if iFlag_create_job ==1:
    sFilename = sWorkspace_output + '/' + sDate  + 'submit.bash'
    ofs = open(sFilename, 'w')
    sLine  = '#!/bin/bash' + '\n'
    ofs.write(sLine)

sFilename_configuration_in = realpath( sPath +  '/examples/sag/pyhexwatershed_sag_mpas.json' )

    
if os.path.isfile(sFilename_configuration_in):
    print(sFilename_configuration_in)
else:
    print('This configuration file does not exist: ', sFilename_configuration_in )
    exit()
    
#mpas mesh only has one resolution
iFlag_stream_burning_topology = 1 
iFlag_use_mesh_dem = 1
iFlag_elevation_profile = 1
oPyhexwatershed = pyhexwatershed_read_model_configuration_file(sFilename_configuration_in,\
                iCase_index_in=iCase_index,iFlag_stream_burning_topology_in=iFlag_stream_burning_topology,\
                iFlag_use_mesh_dem_in=iFlag_use_mesh_dem,\
                iFlag_elevation_profile_in=iFlag_elevation_profile,\
                dResolution_meter_in = dResolution_meter, sDate_in= sDate, sMesh_type_in= sMesh_type)   
if iFlag_create_job ==1:
    oPyhexwatershed._create_hpc_job()
    print(iCase_index)
    sLine  = 'cd ' + oPyhexwatershed.sWorkspace_output + '\n'
    ofs.write(sLine)
    sLine  = 'sbatch submit.job' + '\n'
    ofs.write(sLine)


if iFlag_visualization == 1:
    sFilename = os.path.join(  oPyhexwatershed.sWorkspace_output_hexwatershed, 'surface_elevation.png' )
    oPyhexwatershed._plot(sFilename, iFlag_type_in =1, sVariable_in = 'elevation', aExtent_in=aExtent_full,pProjection_map_in=pProjection_map)     
    sFilename = os.path.join(  oPyhexwatershed.sWorkspace_output_hexwatershed, 'surface_slope.png' )        
    oPyhexwatershed._plot(sFilename, iFlag_type_in =1, sVariable_in = 'slope', aExtent_in=aExtent_full,pProjection_map_in=pProjection_map) 
    sFilename = os.path.join(  oPyhexwatershed.sWorkspace_output_hexwatershed, 'drainage_area.png' )
    oPyhexwatershed._plot(sFilename, iFlag_type_in =1, sVariable_in = 'drainagearea', aExtent_in=aExtent_full,pProjection_map_in=pProjection_map)   
    sFilename = os.path.join(  oPyhexwatershed.sWorkspace_output_hexwatershed, 'flow_direction.png' )
    oPyhexwatershed._plot(sFilename, iFlag_type_in =2, sVariable_in = 'flow_direction', aExtent_in=aExtent_full,pProjection_map_in=pProjection_map) 
    sFilename = os.path.join(  oPyhexwatershed.sWorkspace_output_hexwatershed, 'flow_direction_w_mesh.png' )
    oPyhexwatershed._plot(sFilename, iFlag_type_in =3, sVariable_in = 'flow_direction', aExtent_in=aExtent_full,pProjection_map_in=pProjection_map)    
    sFilename = os.path.join(  oPyhexwatershed.sWorkspace_output_hexwatershed, 'flow_direction_w_observation.png' )
    oPyhexwatershed._plot(sFilename, iFlag_type_in =4, sVariable_in = 'flow_direction', aExtent_in=aExtent_full,pProjection_map_in=pProjection_map)  
    sFilename = os.path.join(  oPyhexwatershed.sWorkspace_output_hexwatershed, 'travel_distance.png' )
    oPyhexwatershed._plot(sFilename, iFlag_type_in =1, sVariable_in = 'distance_to_outlet', aExtent_in=aExtent_full, pProjection_map_in=pProjection_map)    


if iFlag_create_job ==1:
    ofs.close()
    os.chmod(sFilename, stat.S_IREAD | stat.S_IWRITE | stat.S_IXUSR)   
