# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

import numpy as np

class Roi():
    def __init__(self, limits):
        self.x_min = limits[0]
        self.x_max = limits[1]
        self.y_min = limits[2]
        self.y_max = limits[3]

    def set_x_limit(self, x_limit):
        self.x_min = x_limit[0]
        self.x_max = x_limit[1]

    def set_y_limit(self, y_limit):
        self.y_max = y_limit[0]
        self.y_max = y_limit[1]

    def set_x_max(self, x_max):
        if self.x_max > x_max:
            self.x_max = x_max
        if self.x_min >= x_max:
            self.x_min = 0

    def set_y_max(self, y_max):
        if self.y_max > y_max:
            self.y_max = y_max
        if self.y_min >= y_max:
            self.y_min = y_max - 1

    def get_width(self):
        return self.x_max - self.x_min

    def get_height(self):
        return self.y_max - self.y_min

    def get_x_limits(self):
        return [self.x_min, self.x_max]

    def get_y_limits(self):
        return [self.y_min, self.y_max]

    def as_list(self):
        return [self.x_min, self.x_max, self.y_min, self.y_max]

    def set_roi(self, limits):
        self.x_min = limits[0]
        self.x_max = limits[1]
        self.y_min = limits[2]
        self.y_max = limits[3]


class RoiDataManager():
    def __init__(self, roi_num):
        self.roi_num = roi_num
        self._img_dimensions_list = []
        self._rois_list = []
        self._num = 0
        self._current = None

    def _exists(self, dimension):
        if self._get_dimension_ind(dimension) is not None:
            return True
        else:
            return False

    def _add(self, img_dimension, rois):
        if self._exists(img_dimension):
            ind = self._get_dimension_ind(img_dimension)
            self._rois_list[ind] = rois
        else:
            self._img_dimensions_list.append(img_dimension)
            self._rois_list.append(rois)
            self._num += 1

    def _get_dimension_ind(self, img_dimension):
        for ind in range(self._num):
            if self._img_dimensions_list[ind] == img_dimension:
                self._current = ind
                return ind
        self._current = None
        return None

    def get_rois(self, img_dimension):
        """
        Tries to get stored RoiData information for the provided image dimension. If the
        image dimensions have not been used before the roi will be initialized by 2 stripes
        :param img_dimension: len 2 array with width and height)
        :return: RoiData object
        :type: RoiData
        """
        if img_dimension is None:
            img_dimension = (1, 1)

        if self._exists(img_dimension):
            return self._rois_list[self._get_dimension_ind(img_dimension)]
        else:
            rois = []
            part_height = img_dimension[1]/(2.0*self.roi_num+1.0)
            for ind in range(self.roi_num):
                limits =  np.array([0.25 * (img_dimension[0]) - 1,
                                    0.75 * (img_dimension[0]) - 1,
                                    (2*ind+1) * part_height -1 ,
                                    (2*ind+2) * part_height -1])
                limits = np.round(limits)
                rois.append(Roi(limits))

            self._add(img_dimension, rois)
            return self._rois_list[self._get_dimension_ind(img_dimension)]

    def get_roi(self, index, img_dimension):
         return self.get_rois(img_dimension)[index]

    def set_roi(self, index, img_dimension, limits):
        if self._exists(img_dimension):
            self._rois_list[self._get_dimension_ind(img_dimension)][index] = Roi(limits)
        else:
            self.get_rois(img_dimension)
            self.set_roi(index, img_dimension, limits)

