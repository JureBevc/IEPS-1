import colorlog
import os

ROOT_DIR = os.path.dirname(__file__)


def get_logger(name=None):
    format_str = '%(log_color)s%(asctime)s %(name)-10s %(levelname)-6s [%(filename)s:%(lineno)d] %(message)s'
    datefmt = '%m-%d %H:%M'
    colorlog.basicConfig(
        format=format_str,
        datefmt=datefmt,
        filename=os.path.join(ROOT_DIR, 'logs/crawldb.log'),
        filemode='a'
    )

    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter(fmt=format_str, datefmt=datefmt))

    logger = colorlog.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel('DEBUG')
    return logger
