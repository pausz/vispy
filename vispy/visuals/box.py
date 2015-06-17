# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Vispy Development Team. All Rights Reserved.
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------

from ..geometry import create_box
from ..gloo import set_state
from .mesh import MeshVisual


class BoxVisual(MeshVisual):
    """Visual that displays a box.

    Parameters
    ----------
    width : float
        Box width.
    height : float
        Box height.
    depth : float
        Box depth.
    width_segments : int
        Box segments count along the width.
    height_segments : float
        Box segments count along the height.
    depth_segments : float
        Box segments count along the depth.
    planes: array_like
        Any combination of ``{'-x', '+x', '-y', '+y', '-z', '+z'}``
        Included planes in the box construction.
    vertex_colors : ndarray
        Same as for `MeshVisual` class. See `create_plane` for vertex ordering.
    face_colors : ndarray
        Same as for `MeshVisual` class. See `create_plane` for vertex ordering.
    color : Color
        The `Color` to use when drawing the cube faces.
    edge_color : tuple or Color
        The `Color` to use when drawing the cube edges. If `None`, then no
        cube edges are drawn.
    """

    def __init__(self, width=1, height=1, depth=1, width_segments=1,
                 height_segments=1, depth_segments=1, planes=None,
                 vertex_colors=None, face_colors=None,
                 color=(0.5, 0.5, 1, 1), edge_color=None):
        vertices, filled_indices, outline_indices = create_box(
            width, height, depth, width_segments, height_segments,
            depth_segments, planes)

        MeshVisual.__init__(self, vertices['position'], filled_indices,
                            vertex_colors, face_colors, color)
        if edge_color:
            self._outline = MeshVisual(vertices['position'], outline_indices,
                                       color=edge_color, mode='lines')
        else:
            self._outline = None

    def draw(self, transforms):
        """Draw the visual

        Parameters
        ----------
        transforms : instance of TransformSystem
            The transforms to use.
        """
        MeshVisual.draw(self, transforms)
        if self._outline:
            set_state(polygon_offset=(1, 1), polygon_offset_fill=True)
            self._outline.draw(transforms)
