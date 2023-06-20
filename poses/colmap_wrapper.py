# import os
# import subprocess
# from poses.set_intrinsic import set_intrinsic


# # $ DATASET_PATH=/path/to/dataset

# # $ colmap feature_extractor \
# #    --database_path $DATASET_PATH/database.db \
# #    --image_path $DATASET_PATH/images

# # $ colmap exhaustive_matcher \
# #    --database_path $DATASET_PATH/database.db

# # $ mkdir $DATASET_PATH/sparse

# # $ colmap mapper \
# #     --database_path $DATASET_PATH/database.db \
# #     --image_path $DATASET_PATH/images \
# #     --output_path $DATASET_PATH/sparse

# # $ mkdir $DATASET_PATH/dense
# def run_colmap(base, dir2, match_type, *, filename, parameters):
#     # print(parameters)
#     basedir = os.path.join(base, dir2)
#     imgdir = os.path.join(base, 'images')
#     maskdir = os.path.join(base, 'mask')

#     clear_args = [
#         'rm', os.path.join(basedir, 'database.db'),
#     ]
#     subprocess.run(clear_args)
    
#     logfile_name = os.path.join(basedir, 'colmap_output.txt')
#     logfile = open(logfile_name, 'w')
    
#     feature_extractor_args = [
#         'colmap', 'feature_extractor', 
#             '--database_path', os.path.join(basedir, 'database.db'), 
#             '--image_path', imgdir,
#             '--ImageReader.mask_path', maskdir,
#             '--ImageReader.single_camera', '1',
#             '--SiftExtraction.use_gpu', '0',
#             # '--SiftExtraction.max_image_size', '1000'
#     ]
#     feat_output = ( subprocess.check_output(feature_extractor_args, universal_newlines=True) )
#     logfile.write(feat_output)
#     print('Features extracted')

#     # at this
#     # set_intrinsic(os.path.join(basedir, 'database.db'))

#     exhaustive_matcher_args = [
#         'colmap', 'exhaustive_matcher', 
#             '--database_path', os.path.join(basedir, 'database.db'), 
#     ]

#     match_output = ( subprocess.check_output(exhaustive_matcher_args, universal_newlines=True) )
#     logfile.write(match_output)
#     print('Features matched')
    
#     p = os.path.join(basedir, 'sparse')
#     if not os.path.exists(p):
#         os.makedirs(p)


#     mapper_args = [
#         'colmap', 'mapper',
#             '--database_path', os.path.join(basedir, 'database.db'),
#             '--image_path', imgdir,
#             '--output_path', os.path.join(basedir, 'sparse'), # --export_path changed to --output_path in colmap 3.6
#             # '--Mapper.num_threads', '16',
#             # '--Mapper.init_min_tri_angle', '4',
#             # '--Mapper.multiple_models', '0',
#             # '--Mapper.extract_colors', '0',
        
#     ]
#     # mapper_args.extend(parameters['mapper'])
#     print(mapper_args)

#     map_output = ( subprocess.check_output(mapper_args, universal_newlines=True) )
#     logfile.write(map_output)
#     print('Sparse map created')

#     p = os.path.join(basedir, 'dense')
#     if not os.path.exists(p):
#         os.makedirs(p)

#     image_undistorter_args = [
#         'colmap', 'image_undistorter',
#         '--image_path', imgdir,
#         '--input_path', os.path.join(basedir, 'sparse', '0'),
#         '--output_path', os.path.join(basedir, 'dense'),
#         '--output_type', 'COLMAP',
#     ]

#     image_undistort_output = ( subprocess.check_output(image_undistorter_args, universal_newlines=True) )
#     logfile.write(image_undistort_output)
#     print('Images undistorted')

#     patch_match_stereo_args = [
#         'colmap', 'patch_match_stereo',
#         '--workspace_path', os.path.join(basedir, 'dense'),
#         '--workspace_format', 'COLMAP',
#         '--PatchMatchStereo.geom_consistency', 'true',
#         # '--PatchMatchStereo.window_radius', '5',
        
