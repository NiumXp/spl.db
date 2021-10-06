# spl.db
Simple and Powerful local database

## Overview
The first step is creating a `Model`.
```py
class Player(spl.Model):
    name: str
    item: str
```
Now, we need to create a `Player` in database. We can do it instanciating the model!
```py
>>> nium = Player(name="Nium", item="Axe")
>>> nium
Player(name='Nium', item='Axe')
```
#### Note
If you don't want this behavior, you can disable it making this:
```py
class Player(spl.Model, save=False):
```
---

If you want to delete the instance from database, you can do this:
```py
del nium
```
### Why not `nium.delete()`?
Because it is not simple.

---

To create a `copy` or `duplicate` the instance, you can use the `copy` and `duplicate` methods.
```py
player = Player.get(name="Nium")

# This creates a simple copy, like `list.copy`.
nium = player.copy()
# Duplicates the `player` in database, but `NiumXp` in name.
niumxp = player.duplicate(name="NiumXp")
```

---

To get amount of instances (in database) from a Model you can use `len`!!
```py
len(Player)  # 18
```

#### Note
This not work for instances! Only subclasses of `Model`.
```py
nium = Player.get(name="Nium")
len(nium)  # Error
```
