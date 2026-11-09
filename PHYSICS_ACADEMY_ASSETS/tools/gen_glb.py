"""Procedural glTF 2.0 binary (GLB) models: molecules, Earth + Moon, DNA helix. Pure numpy, no external 3D library."""
import json, math, struct
import numpy as np
from toolkit import out, hexrgb

def rgba(h, a=1.0): r, g, b = hexrgb(h); return [r / 255, g / 255, b / 255, a]

def uv_sphere(r, c=(0, 0, 0), lat=18, lon=28, color_fn=None):
    pos, nrm, col = [], [], []
    for i in range(lat + 1):
        th = math.pi * i / lat
        for j in range(lon + 1):
            ph = 2 * math.pi * j / lon; n = (math.sin(th) * math.cos(ph), math.cos(th), math.sin(th) * math.sin(ph))
            pos.append([c[0] + r * n[0], c[1] + r * n[1], c[2] + r * n[2]]); nrm.append(list(n))
            if color_fn: col.append(color_fn(n))
    idx = []
    for i in range(lat):
        for j in range(lon):
            a = i * (lon + 1) + j; b = a + lon + 1; idx += [a, a + 1, b, a + 1, b + 1, b]
    return dict(pos=np.array(pos, np.float32), nrm=np.array(nrm, np.float32), idx=np.array(idx, np.uint32), col=np.array(col, np.float32) if color_fn else None)

def cylinder(p0, p1, r, seg=14):
    p0, p1 = np.array(p0, float), np.array(p1, float); ax = p1 - p0; L = np.linalg.norm(ax); ax /= L
    t = np.array([1, 0, 0]) if abs(ax[0]) < .9 else np.array([0, 1, 0]); u = np.cross(ax, t); u /= np.linalg.norm(u); v = np.cross(ax, u)
    pos, nrm = [], []
    for k in range(seg + 1):
        a = 2 * math.pi * k / seg; n = u * math.cos(a) + v * math.sin(a)
        for p in (p0, p1): pos.append(p + n * r); nrm.append(n)
    idx = []
    for k in range(seg): a = 2 * k; idx += [a, a + 1, a + 2, a + 1, a + 3, a + 2]
    return dict(pos=np.array(pos, np.float32), nrm=np.array(nrm, np.float32), idx=np.array(idx, np.uint32), col=None)

def torus(R, r, c=(0, 0, 0), n=96, m=10):
    pos, nrm = [], []
    for i in range(n + 1):
        u = 2 * math.pi * i / n
        for j in range(m + 1):
            v = 2 * math.pi * j / m; nx, ny, nz = math.cos(u) * math.cos(v), math.sin(v), math.sin(u) * math.cos(v)
            pos.append([c[0] + (R + r * math.cos(v)) * math.cos(u), c[1] + r * math.sin(v), c[2] + (R + r * math.cos(v)) * math.sin(u)]); nrm.append([nx, ny, nz])
    idx = []
    for i in range(n):
        for j in range(m): a = i * (m + 1) + j; b = a + m + 1; idx += [a, a + 1, b, a + 1, b + 1, b]
    return dict(pos=np.array(pos, np.float32), nrm=np.array(nrm, np.float32), idx=np.array(idx, np.uint32), col=None)

def merge(meshes):
    pos, nrm, idx, col, off, any_col = [], [], [], [], 0, any(m["col"] is not None for m in meshes)
    for m in meshes:
        pos.append(m["pos"]); nrm.append(m["nrm"]); idx.append(m["idx"] + off); off += len(m["pos"])
        if any_col: col.append(m["col"] if m["col"] is not None else np.ones((len(m["pos"]), 4), np.float32))
    return dict(pos=np.concatenate(pos), nrm=np.concatenate(nrm), idx=np.concatenate(idx), col=np.concatenate(col) if any_col else None)

def _pad(b, ch=b"\x00"): return b + ch * ((-len(b)) % 4)