#     ]

#     patch_match_stereo_output = ( subprocess.check_output(patch_match_stereo_args, universal_newlines=True) )
#     logfile.write(patch_match_stereo_output)
#     print('Parch matched')

#     stereo_fusion_args = [
#         'colmap', 'stereo_fusion',
#         '--workspace_path', os.path.join(basedir, 'dense'),
#         '--workspace_format', 'COLMAP',
#         '--input_type', 'geometric',
#         '--output_path', os.path.join(basedir, 'dense', 'fused.ply'),
#         '--StereoFusion.min_num_pixels', parameters['min_num_pixels'],
#         '--StereoFusion.mask_path', maskdir,
        
#     ]

#     stereo_fusion_output = ( subprocess.check_output(stereo_fusion_args, universal_newlines=True) )
#     logfile.write(stereo_fusion_output)
#     print('Stereo fused')

#     poisson_mesher_args = [
#         'colmap', 'poisson_mesher',
#         '--input_path', os.path.join(basedir, 'dense', 'fused.ply'),
#         '--output_path', os.path.join(basedir, filename),
#         '--PoissonMeshing.trim', parameters['trim']
#     ]
#     print(poisson_mesher_args)

#     poisson_mesher_output = ( subprocess.check_output(poisson_mesher_args, universal_newlines=True) )
#     logfile.write(poisson_mesher_output)
#     print('Possion mesher done')

#     # poisson_mesher_args = [
#     #     'colmap', 'poisson_mesher',
#     #     '--input_path', os.path.join(basedir, 'dense', 'fused.ply'),
#     #     '--output_path', os.path.join(basedir, filename+'_d9.ply'),
#     #     '--PoissonMeshing.trim', '4',
#     #     '--PoissonMeshing.depth', '9'
#     # ]

#     # poisson_mesher_output = ( subprocess.check_output(poisson_mesher_args, universal_newlines=True) )
#     # logfile.write(poisson_mesher_output)
#     # print('Possion mesher done')


#     # delaunay_mesher_args = [
#     #     'colmap', 'delaunay_mesher',
#     #     '--input_path', os.path.join(basedir, 'dense'),
#     #     '--output_path', os.path.join(basedir, 'dense', 'meshed-delaunay.ply'),
#     # ]

#     # delaunay_mesher_output = ( subprocess.check_output(delaunay_mesher_args, universal_newlines=True) )
#     # logfile.write(delaunay_mesher_output)
#     # print('Delaunay mesher done')


#     logfile.close()
    
    
#     print( 'Finished running COLMAP, see {} for logs'.format(logfile_name) )




import os
import subprocess
from poses.set_intrinsic import set_intrinsic


# $ DATASET_PATH=/path/to/dataset

# $ colmap feature_extractor \
#    --database_path $DATASET_PATH/database.db \
#    --image_path $DATASET_PATH/images

# $ colmap exhaustive_matcher \
#    --database_path $DATASET_PATH/database.db

# $ mkdir $DATASET_PATH/sparse

# $ colmap mapper \
#     --database_path $DATASET_PATH/database.db \
#     --image_path $DATASET_PATH/images \
#     --output_path $DATASET_PATH/sparse

