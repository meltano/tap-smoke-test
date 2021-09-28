import json


class ScriptReader:

    stdoutKey = "STDOUT"
    stderrKey = "STDERR"
    exitKey = "EXIT"

    def __init__(self):
        self.scriptKeys = [self.stdoutKey, self.stderrKey, self.exitKey]
        self._return_code = 0

    def open(self, scriptFile: str):
        with open(scriptFile, mode='r') as f:
            for entry in f:
                line = json.loads(entry)
                if line["type"] in self.scriptKeys:
                    # TODO: audit log
                    # TODO: handle stdout writer
                    # TODO: handle stderr writer
                    # TODO: exit handler
                    if line["type"] == self.exitKey:
                        self._return_code = line["code"]
                        break
                    else:
                        # we should handle this line directly and filter out out of the stream
                        continue

                yield line

    def return_code(self) -> int:
        return self._return_code