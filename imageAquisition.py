import os
from datetime import date, datetime
import tarfile
import traceback
import landsatxplore.api
from landsatxplore.earthexplorer import EarthExplorer
from tqdm import tqdm

# Initialize a new API instance and get an access key
api = landsatxplore.api.API("remoteSensingErsl", "ErslRemoteSensing00")

print("Searching for scenes")
# Request
# Images before 1984
scenes_early = api.search(
    dataset='LANDSAT_MSS_C1',
    bbox=(51.1931, 11.2830, 53.5990, 14.8865),
    start_date='1981-01-01',
    end_date='1983-12-31',
    max_cloud_cover=15,
    max_results=1000)

# Images after 1984
scenes = api.search(
    dataset='LANDSAT_TM_C1',
    bbox=(51.1931, 11.2830, 53.5990, 14.8865),
    start_date='1984-01-01',
    end_date='1995-12-31',
    max_cloud_cover=15,
    max_results=1000)

today = date.today()
datemin = datetime.strptime("05-01", "%m-%d").date().replace(year=today.year)
datemax = datetime.strptime("08-31", "%m-%d").date().replace(year=today.year)
selected_scenes = []

combined_scenes = scenes_early + scenes

for scene in combined_scenes:
    time = scene['acquisitionDate']
    if time[-5:] != "02-29":
        scenedate = datetime.strptime(time, '%Y-%m-%d').date().replace(year=today.year)

        if datemin < scenedate < datemax:
            selected_scenes.append(scene)

print('{} scenes found.'.format(len(selected_scenes)))

api.logout()

# Start downloading
ee = EarthExplorer("remoteSensingErsl", "ErslRemoteSensing00")

# Creating the "images" directory
images_dir = os.path.join(os.getcwd(), 'images')
if not os.path.isdir(images_dir):
    os.mkdir(images_dir)

# Downloading scenes
print("Downloading selected scenes")
for scene in tqdm(selected_scenes):
    year = scene['acquisitionDate'][:4]
    scene_id = scene['entityId']
    display_id = scene['displayId']

    pathdir = os.path.join(images_dir, year)
    if not os.path.isdir(pathdir):
        os.mkdir(pathdir)

    # Downloading scenes, if not already downloaded
    if not os.path.isfile(os.path.join(pathdir, display_id + '.tar.gz')):
        try:
            ee.download(scene_id=scene_id, output_dir=pathdir)
        except Exception:
            traceback.print_exc()
    else:
        print("File " + display_id + " already exists")

ee.logout()

print("Extracting images")
# Extracting images
for subdir, dirs, files in os.walk(images_dir):
    for file in files:
        if file.endswith('tar.gz'):
            try: 
                with tarfile.open(subdir + os.sep + file, 'r:gz') as tar:
                    substring_index = file.find('.')
                    extract_dir = subdir + os.sep + file[:substring_index]
                    tar.extractall(extract_dir)
            except Exception:
                print(file)
                traceback.print_exc()


