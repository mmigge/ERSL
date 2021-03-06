import os
import subprocess
import traceback

images = os.getcwd() + '/images/'

subdirs = os.listdir(images)

for direc in subdirs:
    path = images + direc + '/'
    merge_command_1 = ['gdal_merge.py', '-o', images + direc + '/merged_B1.TIF', '-n', '0', '-of', 'GTiff']
    merge_command_2 = ['gdal_merge.py', '-o', images + direc + '/merged_B2.TIF', '-n', '0', '-of', 'GTiff']
    merge_command_3 = ['gdal_merge.py', '-o', images + direc + '/merged_B3.TIF', '-n', '0', '-of', 'GTiff']
    merge_command_4 = ['gdal_merge.py', '-o', images + direc + '/merged_B4.TIF', '-n', '0', '-of', 'GTiff']
    merge_command_5 = ['gdal_merge.py', '-o', images + direc + '/merged_B5.TIF', '-n', '0', '-of', 'GTiff']
    merge_command_6 = ['gdal_merge.py', '-o', images + direc + '/merged_B6.TIF', '-n', '0', '-of', 'GTiff']
    merge_command_7 = ['gdal_merge.py', '-o', images + direc + '/merged_B7.TIF', '-n', '0', '-of', 'GTiff']
    min_command_length = merge_command_7.__len__() + 1
    for subdir, dirs, files in os.walk(path):
        if subdir.endswith('T1') or subdir.endswith('T2'):
            for file in os.listdir(subdir):
                if file.endswith('B1.TIF'):
                    merge_command_1.append(subdir+ '/' + file)
                elif file.endswith('B2.TIF'):
                    merge_command_2.append(subdir + '/' + file)
                elif file.endswith('B3.TIF'):
                    merge_command_3.append(subdir + '/' + file)
                elif file.endswith('B4.TIF'):
                    merge_command_4.append(subdir + '/' + file)
                elif file.endswith('B5.TIF'):
                    merge_command_5.append(subdir + '/' + file)
                elif file.endswith('B6.TIF'):
                    merge_command_6.append(subdir + '/' + file)
                elif file.endswith('B7.TIF'):
                    merge_command_7.append(subdir + '/' + file)

    commands = [merge_command_1, merge_command_2, merge_command_3, merge_command_4, merge_command_5, merge_command_6, merge_command_7]
    for command in commands:
        if command.__len__() >= min_command_length:
            try:
                ps = subprocess.Popen(
                    command,
                    stdout=subprocess.PIPE
                )
                output = ps.communicate()[0]
                for line in output.splitlines():
                    print(line)
            except Exception:
                traceback.print_exc()
