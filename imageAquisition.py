import landsatxplore.api
from landsatxplore.earthexplorer import EarthExplorer

# Initialize a new API instance and get an access key
api = landsatxplore.api.API("remoteSensingErsl", "ErslRemoteSensing00")

# Request
scenes = api.search(
    dataset='LANDSAT_TM_C1',
    bbox=(51.1931, 11.2830, 53.5990, 14.8865),
    start_date='1983-01-01',
    end_date='1995-12-31',
    max_cloud_cover=10,
    max_results=20)

print('{} scenes found.'.format(len(scenes)))

for scene in scenes:
    print(scene['acquisitionDate'])

api.logout()

# Start downloading
ee = EarthExplorer("remoteSensingErsl", "ErslRemoteSensing00")

ee.download(scene_id='LT51960471995178MPS00', output_dir='/home/niklas/Uni/')

ee.logout()
