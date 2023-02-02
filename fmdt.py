"""
Utility functions used in the processing of output for fmdt: https://github.com/alsoc/fmdt

Public API:
    extract_key_information
    extract_all_information
    split_video_at_meteors
"""
import ffmpeg
import numpy as np

# Structure of tracking output table of fmdt-detect after 
# each line gets stripped using whitespace as a delimiter
__OBJECT_ID_COLUMN   = 0
__START_FRAME_COLUMN = 2
__START_X_COLUMN     = 4
__START_Y_COLUMN     = 6
__END_FRAME_COLUMN   = 8
__END_X_COLUMN       = 10
__END_Y_COLUMN       = 12
__OBJECT_TYPE_COLUMN = 14

def extract_key_information(detect_tracks_in: str) -> list[dict]:
    """Extract key information from a detect_tracks.txt file.

    "Key" information refers to the start frame, end frame, and type of 
    object detected

    Parameters
    ----------
    detect_tracks_in (str): The name of a file whose content is the output
        of fmdt_detect

    Returns
    -------
    dict_array (list[dict]): A list of dictionaries of the form
        { 
            "type": <"meteor" | "noise" | "start">
            "frame_start": <int>
            "frame_end": <int>
        }
        where each item in the list corresponds to a single object detected by 
        `fmdt-detect`
    """

    # Utility function to convert a line of interest to a dictionary
    def line_to_dict(split_line: list):

        return {
            "type":         split_line[__OBJECT_TYPE_COLUMN],
            "start_frame":  int(split_line[__START_FRAME_COLUMN]),
            "end_frame":    int(split_line[__END_FRAME_COLUMN])
        }

    # Utility boolean function to extract only the important lines
    interesting_line = lambda line: (" meteor" in line) or (" star" in line) or (" noise" in line)
    
    # Processing of the actual file
    file_tracks = open(detect_tracks_in)
    file_lines  = file_tracks.readlines()
    dict_array = []

    for line in file_lines:
        if interesting_line(line):
            dict_array.append(line_to_dict(line.split()))

    return dict_array

def extract_all_information(detect_tracks_in: str) -> list[dict]:
    """Extract all tracking information from a detect_tracks.txt file.

    Parameters
    ----------
    detect_tracks_in (str): The name of a file whose content is the output
        of fmdt_detect

    Returns
    -------
    dict_array (list[dict]): A list of dictionaries of the form
        { 
            "id":           <int>,
            "start_frame":  <int>,
            "start_x":      <float>,
            "start_y":      <float>,
            "end_frame":    <int>,
            "end_x":        <float>,
            "end_y":        <float>,
            "type":         <"meteor" | "noise" | "start">,
        }
        where each item in the list corresponds to a single object detected by 
        `fmdt-detect`
    """

    # Utility function to convert a line of interest to a dictionary
    def line_to_dict(split_line: list):

        return {
            "id":           int(split_line[__OBJECT_ID_COLUMN]),
            "start_frame":  int(split_line[__START_FRAME_COLUMN]),
            "start_x":      float(split_line[__START_X_COLUMN]),
            "start_y":      float(split_line[__START_Y_COLUMN]),
            "end_frame":    int(split_line[__END_FRAME_COLUMN]),
            "end_x":        float(split_line[__END_X_COLUMN]),
            "end_y":        float(split_line[__END_Y_COLUMN]),
            "type":         split_line[__OBJECT_TYPE_COLUMN]
        }

    # Utility boolean function to extract only the important lines
    interesting_line = lambda line: (" meteor" in line) or (" star" in line) or (" noise" in line)
    
    # Processing of the actual file
    file_tracks = open(detect_tracks_in)
    file_lines  = file_tracks.readlines()
    dict_array = []

    for line in file_lines:
        if interesting_line(line):
            dict_array.append(line_to_dict(line.split()))

    return dict_array


def __retain_meteors(tracking_list: list[dict]) -> list[dict]:
    """Take a list of dictionaries returned by one of the fmdt.extract_* functions
    and filter out objects that are not meteors
    """
    return [obj for obj in tracking_list if obj["type"] == "meteor"]

