"""
Unit tests for the finBERT sentiment wrapper.
"""
from unittest.mock import MagicMock, patch

import pytest

from core.sentiment import SentimentResult, _to_compound, analyze

# _to_compound - pure function, no mocking needed

class TestToCompound:
  def test_positive_label_returns_positive_float(self):
    result = _to_compound("positive", 0.9)
    assert result == 0.9

  def test_negative_label_returns_negative_float(self):
    result = _to_compound("negative", 0.8)
    assert result == -0.8

  def test_neutral_label_returns_zero(self):
    result = _to_compound("neutral", 0.6)
    assert result == 0.0

  def test_rounding_to_4_decimal_places(self):
    result = _to_compound("positive", 0.123456789)
    assert result == round(0.123456789, 4)
