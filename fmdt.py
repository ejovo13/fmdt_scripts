"""
Utility functions used in the processing of output for fmdt: https://github.com/alsoc/fmdt
"""

# TODO: implement functions to split videos based on tracked objects

# Structure of tracking output table of fmdt-detect 
__OBJECT_ID_COLUMN   = 0
__START_FRAME_COLUMN = 2
__START_X_COLUMN     = 4
__START_Y_COLUMN     = 6
__END_FRAME_COLUMN   = 8
__END_X_COLUMN       = 10
__END_Y_COLUMN       = 12
__OBJECT_TYPE_COLUMN = 14

def extract_key_information(detect_tracks_in: str):
    """
    Extract information from a detect_tracks.txt file.

    Returns a list of dictionaries of the form

    { 
        "type": <"meteor" | "noise" | "start">
        "frame_start": <int>
        "frame_end": <int>
    }

    where each dictionary corresponds to a single object detected by 
    `fmdt-detect`
    """

    # Utility function to convert a line of interest to a dictionary
    def line_to_dict(split_line: list):

        return {
            "type":         split_line[__OBJECT_TYPE_COLUMN],
            "start_frame":  split_line[__START_FRAME_COLUMN],
            "end_frame":    split_line[__END_FRAME_COLUMN]
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

def extract_all_information(detect_tracks_in: str):
    """
    Extract all tracking information from a detect_tracks.txt file.

    Returns a list of dictionaries of the form

    { 
        "id":           <int>,
        "start_frame":  <int>,
        "start_x":      <int>,
        "start_y":      <int>,
        "end_frame":    <int>,
        "end_x":        <int>,
        "end_y":        <int>,
        "type":         <"meteor" | "noise" | "start">,
    }

    where each dictionary corresponds to a single object detected by 
    `fmdt-detect`
    """

    # Utility function to convert a line of interest to a dictionary
    def line_to_dict(split_line: list):

        return {
            "id":           split_line[__OBJECT_ID_COLUMN],
            "start_frame":  split_line[__START_FRAME_COLUMN],
            "start_x":      split_line[__START_X_COLUMN],
            "start_y":      split_line[__START_Y_COLUMN],
            "end_frame":    split_line[__END_FRAME_COLUMN],
            "end_x":        split_line[__END_X_COLUMN],
            "end_y":        split_line[__END_Y_COLUMN],
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
    