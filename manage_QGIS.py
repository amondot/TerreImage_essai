# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QGIS_Edu
                                 A QGIS plugin
 Segmentation using OTB application
                              -------------------
        begin                : 2013-11-21
        copyright            : (C) 2013 by CS Systèmes d'Information
        email                : alexia.mondot@c-s.fr
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
# import system libraries
import os

# Import the PyQt
from PyQt4.QtCore import QVariant
from PyQt4.QtGui import QColor

# import GDAL and QGIS libraries
from qgis.core import (QgsMapLayerRegistry,
                       QgsMapLayer,
                       QgsContrastEnhancement,
                       QgsVectorLayer,
                       QgsRasterLayer,
                       QgsRaster,
                       QgsField,
                       QgsFeature,
                       QgsGeometry,
                       )

from terre_image_constant import TerreImageConstant
import OTBApplications

# import loggin for debug messages
import logging
logging.basicConfig()
# create logger
logger = logging.getLogger('TerreImage_manageQGIS')
logger.setLevel(logging.INFO)


def addVectorLayerToQGIS(vectorLayer, layername):
    """
    Add a vector layer to QGIS

    Keyword arguments :
        vectorLayer    --    vector layer to add
        layername      --    name to display in QGIS
        indexGroup     --    index of the group in QGIS where to add the layer.
                             If None given, the layer is added at the root in QGIS.
                             By default, None.
        color          --    If need to color laer with special method. By default False.
        colorByClasses --    Applies a specific lut to colorize field "classif" in vectorlayer
        fieldToColor   --    Field to be based to colorize the vector

    Example of use :
    myvector = "/home/user/myVectorLayer.shp"
    addVectorLayerToQGIS( myvector, os.path.basename(myvector))
    """
    vector = QgsVectorLayer(vectorLayer, layername, "ogr")
    layer_added = QgsMapLayerRegistry.instance().addMapLayer(vector)
    return layer_added


def get_raster_layer(raster, name):
    raster_layer = QgsRasterLayer(raster, name)
    return raster_layer


def add_qgis_raser_layer(raster_layer, canvas, bands = None):
    index_group = TerreImageConstant().index_group
    logger.debug("index_group: " + str(index_group))

    if bands:
        if raster_layer.rasterType() == 2:
            logger.debug(bands)
            pir = bands['pir']
            red = bands['red']
            green = bands['green']
            logger.debug('pir: ' + str(pir))
            logger.debug("red: " + str(red))
            logger.debug("green: " + str(green))
            if pir and red and green:
                renderer = raster_layer.renderer()
                # raster_layer.setDrawingStyle("MultiBandColor")
                renderer.setRedBand(pir)
                renderer.setGreenBand(red)
                renderer.setBlueBand(green)
                # raster_layer.setRenderer( renderer )
            # contrastForRasters( raster_layer, 0, 0, [pir, red, green] )
            histogram_stretching(raster_layer, canvas)

    QgsMapLayerRegistry.instance().addMapLayer(raster_layer)
    TerreImageConstant().legendInterface.moveLayer(raster_layer, index_group)


def addRasterLayerToQGIS(raster, layername, iface=None):
    """
    Add the given raster to qgis and improve contrast between min max

    Keyword arguments:
        raster        --    raster filename to add to QGIS
        layername     --    name to given to the raster layer for display
        indexGroup    --    index of the QGIS group where to move the layer
    """
    index_group = TerreImageConstant().index_group
    if not index_group:
        index_group = 0

    logger.debug("index_group: " + str(index_group))

    if layername == None:
        layername = os.path.basename(raster)

    raster_layer = QgsRasterLayer(raster, layername)
    histogram_stretching(raster_layer, iface.mapCanvas())

    QgsMapLayerRegistry.instance().addMapLayer(raster_layer)
    TerreImageConstant().legendInterface.moveLayer(raster_layer, index_group)
    return raster_layer


