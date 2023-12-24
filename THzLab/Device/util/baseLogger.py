import logging
import json


class BaseLogger(object):
    def __init__(self, log_file=None, log_level='INFO'):
        self.logger = logging.getLogger()

        if log_level == 'INFO':
            self.logger.setLevel(logging.INFO)
        elif log_level == 'DEBUG':
            self.logger.setLevel(logging.DEBUG)
        elif log_level == 'ERROR':
            self.logger.setLevel(logging.ERROR)
        elif log_level == 'WARNING':
            self.logger.setLevel(logging.WARNING)
        else:
            self.logger.setLevel(logging.INFO)

        # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] - %(module)s - %(message)s')

        # 控制台输出
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # 文件输出
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def log(self, level, message, extra_info=None):
        if extra_info:
            message = f"{message} - {json.dumps(extra_info)}"

        getattr(self.logger, level.lower())(message)

    def info(self, message, extra_info=None):
        self.log('INFO', message, extra_info)

    def warning(self, message, extra_info=None):
        self.log('WARNING', message, extra_info)

    def error(self, message, extra_info=None):
        self.log('ERROR', message, extra_info)

    def debug(self, message, extra_info=None):
        self.log('DEBUG', message, extra_info)


if __name__ == '__main__':
    logger = BaseLogger("MyLogger")

    logger.info("This is an information message.", extra_info={"key": "value"})
    logger.warning("This is a warning message.")