def write_glb(path, parts, generator="Physics Academy procedural"):
    """parts: list of dict(name, mesh, color, metallic, roughness)."""
    blob = bytearray(); views, accessors, meshes, materials, nodes = [], [], [], [], []
    def add_view(data, target):
        off = len(blob); blob.extend(_pad(data)); views.append({"buffer": 0, "byteOffset": off, "byteLength": len(data), "target": target}); return len(views) - 1
    for i, p in enumerate(parts):
        m = p["mesh"]; pos = m["pos"].astype(np.float32); nrm = m["nrm"].astype(np.float32); idx = m["idx"].astype(np.uint32)
        attrs = {}
        accessors.append({"bufferView": add_view(pos.tobytes(), 34962), "componentType": 5126, "count": int(len(pos)), "type": "VEC3", "min": pos.min(0).tolist(), "max": pos.max(0).tolist()}); attrs["POSITION"] = len(accessors) - 1
        accessors.append({"bufferView": add_view(nrm.tobytes(), 34962), "componentType": 5126, "count": int(len(nrm)), "type": "VEC3"}); attrs["NORMAL"] = len(accessors) - 1
        if m["col"] is not None:
            accessors.append({"bufferView": add_view(m["col"].astype(np.float32).tobytes(), 34962), "componentType": 5126, "count": int(len(pos)), "type": "VEC4"}); attrs["COLOR_0"] = len(accessors) - 1
        accessors.append({"bufferView": add_view(idx.tobytes(), 34963), "componentType": 5125, "count": int(len(idx)), "type": "SCALAR"}); ia = len(accessors) - 1
        materials.append({"name": p["name"], "pbrMetallicRoughness": {"baseColorFactor": p["color"], "metallicFactor": p.get("metallic", 0.05), "roughnessFactor": p.get("roughness", 0.5)}})
        meshes.append({"name": p["name"], "primitives": [{"attributes": attrs, "indices": ia, "material": i, "mode": 4}]}); nodes.append({"name": p["name"], "mesh": i})
    doc = {"asset": {"version": "2.0", "generator": generator}, "scene": 0, "scenes": [{"nodes": list(range(len(nodes)))}], "nodes": nodes, "meshes": meshes,
           "materials": materials, "accessors": accessors, "bufferViews": views, "buffers": [{"byteLength": len(blob)}]}
    js = _pad(json.dumps(doc, separators=(",", ":")).encode(), b" "); bn = bytes(blob)
    total = 12 + 8 + len(js) + 8 + len(bn)
    with open(out(*path), "wb") as f:
        f.write(struct.pack("<III", 0x46546C67, 2, total)); f.write(struct.pack("<II", len(js), 0x4E4F534A)); f.write(js); f.write(struct.pack("<II", len(bn), 0x004E4942)); f.write(bn)
    return total

# ───────── models ─────────
EL = {"H": ("#FFFFFF", .32), "C": ("#3A3A3A", .5), "O": ("#E8212A", .46), "N": ("#3050F8", .47)}
def molecules():
    s3 = 1 / math.sqrt(3); res = []
    mols = [
        ("H2O", [("O", (0, 0, 0)), ("H", (.87, -.673, 0)), ("H", (-.87, -.673, 0))], [(0, 1, 1), (0, 2, 1)]),
        ("CO2", [("C", (0, 0, 0)), ("O", (1.3, 0, 0)), ("O", (-1.3, 0, 0))], [(0, 1, 2), (0, 2, 2)]),
        ("CH4", [("C", (0, 0, 0))] + [("H", tuple(1.15 * s3 * v for v in vv)) for vv in ((1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1))], [(0, i, 1) for i in range(1, 5)]),
        ("NH3", [("N", (0, .25, 0))] + [("H", (.95 * math.cos(rad), -.35, .95 * math.sin(rad))) for rad in (math.pi / 2, math.pi * 7 / 6, math.pi * 11 / 6)], [(0, i, 1) for i in range(1, 4)]),
        ("O2", [("O", (-.6, 0, 0)), ("O", (.6, 0, 0))], [(0, 1, 2)]),
    ]
    buckets = {}; bonds = []
    for k, (name, atoms, bl) in enumerate(mols):
        ox = (k - 2) * 4.6
        for el, (x, y, z) in atoms:
            col, r = EL[el]; buckets.setdefault(el, []).append(uv_sphere(r, (x + ox, y, z)))
        for a, b, order in bl:
            A = np.array(atoms[a][1]) + [ox, 0, 0]; B = np.array(atoms[b][1]) + [ox, 0, 0]
            d = (B - A); d /= np.linalg.norm(d); off = np.cross(d, [0, 0, 1]); off = off / (np.linalg.norm(off) or 1) * .13 if order == 2 else np.zeros(3)
            for s in ((-1, 1) if order == 2 else (0,)): bonds.append(cylinder(A + off * s, B + off * s, .085 if order == 1 else .07))
    names = {"H": "Hydrogen", "C": "Carbon", "O": "Oxygen", "N": "Nitrogen"}
    parts = [dict(name=names[el], mesh=merge(ms), color=rgba(EL[el][0]), roughness=.35) for el, ms in buckets.items()]
    parts.append(dict(name="Bonds", mesh=merge(bonds), color=rgba("#B0B8C8"), metallic=.4, roughness=.4)); return parts

