
import os, sys, stat
from sre_constants import IN
from pathlib import Path
from os.path import realpath
import argparse
import logging
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(format='%(asctime)s %(message)s')
logging.warning('is the time pyhexwatershed simulation started.')

from pyhexwatershed.classes.pycase import hexwatershedcase
from pyhexwatershed.pyhexwatershed_read_model_configuration_file import pyhexwatershed_read_model_configuration_file


sMesh_type = 'mpas'
iCase_index = 1
dResolution_meter=5000
sDate='20220607'
sPath = str( Path().resolve() )
iFlag_option = 1
sWorkspace_data = realpath( sPath +  '/data/susquehanna' )
sWorkspace_input =  str(Path(sWorkspace_data)  /  'input')
sWorkspace_output=  '/compyfs/liao313/04model/pyhexwatershed/susquehanna'


aMesh_type = ['hexagon', 'square','latlon','mpas']
aResolution_meter = [5000, 40000]
iCase_index = 1

#generate a bash job script

sFilename = sWorkspace_output + '/' + sDate  + 'submit.bash'
ofs = open(sFilename, 'w')
sLine  = '#!/bin/bash' + '\n'
ofs.write(sLine)
for iMesh_type in range(1, 5):
    sMesh_type = aMesh_type[iMesh_type-1]
    if sMesh_type=='hexagon':
        sFilename_configuration_in = realpath( sPath +  '/example/susquehanna/pyhexwatershed_susquehanna_hexagon.json' )
    else:
        if sMesh_type=='square':
            sFilename_configuration_in = realpath( sPath +  '/example/susquehanna/pyhexwatershed_susquehanna_square.json' )
        else:
            if sMesh_type=='latlon':
                sFilename_configuration_in = realpath( sPath +  '/example/susquehanna/pyhexwatershed_susquehanna_latlon.json' )
            else:
                sFilename_configuration_in = realpath( sPath +  '/example/susquehanna/pyhexwatershed_susquehanna_mpas.json' )

    
    if os.path.isfile(sFilename_configuration_in):
        print(sFilename_configuration_in)
    else:
        print('This configuration file does not exist: ', sFilename_configuration_in )
        exit()
    if iMesh_type != 4:
        for iResolution in range(1, 3):    
            iFlag_stream_burning_topology = 0 
            dResolution_meter = aResolution_meter[iResolution-1]
            iFlag_stream_burning_topology = 0
            iFlag_use_mesh_dem = 0
            iFlag_elevation_profile = 0
            oPyhexwatershed = pyhexwatershed_read_model_configuration_file(sFilename_configuration_in,\
                iCase_index_in=iCase_index,\
                    iFlag_stream_burning_topology_in=iFlag_stream_burning_topology,\
                        iFlag_use_mesh_dem_in=iFlag_use_mesh_dem,\
                            iFlag_elevation_profile_in=iFlag_elevation_profile,\
                     dResolution_meter_in = dResolution_meter, sDate_in= sDate, sMesh_type_in= sMesh_type)   
            oPyhexwatershed.create_hpc_job()
            oPyhexwatershed.export_config_to_json()
            print(iCase_index)

            sLine  = 'cd ' + oPyhexwatershed.sWorkspace_output + '\n'
            ofs.write(sLine)
            sLine  = 'sbatch submit.job' + '\n'
            ofs.write(sLine)

            iCase_index = iCase_index + 1

            iFlag_stream_burning_topology = 1
            oPyhexwatershed = pyhexwatershed_read_model_configuration_file(sFilename_configuration_in,\
                iCase_index_in=iCase_index,  iFlag_stream_burning_topology_in=iFlag_stream_burning_topology,\
                      iFlag_use_mesh_dem_in=iFlag_use_mesh_dem,\
                            iFlag_elevation_profile_in=iFlag_elevation_profile,\
                    dResolution_meter_in = dResolution_meter, sDate_in= sDate, sMesh_type_in= sMesh_type)   
            oPyhexwatershed.create_hpc_job()
            oPyhexwatershed.export_config_to_json()
            print(iCase_index)

            sLine  = 'cd ' + oPyhexwatershed.sWorkspace_output + '\n'
            ofs.write(sLine)
            sLine  = 'sbatch submit.job' + '\n'
            ofs.write(sLine)

            iCase_index = iCase_index + 1

            continue            
            
    else:
        #mpas mesh only has one resolution
        iFlag_stream_burning_topology = 0 
        iFlag_use_mesh_dem = 1
        iFlag_elevation_profile = 1
        oPyhexwatershed = pyhexwatershed_read_model_configuration_file(sFilename_configuration_in,\
                iCase_index_in=iCase_index,iFlag_stream_burning_topology_in=iFlag_stream_burning_topology,\
                      iFlag_use_mesh_dem_in=iFlag_use_mesh_dem,\
                            iFlag_elevation_profile_in=iFlag_elevation_profile,\
                     dResolution_meter_in = dResolution_meter, sDate_in= sDate, sMesh_type_in= sMesh_type)   
        oPyhexwatershed.create_hpc_job()
        print(iCase_index)
        sLine  = 'cd ' + oPyhexwatershed.sWorkspace_output + '\n'
        ofs.write(sLine)
        sLine  = 'sbatch submit.job' + '\n'
        ofs.write(sLine)
        iCase_index = iCase_index + 1

        iFlag_stream_burning_topology = 1 
        oPyhexwatershed = pyhexwatershed_read_model_configuration_file(sFilename_configuration_in,\
                iCase_index_in=iCase_index,iFlag_stream_burning_topology_in=iFlag_stream_burning_topology,\
                      iFlag_use_mesh_dem_in=iFlag_use_mesh_dem,\
                            iFlag_elevation_profile_in=iFlag_elevation_profile,\
                     dResolution_meter_in = dResolution_meter, sDate_in= sDate, sMesh_type_in= sMesh_type)   
        oPyhexwatershed.create_hpc_job()
        oPyhexwatershed.export_config_to_json()

        sLine  = 'cd ' + oPyhexwatershed.sWorkspace_output + '\n'
        ofs.write(sLine)
        sLine  = 'sbatch submit.job' + '\n'
        ofs.write(sLine)

        print(iCase_index)
        iCase_index = iCase_index + 1
        pass

ofs.close()
os.chmod(sFilename, stat.S_IREAD | stat.S_IWRITE | stat.S_IXUSR)   
