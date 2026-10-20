import os
import sys
import faiss
import numpy as np
from sklearn.feature_extraction import TfidfVectorizer

from src.exception import CustomException
from src.logger import get_logger
from src.utils import load_object, save_object
logger = get_logger(__name__)

class VectorStore:
    def __init__(self, config:dict):
        self.config = config['vector_store']

    def build(self, chunks:list):
        logger.info("RAG STAGE: Vector Store Build Started.")
        try:
            texts = [c['text'] for c in chunks]
            vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
            tfidf_matrix = TfidfVectorizer.fit_transform(texts).toarray().astype('float32')
            faiss.normalize_L2(tfidf_matrix)
            dimension = tfidf_matrix.shape[1]
            index = faiss.IndexFlatIP(dimension)
            index.add(tfidf_matrix)
        except Exception as e:
            raise CustomException(e, sys)