def __separate_meteor_sequences(tracking_list: list, frame_buffer = 5) -> list[tuple[float, float]]:
    """
    Take a tracking list and compute the disparate sequences of meteors 

    If two meteors are within frame_buffer frames of each other, consider them as part of the
    same sequence
    """

    # Let's convert the tracking list into a list of (start_frame, end_frame) tuples
    start_end = [(obj["start_frame"], obj["end_frame"]) for obj in tracking_list]

    # Now condense overlapping sequences
    start_end_condensed = [start_end[0]]
    ci = 0 # condensed index, will not always be equal to i
    for i in range(len(start_end) - 1):

        # If the end frame of one meteor is close to the start frame of the next, condense the two sequences
        if (start_end_condensed[ci][1] + frame_buffer > start_end[i + 1][0]):
            start_end_condensed[ci] = (start_end_condensed[ci][0], start_end[i + 1][1])
        else:
            ci = ci + 1
            start_end_condensed.append(start_end[i + 1]) 

    return start_end_condensed

# =============================== Video file functions ========================================
def __get_avg_frame_rate(filename) -> float:
    """
    Get the average framerate of a video
    
    Adapted from https://github.com/kkroening/ffmpeg-python/blob/master/examples/video_info.py#L15
    """
    probe = ffmpeg.probe(filename)
    video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
    frame_rates = video_stream['avg_frame_rate'].split('/')
    return float(frame_rates[0]) / float(frame_rates[1])

def __get_video_width(filename) -> int:
    probe = ffmpeg.probe(filename)
    video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
    return int(video_stream['width'])


def __get_video_height(filename) -> int:
    probe = ffmpeg.probe(filename)
    video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
    return int(video_stream['height'])

    
def __decompose_video_filename(filename: str) -> tuple[str, str]:
    """
    Seperate the video filename from the extension

    __decompose_video_filename("vid.mp4") -> ("vid", "mp4") 
    """
    sep = filename.split('.')
    assert len(sep) == 2, "Filename has multiply periods"
    return (sep[0], sep[1])


def __convert_video_to_ndarray(filename: str) -> np.ndarray:
    """
    Convert a video file to a numpy array of size [n_frames, height, width, 3] 

    Taken from ffmpeg-python's documentation https://github.com/kkroening/ffmpeg-python/blob/master/examples/README.md#convert-video-to-numpy-array
    """

    fps = __get_avg_frame_rate(filename)
    w   = __get_video_width(filename)
    h   = __get_video_height(filename)

    out, _ = (
        ffmpeg
        .input(filename)
        .output('pipe:', format='rawvideo', pix_fmt='rgb24')
        .run(capture_stdout=True)
    )
    video = (
        np
        .frombuffer(out, np.uint8)
        .reshape([-1, h, w, 3])
    )

    return video

def __convert_ndarray_to_video(filename_out: str, frames: np.ndarray, framerate=60, vcodec='libx264') -> None:
    """
    Convert a rgb numpy array to video using ffmpeg-python

    Adopted from https://github.com/kkroening/ffmpeg-python/issues/246#issuecomment-520200981 
    """

    _, h, w, _ = frames.shape
    process = (
        ffmpeg
            .input('pipe:', format='rawvideo', pix_fmt='rgb24', s='{}x{}'.format(w, h))
            .output(filename_out, pix_fmt='yuv420p', vcodec=vcodec, r=framerate)
            .overwrite_output()
            .run_async(pipe_stdin=True)
    )
    for frame in frames:
        process.stdin.write(
            frame
                .astype(np.uint8)
                .tobytes()
        )
    process.stdin.close()
    process.wait()

def split_video_at_meteors(video_filename: str, detect_tracks_in: str, nframes_before=3, nframes_after=3):
    """
    Split a video into small segments of length (nframes_before + nframes_after + 1) frames
    for each meteor detected 
    """

    # Preprocessing of information held in `detect_tracks_in`
    tracking_list = extract_key_information(detect_tracks_in)
    tracking_list = __retain_meteors(tracking_list)
    seqs = __separate_meteor_sequences(tracking_list)
    video_name, extension = __decompose_video_filename(video_filename) 

    # Querying of video information, extraction of frames
    frames = __convert_video_to_ndarray(video_filename)
    frame_rate = __get_avg_frame_rate(video_filename)
    total_frames, _, _, _ = frames.shape

    # Max number of digits for the frames in `seqs`
    max_digits = len(str(seqs[-1][1]))
    format_str = '0' + str(max_digits)

    # function to create appropriate name of output videos
    seq_video_name = lambda seq: f'{video_name}_f{format(seq[0], format_str)}-{format(seq[1], format_str)}.{extension}'

    for s in seqs:

        # Ensure that f_start and f_end are valid
        f_start = s[0] - nframes_before if s[0] - nframes_before >= 0 else 0
        f_end   = s[1] + nframes_after  if s[1] + nframes_after  <= total_frames else total_frames

        frames_seq = frames[f_start:f_end, :, :, :]
        __convert_ndarray_to_video(seq_video_name(s), frames_seq, frame_rate)
