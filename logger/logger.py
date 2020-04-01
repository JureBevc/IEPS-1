import colorlog


def get_logger(name=None, level="DEBUG"):
    format_str = '%(log_color)s%(asctime)s %(name)-10s %(levelname)-6s [%(filename)s:%(lineno)d] %(message)s'
    datefmt = '%m-%d %H:%M'
    colorlog.basicConfig(
        format=format_str,
        datefmt=datefmt,
        filename='logs/crawldb.log',
        filemode='a'
    )

    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter(fmt=format_str, datefmt=datefmt))

    logger = colorlog.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(level)
    return logger