"""Demonstration to detect, visualize, and split a video

"""

import fmdt

in_video  = "demo.mp4"
tracks    = "demo_tracks.txt"
bbs       = "demo_bbs.txt"
visu      = "demo_visu.mp4"

fmdt.detect(in_video, tracks, bbs)
fmdt.visu(in_video, tracks, bbs, visu)
fmdt.split_video_at_meteors(visu, tracks)

# TODO: Improve the api to save information between calls.
# It would be really nice to take the above block of code and 
# convert it into
#
# (
#     fmdt
#     .detect(in_video, tracks, bbs)
#     .visu()
#     .split()
# )
#
#