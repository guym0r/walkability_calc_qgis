from qgis.core import QgsMapLayerProxyModel, Qgis, QgsProject
import processing
import math

from .config import *

def _intersenct(input_layer, overlay_layer, layer_name):
    result_layer = processing.run("native:intersection", {'INPUT':input_layer,'OVERLAY':overlay_layer,'INPUT_FIELDS':[],'OVERLAY_FIELDS':[],'OVERLAY_FIELDS_PREFIX':'','OUTPUT':'TEMPORARY_OUTPUT'})['OUTPUT']

    #result_layer.setCrs(input_layer.crs())
    result_layer.setCrs(overlay_layer.crs())

    if DEBUG:
            print(result_layer)
            result_layer.setName("DEBUG_"+layer_name)
            QgsProject.instance().addMapLayer(result_layer)
    else:
        result_layer.setName(layer_name)

    return result_layer

def _buffer(input_layer, buffer_distance, layer_name):
    result_layer = (processing.run("native:buffer", {'INPUT':input_layer,'DISTANCE':buffer_distance,'SEGMENTS':5,'END_CAP_STYLE':0,'JOIN_STYLE':0,'MITER_LIMIT':2,'DISSOLVE':False,'OUTPUT':'TEMPORARY_OUTPUT'}))['OUTPUT']

    if DEBUG:
        print(result_layer)
        result_layer.setName("DEBUG_"+layer_name)
        QgsProject.instance().addMapLayer(result_layer)

    else:
        result_layer.setName(layer_name)

    return result_layer

def _diffence(layer_1, layer_2, layer_name):
    result_layer = (processing.run("native:difference", {'INPUT': layer_1,'OVERLAY':layer_2,'OUTPUT':'TEMPORARY_OUTPUT'}))['OUTPUT']

    if DEBUG:
        print(result_layer)
        result_layer.setName("DEBUG_"+layer_name)
        QgsProject.instance().addMapLayer(result_layer)

    else:
        result_layer.setName(layer_name)

    return result_layer

def _saperate(layer, layer_name):
    result_layer = (processing.run("native:multiparttosingleparts", {'INPUT':layer,'OUTPUT':'TEMPORARY_OUTPUT'}))['OUTPUT']

    if DEBUG:
        print(result_layer)
        result_layer.setName("DEBUG_" + layer_name)
        QgsProject.instance().addMapLayer(result_layer)

    else:
        result_layer.setName(layer_name)

    return result_layer

#filter layer:
#f = QgsFeatureRequest().setFilterExpression( '"fclass" = \'path\'' )

def _create_heatmap(input_layer, radius, layer_name): # TODO want raw or scaled
    result_layer = (processing.run("qgis:heatmapkerneldensityestimation", {'INPUT':input_layer,'RADIUS':radius,'RADIUS_FIELD':'','PIXEL_SIZE':1,'WEIGHT_FIELD':'','KERNEL':0,'DECAY':0,'OUTPUT_VALUE':0,'OUTPUT':'TEMPORARY_OUTPUT'}))['OUTPUT']

    if DEBUG:
        print(result_layer)
        result_layer.setName("DEBUG_" + layer_name)
        QgsProject.instance().addMapLayer(result_layer)

    else:
        result_layer.setName(layer_name)

    return result_layer

def get_layer_extent_str(input_layer):
    layer_extent_str = str(round(input_layer.extent().xMinimum(), EXTENT_ACCUARY)) + "," + str(round(input_layer.extent().xMaximum(), EXTENT_ACCUARY)) + "," + str(round(input_layer.extent().yMinimum(), EXTENT_ACCUARY)) + "," + str(round(input_layer.extent().yMaximum(), EXTENT_ACCUARY)) + " [" + input_layer.crs().authid() + "]"

    if DEBUG:
        print("layer: " + input_layer.name() + ", extent str: " + layer_extent_str)

    return layer_extent_str

def _vector_to_raster(input_layer, burn_value, extent_layer):
    return
    #processing.run("gdal:rasterize", {'INPUT':input_layer,'FIELD':'','BURN':burn_value,'USE_Z':False,'UNITS':1,'WIDTH':1,'HEIGHT':1,'EXTENT':get_layer_extent_str(extent_layer),'NODATA':0,'OPTIONS':'','DATA_TYPE':5,'INIT':None,'INVERT':False,'EXTRA':'','OUTPUT':'TEMPORARY_OUTPUT'})