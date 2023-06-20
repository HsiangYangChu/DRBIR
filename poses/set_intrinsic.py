# This script is based on an original implementation by True Price.
# Created by liminghao
import sys
import numpy as np
import sqlite3

IS_PYTHON3 = sys.version_info[0] >= 3

def array_to_blob(array):
    if IS_PYTHON3:
        return array.tostring()
    else:
        return np.getbuffer(array)

def blob_to_array(blob, dtype, shape=(-1,)):
    if IS_PYTHON3:
        return np.fromstring(blob, dtype=dtype).reshape(*shape)
    else:
        return np.frombuffer(blob, dtype=dtype).reshape(*shape)

class COLMAPDatabase(sqlite3.Connection):

    @staticmethod
    def connect(database_path):
        return sqlite3.connect(database_path, factory=COLMAPDatabase)

    def __init__(self, *args, **kwargs):
        super(COLMAPDatabase, self).__init__(*args, **kwargs)

        self.create_tables = lambda: self.executescript(CREATE_ALL)
        self.create_cameras_table = \
            lambda: self.executescript(CREATE_CAMERAS_TABLE)
        self.create_descriptors_table = \
            lambda: self.executescript(CREATE_DESCRIPTORS_TABLE)
        self.create_images_table = \
            lambda: self.executescript(CREATE_IMAGES_TABLE)
        self.create_two_view_geometries_table = \
            lambda: self.executescript(CREATE_TWO_VIEW_GEOMETRIES_TABLE)
        self.create_keypoints_table = \
            lambda: self.executescript(CREATE_KEYPOINTS_TABLE)
        self.create_matches_table = \
            lambda: self.executescript(CREATE_MATCHES_TABLE)
        self.create_name_index = lambda: self.executescript(CREATE_NAME_INDEX)

    def update_camera(self, model, width, height, params, camera_id):
        params = np.asarray(params, np.float64)
        cursor = self.execute(
            "UPDATE cameras SET model=?, width=?, height=?, params=?, prior_focal_length=True WHERE camera_id=?",
            (model, width, height, array_to_blob(params),camera_id))
        return cursor.lastrowid

def set_intrinsic(database_path):
    import os
    if os.path.exists(database_path)==False:
        print("ERROR: database path dosen't exist -- please check database.db.")
        return
    # Open the database.
    db = COLMAPDatabase.connect(database_path)
    # Get the length
    rows = db.execute("SELECT * FROM cameras")
    size = 0
    for r in rows:
        size += 1
    # Change the cameras
    for i in range(size):
        cameraModel = 'SIMPLE_RADIAL'
        width = 800
        height = 800
        params = np.array([1111.11, 400.0, 400.0])
        cameraId = i + 1
        db.update_camera(cameraModel, width, height, params, cameraId)
    # Commit the data to the file.
    db.commit()
    # Close database.db.
    db.close()
    
