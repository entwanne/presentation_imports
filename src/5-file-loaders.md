# Importer de nouveaux types de fichiers

## Importer de nouveaux types de fichiers

- Le _file finder_ par défaut de Python gère l'import de fichiers `.py`, `.pyc` et `.so`/`.dll`
    - La classe `FileFinder` est pour cela instanciée en lui précisant les extensions supportées et les _loaders_ associés
    - On peut donc utiliser `FileFinder` pour gérer d'autres extensions de fichiers avec d'autres _loaders_

## Python++

- On peut utiliser le mécanisme des _loaders_ pour étendre la syntaxe de Python
    - Par exemple en ajoutant un opérateur d'incrémentation (`++`)
    - L'idée serait que `foo++` soit transformé en `(foo := foo + 1)` au chargement du module

- `FileLoader` pourra être utilisé avec une transformation de l'entrée
    - Il ressemble à `SourceLoader` en plus minimaliste
    - On surchargera `get_source` plutôt que `get_data` (qui renvoie le contenu brut)

## Python++

- Le _loader_ s'occupe de lire la source et transformer les _tokens_

```python
import tokenize


class BetterPythonLoader(importlib.abc.FileLoader):
    def get_source(self, fullname):
        path = self.get_filename(fullname)
        with open(path, 'rb') as f:
            tokens = list(tokenize.tokenize(f.readline))
        tokens = transform(tokens)
        return tokenize.untokenize(tokens)
```

## Python++

- La transformation consiste à détecter les `+` enchaînés et à les remplacer par une expression d'incrémentation

```python
def transform(tokens):
    stack = []
    for token in tokens:
        match token.type:
            case tokenize.NAME if not stack:
                stack.append(token)
            case tokenize.OP if stack and token.string == '+':
                if len(stack) < 2:
                    stack.append(token)
                else:
                    yield from increment_token(token, stack)
            case _:
                yield from stack
                stack.clear()
                yield token
```

## Python++

- On produit alors les _tokens_ correspondant à cette expression

```python
def increment_token(token, stack):
    name_token = stack.pop(0)
    stack.clear()

    start = name_token.start
    end = token.end
    line = name_token.line

    yield tokenize.TokenInfo(type=tokenize.OP, string='(', start=start, end=start, line=line)
    yield tokenize.TokenInfo(type=tokenize.NAME, string=name_token.string, start=start, end=start, line=line)
    yield tokenize.TokenInfo(type=tokenize.OP, string=':=', start=start, end=start, line=line)
    yield tokenize.TokenInfo(type=tokenize.NAME, string=name_token.string, start=start, end=start, line=line)
    yield tokenize.TokenInfo(type=tokenize.OP, string='+', start=start, end=start, line=line)
    yield tokenize.TokenInfo(type=tokenize.NUMBER, string='1', start=start, end=start, line=line)
    yield tokenize.TokenInfo(type=tokenize.OP, string=')', start=start, end=end, line=line)
```

## Python++

- Il suffit alors de configurer un _finder_ lié à ce _loader_

```python
path_hook = importlib.machinery.FileFinder.path_hook(
    (importlib.machinery.SourceFileLoader, ['.py']),
    (BetterPythonLoader, ['.pycc']),
)
sys.path_hooks.insert(0, path_hook)
sys.path_importer_cache.clear()
```

## Python++

- Et de tester !

```python
%%writefile increment.pycc
def test(x=0):
    for _ in range(10):
        print(x++)
```

```python
import increment
increment.test(4)
```

## Transformer le texte lu en entrée

- On peut aussi imaginer vouloir lire (et décoder) des fichiers Python chiffrés
    - En guise de chiffrement j'utilisera ici du rot-13 🙃

- On pourra la encore utiliser un `FileLoader`

## Transformer le texte lu en entrée

- Idem, le _loader_ transforme la source et est branché à un _finder_

```python
import codecs
import importlib.machinery


class Rot13Loader(importlib.abc.FileLoader):
    def get_source(self, fullname):
        data = self.get_data(self.get_filename(fullname))
        return codecs.encode(data.decode(), 'rot_13')


path_hook = importlib.machinery.FileFinder.path_hook(
    (importlib.machinery.SourceFileLoader, ['.py']),
    (Rot13Loader, ['.pyr']),
)
sys.path_hooks.insert(0, path_hook)
sys.path_importer_cache.clear()
```

## Transformer le texte lu en entrée

- Qui permet d'importer des fichiers `.pyr`

```python
%%writefile secret.pyr
qrs gbgb():
    erghea 4
```

```python
import secret
secret.toto()
```

```python
%%writefile secret2.pyr
qrs gbgb():
    erghea 42
```

```python
import secret2
secret2.toto()
```

## Import brainfuck

- Enfin on peut étendre le mécanisme d'imports pour gérer d'autres langages que Python
- Par exemple un interpréteur brainfuck sous forme de _loader_

```python
import ast
import pathlib

# définition des opérateurs
OPS = {
    '>': ast.parse('cur += 1').body,
    '<': ast.parse('cur -= 1').body,
    '+': ast.parse('mem[cur] = mem.get(cur, 0) + 1').body,
    '-': ast.parse('mem[cur] = mem.get(cur, 0) - 1').body,
    '.': ast.parse('print(chr(mem.get(cur, 0)), end="")').body,
    'init': ast.parse('mem, cur = {}, 0').body,
    'test': ast.parse('mem.get(cur, 0)').body[0].value,
}
```

## Import brainfuck

- Un _loader_ basqieu qui implémente juste `exec_module`

```python
class BrainfuckLoader(importlib.abc.Loader):

    def __init__(self, fullname, path):
        self.path = pathlib.Path(path)

    def exec_module(self, module):
        content = self.path.read_text()
        body = parse_body(content)
        tree = parse_tree(body)
        code = compile(tree, self.path, 'exec')
        exec(code, module.__dict__)
```

## Import brainfuck

- Une fonction qui transforme les _tokens_ brainfuck en nœuds AST Python

```python
def parse_body(content):
    body = [*OPS['init']]
    stack = [body]

    for char in content:
        current = stack[-1]
        match char:
            case '[':
                loop = ast.While(
                    test=OPS['test'],
                    body=[ast.Pass()],
                    orelse=[],
                )
                current.append(loop)
                stack.append(loop.body)
            case ']':
                stack.pop()
            case c if c in OPS:
                current.extend(OPS[c])
            case ' ' | '\n':
                pass
            case _:
                raise SyntaxError

    return body
```

## Import brainfuck

- Que l'on utilise pour construire un AST de module contenant une fonction, ensuite compilé

```python
def parse_tree(body):
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
    return tree
```

## Import brainfuck

- À nouveau le _loader_ est configuré dans les _path hooks_

```python
path_hook = importlib.machinery.FileFinder.path_hook(
    (importlib.machinery.SourceFileLoader, ['.py']),
    (BrainfuckLoader, ['.bf']),
)
sys.path_hooks.insert(0, path_hook)
sys.path_importer_cache.clear()
```

## Import brainfuck

- Et permet d'importer notre fichier markdown et d'exposer une fonction `run`

```bf
%%writefile hello.bf
++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++.>+.+++++++..+++.>++.<<+++++++++++++++.>.+++.------.--------.>+.>.
```

```python
import hello
hello.run()
```
