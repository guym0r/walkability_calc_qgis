# -*- coding: utf-8 -*-
"""
/***************************************************************************
 WalkabilityCalc
                                 A QGIS plugin
 This plugin caculate the a score of walkabilty in a points
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2022-07-08
        copyright            : (C) 2022 by Guy Moria
        email                : guymoria2@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load WalkabilityCalc class from file WalkabilityCalc.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .walkability_calc import WalkabilityCalc
    return WalkabilityCalc(iface)
