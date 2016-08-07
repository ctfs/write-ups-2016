# DEFCON oCTF 2016 - puzzletime

**Category:** Programming, Misc
**Points:** 200
**Author:** Yen
**Description:**

> file: puzzle.txt

## Write-up

We are given a CSV file:

```
Value,Right Edge Id,Bottom Edge Id,Left Edge Id,Top Edge Id
0x111811,105686801264,887560873655,312990448974,548925778434
...
```

We can see there are some "values" which are connected by edges. Moreover, it seems that this values lay in squares.

First, we should get rid of Edge Ids and have ony values connected with values by a direction:

```python
from collections import defaultdict

by_edge_id = {}
dirs = [(1, 0),(0, 1),(-1, 0),(0, -1)]
inv_dir = lambda x: (-x[0], -x[1])

edges = defaultdict(dict)

index2val = {}
m = {}
for i, line in enumerate(sorted(open("puzzle.txt"))):
    line = line.strip()
    if not line or "Id" in line:
        continue
    v, r, d, l, u = line.strip().split(",")
    v = int(v[2:], 16)
    index2val[i] = v
    r, d, l, u = map(int, [r, d, l, u])
    for dir, eid in zip(dirs, [r, d, l, u]):
        if eid not in by_edge_id:
            by_edge_id[eid] = (dir, i)
        else:
            dir, i0 = by_edge_id[eid]
            edges[i0][dir] = i
            edges[i][inv_dir(dir)] = i0
```

Now we can assign coordinates to each square. The values are 3 bytes and probably correspond to RGB. Therefore after assigning coordinates to squares, we can draw an image.

```python
xmin, ymin = 999999999, 999999999
xmax, ymax = -99999999, -99999999

mp = {}
visited = set()
stack = []
stack.append((0, 0, 0))
while stack:
    i, x, y = stack.pop()
    xmin = min(x, xmin)
    ymin = min(y, ymin)
    xmax = max(x, xmax)
    ymax = max(y, ymax)

    visited.add(i)
    mp[y,x] = i
    for dir, i2 in edges[i].items():
        if i2 not in visited:
            stack.append( (i2, x+dir[0], y+dir[1]) )

from struct import pack
from PIL import Image

im = Image.new("RGB", (xmax - xmin + 1, ymax - ymin + 1), "green")
for y, x in mp:
    i = mp[y,x]
    val = index2val[i]
    color = map(ord, pack("<I", val)[:3])
    im.putpixel((x - xmin, y - ymin), tuple(color))

im.save("out.png")
```

The image:

![Final Picture](https://img.vos.uz/7h6yhvcg.png)

The flag:

**PuzzleGoatKeyIsBestKey**

# Other write-ups and resources

* none yet
