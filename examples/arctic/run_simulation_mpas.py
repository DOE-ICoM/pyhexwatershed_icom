
import os, sys, stat

from pathlib import Path
from os.path import realpath
from shutil import copy2
import cartopy.crs as ccrs

from pyhexwatershed.classes.pycase import hexwatershedcase
from pyhexwatershed.configuration.read_configuration_file import pyhexwatershed_read_configuration_file
from pyhexwatershed.configuration.change_json_key_value import change_json_key_value

iFlag_create_job = 0
iFlag_visualization = 1
iCase_index = 4
sMesh_type = 'mpas'

dResolution_meter=5000
sDate='20240601'

sPath = str( Path().resolve() )
iFlag_option = 1
sWorkspace_data = realpath( sPath +  '/data/arctic' )
sWorkspace_input =  str(Path(sWorkspace_data)  /  'input')
sWorkspace_output=  '/compyfs/liao313/04model/pyhexwatershed/arctic'

if os.path.exists(sWorkspace_output) == False:
    os.makedirs(sWorkspace_output)

#generate a bash job script
if iFlag_create_job ==1:
    sFilename = sWorkspace_output + '/' + sDate  + 'submit.bash'
    ofs = open(sFilename, 'w')
    sLine  = '#!/bin/bash' + '\n'
    ofs.write(sLine)

sFilename_configuration_in = realpath( sPath +  '/data/arctic/input/pyhexwatershed_arctic_mpas_icom2.json' )


if os.path.isfile(sFilename_configuration_in):
    print(sFilename_configuration_in)
else:
    print('This configuration file does not exist: ', sFilename_configuration_in )
    exit()

#mpas mesh only has one resolution
iFlag_stream_burning_topology = 1
iFlag_use_mesh_dem = 1
iFlag_elevation_profile = 1

#we want to copy the example configuration file to the output directory
sFilename_configuration_copy= os.path.join( sWorkspace_output, 'pyhexwatershed_configuration_copy.json' )
copy2(sFilename_configuration_in, sFilename_configuration_copy)
sFilename_configuration = sFilename_configuration_copy

change_json_key_value(sFilename_configuration, 'sWorkspace_output', sWorkspace_output)



oPyhexwatershed = pyhexwatershed_read_configuration_file(sFilename_configuration,
                iCase_index_in=iCase_index,iFlag_stream_burning_topology_in=iFlag_stream_burning_topology,
                iFlag_use_mesh_dem_in=iFlag_use_mesh_dem,
                iFlag_elevation_profile_in=iFlag_elevation_profile,
                dResolution_meter_in = dResolution_meter, sDate_in= sDate, sMesh_type_in= sMesh_type)

oPyhexwatershed.iFlag_global = 1

if iFlag_create_job ==1:
    oPyhexwatershed._pyhexwatershed_create_hpc_job()
    print(iCase_index)
    sLine  = 'cd ' + oPyhexwatershed.sWorkspace_output + '\n'
    ofs.write(sLine)
    sLine  = 'sbatch submit.job' + '\n'
    ofs.write(sLine)

if iFlag_visualization == 1:

    pProjection_map = ccrs.Orthographic(central_longitude=0,  central_latitude=90, globe=None)
    pProjection_data = ccrs.Geodetic()


    #sFilename = os.path.join(  oPyhexwatershed.sWorkspace_output_hexwatershed, 'surface_elevation.png' )
    #oPyhexwatershed.plot(sFilename, iFlag_type_in =1, sVariable_in = 'elevation',
    #                  pProjection_map_in = pProjection_map,
    #                    pProjection_data_in=pProjection_data)


    sFilename = os.path.join(  oPyhexwatershed.sWorkspace_output_hexwatershed, 'flow_direction.png')
    oPyhexwatershed.plot(iFlag_type_in =2, sFilename_output_in = sFilename,
                         sVariable_in = 'flow_direction',
                         iDPI_in = 600,
                         iFigwidth_in=18,
                         iFigheight_in=18,
                         pProjection_map_in = pProjection_map,
                         pProjection_data_in=pProjection_data)

    aExtent_zoom = [-74.0,-10.0, 59,84]
    pProjection_map = ccrs.Orthographic(central_longitude=-41,  central_latitude=74, globe=None)

    sFilename = os.path.join(  oPyhexwatershed.sWorkspace_output_hexwatershed, 'flow_direction_greenland.png')
    oPyhexwatershed.plot(iFlag_type_in =2, sFilename_output_in = sFilename,
                         sVariable_in = 'flow_direction',
                         iDPI_in = 600,
                          iFigwidth_in=18,
                        iFigheight_in=18,
                        aExtent_in= aExtent_zoom,
                      pProjection_map_in = pProjection_map,
                        pProjection_data_in=pProjection_data)

    #sFilename = os.path.join(  oPyhexwatershed.sWorkspace_output_hexwatershed, 'flow_direction_w_mesh.png' )
    #oPyhexwatershed.plot(sFilename, iFlag_type_in =3, sVariable_in = 'flow_direction', iFlag_arctic_in=1,
    #                  pProjection_map_in = pProjection_map,
    #                    pProjection_data_in=pProjection_data)



if iFlag_create_job ==1:
    ofs.close()
    os.chmod(sFilename, stat.S_IREAD | stat.S_IWRITE | stat.S_IXUSR)
