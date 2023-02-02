"""Unit tests for fmdt.py
"""

import fmdt
import numpy as np
import os

video = "demo.mp4"

def assert_conversion_correctness(filename):
    """Assert that the conversion functions between a video and ndarray are lossless
    """
    name, ext = fmdt.__decompose_video_filename(filename)
    filename_conv = f"{name}_conv.{ext}"
    
    frames = fmdt.__convert_video_to_ndarray(filename)
    fmdt.__convert_ndarray_to_video(filename_conv, frames, fmdt.__get_avg_frame_rate(video))
    conv_frames = fmdt.__convert_video_to_ndarray(video)
    os.remove(filename_conv)

    assert np.array_equiv(frames, conv_frames), "Conversion between video and ndarray altered at least one frame"
    print("Validated converstion correctness")

assert_conversion_correctness(video)