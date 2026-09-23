from detection.person_segmentation import PersonSegmenter
from detection.pose_detection import PoseDetector
from tracking.tracker import PersonTracker


class VisionPipeline:
    def __init__(self, pose_interval=3):
        self.segmenter = PersonSegmenter()
        self.pose_detector = PoseDetector()
        self.tracker = PersonTracker()

        self.pose_interval = pose_interval
        self.frame_count = 0
        self.last_pose_result = None

    def process(self, frame):
        self.frame_count += 1

        # ------------------------------------------
        # PERSON SEGMENTATION + TRACKING
        # ------------------------------------------

        segmentation_results = self.segmenter.model.track(
            frame,
            classes=[0],
            conf=0.4,
            persist=True,
            verbose=False
        )

        segmentation_result = segmentation_results[0]

        tracked_people = self.tracker.update(
            segmentation_result
        )

        output = segmentation_result.plot()

        # ------------------------------------------
        # POSE
        # Run only every Nth frame
        # ------------------------------------------

        if (
            self.frame_count % self.pose_interval == 0
            or self.last_pose_result is None
        ):
            self.last_pose_result = (
                self.pose_detector.detect(frame)
            )

        output = self.last_pose_result.plot(
            img=output,
            boxes=False
        )

        return output, tracked_people