# $ mkdir $DATASET_PATH/dense
def run_colmap(basedir, match_type):

    clear_args = [
        'rm', os.path.join(basedir, 'database.db'),
    ]
    subprocess.run(clear_args)
    
    logfile_name = os.path.join(basedir, 'colmap_output.txt')
    logfile = open(logfile_name, 'w')
    
    feature_extractor_args = [
        'colmap', 'feature_extractor', 
            '--database_path', os.path.join(basedir, 'database.db'), 
            '--image_path', os.path.join(basedir, 'images'),
            '--ImageReader.single_camera', '1',
            '--SiftExtraction.use_gpu', '0',
    ]
    feat_output = ( subprocess.check_output(feature_extractor_args, universal_newlines=True) )
    logfile.write(feat_output)
    print('Features extracted')

    # at this
    # set_intrinsic(os.path.join(basedir, 'database.db'))

    exhaustive_matcher_args = [
        'colmap', 'exhaustive_matcher', 
            '--database_path', os.path.join(basedir, 'database.db'), 
    ]

    match_output = ( subprocess.check_output(exhaustive_matcher_args, universal_newlines=True) )
    logfile.write(match_output)
    print('Features matched')
    
    p = os.path.join(basedir, 'sparse')
    if not os.path.exists(p):
        os.makedirs(p)


    mapper_args = [
        'colmap', 'mapper',
            '--database_path', os.path.join(basedir, 'database.db'),
            '--image_path', os.path.join(basedir, 'images'),
            '--output_path', os.path.join(basedir, 'sparse'), # --export_path changed to --output_path in colmap 3.6
            # '--Mapper.num_threads', '16',
            # '--Mapper.init_min_tri_angle', '4',
            # '--Mapper.multiple_models', '0',
            # '--Mapper.extract_colors', '0',
    ]

    map_output = ( subprocess.check_output(mapper_args, universal_newlines=True) )
    logfile.write(map_output)
    print('Sparse map created')

    p = os.path.join(basedir, 'dense')
    if not os.path.exists(p):
        os.makedirs(p)

    image_undistorter_args = [
        'colmap', 'image_undistorter',
        '--image_path', os.path.join(basedir, 'images'),
        '--input_path', os.path.join(basedir, 'sparse', '0'),
        '--output_path', os.path.join(basedir, 'dense'),
        '--output_type', 'COLMAP',
        '--max_image_size', '2000',
    ]

    image_undistort_output = ( subprocess.check_output(image_undistorter_args, universal_newlines=True) )
    logfile.write(image_undistort_output)
    print('Images undistorted')

    patch_match_stereo_args = [
        'colmap', 'patch_match_stereo',
        '--workspace_path', os.path.join(basedir, 'dense'),
        '--workspace_format', 'COLMAP',
        '--PatchMatchStereo.geom_consistency', 'true',
    ]

    patch_match_stereo_output = ( subprocess.check_output(patch_match_stereo_args, universal_newlines=True) )
    logfile.write(patch_match_stereo_output)
    print('Parch matched')

    stereo_fusion_args = [
        'colmap', 'stereo_fusion',
        '--workspace_path', os.path.join(basedir, 'dense'),
        '--workspace_format', 'COLMAP',
        '--input_type', 'geometric',
        '--output_path', os.path.join(basedir, 'dense', 'fused.ply'),
        '--StereoFusion.min_num_pixels', '115',
    ]

    stereo_fusion_output = ( subprocess.check_output(stereo_fusion_args, universal_newlines=True) )
    logfile.write(stereo_fusion_output)
    print('Stereo fused')

    poisson_mesher_args = [
        'colmap', 'poisson_mesher',
        '--input_path', os.path.join(basedir, 'dense', 'fused.ply'),
        '--output_path', os.path.join(basedir, 'dense', 'meshed-poisson.ply'),
        '--PoissonMeshing.trim', '4'
    ]

    poisson_mesher_output = ( subprocess.check_output(poisson_mesher_args, universal_newlines=True) )
    logfile.write(poisson_mesher_output)
    print('Possion mesher done')

    # delaunay_mesher_args = [
    #     'colmap', 'delaunay_mesher',
    #     '--input_path', os.path.join(basedir, 'dense'),
    #     '--output_path', os.path.join(basedir, 'dense', 'meshed-delaunay.ply'),
    # ]

    # delaunay_mesher_output = ( subprocess.check_output(delaunay_mesher_args, universal_newlines=True) )
    # logfile.write(delaunay_mesher_output)
    # print('Delaunay mesher done')


    logfile.close()
    
    
    print( 'Finished running COLMAP, see {} for logs'.format(logfile_name) )


