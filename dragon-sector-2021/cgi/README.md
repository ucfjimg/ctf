# CTF Gateway Interface

The challenge text:

* Real-world vulnerabilities bring many surprises. Anyone here remembers CGI?
* Note: To get the flag you need to run ./cgi-bin/x
* http://ctfgatewayinterface.hackable.software:8888/

The challenge was categorized as Miscellaneous, Easy. 42 teams solved it for a dynamic
score of 202 points.

We are given the Python source to the server. Connecting to the server gives us a login screen:

![CTFGatewayInterface login screen](https://github.com/ucfjimg/ctf/blob/master/dragon-sector-2021/cgi/index.png)

which we will never use again as we're just going to hit the endpoint with `curl` or a custom client.

Inspecting the source code gives a straightforward implementation of an `http` server in Python. The server can serve a handful of static resources (`index.html` and the images it uses). If the URI starts with `/cgi-bin/`, then the server parses it for a filename and query parameters. On most errors, `418 I'm a teapot` is returned, making it easier to play with the challenge initially on a local instance with proper logging. The two interesting things in `server.py` are

```
  if file_name.lower() == "x":
    return meh(s, 403,
      "Well, running x would give you the flag, so how about no.")
```

which prevents us from just asking for the flag directly, and 

```
  st = os.stat(file_path)
  if not (st.st_mode & stat.S_IEXEC):
    try:
      os.chmod(file_path, st.st_mode | stat.S_IEXEC)
    except PermissionError:
      return meh(s, 503, "Service Unavailable")
```

If the CGI script to be run exists, but isn't executable, the server sets it to be executable before trying to call it. Now if only we had a way to write into the `cgi-bin` directory where the scripts live...

Looking at the scripts already in that directory, we find three, plus a Python file with some helper functions. `startAuth.cgi` is used by the login page to write a salted, hashed version of the entered password to a session file, and `authResult.cgi` reads the hash back and compares it against the hash of the correct password. This, however, is a red herring; logging in won't get us any closer to the flag. The third script, called simply `x`, simply prints the fact that on the real server, it would print the flag.

Looking more deeply at `startAuth.cgi`, we note that it writes the session files into the `cgi-bin` folder! Here is what we're looking for: we know we can force the server to `chmod +x` the session file and execute it. The relevant code in `startAuth.cgi` is 

```
sid = os.urandom(20).hex()

hash = hashlib.sha256(SALT + decode_param_value(password)).digest()

with open(f"session_{sid}", "wb") as f:
  f.write(hash)

respond_and_exit({
    "sid": sid
})
```

We are returned the session id `sid`, so we can build the name of the script. We know the salt from the helper library (it's `SaltyMcSaltFace`) and `decode_param_value` just replaces any URI encodings with their proper values. We have reduced the challenge to the problem of finding a password that, when SHA-256 hashed with the salt, will produce a string that will execute `x`.

The file will be executed using the Python `subprocess.run` call. Any non-ASCII characters in the file will cause it to be treated as an image, so looking for `./x ` following by a random string is intractable. We have to find a hash with about 60 fixed bits - 32 for the first four bytes, and the low bit of all the other bits clear. (Even this isn't quite enough as the control characters 0x00-0x1f must also be omitted.) 2^60 is a bit much to brute force.

However, there is another option - using shebang syntax. If the first four bytes of the hash are `#!x\n`, then the kernel will treat `x` as a script interpreter. Whatever is after the newline is the script interpreter's problem, binary or not. We should be able to brute force 2^32 easily, and with a simple C program we do just that. The password (one possible of many) is

```AAAAEFCOHPN```

One other quirk remains: the server does not respond with a proper http header when the flag is recovered. `curl` errors out because of this. However, a simple Python script can do the same transaction. We recover the flag:

```DrgnS{valisMadeMeChangeTheFlagPfff}```


