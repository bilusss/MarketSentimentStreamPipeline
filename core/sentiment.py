"""
This module will contain the sentiment analysis logic
Singleton will be used to ensure only one instance of the analyzer is created - finBERT weights 400MB

finBERT is a pre-trained BERT model for financial text classification.
FinBERT is a pre-trained NLP model to analyze sentiment of financial text.
It is built by further training the BERT language model in the finance domain,
using a large financial corpus and thereby fine-tuning it for financial sentiment classification.

The model will give softmax outputs for three labels: positive, negative or neutral.
"""

from core.logger import get_logger
from dataclasses import dataclass
from functools import lru_cache

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

logger = get_logger("sentiment")

MODEL_NAME = "ProsusAI/finbert"

# Singleton loading

@lru_cache(maxsize=1)
def _load_pipeline():
  """
  If GPU is available then it is set to default device
  @lru_cache makes sure it only has 1 instance
  """
  if torch.cuda.is_available():
    device=0
  else:
    device=-1
  
  logger.info(f"Loading finBERT sentiment model")
  tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
  model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
  
  nlp = pipeline(
    "text-classification",
    model=model,
    tokenizer=tokenizer,
    device=device,
    top_k=None,
    truncation=True,
    max_length=512, # finBERT hard limit
  )
  logger.info(f"finBERT loaded successfully")
  
  return nlp

# Public interface

@dataclass(frozen=True)
class SentimentResult:
  label: str # positive, negative or neutral
  score: float # confidence of the for winning label: 0.0 - 1.0
  compound: float # signed score: positive: +score, negative: -score, neutral -> 0

def analyze(text: str) -> SentimentResult:
  """
  Analyze sentiment of a single text snippet
  Truncates input to 512 tokens (finBERT hard limit).
  
  Returns:
  - label: the dominant sentiment class
  - score: model confidence (0–1)
  - compound: signed value in [-1, 1] for easy numerical aggregation
  
  Example:
  result = analyze("Bitcoin crashes amid regulatory fears")
  result.label
  # 'negative'
  result.compound  # something like -0.87
  """
  if not text or not text.strip():
    logger.debug(f"Empty text passed, returning neutral")
    return SentimentResult("neutral", 0.0, 0.0)
  
  nlp = _load_pipeline()
  try:
    # pipeline returns: [[{"label": "positive", "score": 0.9}, ...]]
    results: list[dict] = nlp(text)[0]
  except Exception as e:
    logger.exception(f"finBERT inference failed for text: {text} - error: {e}")
    return SentimentResult(label="neutral", score=0.0, compound=0.0)
  
  # Map to a dict for easy lookup
  scores_by_label = {r["label"]: r["score"] for r in results}
  winning_label = max(scores_by_label, key=scores_by_label.__getitem__)
  winning_score = scores_by_label[winning_label]
  
  # Build a signed compound score
  compound = _to_compound(winning_label, winning_score)
  return SentimentResult(label=winning_label, score=winning_score, compound=compound)

def _to_compound(label: str, score: float) -> float:
  """
  Convert (label, score) to a signed float in [-1, 1].
  
  Why not just use the raw score?  Because score is always positive (it's
  a softmax probability).  The compound sign encodes direction, making
  aggregation straightforward: mean(compounds) tells you the net market mood.
  """
  if label == "positive":
      return round(score, 4)
  if label == "negative":
      return round(-score, 4)
  return 0.0