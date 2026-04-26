import logging 


def get_logger(name = __name__ , level = logging.INFO): 
    logger = logging.getLogger(name) 

    if not logger.handlers:     
        logger.setLevel(level) 

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handle = logging.StreamHandler() 
        console_handle.setFormatter(formatter) 

        ## saving logs to .txt 
        file_handle = logging.FileHandler("logs.txt") 
        file_handle.setFormatter(formatter) 

        logger.addHandler(console_handle) 
        logger.addHandler(file_handle)
        
    return logger 
