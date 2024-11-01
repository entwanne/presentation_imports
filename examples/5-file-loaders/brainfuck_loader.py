import ast
import importlib
import importlib.abc
import importlib.machinery
import pathlib
import sys


class BrainfuckLoader(importlib.abc.Loader):
    OPS = {
        '>': ast.parse('cur += 1').body,
        '<': ast.parse('cur -= 1').body,
        '+': ast.parse('mem[cur] = mem.get(cur, 0) + 1').body,
        '-': ast.parse('mem[cur] = mem.get(cur, 0) - 1').body,
        '.': ast.parse('print(chr(mem.get(cur, 0)), end="")').body,
        'init': ast.parse('mem, cur = {}, 0').body,
        'test': ast.parse('mem.get(cur, 0)').body[0].value,
    }

    def __init__(self, fullname, path):
        self.path = pathlib.Path(path)

    def exec_module(self, module):
        content = self.path.read_text()
        body = [*self.OPS['init']]
        stack = [body]

        for char in content:
            current = stack[-1]
            match char:
                case '[':
                    loop = ast.While(
                        test=self.OPS['test'],
                        body=[ast.Pass()],
                        orelse=[],
                    )
                    current.append(loop)
                    stack.append(loop.body)
                case ']':
                    stack.pop()
                case c if c in self.OPS:
                    current.extend(self.OPS[c])
                case _:
                    raise SyntaxError

        tree = ast.Module(
            body=[
                ast.FunctionDef(
                    name='run',
                    args=ast.arguments(posonlyargs=[], args=[], kwonlyargs=[], kw_defaults=[], defaults=[]),
                    decorator_list=[],
                    body=body,
                ),
            ],
            type_ignores=[],
        )

        ast.fix_missing_locations(tree)
        code = compile(tree, self.path, 'exec')
        exec(code, module.__dict__)


path_hook = importlib.machinery.FileFinder.path_hook(
    (importlib.machinery.SourceFileLoader, ['.py']),
    (BrainfuckLoader, ['.bf']),
)
sys.path_hooks.insert(0, path_hook)
sys.path_importer_cache.clear()

import hello
hello.run()

sys.path_hooks.remove(path_hook)
sys.path_importer_cache.clear()
