import importlib

def process(task: str):
    lib = importlib.import_module(f"src.tools.{task}")
    return lib.process()