def histogram_stretching(raster_layer, canvas):
    # histogramStretch( true, QgsRaster::ContrastEnhancementCumulativeCut );
    # the_limits =QgsRaster::ContrastEnhancementCumulativeCut
    #   QgsRectangle myRectangle;
    #   if ( visibleAreaOnly )
    #     myRectangle = mMapCanvas->mapRenderer()->outputExtentToLayerExtent( myRasterLayer, mMapCanvas->extent() );
    #
    #   myRasterLayer->setContrastEnhancement( QgsContrastEnhancement::StretchToMinimumMaximum, the_limits, myRectangle );
    #
    #   myRasterLayer->setCacheImage( NULL );
    #   mMapCanvas->refresh();
    the_limits = QgsRaster.ContrastEnhancementCumulativeCut
    logger.debug("the_limits " + str(the_limits))
    raster_layer.setContrastEnhancement(QgsContrastEnhancement.StretchToMinimumMaximum, the_limits)
    raster_layer.setCacheImage(None)
    canvas.refresh()
    canvas.repaint()


def histogram_stretching_for_threshold(raster_layer, canvas):
    # histogramStretch( true, QgsRaster::ContrastEnhancementCumulativeCut );
    # the_limits =QgsRaster::ContrastEnhancementCumulativeCut
    #   QgsRectangle myRectangle;
    #   if ( visibleAreaOnly )
    #     myRectangle = mMapCanvas->mapRenderer()->outputExtentToLayerExtent( myRasterLayer, mMapCanvas->extent() );
    #
    #   myRasterLayer->setContrastEnhancement( QgsContrastEnhancement::StretchToMinimumMaximum, the_limits, myRectangle );
    #
    #   myRasterLayer->setCacheImage( NULL );
    #   mMapCanvas->refresh();
    the_limits = QgsRaster. ContrastEnhancementMinMax
    logger.debug("the_limits " + str(the_limits))
    raster_layer.setContrastEnhancement(QgsContrastEnhancement.StretchToMinimumMaximum, the_limits)
    raster_layer.setCacheImage(None)
    canvas.refresh()
    canvas.repaint()


def get_min_max_via_qgis(the_raster_layer, num_band):
    #     my_raster_stats = the_raster_layer.data_provider().bandStatistics( num_band )#, 2, 98  )
    #     my_min = my_raster_stats.minimumValue
    #     my_max = my_raster_stats.maximumValue
    #
    #     data_p = the_raster_layer.data_provider()
    my_min, my_max = the_raster_layer.data_provider().cumulativeCut(num_band, 0.2, 0.98)
    #     min, max = data_p.cumulativeCut(num_band, 0.02, 0.98)
    #     logger.debug("qgis min max :" + str(my_min) + str(my_max))
    #     logger.debug("min max 2 : " + str(min) + str(max))
    return my_min, my_max


def contrastForRasters(the_raster_layer, min_layer, max_layer, band = None):
    """
    Applies a contrast between min and max. If given min and max are 0, then calculates the min and max from gdal.
    """
    # type of layer : raster, vector, other
    type_of_layer = the_raster_layer.type()

    # take the layer renderer to get the min and max
    layer_renderer = the_raster_layer.renderer()  # for qgis > 1.9
    data_provider = the_raster_layer.data_provider()

    # the layer has to be a raster layer
    if type_of_layer == 1:
        if the_raster_layer.rasterType() == 0 and layer_renderer:
            # gray band
            # layer_renderer <qgis.core.QgsSingleBandGrayRenderer object at 0x514caf0>
            layerCE = layer_renderer.contrastEnhancement()
            # take the contrast enhancement of the layer threw the renderer
            if layerCE:
                layerCE.setContrastEnhancementAlgorithm(3)  # qgis 1.9
                layerCE.setMinimumValue(min_layer)
                layerCE.setMaximumValue(max_layer)
        elif the_raster_layer.rasterType() == 2 and layer_renderer:
            if min_layer == 0 and max_layer == 0:
                if band:
                    min1, max1 = get_min_max_via_qgis(the_raster_layer, band[0])
                    min2, max2 = get_min_max_via_qgis(the_raster_layer, band[1])
                    min3, max3 = get_min_max_via_qgis(the_raster_layer, band[2])

# #                     min1, max1, _, _ = terre_image_utils.computeStatistics(the_raster_layer.source(),0, band[0])
# #                     min2, max2, _, _ = terre_image_utils.computeStatistics(the_raster_layer.source(),0, band[1])
# #                     min3, max3, _, _ = terre_image_utils.computeStatistics(the_raster_layer.source(),0, band[2])
# #                     #print min1, max1, min2, max2, min3, max3
                else:
                    min1, max1, _, _ = OTBApplications.computeStatistics(the_raster_layer.source(), 0, 1)
                    min2, max2, _, _ = OTBApplications.computeStatistics(the_raster_layer.source(), 0, 2)
                    min3, max3, _, _ = OTBApplications.computeStatistics(the_raster_layer.source(), 0, 3)

                red_enhancement = QgsContrastEnhancement(data_provider.dataType(0))
                green_enhancement = QgsContrastEnhancement(data_provider.dataType(1))
                blue_enhancement = QgsContrastEnhancement(data_provider.dataType(2))
                # set stretch to min max
                red_enhancement.setMinimumValue(min1)
                red_enhancement.setMaximumValue(max1)
                green_enhancement.setMinimumValue(min2)
                green_enhancement.setMaximumValue(max2)
                blue_enhancement.setMinimumValue(min3)
                blue_enhancement.setMaximumValue(max3)
                red_enhancement.setContrastEnhancementAlgorithm(3)
                green_enhancement.setContrastEnhancementAlgorithm(3)
                blue_enhancement.setContrastEnhancementAlgorithm(3)
                layer_renderer.setRedContrastEnhancement(red_enhancement)  # , QgsRaster.ContrastEnhancementCumulativeCut  )
                layer_renderer.setGreenContrastEnhancement(green_enhancement)  # , QgsRaster.ContrastEnhancementCumulativeCut  )
                layer_renderer.setBlueContrastEnhancement(blue_enhancement)  # , QgsRaster.ContrastEnhancementCumulativeCut  )
        the_raster_layer.triggerRepaint()


def display_one_band(layer, keyword, iface):
    index_group = TerreImageConstant().index_group
    logger.debug("keyword " + str(keyword))
    corres = {'red': "_bande_rouge", 'green': "_bande_verte", 'blue': "_bande_bleue",
              'pir': "_bande_pir", 'mir': "_bande_mir", "nat": "_couleurs_naturelles"}

    raster_layer = QgsRasterLayer(layer.get_source(), layer.name() + corres[keyword])

    if keyword == 'nat':
        logger.debug("display on natural colors")
        band_red = layer.bands['red']
        band_green = layer.bands['green']
        band_blue = layer.bands['blue']
        renderer = raster_layer.renderer()
        # raster_layer.setDrawingStyle("MultiBandColor")
        renderer.setRedBand(band_red)
        renderer.setGreenBand(band_green)
        renderer.setBlueBand(band_blue)
        # raster_layer.setRenderer( renderer )
        # contrastForRasters( raster_layer, 0, 0, [pir, red, green] )
        histogram_stretching(raster_layer, iface.mapCanvas())
        QgsMapLayerRegistry.instance().addMapLayer(raster_layer)
        TerreImageConstant().legendInterface.moveLayer(raster_layer, index_group)
        return raster_layer
    else:

        band = layer.bands[keyword]
        if band:
            logger.debug("band num: " + str(band))
            raster_layer.setDrawingStyle("MultiBandSingleBandGray")
            renderer = raster_layer.renderer()
            logger.debug(renderer)
            renderer.setGrayBand(band)

            # contrastForRasters( raster_layer, 0, 0 )
            histogram_stretching(raster_layer, iface.mapCanvas())
            QgsMapLayerRegistry.instance().addMapLayer(raster_layer)
            TerreImageConstant().legendInterface.moveLayer(raster_layer, index_group)
            return raster_layer


