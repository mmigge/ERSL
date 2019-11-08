from landsat.google_download import GoogleDownload
x = GoogleDownload(start='1983-01-01', end='1983-03-28', satellite=4, latitude="52.29", longitude="18.4", output_path='/home/niklas/Uni/02_03_thirdMaster/remoteSensing/images')
print(x)
x.download()
