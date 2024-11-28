import signal
import time

def handler(signum, frame):
    signame = signal.Signals(signum).name
    raise RuntimeError(f"Signal handler called with signal {signame} ({signum})")

for sig in signal.Signals:
    try:
        signal.signal(sig, handler)
    except OSError:
        pass

time.sleep(1e6)
