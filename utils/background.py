import threading

def run_in_background(target, *args, **kwargs):
    """
    Runs a target function in a separate thread.
    Useful for fire-and-forget tasks like sending notifications or generating PDFs.
    """
    thread = threading.Thread(target=target, args=args, kwargs=kwargs)
    thread.start()
