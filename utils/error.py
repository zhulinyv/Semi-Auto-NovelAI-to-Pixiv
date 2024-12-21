class UploadError(Exception):
    def __init__(self, *args):
        super().__init__(*args)

    def __str__(self):
        return "上传错误!"


class UploadTooFastError(Exception):
    def __init__(self, *args):
        super().__init__(*args)

    def __str__(self):
        return "上传过快!"


class Waifu2xError(Exception):
    def __init__(self, *args):
        super().__init__(*args)

    def __str__(self):
        return "超分错误!"


class VideoCardError(Exception):
    def __init__(self, *args):
        super().__init__(*args)

    def __str__(self):
        return "显卡错误!"
