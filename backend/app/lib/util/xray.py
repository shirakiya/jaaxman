from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core.exceptions.exceptions import SegmentNotFoundException
from aws_xray_sdk.core.models.dummy_entities import DummySegment


def current_segment():
    try:
        segment = xray_recorder.current_segment()
        if segment:
            return segment
    except SegmentNotFoundException:
        pass

    return DummySegment()
