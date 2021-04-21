import logging


def log():
    logging.basicConfig(level=logging.INFO, filename='app.log', filemode='a',
                        format='%(name)s - %(levelname)s - %(message)s')

    # Log Levels: Info, Warning, Error, Critical, Debug, etc...
    logging.info("Program Started")  # Would replace using print("Program Started")
    logging.warning("import statement not used")
    logging.error("NameError raised")

    try:
        x = 1 / 0
    except ZeroDivisionError as e:
        logging.exception("Division By Zero Attempted")

    logger = logging.getLogger(__name__)

    # Handlers are used to better manage where a logger will log to.
    file_handler = logging.FileHandler('file.log')
    console_handler = logging.StreamHandler()

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    logger.info("Test Output")


def _test():
    log()


if __name__ == '__main__': _test()
