a = {"d": "hi", "ndict": {"a": "hello", "b": "world"}}

b = a["ndict"]
b["a"] = "goodbye"

print(a["ndict"]["a"])


import time

print(time.time())