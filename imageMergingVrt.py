import os
import subprocess
import traceback

images = os.getcwd() + '/images/'

subdirs = os.listdir(images)

pixel_function = """    <PixelFunctionType>average</PixelFunctionType>
    <PixelFunctionLanguage>Python</PixelFunctionLanguage>
    <PixelFunctionCode><![CDATA[
import numpy as np

def average(in_ar, out_ar, xoff, yoff, xsize, ysize, raster_xsize,raster_ysize, buf_radius, gt, **kwargs):
    div = np.zeros(in_ar[0].shape)
    for i in range(len(in_ar)):
        div += (in_ar[i] != 0)
    div[div == 0] = 1

    y = np.sum(in_ar, axis = 0, dtype = 'uint16')
    y = y / div

    np.clip(y,0,255, out = out_ar)
]]>
    </PixelFunctionCode>
"""

for direc in subdirs:
    path = images + direc + '/'
    merge_command_1 = ['gdalbuildvrt', images + direc + '/raster.vrt', '-srcnodata', '0']
    min_command_length = merge_command_1.__len__() + 1
    for subdir, dirs, files in os.walk(path):
        if subdir.endswith('T1') or subdir.endswith('T2'):
            for file in os.listdir(subdir):
                if file.endswith('B1.TIF'):
                    merge_command_1.append(subdir + '/' + file)

    commands = [merge_command_1]
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

            print(index)

            contents.insert(index, pixel_function)

            f = open(path + files, "w")
            contents = "".join(contents)
            f.write(contents)
            f.close()

            translate_command_1 = ['gdal_translate', '--config', 'GDAL_VRT_ENABLE_PYTHON', 'YES', path + files, path + 'raster.tif']

            ps = subprocess.Popen(
                translate_command_1,
                stdout=subprocess.PIPE
            )
            output = ps.communicate()[0]
            for line in output.splitlines():
                print(line)