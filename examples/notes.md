https://docs.python.org/3/reference/import.html
https://docs.python.org/3/library/importlib.html#approximating-importlib-import-module

sys.modules
__import__
importlib.import_module

sys.path
sys.path_hooks
sys.path_importer_cache

sys.meta_path
# -> finders
finder.find_spec # -> ModuleSpec
# finder.find_module -> deprecated
spec.loader # -> Loader, SourceLoader
loader.create_module(spec) -> optional (can return None or a module object)
#loader.load_module() -> deprecated
loader.exec_module(mod)
#loader.get_code(mod_name) # -> SourceLoader.get_data(fullpath)
