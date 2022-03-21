# if the car doesn't steer try lowering this value
STEERING_SIMILARITY_THRESHOLD = -1.0
# Setting this to True to see the similarity value in the console to 
# help fine tune the steering threshold value. This value should not be 
# lower then the value that is reported when the countersteering icon is red. 
# Otherwise you'll be steering right the whole time and we do not want to do that in corners.
# This will also give you a small window next to the chiaki stream this should display the 
# countersteering icon.
SHOW_SIMILARITY_DEBUG = False