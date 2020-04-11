
/**
 * @file data.h
 * @author Chang Liao (chang.liao@pnnl.gov)
 * @brief The header of data I/O component source code.
 * @version 0.1
 * @date 2017-01-25
 * 
 * @copyright Copyright (c) 2019
 * 
 */
#pragma once

//50==================================================
//C header
//50==================================================
//C++ header
#include <algorithm>
#include <array>  //the small sized array
#include <fstream> //file stream
#include <iterator> //for vector and stream
#include <string> //c++ string
#include <vector> //vector
#include <exception>
#include "gdal.h"
#include "system.h"
//50==================================================
using namespace std;
//50==================================================


template <typename T>
T** create2DArray(unsigned nrows, unsigned ncols, const T& val = T())
{
   if (nrows == 0)
        throw std::invalid_argument("number of rows is 0");
   if (ncols == 0)
        throw std::invalid_argument("number of columns is 0");
   T** ptr = nullptr;
   T* pool = nullptr;
   try
   {
       ptr = new T*[nrows];  // allocate pointers (can throw here)
       pool = new T[nrows*ncols]{val};  // allocate pool (can throw here)

       // now point the row pointers to the appropriate positions in
       // the memory pool
       for (unsigned i = 0; i < nrows; ++i, pool += ncols )
           ptr[i] = pool;

       // Done.
       return ptr;
   }
   catch (std::bad_alloc& ex)
   {
       delete [] ptr; // either this is nullptr or it was allocated
       throw ex;  // memory allocation error
   }
}

template <typename T>
void delete2DArray(T** arr)
{
   delete [] arr[0];  // remove the pool
   delete [] arr;     // remove the pointers
}

class data
{
 public:
  data();
  ~data();
  //50==================================================
  //Traditional data IO
  //50==================================================
  static float * read_binary(std::string sFilename_in);
  static float ** read_binary(std::string sFilename_in,
                              long lColumn_in,
                              long lRow_in);
  static std::vector<double> read_binary_vector(std::string sFilename_in);
  static int write_binary_vector(std::string sFilename_in,
                                 vector <double> vData_in);
  //50==================================================
  //advanced data io using MPI
  //dataIO using PETSc
  //50==================================================
  //Mat Read_Binary(string filErtame,int m,int n);
  //50==================================================
 
};
