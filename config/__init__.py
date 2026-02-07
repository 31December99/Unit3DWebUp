import logging
from config.itt import itt_data
from config.sis import sis_data

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

tracker_list = {'ITT': itt_data, 'SIS': sis_data}
