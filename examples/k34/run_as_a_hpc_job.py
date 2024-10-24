
import os, stat

from pathlib import Path
from os.path import realpath
from shutil import copy2
import cartopy.crs as ccrs

from pyhexwatershed.configuration.read_configuration_file import pyhexwatershed_read_configuration_file


iFlag_create_job = 0
iFlag_visualization = 1

sMesh_type = 'square'
iCase_index = 1
dResolution_meter=5000
sDate='20240101'

aExtent_full = [-150.1,-146.3, 67.8,70.7]
dLongitude_outlet_degree=-148.36105
dLatitude_outlet_degree=69.29553
pProjection_map = ccrs.Orthographic(central_longitude=  dLongitude_outlet_degree, \
        central_latitude= dLatitude_outlet_degree, globe=None)

sPath = str( Path().resolve() )
iFlag_option = 1
sWorkspace_data = realpath( sPath +  '/data/sag' )
sWorkspace_input =  str(Path(sWorkspace_data)  /  'input')
sWorkspace_output=  '/compyfs/liao313/04model/pyhexwatershed/k34'


#generate a bash job script
if iFlag_create_job ==1:
    sFilename = sWorkspace_output + '/' + sDate  + 'submit.bash'
    ofs = open(sFilename, 'w')
    sLine  = '#!/bin/bash' + '\n'
    ofs.write(sLine)

sFilename_configuration_in = realpath( sWorkspace_input +  '/pyhexwatershed_sag_mpas.json' )



if os.path.isfile(sFilename_configuration_in):
    print(sFilename_configuration_in)
else:
    print('This configuration file does not exist: ', sFilename_configuration_in )
    exit()


iFlag_stream_burning_topology = 0
iFlag_use_mesh_dem = 0
iFlag_elevation_profile = 0
oPyhexwatershed = pyhexwatershed_read_configuration_file(sFilename_configuration_in,
                    iCase_index_in=iCase_index,iFlag_stream_burning_topology_in=iFlag_stream_burning_topology,
                    iFlag_use_mesh_dem_in=iFlag_use_mesh_dem,
                    iFlag_elevation_profile_in=iFlag_elevation_profile,
                    sDate_in= sDate, sMesh_type_in= sMesh_type)

sWorkspace_output_dummy = oPyhexwatershed.sWorkspace_output
sWorkspace_output_dummy = oPyhexwatershed.sWorkspace_output
#copy to the output directory
sFilename_configuration_copy= os.path.join( sWorkspace_output_dummy, 'pyhexwatershed_configuration_copy.json' )
#copy the configuration file to the output directory
copy2(sFilename_configuration_in, sFilename_configuration_copy)
#also copy the basin configuration file to the output directory
sFilename_configuration_basins_copy = os.path.join( sWorkspace_output_dummy, 'pyflowline_configuration_basins_copy.json' )
sFilename_configuration = sFilename_configuration_copy

oPyhexwatershed = pyhexwatershed_read_configuration_file(sFilename_configuration,
                iCase_index_in=iCase_index,iFlag_stream_burning_topology_in=iFlag_stream_burning_topology,
                iFlag_use_mesh_dem_in=iFlag_use_mesh_dem,
                iFlag_elevation_profile_in=iFlag_elevation_profile,
                dResolution_meter_in = dResolution_meter, sDate_in= sDate, sMesh_type_in= sMesh_type)

if iFlag_create_job ==1:
    oPyhexwatershed._pyhexwatershed_create_hpc_job()
    print(iCase_index)
    sLine  = 'cd ' + oPyhexwatershed.sWorkspace_output + '\n'
    ofs.write(sLine)
    sLine  = 'sbatch submit.job' + '\n'
    ofs.write(sLine)
else:
    oPyhexwatershed.pyhexwatershed_export()
    pass


if iFlag_visualization == 1:

    sFilename = os.path.join(  oPyhexwatershed.sWorkspace_output_hexwatershed, 'priority_flood.gif' )
    #oPyhexwatershed._animate(sFilename, iFlag_type_in =1,iFigwidth_in=5, iFigheight_in=7, pProjection_map_in=pProjection_map)
    sFilename = os.path.join(  oPyhexwatershed.sWorkspace_output_hexwatershed, 'priority_flood_track.gif' )
    #oPyhexwatershed._animate(sFilename, iFlag_type_in =2,iFigwidth_in=5, iFigheight_in=7, pProjection_map_in=pProjection_map)
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
