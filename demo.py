"""Demonstration to detect, visualize, and split a video

"""

import fmdt

in_video  = "demo.mp4"
tracks    = "demo_tracks.txt"
bbs       = "demo_bbs.txt"
visu      = "demo_visu.mp4"

fmdt.detect(vid_in_path=in_video, out_track_file=tracks, trk_bb_path=bbs, trk_all=True, log=True)
fmdt.visu(in_video=in_video, in_track_file=tracks, in_bb_file=bbs, out_visu_file=visu, show_id=True)
fmdt.split_video_at_meteors(visu, tracks, 5, 5, overwrite=True, exact_split=True, log=True)

