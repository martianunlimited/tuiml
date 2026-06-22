"""Streaming and online machine learning algorithms.

This module provides algorithms that can learn incrementally from data streams,
often with limited memory and processing time per instance.
"""

from tuiml.algorithms.streaming.adwin import ADWINDetector
from tuiml.algorithms.streaming.hoeffding_tree import HoeffdingTreeClassifier
from tuiml.algorithms.streaming.arf import AdaptiveRandomForestClassifier

__all__ = [
    "ADWINDetector",
    "HoeffdingTreeClassifier",
    "AdaptiveRandomForestClassifier",
]
