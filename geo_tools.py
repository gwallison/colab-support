# -*- coding: utf-8 -*-
"""
Created on Sun Nov  6 17:01:07 2022

@author: Gary
"""

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

final_crs = 4326 # WGS84
proj_crs = 3857 # convert to this when calculating distances
def_buffer = 1609.34 # one mile



# shapefile names
#district_fn = r"C:\MyDocs\OpenFF\data\external_refs\shape_files\schools\School_District_Composites_SY_2020-21_TL_21.zip"

def make_as_well_gdf(in_df,latName='bgLatitude',lonName='bgLongitude',
                in_crs=final_crs):
    # produce a gdf grouped by api10 (that is, by wells)
    in_df['api10'] = in_df.APINumber.str[:10]
    gb = in_df.groupby('api10',as_index=False)[[latName,lonName]].first()
    gdf =  gpd.GeoDataFrame(gb, geometry= gpd.points_from_xy(gb[lonName], 
                                                             gb[latName],
                                                             crs=final_crs))
    return gdf
    
def find_schools_near_well_set(well_gdf,buffer_m=def_buffer):
    # return a df with all schools within bufferrange of point
    return pd.DataFrame()

def find_wells_near_point(lat,lon,wellgdf,crs=final_crs,name='test',
                          buffer_m=def_buffer, bbnum=0.25):
    # use bounding box to shrink number of wells to check
    t = wellgdf.cx[lon-bbnum:lon+bbnum, lat-bbnum:lat+bbnum]
    t = t.to_crs(proj_crs)
    s = gpd.GeoSeries([Point(lon,lat)],crs=crs)
    s = s.to_crs(proj_crs)
    s = gpd.GeoDataFrame(geometry=s.geometry.buffer(buffer_m))
    s['name'] = name
    tmp = gpd.sjoin(t,s,how='inner',predicate='within')
    return tmp.api10.tolist()

# if __name__ == '__main__':
    #num_wells_per_district()
