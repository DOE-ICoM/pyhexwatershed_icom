
import os,  stat

from pathlib import Path
from os.path import realpath

import cartopy.crs as ccrs

import logging
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(format='%(asctime)s %(message)s')
logging.warning('is the time pyhexwatershed simulation started.')

from pyhexwatershed.classes.pycase import hexwatershedcase
from pyhexwatershed.pyhexwatershed_read_model_configuration_file import pyhexwatershed_read_model_configuration_file


sMesh_type = 'mpas'
iCase_index = 2
dResolution_meter=5000
iFlag_create_job=0
iFlag_visualization =1
aExtent_full = None
dLongitude_outlet_degree=-117
dLatitude_outlet_degree=42
pProjection_map = None
sDate='20230701'
sPath = str( Path().resolve() )
iFlag_option = 1
sWorkspace_data = realpath( sPath +  '/data/yangtze' )
sWorkspace_input =  str(Path(sWorkspace_data)  /  'input')
sWorkspace_output=  '/compyfs/liao313/04model/pyhexwatershed/yangtze'


aMesh_type = ['mpas']
aResolution_meter = [5000]

if os.path.isdir(sWorkspace_output):
    pass
else:   
    os.makedirs(sWorkspace_output, exist_ok=True)

#generate a bash job script
if iFlag_create_job ==1:
    sFilename = sWorkspace_output + '/' + sDate  + 'submit.bash'
    ofs = open(sFilename, 'w')
    sLine  = '#!/bin/bash' + '\n'
    ofs.write(sLine)

sFilename_configuration_in = realpath( sPath +  '/examples/yangtze/pyhexwatershed_yangtze_mpas.json' )

    
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

#120.24780,31.93805,120.24780,31.93805
119.67564,32.21362

oPyhexwatershed.pPyFlowline.aBasin[0].dLongitude_outlet_degree=119.67564
oPyhexwatershed.pPyFlowline.aBasin[0].dLatitude_outlet_degree=32.21362

if iFlag_create_job ==1:
    oPyhexwatershed._create_hpc_job()
    print(iCase_index)
    sLine  = 'cd ' + oPyhexwatershed.sWorkspace_output + '\n'
    ofs.write(sLine)
    sLine  = 'sbatch submit.job' + '\n'
    ofs.write(sLine)


if iFlag_visualization == 1:
    pBasin_hexwatershed = oPyhexwatershed.aBasin[0]
    sWorkspace_output_basin = pBasin_hexwatershed.sWorkspace_output_basin

    #polyline
    sFilename = os.path.join( sWorkspace_output_basin, 'flow_direction.png' )
    #oPyhexwatershed.plot( sVariable_in = 'flow_direction', sFilename_output_in = sFilename)

    #polygon


    
    sFilename = os.path.join(  sWorkspace_output_basin, 'surface_elevation.png' )    
    #oPyhexwatershed.plot( sVariable_in = 'elevation', sFilename_output_in = sFilename)     

    sFilename = os.path.join(  sWorkspace_output_basin, 'surface_slope.png' )        
    #oPyhexwatershed.plot( sVariable_in = 'slope', sFilename_output_in = sFilename)
    
    sFilename = os.path.join( sWorkspace_output_basin, 'drainage_area.png' )
    #oPyhexwatershed.plot( sVariable_in = 'drainagearea',  sFilename_output_in = sFilename)
    
    sFilename = os.path.join(  sWorkspace_output_basin, 'travel_distance.png' )
    #oPyhexwatershed.plot( sVariable_in = 'distance_to_outlet', sFilename_output_in = sFilename)
    #mixed
    sFilename = os.path.join( sWorkspace_output_basin, 'flow_direction_w_mesh.pdf' )
    oPyhexwatershed.plot( sVariable_in = 'flow_direction_with_mesh', sFilename_output_in = sFilename)  
    
    sFilename = os.path.join(  sWorkspace_output_basin, 'flow_direction_w_observation.png' )
    #oPyhexwatershed.plot( sVariable_in = 'flow_direction',  sFilename_output_in = sFilename)
    
    



if iFlag_create_job ==1:
    ofs.close()
    os.chmod(sFilename, stat.S_IREAD | stat.S_IWRITE | stat.S_IXUSR)   
