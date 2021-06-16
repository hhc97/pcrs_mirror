from contextlib import redirect_stdout
import io
import python_ta


# Pickle issues forced this to be moved to its own module.
# Required to be at the global scope and shouldn't have django dependencies
def pyta_runner(q, pytaConfig, fname):
    with io.StringIO() as buf, redirect_stdout(buf):
        try:
            python_ta.check_all(fname, config=pytaConfig)
            output = buf.getvalue()
        except Exception as e: # Usually an index error in PyTA
            output = f'[Line 1] PyTA could not be run'
    q.put(output, timeout=1)    # 1 second timeout to avoid deadlock