def earth_moon():
    def land(n):
        x, y, z = n; v = math.sin(3 * x + 1.2) * math.cos(2.5 * y) + math.sin(4 * z - .7) * math.cos(3 * x) + .5 * math.sin(7 * y + 2 * z)
        if abs(y) > .9: return rgba("#F4F8FF")
        if v > .55: return rgba("#8D6E3F")
        if v > .3: return rgba("#4CAF50")
        return rgba("#1E6FD9") if abs(y) < .8 else rgba("#2B82E8")
    earth = uv_sphere(1.0, (0, 0, 0), 48, 96, land); moon = uv_sphere(.27, (2.6, .25, 0), 24, 40); ring = torus(2.6, .012, (0, .25, 0))
    return [dict(name="Earth", mesh=earth, color=[1, 1, 1, 1], roughness=.7), dict(name="Moon", mesh=moon, color=rgba("#BDBDBD"), roughness=.9),
            dict(name="MoonOrbit", mesh=ring, color=rgba("#35D5E8"), metallic=0, roughness=.3)]

def dna():
    A, B, R = [], [], []; n, turns = 48, 3; H = 6.0
    for i in range(n + 1):
        t = i / n; a = 2 * math.pi * turns * t; y = H * t; pa = (.55 * math.cos(a), y, .55 * math.sin(a)); pb = (.55 * math.cos(a + math.pi), y, .55 * math.sin(a + math.pi))
        A.append(uv_sphere(.13, pa, 8, 12)); B.append(uv_sphere(.13, pb, 8, 12))
        if i % 3 == 0: R.append(cylinder(pa, pb, .05))
    return [dict(name="StrandA", mesh=merge(A), color=rgba("#35D5E8"), roughness=.3), dict(name="StrandB", mesh=merge(B), color=rgba("#F04FB5"), roughness=.3), dict(name="Rungs", mesh=merge(R), color=rgba("#EAF4FF"), roughness=.5)]

def run():
    r = {}
    r["molecules.glb"] = write_glb(("04_LABORATORIES", "3d_models", "molecules.glb"), molecules())
    r["earth_models.glb"] = write_glb(("04_LABORATORIES", "3d_models", "earth_models.glb"), earth_moon())
    r["dna_helix.glb"] = write_glb(("04_LABORATORIES", "3d_models", "dna_helix.glb"), dna()); return r

# ───────── validation + software preview ─────────
def read_glb(path):
    b = open(path, "rb").read(); magic, ver, total = struct.unpack("<III", b[:12]); assert magic == 0x46546C67 and ver == 2 and total == len(b), "bad header"
    jl, jt = struct.unpack("<II", b[12:20]); assert jt == 0x4E4F534A; doc = json.loads(b[20:20 + jl]); o = 20 + jl; bl, bt = struct.unpack("<II", b[o:o + 8]); assert bt == 0x004E4942
    return doc, b[o + 8:o + 8 + bl]
