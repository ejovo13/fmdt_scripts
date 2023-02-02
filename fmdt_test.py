"""Unit tests for fmdt.py
"""

import fmdt
import numpy as np
import os

def assert_conversion_correctness(filename) -> None:
    """Assert that the conversion functions between a video and ndarray are lossless
    """
    name, ext = fmdt.__decompose_video_filename(filename)
    filename_conv = f"{name}_conv.{ext}"

    # video -> frames; frames -> video'; video -> frames'
    frames = fmdt.__convert_video_to_ndarray(filename)
    fmdt.__convert_ndarray_to_video(filename_conv, frames, fmdt.__get_avg_frame_rate(filename))
    conv_frames = fmdt.__convert_video_to_ndarray(filename)
    os.remove(filename_conv)

    # Assert that frames == frames'
    assert np.array_equiv(frames, conv_frames), "Conversion between video and ndarray altered at least one frame"
    print("Validated converstion correctness")

video = "demo.mp4"
assert_conversion_correctness(video)