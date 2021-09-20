from loguru import logger

logger.add('../logs/app.log', format="{time} - {level} - {message}", level='DEBUG',
           rotation='00:00', compression='zip')
