"""
API to call fmdt executables. Assumes that fmdt-detect and other executables
are on the system path
"""

import shutil
import subprocess

def detect(in_video: str, out_track_file: str | None = None, out_bb_file: str | None = None) -> None:

    fmdt_detect_exe = shutil.which("fmdt-detect")
    fmdt_detect_found = not fmdt_detect_exe is None
    assert fmdt_detect_found, "fmdt-detect executable not found"

    args = [fmdt_detect_exe, "--in-video", in_video]

    if not out_bb_file is None:
        args.extend(["--out-bb", out_bb_file])

    if out_track_file is None:
        subprocess.run(args)
    else:
        with open(out_track_file, 'w') as outfile:
            subprocess.run(args, stdout=outfile)


def visu(in_video: str, in_track_file: str, in_bb_file: str, out_visu_file: str | None = None, show_id: bool = False) -> None:

    fmdt_visu_exe = shutil.which("fmdt-visu")
    fmdt_visu_found = not fmdt_visu_exe is None
    assert fmdt_visu_found, "fmdt-visu executable not found"   

    args = [fmdt_visu_exe, "--in-video", in_video, "--in-tracks", in_track_file, "--in-bb", in_bb_file] 

    if not out_visu_file is None:
        args.extend(["--out-video", out_visu_file])

    if show_id:
        args.append("--show-id")

    subprocess.run(args)