import Metashape
import numpy as np
import math

def point_on_3d(point2D, camera):
    """
    Projects a 2D point from the camera image onto the 3D model surface.

    Args:
        point2D (Metashape.Vector): 2D point in the camera's image coordinates.
        camera (Metashape.Camera): Camera object associated with the image.

    Returns:
        Metashape.Vector or None: 3D point on the surface, or None if projection fails.
    """
    sensor = camera.sensor
    point3D = surface.pickPoint(camera.center, camera.transform.mulp(sensor.calibration.unproject(point2D)))
    if point3D is None: return
    else: return point3D

def calculate_surface_angle(teta, distance_1, distance_2):
    """
    Calculates the surface angle based on distances and the angle between two points.

    Args:
        teta (float): Angle between the two points in radians.
        distance_1 (float): Distance from the camera to the first point.
        distance_2 (float): Distance from the camera to the second point.

    Returns:
        float: Surface angle in degrees.
    """
    distance_on_surface = math.sqrt(distance_1**2 + distance_2**2 - 2*distance_1*distance_2*math.cos(teta))
    alpha = math.asin(math.sin(teta)*distance_1/distance_on_surface)
    radian = alpha + teta/2
    degrees = math.degrees(radian)
    return degrees

GAP_PERC = 1 # Percentage value of size of the circle relative to size of the image

doc = Metashape.app.document
chunk = doc.chunk
surface = chunk.model

camera_indexes = []
camera_labels = []
camera_path = []
selected_camera_indexes = []

# Selecting the enabled cameras
for index, camera in enumerate(chunk.cameras):
    camera_labels.append(camera.label)
    camera_path.append(camera.photo.path)
    if camera.enabled:
        camera_indexes.append(index)


for camera_index in camera_indexes:
    camera = chunk.cameras[camera_index]
    sensor = camera.sensor
    
    center_x = sensor.calibration.width / 2
    center_y = sensor.calibration.height / 2
    gap = (center_x + center_y)*GAP_PERC//100
    focal_len = sensor.calibration.f
    teta = 2*math.atan(gap/focal_len) 

    center_point2D = Metashape.Vector([center_x, center_y])
    center_point3D = point_on_3d(center_point2D, camera)
    center_point3D_transformed = chunk.crs.project(chunk.transform.matrix.mulp(center_point3D))
    camera_center_transformed = chunk.crs.project(chunk.transform.matrix.mulp(camera.center))
    if center_point3D is not None:
        center_dist = (camera_center_transformed - center_point3D_transformed).norm()
    else:
        center_dist = -1

    point2D = []
    point2D.append(Metashape.Vector([center_x + gap, center_y]))
    point2D.append(Metashape.Vector([center_x - gap, center_y]))
    point2D.append(Metashape.Vector([center_x, center_y + gap]))
    point2D.append(Metashape.Vector([center_x, center_y - gap]))

    point3D = []
    distance = []
    for i in range(0,4):
        point3D.append(point_on_3d(point2D[i], camera))
        if point3D[i] is None: 
            distance.append(None)
            continue
        # print(point3D[i])
        dis = (camera.center - point3D[i]).norm()
        distance.append(dis)
        # print("camera: " ,camera_index," point: ", i, " dist: ", distance)
    if distance[0] and distance[1] is not None:
        rotation_x = calculate_surface_angle(teta, distance[0], distance[1])
    else:
        rotation_x = -1

    if distance[2] and distance[3] is not None:
        rotation_y = calculate_surface_angle(teta, distance[2], distance[3])
    else:
        rotation_y = -1
    
    print("camera: ", camera_index, "x: ", rotation_x, "y: ", rotation_y, "dist", center_dist)