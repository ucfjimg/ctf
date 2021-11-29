# Compress The Flag

The challenge text:

* Technically this isn't a good compression benchmark, but it's the only one we have.

* nc compresstheflag.hackable.software 1337

The challenge was categorized as Miscellaneous, Easy. 75 teams solved it for a dynamic
score of 156 points.

We are given the Python source to the server.

Connecting to the server gives us instructions:

```
Please send: seed:string\n
I'll then show you the compression benchmark results!
Note: Flag has format DrgnS{[A-Z]+}
```

Sending a string such as `1:abc` returns

```
1:abc
    none   28
    zlib   36
    bzip2   67
    lzma   84
```

By looking at the server source, we can see what's going on. The seed value is used to seed a random number generator, which is then used
to shuffle the flag. The string we pass is prepended to the shuffled flag, and the result is compressed with the three listed compression
algorithms. We aren't given the compressed text (that would be way too easy), but we are given the lengths of the compressed text. From
this we can recover the flag.

The obvious insight here is that the closer our string is to the shuffled flag, the better the entire string will compress, as the algorithms will hopefully use our earlier string to represent part of the flag. We also have some control over which pieces of the flag appear where after shuffling; by tweaking the seed, we can spread the known text out rather than just having it all all the start and end of the flag. This makes the problem more tractable: it's fairly quick to iterate through all combinations of three letters; that's only 26^3 combinations (note we are told the 
unknown part of the flag is only upper case.) However, if we can find a shuffle that has known characters bracketing three unknown characters, we end up with a sequence of 5 good characters when we find the right combination rather than just 3. This is a much stronger signal and improves the chance that the compression will perform noticably better.

By sending a string of length one, we can determine (from the `none` compression) that the total flag is 25 characters long, and the unknown part is 18 characters long. Using a seed of `25632`, and replacing the unknown parts with `x`, we get the shuffled flag `xx{xnxxxDxxxxgxxxxx}xxSrx`.

From here we start to brute force. This was done semi-manually, but goes fairly quickly. We start with `xx{xn` and replace `xxx` with all combinations, then sort the results by the sum of the returned compression scores for each triple. In this case, the lowest scoring triples are  

```[('GTA', 218), ('UTA', 218), ('ATA', 218), ('DTA', 218), ('ITA', 218), ('CTA', 218), ('ETA', 218)]```

The first character is not recovered, but we are fairly sure the string `T{An` is in the shuffled flag. We can not try `T{anxxx` and so on.

By successive enumeration we can eventually recover the shuffled flag. Each trial takes about 35 seconds and recovers 2 or 3 characters; the total to recover is 18 characters, so recovery doesn't take very long. Unshuffling the flag at the end gives

```DrgnS{THISISACRIMEIGUESS}```




