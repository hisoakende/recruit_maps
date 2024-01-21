class NotPermitted(BaseException):
    pass


class TagDoesntExist(BaseException):
    pass


class TagAlreadyIsLiked(BaseException):
    """You've already liked this tag"""


class TagIsNotLiked(BaseException):
    """You haven't liked this tag yet"""
