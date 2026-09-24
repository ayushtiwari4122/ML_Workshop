import nltk
import sys
from src.logger import get_logger
logger = get_logger(__name__)
from src.exception import CustomException
REQUIRED_RESOURCES = [
    "punkt",
    "punkt_tab",
    "averaged_perceptron_tagger",
    "averaged_perceptron_tagger_eng"
    "maxnet_ne_chunker",
    "maxnet_ne_chunker_tab",
    "words",
    "vader_lexicon",
    "stopwords",
    "wordnet",
]


if __name__=="__main__":
    logger.info("Downloading NLTK pretrained models...")
    print("DOwnloading NLTK pretrained models...")
    for i in REQUIRED_RESOURCES:
        try:
            nltk.download(i)
        except Exception as e:
            raise CustomException(e, sys)

        logger.info("All Models Downloaded)")