import colorlog


def get_logger(name=None):
    format_str = '%(log_color)s%(asctime)s %(levelname)-6s [%(filename)s:%(lineno)d] %(message)s'
    colorlog.basicConfig(
        format=format_str,
        datefmt='%m-%d %H:%M',
        filename='crawldb.log',
        filemode='a'
    )

    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter(format_str))

    logger = colorlog.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel('DEBUG')
    return logger
