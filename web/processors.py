import os
import difflib
import subprocess

from web import app


@app.context_processor
def inject_grader():
    def run_grade(stale):
        dummy = open("sandbox/foo.py", "w+")
        dummy.write(stale)
        dummy.close()

        subprocess.call("python -m black sandbox/foo.py", shell=True)

        dummy = open("sandbox/foo.py", "r")
        f = dummy.read()
        diff = difflib.SequenceMatcher(None, stale, f)
        dummy.close()
        os.remove("sandbox/foo.py")

        r = round(diff.ratio(), 2) * 100

        if r >= 90:
            color = "#008000"
        elif r >= 80:
            color = "#ffff00"
        else:
            color = "#ff0000"

        return [str(r), color, str(f)]

    return dict(run_grade=run_grade)