def validate(path):
    doc, blob = read_glb(path); assert doc["buffers"][0]["byteLength"] == len(blob) or len(blob) - doc["buffers"][0]["byteLength"] < 4
    sizes = {"SCALAR": 1, "VEC3": 3, "VEC4": 4}; ct = {5126: np.float32, 5125: np.uint32}
    for acc in doc["accessors"]:
        v = doc["bufferViews"][acc["bufferView"]]; n = sizes[acc["type"]] * acc["count"] * np.dtype(ct[acc["componentType"]]).itemsize; assert v["byteOffset"] + n <= len(blob) and v["byteLength"] >= n
        assert v["byteOffset"] % 4 == 0
        data = np.frombuffer(blob, ct[acc["componentType"]], sizes[acc["type"]] * acc["count"], v["byteOffset"])
        if "min" in acc: arr = data.reshape(-1, 3); assert np.allclose(arr.min(0), acc["min"], atol=1e-4) and np.allclose(arr.max(0), acc["max"], atol=1e-4)
    for m in doc["meshes"]:
        for p in m["primitives"]:
            cnt = doc["accessors"][p["attributes"]["POSITION"]]["count"]; ia = doc["accessors"][p["indices"]]; v = doc["bufferViews"][ia["bufferView"]]
            idx = np.frombuffer(blob, np.uint32, ia["count"], v["byteOffset"]); assert idx.max() < cnt and ia["count"] % 3 == 0
    return doc, blob
def preview(path, png, rot=(.35, -.5), size=420):
    from PIL import Image, ImageDraw
    doc, blob = validate(path); tris = []
    for m, mat in zip(doc["meshes"], doc["materials"]):
        p = m["primitives"][0]; pa = doc["accessors"][p["attributes"]["POSITION"]]; v = doc["bufferViews"][pa["bufferView"]]
        pos = np.frombuffer(blob, np.float32, pa["count"] * 3, v["byteOffset"]).reshape(-1, 3)
        ia = doc["accessors"][p["indices"]]; iv = doc["bufferViews"][ia["bufferView"]]; idx = np.frombuffer(blob, np.uint32, ia["count"], iv["byteOffset"]).reshape(-1, 3)
        col = None
        if "COLOR_0" in p["attributes"]: ca = doc["accessors"][p["attributes"]["COLOR_0"]]; cv = doc["bufferViews"][ca["bufferView"]]; col = np.frombuffer(blob, np.float32, ca["count"] * 4, cv["byteOffset"]).reshape(-1, 4)
        base = np.array(mat["pbrMetallicRoughness"]["baseColorFactor"][:3])
        for t in idx: tris.append((pos[t], col[t][:, :3].mean(0) if col is not None else base))
    allp = np.concatenate([t[0] for t in tris]); c = (allp.min(0) + allp.max(0)) / 2; sc = (size * .45) / (allp.max(0) - allp.min(0)).max()
    ax, ay = rot; Rx = np.array([[1, 0, 0], [0, math.cos(ax), -math.sin(ax)], [0, math.sin(ax), math.cos(ax)]]); Ry = np.array([[math.cos(ay), 0, math.sin(ay)], [0, 1, 0], [-math.sin(ay), 0, math.cos(ay)]])
    items = []
    for p3, col in tris:
        q = ((p3 - c) @ Ry.T) @ Rx.T; n = np.cross(q[1] - q[0], q[2] - q[0]); nl = np.linalg.norm(n)
        if nl < 1e-9: continue
        n /= nl; 
        if n[2] < 0: n = -n
        light = .35 + .65 * max(0, float(n @ np.array([.4, .6, .7]) / np.linalg.norm([.4, .6, .7])))
        items.append((q[:, 2].mean(), [(size / 2 + q[k, 0] * sc, size / 2 - q[k, 1] * sc) for k in range(3)], tuple(int(255 * min(1, x * light)) for x in col)))
    items.sort(key=lambda t: t[0]); im = Image.new("RGB", (size, size), (10, 16, 32)); d = ImageDraw.Draw(im)
    for _, pts, col in items: d.polygon(pts, fill=col)
    im.save(png); return len(tris)
if __name__ == "__main__":
    print(run())
    for n in ("molecules", "earth_models", "dna_helix"): print(n, "triangles:", preview(out("04_LABORATORIES", "3d_models", n + ".glb"), f"/tmp/{n}.png"))
