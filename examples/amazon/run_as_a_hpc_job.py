
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
sDate='20221115'
sPath = str( Path().resolve() )
iFlag_option = 1
sWorkspace_data = realpath( sPath +  '/data/amazon' )
sWorkspace_input =  str(Path(sWorkspace_data)  /  'input')
sWorkspace_output=  '/compyfs/liao313/04model/pyhexwatershed/amazon'


aMesh_type = ['mpas']
aResolution_meter = [5000]
iCase_index = 1

#generate a bash job script

sFilename = sWorkspace_output + '/' + sDate  + 'submit.bash'
ofs = open(sFilename, 'w')
sLine  = '#!/bin/bash' + '\n'
ofs.write(sLine)

sFilename_configuration_in = realpath( sPath +  '/examples/amazon/pyhexwatershed_amazon_mpas.json' )

    
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
oPyhexwatershed._create_hpc_job()
print(iCase_index)
sLine  = 'cd ' + oPyhexwatershed.sWorkspace_output + '\n'
ofs.write(sLine)
sLine  = 'sbatch submit.job' + '\n'
ofs.write(sLine)


pass

ofs.close()
os.chmod(sFilename, stat.S_IREAD | stat.S_IWRITE | stat.S_IXUSR)   
