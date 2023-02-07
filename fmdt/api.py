"""
API to call fmdt executables. Assumes that fmdt-detect and other executables
are on the system path
"""

import shutil
import subprocess

def detect(
        vid_in_path: str, 
        vid_in_start: int | None = None,
        vid_in_stop: int | None = None,
        vid_in_skip: int | None = None,
        vid_in_buff: bool | None = None,
        vid_in_loop: int | None = None,
        vid_in_threads: int | None = None,
        light_min: int | None = None,
        light_max: int | None = None,
        ccl_fra_path: str | None = None,
        ccl_fra_id: bool | None = None,
        mrp_s_min: int | None = None,
        mrp_s_max: int | None = None,
        knn_k: int | None = None,
        knn_d: int | None = None,
        knn_s: int | None = None,
        trk_ext_d: int | None = None,
        trk_ext_o: int | None = None,
        trk_angle: float | None = None,
        trk_star_min: int | None = None,
        trk_meteor_min: int | None = None,
        trk_meteor_max: int | None = None,
        trk_ddev: float | None = None,
        trk_all: bool | None = None,
        trk_bb_path: str | None = None,
        trk_mag_path: str | None = None,
        out_track_file: str | None = None,
    ) -> None:

    fmdt_detect_exe = shutil.which("fmdt-detect")
    fmdt_detect_found = not fmdt_detect_exe is None
    assert fmdt_detect_found, "fmdt-detect executable not found"

    args = [fmdt_detect_exe, "--in-video", vid_in_path]

    if not vid_in_skip is None:
        args.extend(["--vid-in-skip", vid_in_skip])

    if not vid_in_buff is None:
        args.extend(["--vid-in-buff"])

    if not vid_in_threads is None:
        args.extend(["--vid-in-threads", vid_in_threads])

    if not light_min is None:
        args.extend(["--ccl-hyst-lo", light_min])

    if not light_max is None:
        args.extend(["--ccl-hyst-hi", light_max])

    if not ccl_fra_path is None:
        args.extend(["--ccl_fra_path", ccl_fra_path])

    if not ccl_fra_id is None:
        args.extend(["--ccl-fra-id"])

    if not mrp_s_min is None:
        args.extend(["--mrp-s-min", mrp_s_min])

    if not mrp_s_max is None:
        args.extend(["--mrp-s-max", mrp_s_max])

    if not knn_k is None:
        args.extend(["--knn-k", knn_k])

    if not knn_d is None:
        args.extend(["--knn-d", knn_d])

    if not knn_s is None:
        args.extend(["--knn-s", knn_s])

    if not trk_ext_d is None:
        args.extend(["--trk-ext-d", trk_ext_d])

    if not trk_ext_o is None:
        args.extend(["--trk-ext-o", trk_ext_o])

    if not trk_angle is None:
        args.extend(["--trk-angle", trk_angle])

    if not trk_star_min is None:
        args.extend(["--trk-star-min", trk_star_min])

    if not vid_in_start is None:
        args.extend(["--vid-in-start", vid_in_start])

    if not vid_in_stop is None:
        args.extend(["--vid-in-stop", vid_in_stop])

    if not trk_bb_path is None:
        args.extend(["--trk-bb-path", trk_bb_path])

    if not vid_in_loop is None:
        args.extend(["--vid-in-loop", vid_in_loop])

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