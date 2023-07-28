import xml.etree.ElementTree as ET
from contextlib import ExitStack as DoesNotRaise
from test.utils import mock_detections
from typing import List, Optional, Tuple

import numpy as np
import pytest

from supervision.dataset.formats.pascal_voc import (
    detections_to_pascal_voc,
    load_pascal_voc_annotations,
    object_to_pascal_voc,
)
from supervision.detection.core import Detections


def are_xml_elements_equal(elem1, elem2):
    if (
        elem1.tag != elem2.tag
        or elem1.attrib != elem2.attrib
        or elem1.text != elem2.text
        or len(elem1) != len(elem2)
    ):
        return False

    for child1, child2 in zip(elem1, elem2):
        if not are_xml_elements_equal(child1, child2):
            return False

    return True


@pytest.mark.parametrize(
    "xyxy, name, polygon, expected_result, exception",
    [
        (
            [0, 0, 10, 10],
            "test",
            None,
            ET.fromstring(
                """<object><name>test</name><bndbox><xmin>0</xmin><ymin>0</ymin><xmax>10</xmax><ymax>10</ymax></bndbox></object>"""
            ),
            DoesNotRaise(),
        ),
        (
            [0, 0, 10, 10],
            "test",
            [[0, 0], [10, 0], [10, 10], [0, 10]],
            ET.fromstring(
                """<object><name>test</name><bndbox><xmin>0</xmin><ymin>0</ymin><xmax>10</xmax><ymax>10</ymax></bndbox><polygon><x1>0</x1><y1>0</y1><x2>10</x2><y2>0</y2><x3>10</x3><y3>10</y3><x4>0</x4><y4>10</y4></polygon></object>"""
            ),
            DoesNotRaise(),
        ),
    ],
)
def test_object_to_pascal_voc(
    xyxy: np.ndarray,
    name: str,
    polygon: Optional[np.ndarray],
    expected_result,
    exception: Exception,
):
    with exception:
        result = object_to_pascal_voc(xyxy=xyxy, name=name, polygon=polygon)
        with open("/tmp/test.xml", "w") as f:
            f.write(ET.tostring(result).decode())
        with open("/tmp/exptest.xml", "w") as f:
            f.write(ET.tostring(expected_result).decode())
        assert are_xml_elements_equal(result, expected_result)


def test_load_pascal_voc_annotations(expected_result, exception: Exception):
    ...


def test_detections_to_pascal_voc(expected_result, exception: Exception):
    ...