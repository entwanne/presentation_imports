# La mécanique des imports
#### <div align="right">Antoine "entwanne" Rozo</div>

<div align="right"><img src="img/schtroumpf_flat_rounded.png" style="width: 5em;" /></div>

<div align="right"><img src="img/cc_by_sa.svg" style="width: 5em;" /></div>

```python skip
%%code_wrap modules_cache
import sys
__modules = sys.modules.copy()
__code__
sys.modules.clear()
sys.modules.update(__modules)
del __modules
__ret__
```

## La mécanique des imports

* Comprendre ce qu'il se passe lors d'un import
* Interférer sur la découverte des modules
* Modifier le comportement de l'import

---

* <https://github.com/entwanne/presentation_imports>
