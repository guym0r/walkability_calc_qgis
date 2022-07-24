from qgis.core import QgsMapLayerProxyModel, Qgis, QgsProject, QgsRasterLayer, QgsExpressionContext, QgsExpressionContextUtils, QgsField
import processing
import math

from .config import *

def _intersenct(output_layer_name, input_layer, overlay_layer):
    result_layer = processing.run("native:intersection", {'INPUT':input_layer,'OVERLAY':overlay_layer,'INPUT_FIELDS':[],'OVERLAY_FIELDS':[],'OVERLAY_FIELDS_PREFIX':'','OUTPUT':'TEMPORARY_OUTPUT'})['OUTPUT']

    #result_layer.setCrs(input_layer.crs())
    result_layer.setCrs(overlay_layer.crs()) # TODO remove

    if DEBUG:
            print(result_layer)
            result_layer.setName(DEBUG_LAYER_PREFIX + output_layer_name)
            QgsProject.instance().addMapLayer(result_layer)
    else:
        result_layer.setName(output_layer_name)

    return result_layer

def _buffer(output_layer_name, input_layer, buffer_distance):
    result_layer = (processing.run("native:buffer", {'INPUT':input_layer,'DISTANCE':buffer_distance,'SEGMENTS':5,'END_CAP_STYLE':0,'JOIN_STYLE':0,'MITER_LIMIT':2,'DISSOLVE':False,'OUTPUT':'TEMPORARY_OUTPUT'}))['OUTPUT']

    if DEBUG:
        print(result_layer)
        result_layer.setName(DEBUG_LAYER_PREFIX + output_layer_name)
        QgsProject.instance().addMapLayer(result_layer)

    else:
        result_layer.setName(output_layer_name)

    return result_layer

def _diffence(output_layer_name, layer_1, layer_2):
    result_layer = (processing.run("native:difference", {'INPUT': layer_1,'OVERLAY':layer_2,'OUTPUT':'TEMPORARY_OUTPUT'}))['OUTPUT']

    if DEBUG:
        print(result_layer)
        result_layer.setName(DEBUG_LAYER_PREFIX + output_layer_name)
        QgsProject.instance().addMapLayer(result_layer)

    else:
        result_layer.setName(output_layer_name)

    return result_layer

def _saperate(output_layer_name, layer):
    result_layer = (processing.run("native:multiparttosingleparts", {'INPUT':layer,'OUTPUT':'TEMPORARY_OUTPUT'}))['OUTPUT']

    if DEBUG:
        print(result_layer)
        result_layer.setName(DEBUG_LAYER_PREFIX + output_layer_name)
        QgsProject.instance().addMapLayer(result_layer)

    else:
        result_layer.setName(output_layer_name)

    return result_layer

#filter layer:
#f = QgsFeatureRequest().setFilterExpression( '"fclass" = \'path\'' )

def _create_heatmap(output_layer_name, input_layer, radius): # TODO want raw or scaled?
    result_layer_path = (processing.run("qgis:heatmapkerneldensityestimation", {'INPUT':input_layer,'RADIUS':radius,'RADIUS_FIELD':'','PIXEL_SIZE':1,'WEIGHT_FIELD':'','KERNEL':0,'DECAY':0,'OUTPUT_VALUE':0,'OUTPUT':'TEMPORARY_OUTPUT'}))['OUTPUT']

    result_layer = QgsRasterLayer(result_layer_path, output_layer_name)

    if DEBUG:
        print(result_layer)
        result_layer.setName(DEBUG_LAYER_PREFIX + output_layer_name)
        QgsProject.instance().addMapLayer(result_layer)

    return result_layer

def get_layer_extent_str(input_layer):
    layer_extent_str = str(round(input_layer.extent().xMinimum(), EXTENT_ACCUARY)) + "," + str(round(input_layer.extent().xMaximum(), EXTENT_ACCUARY)) + "," + str(round(input_layer.extent().yMinimum(), EXTENT_ACCUARY)) + "," + str(round(input_layer.extent().yMaximum(), EXTENT_ACCUARY)) + " [" + input_layer.crs().authid() + "]"

    if DEBUG:
        print("layer: " + input_layer.name() + ", extent str: " + layer_extent_str)

    return layer_extent_str

def _vector_to_raster(output_layer_name, input_layer, burn_value, extent_layer):
    result_layer_path = (processing.run("gdal:rasterize", {'INPUT':input_layer,'FIELD':'','BURN':burn_value,'USE_Z':False,'UNITS':1,'WIDTH':1,'HEIGHT':1,'EXTENT':get_layer_extent_str(extent_layer),'NODATA':0,'OPTIONS':'','DATA_TYPE':5,'INIT':None,'INVERT':False,'EXTRA':'','OUTPUT':'TEMPORARY_OUTPUT'}))['OUTPUT']

    result_layer = QgsRasterLayer(result_layer_path, output_layer_name)

    if DEBUG:
        print(result_layer)
        result_layer.setName(DEBUG_LAYER_PREFIX + output_layer_name)
        QgsProject.instance().addMapLayer(result_layer)

    return result_layer

def _zonal_statistics(output_layer_name, vector_layer, raster_layer, attribute_prefix, stats):
    result_layer = (processing.run("native:zonalstatisticsfb", {'INPUT':vector_layer,'INPUT_RASTER':raster_layer,'RASTER_BAND':1,'COLUMN_PREFIX':attribute_prefix,'STATISTICS':stats,'OUTPUT':'TEMPORARY_OUTPUT'}))['OUTPUT']

    if DEBUG:
        print(result_layer)
        result_layer.setName(DEBUG_LAYER_PREFIX + output_layer_name)
        QgsProject.instance().addMapLayer(result_layer)

    return result_layer

# Expressions

def _find_attr_min_max_value(input_layer, attr_name):
    min_val = 10000000000000 # FIX
    max_val = 0
    attr_idx = input_layer.fields().lookupField(attr_name)
    for f in input_layer.getFeatures():
        if (f[attr_idx] < min_val):
            min_val = f[attr_idx]
        if (f[attr_idx] > max_val):
            max_val = f[attr_idx]

    return min_val, max_val

def _add_field_by_expression(input_layer, new_attr_name, new_attr_type, expression):
    counter = 0

    input_layer.startEditing()
    input_layer.addAttribute(QgsField(new_attr_name, new_attr_type))
    input_layer.commitChanges()
    
    input_layer.startEditing()
    context = QgsExpressionContext() # TODO check if need context
    context.setFields(input_layer.fields())
    attr_idx = input_layer.fields().lookupField(new_attr_name)

    for f in input_layer.getFeatures():
        context.setFeature(f)
        temp = expression.evaluate(context)
        if counter % 200 == 0:
            print(temp)
        f[attr_idx] = temp
        input_layer.updateFeature(f)
        counter += 1

    input_layer.commitChanges()
    print(input_layer.name())
