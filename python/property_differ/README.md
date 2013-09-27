Takes two (Java) property files and compares keys. Also reports duplicate keys.

Uses following formats for key-value rows:

```
# hash sign means comment row
<whitespace>key<whitespace>:<whitspace>value<whitepspace>
<whitespace>key<whitespace>=<whitspace>value<whitepspace>
# Empty rows are ignored. Also rows that do not comply to above shown formats.
```

Run example:

```
# ./propdiff.py testproperties/p{1,2}.properties
testproperties/p1.properties has following duplicate key: key1.duplicate
testproperties/p2.properties has following duplicate keys: key1.duplicate, key2.duplicate
testproperties/p1.properties has following unique keys: key.only.in.1, row.colon.separator
testproperties/p2.properties has following unique keys: key2.duplicate, key.only.in.2
```