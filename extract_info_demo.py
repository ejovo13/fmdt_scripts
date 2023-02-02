"""
Script that demos the extraction of information from a detect tracks file produced by fmdt
"""
import fmdt.core as fmdt

# TODO: verify that 

ex_file_0 = "ex0_detect_tracks.txt"
ex_file_1 = "ex1_detect_tracks.txt"

# Sample extraction of key information: frame_start, frame_end, and object type
info0 = fmdt.extract_key_information(ex_file_0)
info1 = fmdt.extract_key_information(ex_file_1)

print(info0); print()
print(info1); print()

# Sample extraction of all information
info_all_0 = fmdt.extract_all_information(ex_file_0)
info_all_1 = fmdt.extract_all_information(ex_file_1)

# print(info_all_0[0]); print()
# print(info_all_1[0])

start_end = fmdt.utils.separate_meteor_sequences(info1)

print(start_end)