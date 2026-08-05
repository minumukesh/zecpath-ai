from utils.logger import setup_logger


def test_logger():
    logger = setup_logger("ZecpathAI")
    logger.info("Zecpath AI logging system is working.")

    assert logger is not None