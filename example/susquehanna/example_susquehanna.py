
import os, sys
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
            dResolution_meter = aResolution_meter[iResolution-1]
            oPyhexwatershed = pyhexwatershed_read_model_configuration_file(sFilename_configuration_in,\
                iCase_index_in=iCase_index, dResolution_meter_in = dResolution_meter, sDate_in= sDate, sMesh_type_in= sMesh_type)   
            oPyhexwatershed.create_hpc_job()
            iCase_index = iCase_index + 1
            continue            
            
    else:
        #mpas mesh only has one resolution
        oPyhexwatershed = pyhexwatershed_read_model_configuration_file(sFilename_configuration_in,\
                iCase_index_in=iCase_index, dResolution_meter_in = dResolution_meter, sDate_in= sDate, sMesh_type_in= sMesh_type)   
        oPyhexwatershed.create_hpc_job()
        iCase_index = iCase_index + 1
        pass
