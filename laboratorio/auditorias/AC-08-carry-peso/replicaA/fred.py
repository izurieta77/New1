import urllib.request, time, sys
for s in ["DFEDTARU","DFEDTAR","DFF","DTB3"]:
    for i in range(3):
        try:
            req = urllib.request.Request(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={s}")
            data = urllib.request.urlopen(req, timeout=60).read()
            open(f"{s}.csv","wb").write(data)
            lines = data.decode().strip().splitlines()
            print(s, len(lines), lines[0], lines[1], lines[-1]); break
        except Exception as e:
            print(s, "try", i, type(e).__name__, str(e)[:80]); time.sleep(3)
