"""Streaming and online machine learning algorithms.

This module provides algorithms that can learn incrementally from data streams,
often with limited memory and processing time per instance.
"""

from tuiml.algorithms.streaming.adwin import ADWINDetector
from tuiml.algorithms.streaming.hoeffding_tree import HoeffdingTreeClassifier
from tuiml.algorithms.streaming.arf import AdaptiveRandomForestClassifier
from tuiml.algorithms.streaming.ddm_detectors import DDMDetector, EDDMDetector
from tuiml.algorithms.streaming.streaming_ensembles import OzaBagClassifier, LeveragingBagClassifier

__all__ = [
    "ADWINDetector",
    "HoeffdingTreeClassifier",
    "AdaptiveRandomForestClassifier",
    "DDMDetector",
    "EDDMDetector",
    "OzaBagClassifier",
    "LeveragingBagClassifier",
]
