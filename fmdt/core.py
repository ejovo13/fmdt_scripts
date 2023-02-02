"""
Core functions used in the processing of output for fmdt: https://github.com/alsoc/fmdt

Public API:
    extract_key_information
    extract_all_information
    split_video_at_meteors
"""

import fmdt.utils as utils

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
    def line_to_dict(split_line: list[str]):

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
    def line_to_dict(split_line: list[str]):

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

def split_video_at_meteors(video_filename: str, detect_tracks_in: str, nframes_before=3, nframes_after=3, overwrite=False) -> None:
    """
    Split a video into small segments of length (nframes_before + nframes_after + sequence_length) frames
    for each meteor detected 
    """
    utils.assert_file_exists(video_filename)
    utils.assert_file_exists(detect_tracks_in)

    # Preprocessing of information held in `detect_tracks_in`
    tracking_list = extract_key_information(detect_tracks_in)
    tracking_list = utils.retain_meteors(tracking_list)
    seqs = utils.separate_meteor_sequences(tracking_list)
    video_name, extension = utils.decompose_video_filename(video_filename) 

    # Querying of video information, extraction of frames
    # frames = utils.convert_video_to_ndarray(video_filename)
    # frame_rate = utils.get_avg_frame_rate(video_filename)
    # total_frames, _, _, _ = frames.shape

    # Max number of digits for the frames in `seqs`
    max_digits = len(str(seqs[-1][1]))
    format_str = '0' + str(max_digits)

    # function to create appropriate name of output videos
    seq_video_name = lambda seq: f'{video_name}_f{format(seq[0], format_str)}-{format(seq[1], format_str)}.{extension}'

    for s in seqs:

        # Ensure that f_start and f_end are valid
        f_start = s[0] - nframes_before if s[0] - nframes_before >= 0 else 0
        # f_end   = s[1] + nframes_after  if s[1] + nframes_after  <= total_frames else total_frames
        f_end   = s[1] + nframes_after

        # frames_seq = frames[f_start:f_end, :, :, :]
        # utils.convert_ndarray_to_video(seq_video_name(s), frames_seq, frame_rate)
        utils.extract_video_frames(video_filename, f_start, f_end, seq_video_name(s), overwrite=overwrite)