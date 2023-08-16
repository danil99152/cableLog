class Exceptions:
    __slots__ = []

    @staticmethod
    def get_exception(e) -> str:
        exception = f"Cannot get it because {e}"
        return exception

    @staticmethod
    def delete_exception(e) -> str:
        exception = f"Position was not deleted because {e}"
        return exception

    @staticmethod
    def patch_exception(e) -> str:
        exception = f"Wasn't patched because {e}"
        return exception

    @staticmethod
    def post_exception(e) -> str:
        exception = f"Wasn't posted because {e}"
        return exception
