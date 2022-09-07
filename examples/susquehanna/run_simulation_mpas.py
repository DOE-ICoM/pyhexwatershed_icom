
import os, sys, stat
from pathlib import Path
from os.path import realpath

from pyhexwatershed.pyhexwatershed_read_model_configuration_file import pyhexwatershed_read_model_configuration_file

#===========================
#setup workspace path
#===========================
sPath_parent = str(Path(__file__).parents[2]) # data is located two dir's up
sPath_data = realpath( sPath_parent +  '/data/susquehanna' )
sWorkspace_input =  str(Path(sPath_data)  /  'input')
sWorkspace_output = '/compyfs/liao313/04model/pyhexwatershed/susquehanna'

#===================================
#you need to update this file based on your own case study
#===================================
sFilename_configuration_in = realpath( sPath_parent +  '/examples/susquehanna/pyhexwatershed_susquehanna_mpas.json' )
if os.path.isfile(sFilename_configuration_in):
    pass
else:
    print('This configuration does not exist: ', sFilename_configuration_in )


#===========================
#setup case information
#===========================
iFlag_create_job=1
iFlag_visualization =0 
iCase_index = 13
sMesh_type = 'mpas'
sDate='20220901'

#===================================
#setup output and HPC job 
#===================================
if iFlag_create_job ==1:
    sSlurm = 'short'
    sFilename = sWorkspace_output + '/' + sMesh_type + '.bash'
    ofs = open(sFilename, 'w')
    sLine  = '#!/bin/bash' + '\n'
    ofs.write(sLine)

#===================================
#visualization spatial extent
#===================================
aExtent_full = [-78.5,-75.5, 39.2,42.5]
aExtent_meander = [-76.5,-76.2, 41.6,41.9] #meander
aExtent_braided = [-77.3,-76.5, 40.2,41.0] #braided
aExtent_confluence = [-77.3,-76.5, 40.2,41.0] #confluence
aExtent_outlet = [-76.0,-76.5, 39.5,40.0] #outlet
aExtent_dam = [-75.75,-76.15, 42.1,42.5] #dam  

    
dResolution_meter = 5000
iFlag_use_mesh_dem = 1
iFlag_elevation_profile = 1
#===================================
#topology turn off
#===================================
iFlag_stream_burning_topology = 0

oPyhexwatershed = pyhexwatershed_read_model_configuration_file(sFilename_configuration_in,\
    iCase_index_in=iCase_index,\
        iFlag_stream_burning_topology_in=iFlag_stream_burning_topology,\
            iFlag_use_mesh_dem_in=iFlag_use_mesh_dem,\
                iFlag_elevation_profile_in=iFlag_elevation_profile,\
         dResolution_meter_in = dResolution_meter, sDate_in= sDate, sMesh_type_in= sMesh_type)   

if iFlag_create_job ==1:
    oPyhexwatershed._create_hpc_job()   
    sLine  = 'cd ' + oPyhexwatershed.sWorkspace_output + '\n'
    ofs.write(sLine)
    sLine  = 'sbatch submit.job' + '\n'
    ofs.write(sLine)

iCase_index = iCase_index + 1
#===================================
#topology turn on
#===================================
iFlag_stream_burning_topology = 1
oPyhexwatershed = pyhexwatershed_read_model_configuration_file(sFilename_configuration_in,\
    iCase_index_in=iCase_index,  iFlag_stream_burning_topology_in=iFlag_stream_burning_topology,\
          iFlag_use_mesh_dem_in=iFlag_use_mesh_dem,\
                iFlag_elevation_profile_in=iFlag_elevation_profile,\
        dResolution_meter_in = dResolution_meter, sDate_in= sDate, sMesh_type_in= sMesh_type)   

if iFlag_create_job ==1:
    oPyhexwatershed._create_hpc_job()   
    sLine  = 'cd ' + oPyhexwatershed.sWorkspace_output + '\n'
    ofs.write(sLine)
    sLine  = 'sbatch submit.job' + '\n'
    ofs.write(sLine)
iCase_index = iCase_index + 1
          
              

if iFlag_create_job ==1:
    ofs.close()
    os.chmod(sFilename, stat.S_IREAD | stat.S_IWRITE | stat.S_IXUSR) 
