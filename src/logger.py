import logging

def get_logger(name=__name__):
    logger = logging.getLogger(name)
    if not logger.hasHandlers():

        logger.setLevel(logging.DEBUG)
        

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        
        logger.addHandler(console_handler)
    
    return logger