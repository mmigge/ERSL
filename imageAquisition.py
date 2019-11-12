#from landsat.google_download import GoogleDownload
#
#x = GoogleDownload(start='1983-01-01', end='1983-06-28', satellite=4, latitude="52.29", longitude="18.4",
#                   output_path='/home/niklas/Uni/02_03_thirdMaster/remoteSensing/images/lowClouds',
#                   max_cloud_percent=20)
##low = x.candidate_scenes(return_list=True)
#print(low)
#x.download()

import landsatxplore.api

# Initialize a new API instance and get an access key
api = landsatxplore.api.API("remoteSensingErsl", "ErslRemoteSensing00")

# Request
scenes = api.search(
    dataset='LANDSAT_TM_C1',
    bbox=(51.1931, 11.2830, 53.5990, 14.8865),
    start_date='1983-01-01',
    end_date='1995-12-31',
    max_cloud_cover=10,
    max_results=2000)

print('{} scenes found.'.format(len(scenes)))

for scene in scenes:
    print(scene['acquisitionDate'])

api.logout()
