import logging


def setup_logger(name: str = "financial_pipeline", log_path: str = "financial_pipeline.log", level: int = logging.INFO) -> logging.Logger:
    """Configure a centralized logger with standard format."""

    logger = logging.getLogger(name)
    logger.setLevel(level)

    fh = logging.FileHandler(log_path)
    fh.setLevel(level)

    ch = logging.StreamHandler()
    ch.setLevel(level)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger
