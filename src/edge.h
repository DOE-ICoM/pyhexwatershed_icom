#pragma once
#include <string>
#include <vector>
#include "global.h"
#include "vertex.h"
using namespace std;
namespace hexwatershed
{
class edge
{
     public:
      edge();

    ~edge();
    long lIndex;
    double dLength ; //map projection
    std::vector<vertex> vVertex;
    bool operator==(const edge &cEdge);
};
} // namespace hexwatershed