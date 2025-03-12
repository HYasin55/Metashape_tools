"""
Projection of a point on image to a model
H. Yasin Ozturk - March 2025
"""

import Metashape

def add_single_marker(point, marker_name, marker_group, camera, surface):
    """
    Projects a 2D image point onto a 3D surface and adds a marker at the intersection.

    Args:
        point2D_image (list/tuple): 2D coordinates [x, y] in the image, with origin at the upper-left corner.
        marker_name (str): Name/label for the new marker.
        marker_group_name (str): Name of the marker group to assign the marker to.
        camera (Metashape.Camera): Camera object associated with the image.
        surface (Metashape.Model): 3D model surface to project the point onto.

    Returns:
        Metashape.Vector or None: 3D coordinates of the added marker, or None if projection failed.
    """
    point2D = Metashape.Vector([point[1],point[0]])
    sensor = camera.sensor
    point3D = surface.pickPoint(camera.center, camera.transform.mulp(sensor.calibration.unproject(point2D)))
    if point3D is None: return None
    marker = chunk.addMarker(point3D)
    marker.label = marker_name
    marker.group = marker_group
    return marker.position

doc = Metashape.app.document
chunk = doc.chunk
camera = chunk.cameras[0] 
surface = chunk.model # Possible selections: tie points, dense cloud points or model

# Define required point, marker name and group name
POINT = [1300, 1400]
MARKER_NAME = "NewMarker"
MARKER_GROUP_NAME = "NewGroup"

marker_group = chunk.addMarkerGroup()
marker_group.label = MARKER_GROUP_NAME

sensor = camera.sensor
calibration = sensor.calibration

point3D = add_single_marker(point = POINT, marker_name = MARKER_NAME, marker_group = marker_group, camera = camera, surface = surface)
print("3D Coordinates of the added marker: ", point3D)