def show_clicked_point(point, name, iface, vl=None):
    """ Displays the extent from the listeOfPoints

        Keyword arguments:
            listPoints        --    list of point to draw the extent
            name              --    name of the layer to display the extent name_extent
            indexGroupProduct --    index of the product group in qgis where to move the layers
    """
    # set True to set a define color to the extent and the world
    setColor = False

    # create layer
    # if vl == None :
    vl = QgsVectorLayer("Point?crs=epsg:4326", name, "memory")
    pr = vl.data_provider()

    # add fields
    pr.addAttributes([QgsField("spectral_angle", QVariant.String)])

    # add a feature
    fet = QgsFeature()

    geometry = QgsGeometry.fromPoint(point)

    # fet.setGeometry( qgis.core.QgsGeometry.fromPolygon( qgis.core.QgsGeometry.\
    # QgsPolygon(4.45 43.95, 4.45 44.400433068, 5.000403625 44.400433068,5.000403625 43.95) ) )
    fet.setGeometry(geometry)

    # ( 4.45, 43.95 ) to (5.000403625, 44.400433068 )
    pr.addFeatures([fet])

    # set color to the extent
    if setColor:
        if vl.isUsingRendererV2():
            # new symbology - subclass of qgis.core.QgsFeatureRendererV2 class
            rendererV2 = vl.rendererV2()
            symbol = rendererV2.symbol()
            for i in xrange(symbol.symbolLayerCount()):
                symbol.symbolLayer(i).setColor(QColor(168, 255, 0))

    # update layer's extent when new features have been added
    # because change of extent in provider is not propagated to the layer
    vl.updateExtents()

    QgsMapLayerRegistry.instance().addMapLayers([vl])
    return vl


def custom_stretch(the_raster_layer, values, canvas, mono = False):
    """
    Applies a contrast between min and max. If given min and max are 0, then calculates the min and max from gdal.
    """
