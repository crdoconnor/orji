class Lookup:
    def __init__(self, text):
        self._text = text

        split = text.split("//")
        if len(split) == 1:
            self.filepath = split[0]
            self.ref = None
        elif len(split) == 2:
            self.filepath = split[0]
            self.ref = split[1]
        else:
            raise NotImplementedError
