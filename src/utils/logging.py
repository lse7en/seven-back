from loguru import logger


def call_logger(func):
    async def wrapper(*args, **kwargs):
        logger.debug(
            f"Calling function: {func.__name__}, args: {args}, kwargs: {kwargs}"
        )
        result = await func(*args, **kwargs)
        logger.debug(f"Function {func.__name__} finished with result: {result}")
        return result

    return wrapper
