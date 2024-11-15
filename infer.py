import argparse
from collections import defaultdict, deque

import cv2
import numpy as np
from ultralytics import YOLO

import supervision as sup

SRC = np.array([[1252, 787], [2298, 803], [5039, 2159], [-550, 2159]])

W = 25
H = 250

DST = np.array(
    [
        [0, 0],
        [W - 1, 0],
        [W - 1, H - 1],
        [0, H - 1],
    ]
)

class Warp:
    def __init__(self, src: np.ndarray, dst: np.ndarray) -> None:
        src = src.astype(np.float32)
        dst = dst.astype(np.float32)
        self.mtx = cv2.getPerspectiveTransform(src, dst)

    def warp_pts(self, pts: np.ndarray) -> np.ndarray:
        if pts.size == 0:
            return pts

        pts = pts.reshape(-1, 1, 2).astype(np.float32)
        new_pts = cv2.perspectiveTransform(pts, self.mtx)
        return new_pts.reshape(-1, 2)

def get_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Vehicle Speed Estimation with YOLO and Supervision"
    )
    p.add_argument(
        "--in_vid",
        required=True,
        help="Input video path",
        type=str,
    )
    p.add_argument(
        "--out_vid",
        required=True,
        help="Output video path",
        type=str,
    )
    p.add_argument(
        "--conf",
        default=0.3,
        help="Confidence threshold",
        type=float,
    )
    p.add_argument(
        "--iou", default=0.7, help="IOU threshold for NMS", type=float
    )

    return p.parse_args()

if __name__ == "__main__":
    args = get_args()

    v_info = sup.VideoInfo.from_video_path(video_path=args.in_vid)
    mdl = YOLO("yolov8x.pt")

    trk = sup.ByteTrack(
        frame_rate=v_info.fps, track_activation_threshold=args.conf
    )

    thk = sup.calculate_optimal_line_thickness(
        resolution_wh=v_info.resolution_wh
    )
    txt_scale = sup.calculate_optimal_text_scale(resolution_wh=v_info.resolution_wh)
    box_ann = sup.BoxAnnotator(thickness=thk)
    lbl_ann = sup.LabelAnnotator(
        text_scale=txt_scale,
        text_thickness=thk,
        text_position=sup.Position.BOTTOM_CENTER,
    )
    trc_ann = sup.TraceAnnotator(
        thickness=thk,
        trace_length=v_info.fps * 2,
        position=sup.Position.BOTTOM_CENTER,
    )

    frm_gen = sup.get_video_frames_generator(source_path=args.in_vid)

    zone = sup.PolygonZone(polygon=SRC)
    wp = Warp(src=SRC, dst=DST)

    coords = defaultdict(lambda: deque(maxlen=v_info.fps))

    with sup.VideoSink(args.out_vid, v_info) as sink:
        for frm in frm_gen:
            res = mdl(frm)[0]
            dets = sup.Detections.from_ultralytics(res)
            dets = dets[dets.confidence > args.conf]
            dets = dets[zone.trigger(dets)]
            dets = dets.with_nms(threshold=args.iou)
            dets = trk.update_with_detections(detections=dets)

            pts = dets.get_anchors_coordinates(
                anchor=sup.Position.BOTTOM_CENTER
            )
            pts = wp.warp_pts(pts=pts).astype(int)

            for tid, [_, y] in zip(dets.tracker_id, pts):
                coords[tid].append(y)

            lbls = []
            for tid in dets.tracker_id:
                if len(coords[tid]) < v_info.fps / 2:
                    lbls.append(f"#{tid}")
                else:
                    start = coords[tid][-1]
                    end = coords[tid][0]
                    dist = abs(start - end)
                    time = len(coords[tid]) / v_info.fps
                    spd = dist / time * 3.6
                    lbls.append(f"#{tid} {int(spd)} km/h")

            ann_frm = frm.copy()
            ann_frm = trc_ann.annotate(
                scene=ann_frm, detections=dets
            )
            ann_frm = box_ann.annotate(
                scene=ann_frm, detections=dets
            )
            ann_frm = lbl_ann.annotate(
                scene=ann_frm, detections=dets, labels=lbls
            )

            sink.write_frame(ann_frm)
            # cv2.imshow("frame", ann_frm)
            # if cv2.waitKey(1) & 0xFF == ord("q"):
            #     break
        cv2.destroyAllWindows()
