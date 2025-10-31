import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctimes)s')


# Chemin vers les données brutes
RAW_DATA_PATH = "data/raw"
MANUALS_PATH = os.path.join(RAW_DATA_PATH, "manuals")
FAQ_PATH = os.path.join(RAW_DATA_PATH, "faq")

