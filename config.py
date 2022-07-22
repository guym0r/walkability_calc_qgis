ROADS_BUFFER_DISTANCE = 10
ROADS_BUFFER_DIFFRENCE = 7
DEBUG = True
EXTENT_ACCUARY = 4
EXTENT_ZERO_FILL = 9
HEATMAP_RADIUS_SIZE = 600
DEBUG_LAYER_PREFIX = "DEBUG_" # TODO use it 
SIDEWALK_RASTERIZE_BURN = 1
SHADES_RASTERIZE_BURN = 100
SHADES_SIDEWALKS_RASTERIZE_BURN = 1
TREE_BUFFER = 1

#zonal statistics consts
ZS_SUM = 1
ZS_MEAN = 2



#WALK_CALC_EXPRESSION = '0.2 *(pois_mean - minimum(pois_mean)) / (maximum(pois_mean) - minimum(pois_mean))  + 0.2 *(tran_mean - minimum(tran_mean))/( maximum(tran_mean) - minimum(tran_mean)) + 0.6 *( shade_sum - minimum(shade_sum)) / ( maximum(shade_sum) - minimum(shade_sum))'

#WALK_CALC_EXPRESSION = '0.2 *("poi_mean" - min("poi_mean")) / (max("poi_mean") - min("poi_mean")) + 0.2 *("tr_mean" - min("tr_mean"))/( max("tr_mean") - min("tr_mean")) + 0.6 *("shade_sum" - min("shade_sum")) / ( max("shade_sum") - min("shade_sum"))'
WALK_CALC_EXPRESSION = '"poi_mean"'