#     logger.info("#######################")
    logger.info("custom stretch: values")
    logger.info(values)

    # print "custom stretch"
    # print canvas
    # print "layer :", the_raster_layer

    # type of layer : raster, vector, other
    type_of_layer = the_raster_layer.type()

    # take the layer renderer to get the min and max
    layer_renderer = the_raster_layer.renderer()  # for qgis > 1.9
    data_provider = the_raster_layer.dataProvider()

    # print "values", values
    # the layer has to be a raster layer
    if type_of_layer == 1:
        if (the_raster_layer.rasterType() == 0 or mono) and layer_renderer:
            min_layer, max_layer = values[0]
            # gray band
            # layer_renderer <qgis.core.QgsSingleBandGrayRenderer object at 0x514caf0>
            gray_enhancement = QgsContrastEnhancement(data_provider.dataType(1))
            # take the contrast enhancement of the layer threw the renderer
            if gray_enhancement:
                gray_enhancement.setContrastEnhancementAlgorithm(1)  # qgis 1.9
                gray_enhancement.setMinimumValue(min_layer)
                gray_enhancement.setMaximumValue(max_layer)
                layer_renderer.setContrastEnhancement(gray_enhancement)

        elif the_raster_layer.rasterType() == 2 and layer_renderer:
            # print "layer 3 bandes"
            min_red, max_red = values[0]
            min_green, max_green = values[1]
            min_blue, max_blue = values[2]
            logger.debug("red : " + str(min_red) + " " + str(max_red))
            logger.debug("green : " + str(min_green) + " " + str(max_green))
            logger.debug("blue : " + str(min_blue) + " " + str(max_blue))

            red_enhancement = QgsContrastEnhancement(data_provider.dataType(1))
            green_enhancement = QgsContrastEnhancement(data_provider.dataType(2))
            blue_enhancement = QgsContrastEnhancement(data_provider.dataType(3))
            logger.debug("red_enhancement : " + str(red_enhancement))
            logger.debug("green_enhancement : " + str(green_enhancement))
            logger.debug("blue_enhancement : " + str(blue_enhancement))

            # set stretch to min max
            red_enhancement.setMinimumValue(min_red)
            red_enhancement.setMaximumValue(max_red)
            green_enhancement.setMinimumValue(min_green)
            green_enhancement.setMaximumValue(max_green)
            blue_enhancement.setMinimumValue(min_blue)
            blue_enhancement.setMaximumValue(max_blue)
            logger.debug("red (1): " + str(red_enhancement.minimumValue()) + " " + str(red_enhancement.maximumValue()))
            logger.debug("green (1): " + str(green_enhancement.minimumValue()) + " " + str(green_enhancement.maximumValue()))
            logger.debug("blue (1): " + str(blue_enhancement.minimumValue()) + " " + str(blue_enhancement.maximumValue()))
            red_enhancement.setContrastEnhancementAlgorithm(1)
            green_enhancement.setContrastEnhancementAlgorithm(1)
            blue_enhancement.setContrastEnhancementAlgorithm(1)
            logger.debug("red (2): " + str(red_enhancement.minimumValue()) + " " + str(red_enhancement.maximumValue()))
            logger.debug("green (2): " + str(green_enhancement.minimumValue()) + " " + str(green_enhancement.maximumValue()))
            logger.debug("blue (2): " + str(blue_enhancement.minimumValue()) + " " + str(blue_enhancement.maximumValue()))

            # print "blue enhancement", blue_enhancement
            # print "blue max", blue_enhancement.maximumValue()
            # print "blue min", blue_enhancement.minimumValue()

            layer_renderer.setRedContrastEnhancement(red_enhancement)  # , QgsRaster.ContrastEnhancementCumulativeCut  )
            layer_renderer.setGreenContrastEnhancement(green_enhancement)  # , QgsRaster.ContrastEnhancementCumulativeCut  )
            layer_renderer.setBlueContrastEnhancement(blue_enhancement)  # , QgsRaster.ContrastEnhancementCumulativeCut  )

            # print "layer renderer"
            red_enhancement_debug = layer_renderer.redContrastEnhancement()
            green_enhancement_debug = layer_renderer.greenContrastEnhancement()
            blue_enhancement_debug = layer_renderer.blueContrastEnhancement()
            logger.debug("red (3): " + str(red_enhancement_debug.minimumValue()) + " " + str(red_enhancement_debug.maximumValue()))
            logger.debug("green (3): " + str(green_enhancement_debug.minimumValue()) + " " + str(green_enhancement_debug.maximumValue()))
            logger.debug("blue (3): " + str(blue_enhancement_debug.minimumValue()) + " " + str(blue_enhancement_debug.maximumValue()))

        # print "end"
        the_raster_layer.setCacheImage(None)
        the_raster_layer.triggerRepaint()
        # print "2"
    canvas.refresh()
    canvas.repaint()
    # print "3"
    # TODO : pourquoi lorsqu'on fait un histogramme sur la bande pir, on a pour affichage des précédentes valeurs:
    # layer renderer <qgis._core.QgsSingleBandGrayRenderer object at 0x7fdd144558a0>
    # the_raster_layer 2
#     print "layer renderer", layer_renderer
#     print "the_raster_layer", the_raster_layer.rasterType()
#     if type_of_layer == 1:
#         if the_raster_layer.rasterType() == 2 and layer_renderer:
#             red_enhancement_debug = layer_renderer.redContrastEnhancement()
#             green_enhancement_debug = layer_renderer.greenContrastEnhancement()
#             blue_enhancement_debug = layer_renderer.blueContrastEnhancement()
#             logger.debug("red end: " + str(red_enhancement_debug.minimumValue()) + " " + str(red_enhancement_debug.maximumValue()))
#             logger.debug("green end: " + str(green_enhancement_debug.minimumValue()) + " " + str(green_enhancement_debug.maximumValue()))
#             logger.debug("blue end: " + str(blue_enhancement_debug.minimumValue()) + " " + str(blue_enhancement_debug.maximumValue()))
#     logger.info("#######################")


def get_raster_layers():
    canvas = TerreImageConstant().canvas

    rasterlayers = []

    for i in range(canvas.layerCount()):
        layer = canvas.layer(i)
        if layer is not None and layer.isValid() and layer.type() == QgsMapLayer.RasterLayer:
            rasterlayers.append(layer)
    return rasterlayers
