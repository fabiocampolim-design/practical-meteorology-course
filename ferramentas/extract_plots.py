import json, base64, os

here = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(here)
for nb_name, tag in [("cap04_vapor", "c4"), ("cap05_estabilidade", "c5"),
                     ("cap06_nuvens", "c6")]:
    nb = json.load(open(os.path.join(root, "notebooks", f"{nb_name}.ipynb"), encoding="utf-8"))
    n = 0
    for cell in nb["cells"]:
        for out in cell.get("outputs", []):
            data = out.get("data", {})
            if "image/png" in data:
                n += 1
                with open(os.path.join(here, f"{tag}_plot{n:02d}.png"), "wb") as f:
                    f.write(base64.b64decode(data["image/png"]))
    print(tag, n, "plots")
