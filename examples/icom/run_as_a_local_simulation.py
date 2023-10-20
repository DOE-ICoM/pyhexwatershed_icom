
import os, sys, stat

from pathlib import Path
from os.path import realpath
import argparse


from pyhexwatershed.classes.pycase import hexwatershedcase
from pyhexwatershed.pyhexwatershed_read_model_configuration_file import pyhexwatershed_read_model_configuration_file


sMesh_type = 'mpas'
iCase_index = 1
dResolution_meter=5000
sDate='20220607'
sPath = str( Path().resolve() )
iFlag_option = 1
sWorkspace_data = realpath( sPath +  '/data/icom' )
sWorkspace_input =  str(Path(sWorkspace_data)  /  'input')
sWorkspace_output=  '/compyfs/liao313/04model/pyhexwatershed/icom'

#generate a bash job script

sFilename = sWorkspace_output + '/' + sDate  + 'submit.bash'
ofs = open(sFilename, 'w')
sLine  = '#!/bin/bash' + '\n'
ofs.write(sLine)

sFilename_configuration_in = realpath( sPath +  '/examples/icom/pyhexwatershed_icom_mpas_dam.json' )

    
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

if oPyhexwatershed.iFlag_global==1:
    #global simulation
    #we can only suport MPAS/latlon mesh at global scale right now
    pass
else:
    #regional simulation
    if oPyhexwatershed.iFlag_multiple_outlet == 1:
        oPyhexwatershed.setup()       
        oPyhexwatershed.run_pyflowline()        
        oPyhexwatershed.pPyFlowline.export()        
        oPyhexwatershed.export_config_to_json()
        oPyhexwatershed.run_hexwatershed()        
        oPyhexwatershed.export()
        pass
    else:
        #single basin example       
        
        oPyhexwatershed.setup()       
        oPyhexwatershed.run_pyflowline()        
        oPyhexwatershed.pPyFlowline.export()        
        oPyhexwatershed.export_config_to_json()
        oPyhexwatershed.run_hexwatershed()
        oPyhexwatershed.analyze()
        oPyhexwatershed.export()
        pass
    pass   


pass

ofs.close()
os.chmod(sFilename, stat.S_IREAD | stat.S_IWRITE | stat.S_IXUSR)   
