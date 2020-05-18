import createTrainingData
import os.path
from os import path

#how decompile a .replay file into .json format, save it locally(optional) returns extracted game frames data and controls:
if path.exists("./replays/44A6E9E811EA97DC6996C5ABEA63DF0F.replay"):
    print('yay')
else:
    print('nay')

try:
    extractedGameStatesAndControls = createTrainingData.convert_replay_to_game_frames("./replays/EE9B6AFF413722B2DBA18AA4BEAABE03.replay","./replay.json",save_json = True)
except:
    print('An exception ocurred')


#how to extract game frames data and controls from a previously decompiled .json file:

#createTrainingData.createAndSaveReplayTrainingDataFromJSON("replay.json", outputFileName = "exampleTrainingData.pbz2")


#how to load the data from a previously saved .pbz2 file:

#gameData = createTrainingData.loadSavedTrainingData("exampleSavedTrainingData.pbz2")


#uncomment below code and replace dummy arg with the path to a valid previously saved training data file. Run to see frame data format

# gameData = createTrainingData.loadSavedTrainingData("insert valid path to saved training data")
# print(f"This variable contains data for {len(gameData)} game frames in addition to controller input data")
# print(gameData[500]["GameState"])
# print(gameData[500]["PlayerData"][0])

