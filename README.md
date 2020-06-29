# HexWatershed
HexWatershed_coastal is a variant version of hexwatershed, which is a hydrology model based on hexagon framework.

The HexWatershed is distributed at:

https://github.com/changliao1025/hexwatershed

# Abstarct

Spatial discretization is the cornerstone of all spatially-distributed numerical simulations including watershed hydrology. Traditional square grid spatial discretization has several limitations including inability to represent adjacency uniformly. 

# Illustration

# Citations
Liao, C., Tesfa, T., Duan, Z., & Leung, L. R. (2020). Watershed delineation on a hexagonal mesh grid. Environmental Modelling & Software, 104702.

https://www.sciencedirect.com/science/article/pii/S1364815219308278

# Acknowledgement
The research described in this paper was primarily funded by DOE INTEGRATED COASTAL MODELING (ICoM). 

# Compile
1. git clone git@github.com:changliao1025/hexwatershed.git
2. Navigate to the directory which has the CMakeLists.txt file
3. Adjust your configuration of the CMakeLists.txt
4. cmake CMakeLists.txt
5. make

# Usage
In order to run the program, you need to prepare a few input files:
1. A MPAS mesh grid
2. A DEM

# Contact
Please contact Chang Liao (chang.liao@pnnl.gov) if you have any questions.

