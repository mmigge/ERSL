import os
import subprocess
import traceback

images = os.getcwd() + '/images/'

subdirs = os.listdir(images)

pixel_function = """    
    <PixelFunctionType>minimum</PixelFunctionType>
    <PixelFunctionLanguage>Python</PixelFunctionLanguage>
    <PixelFunctionCode><![CDATA[
import numpy as np

def minimum(in_ar, out_ar, xoff, yoff, xsize, ysize, raster_xsize,
                   raster_ysize, buf_radius, gt, **kwargs):
    
    temp_tup = ()
    for array in in_ar:
        array = array.astype(float)
        array[array==0]=['nan']
        temp_tup += (array,)
        
    out_ar = np.round_(np.clip(np.nanmin(temp_tup, axis = 0, keepdims = True),0,255))
    
]]>
    </PixelFunctionCode>
"""

for direc in subdirs:
    path = images + direc + '/'
    merge_command_1 = ['gdalbuildvrt', '-allow_projection_difference', images + direc + '/min_merged_B1.vrt', '-srcnodata', '0']
    merge_command_2 = ['gdalbuildvrt', '-allow_projection_difference', images + direc + '/min_merged_B2.vrt', '-srcnodata', '0']
    merge_command_3 = ['gdalbuildvrt', '-allow_projection_difference', images + direc + '/min_merged_B3.vrt', '-srcnodata', '0']
    merge_command_4 = ['gdalbuildvrt', '-allow_projection_difference', images + direc + '/min_merged_B4.vrt', '-srcnodata', '0']
    merge_command_5 = ['gdalbuildvrt', '-allow_projection_difference', images + direc + '/min_merged_B5.vrt', '-srcnodata', '0']
    merge_command_6 = ['gdalbuildvrt', '-allow_projection_difference', images + direc + '/min_merged_B6.vrt', '-srcnodata', '0']
    merge_command_7 = ['gdalbuildvrt', '-allow_projection_difference', images + direc + '/min_merged_B7.vrt', '-srcnodata', '0']
    min_command_length = merge_command_1.__len__() + 1
    for subdir, dirs, files in os.walk(path):
        if subdir.endswith('T1') or subdir.endswith('T2'):
            for file in os.listdir(subdir):
                if file.endswith('B1.TIF'):
                    merge_command_1.append(subdir + '/' + file)
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

    commands = [merge_command_1, merge_command_2, merge_command_3, merge_command_4, merge_command_5, merge_command_6,
                merge_command_7]
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

    for files in os.listdir(path):
        if files.endswith('vrt'):
            f = open(path + files, "r")
            contents = f.readlines()
            f.close()

            index = contents.index('  <VRTRasterBand dataType="Byte" band="1">\n') + 1
            contents[index - 1] = '<VRTRasterBand dataType="Byte" band="1" subClass="VRTDerivedRasterBand">'
            contents.insert(index, pixel_function)

            f = open(path + files, "w")
            contents = "".join(contents)
            f.write(contents)
            f.close()

            translate_command_1 = ['gdal_translate', '--config', 'GDAL_VRT_ENABLE_PYTHON', 'YES', path + files,
                                   path + 'min_merged_B' + files[-5: -4] + '.tif']

            ps = subprocess.Popen(
                translate_command_1,
                stdout=subprocess.PIPE
            )
            output = ps.communicate()[0]
            for line in output.splitlines():
                print(line)
