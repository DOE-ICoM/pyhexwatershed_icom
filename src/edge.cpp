#include "edge.h"
namespace hexwatershed
{

edge::edge()
{
    lIndex = 0;
   dLength = 0;
}
edge::~edge()
{
}

bool edge::operator==(const edge &cEdge)
{
    if (this->vVertex == cEdge.vVertex )
    {
        return true;
    }
    else
    {
        return false;
    }
}
} // namespace hexwatershed