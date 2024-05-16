#!/usr/bin/env python3
import logging
import time
from datetime import datetime
# logging.warning(TypeError)
i = datetime.utcnow()
logging.basicConfig(
    filename="0-temp.log",
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s'
)
logging.info(f"ana 7akan a3trd {i}")
logging.info("ana 7akan a3trd {}" .format(i))
logging.warning(TypeError)
