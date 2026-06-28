#!/usr/bin/env python3
"""
Parametric layered wooden shutter frame example.

Conventions:
- all dimensions are millimetres
- all rotations are degrees
- each item is defined as a dictionary
- rectangular prisms are axis-aligned in local coordinates before rotation
- origin is the local minimum corner before rotation
- this example uses direct derived placement for layer stacking and simple
  face-to-face mating helpers for future extension
"""

from __future__ import annotations

import csv
import math
from pathlib import Path
from typing import Iterable

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


# ============================================================
# IMPORTS AND CONFIGURATION
# ============================================================
OUTPUT_STEM = "layered_shutter_frame_parametric"
OUT_DIR = Path("/mnt/data")
PNG_PATH = OUT_DIR / f"{OUTPUT_STEM}.png"
PDF_PATH = OUT_DIR / f"{OUTPUT_STEM}.pdf"
BOM_CSV_PATH = OUT_DIR / f"{OUTPUT_STEM}_bom.csv"

DPI = 220
FIGSIZE = (12, 8)

COLORS = {
    "polycarbonate": "#dff7ff",
    "solar": "#18385e",
    "steel": "#555555",
    "wood_front": "#d29a58",
    "wood_side": "#b67b3d",
    "wood_edge": "#5a3218",
    "wood_dark": "#8a5528",
}


# ============================================================
# INPUT PARAMETERS
# ============================================================
PARAMS = {
    # Overall face size
    "frame_w": 700.0,
    "frame_h": 1324.0,

    # Exterior / outside layers
    "polycarbonate_t": 10.0,
    "solar_panel_t": 20.0,
    "steel_t": 50.0,

    # Wooden front boards: 7 pcs side-by-side
    "front_board_count": 7,
    "front_board_w": 100.0,
    "front_board_t": 10.0,

    # Side boards and top side board
    "side_board_t": 10.0,
    "side_board_depth": 100.0,
    "top_side_board_t": 10.0,
    "top_side_board_depth": 100.0,
}


# ============================================================
# DERIVED PARAMETERS
# ============================================================
def derive_parameters(p: dict) -> dict:
    d = dict(p)
    d["x0"] = 0.0
    d["x1"] = d["frame_w"]
    d["y0"] = 0.0
    d["y1"] = d["frame_h"]

    d["poly_z0"] = 0.0
    d["poly_z1"] = d["poly_z0"] + d["polycarbonate_t"]
    d["solar_z0"] = d["poly_z1"]
    d["solar_z1"] = d["solar_z0"] + d["solar_panel_t"]
    d["steel_z0"] = d["solar_z1"]
    d["steel_z1"] = d["steel_z0"] + d["steel_t"]
    d["front_z0"] = d["steel_z1"]
    d["front_z1"] = d["front_z0"] + d["front_board_t"]
    d["side_z0"] = d["front_z1"]
    d["side_z1"] = d["side_z0"] + d["side_board_depth"]
    d["frame_t"] = d["side_z1"]

    d["side_y0"] = d["y0"]
    # side boards are shortened by top board thickness so the top board occupies the top end
    d["side_y1"] = d["y1"] - d["top_side_board_t"]
    d["top_side_y0"] = d["side_y1"]
    d["top_side_y1"] = d["y1"]
    return d

D = derive_parameters(PARAMS)


# ============================================================
# PART DICTIONARY DEFINITIONS
# ============================================================
def part(
    part_id: str,
    name: str,
    size: tuple[float, float, float],
    origin: tuple[float, float, float],
    material: str,
    profile: str,
    color: str,
    alpha: float = 0.95,
    rotation: tuple[float, float, float] = (0.0, 0.0, 0.0),
    cuts: list[dict] | None = None,
    notes: str = "",
) -> dict:
    return {
        "id": part_id,
        "name": name,
        "profile": profile,
        "size": tuple(float(v) for v in size),
        "origin": tuple(float(v) for v in origin),
        "rotation": tuple(float(v) for v in rotation),
        "cuts": cuts or [],
        "material": material,
        "color": color,
        "alpha": alpha,
        "notes": notes,
    }


def build_parts(d: dict) -> list[dict]:
    parts: list[dict] = []

    # Outside layers, size = x width, y height, z thickness
    parts.append(part(
        "L01", "polycarbonate sheet", (d["frame_w"], d["frame_h"], d["polycarbonate_t"]),
        (d["x0"], d["y0"], d["poly_z0"]), "polycarbonate", "700x1324x10 sheet",
        COLORS["polycarbonate"], 0.45, notes="outside protective surface"
    ))
    parts.append(part(
        "L02", "solar panel", (d["frame_w"], d["frame_h"], d["solar_panel_t"]),
        (d["x0"], d["y0"], d["solar_z0"]), "solar panel", "700x1324x20 panel",
        COLORS["solar"], 0.90, notes="outer visible solar layer"
    ))
    parts.append(part(
        "L03", "corrugated roofing steel", (d["frame_w"], d["frame_h"], d["steel_t"]),
        (d["x0"], d["y0"], d["steel_z0"]), "steel", "700x1324x50 profiled steel zone",
        COLORS["steel"], 0.92, notes="corrugation represented visually in side view"
    ))

    # Front boards
    for i in range(int(d["front_board_count"])):
        x0 = i * d["front_board_w"]
        parts.append(part(
            f"W{i+1:02d}", f"front board {i+1}",
            (d["front_board_w"], d["frame_h"], d["front_board_t"]),
            (x0, d["y0"], d["front_z0"]), "wood", f"{int(d['front_board_w'])}x{int(d['front_board_t'])} board",
            COLORS["wood_front"], 0.96, notes="one of seven vertical front boards"
        ))

    # Side frame boards
    parts.append(part(
        "S01", "left side board", (d["side_board_t"], d["side_y1"] - d["side_y0"], d["side_board_depth"]),
        (d["x0"], d["side_y0"], d["side_z0"]), "wood", "10x100 side board",
        COLORS["wood_side"], 0.96, notes="shortened 10 mm for top side board"
    ))
    parts.append(part(
        "S02", "right side board", (d["side_board_t"], d["side_y1"] - d["side_y0"], d["side_board_depth"]),
        (d["x1"] - d["side_board_t"], d["side_y0"], d["side_z0"]), "wood", "10x100 side board",
        COLORS["wood_side"], 0.96, notes="shortened 10 mm for top side board"
    ))
    parts.append(part(
        "S03", "top side board", (d["frame_w"], d["top_side_board_t"], d["top_side_board_depth"]),
        (d["x0"], d["top_side_y0"], d["side_z0"]), "wood", "10x100 top board",
        COLORS["wood_side"], 0.96, notes="covers the top end of both side boards"
    ))
    return parts

PARTS = build_parts(D)


# ============================================================
# GEOMETRY HELPERS
# ============================================================
def rotation_matrix_degrees(rx: float, ry: float, rz: float) -> np.ndarray:
    ax, ay, az = np.deg2rad([rx, ry, rz])
    cx, sx = math.cos(ax), math.sin(ax)
    cy, sy = math.cos(ay), math.sin(ay)
    cz, sz = math.cos(az), math.sin(az)
    rxm = np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]], dtype=float)
    rym = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]], dtype=float)
    rzm = np.array([[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]], dtype=float)
    return rzm @ rym @ rxm


def local_box_vertices(size: tuple[float, float, float]) -> np.ndarray:
    lx, ly, lz = size
    return np.array([
        [0, 0, 0], [lx, 0, 0], [lx, ly, 0], [0, ly, 0],
        [0, 0, lz], [lx, 0, lz], [lx, ly, lz], [0, ly, lz],
    ], dtype=float)


def world_vertices(p: dict) -> np.ndarray:
    vertices = local_box_vertices(tuple(p["size"]))
    r = rotation_matrix_degrees(*p.get("rotation", (0.0, 0.0, 0.0)))
    origin = np.array(p.get("origin", (0.0, 0.0, 0.0)), dtype=float)
    return vertices @ r.T + origin


def box_faces(vertices: np.ndarray) -> list[list[np.ndarray]]:
    idx = [[0, 1, 2, 3], [4, 5, 6, 7], [0, 1, 5, 4], [2, 3, 7, 6], [1, 2, 6, 5], [0, 3, 7, 4]]
    return [[vertices[i] for i in face] for face in idx]


def aabb(p: dict) -> tuple[np.ndarray, np.ndarray]:
    v = world_vertices(p)
    return v.min(axis=0), v.max(axis=0)


def translate_part(p: dict, delta: Iterable[float]) -> None:
    p["origin"] = tuple(np.array(p["origin"], dtype=float) + np.array(delta, dtype=float))


def face_coordinate(p: dict, face: str) -> float:
    mn, mx = aabb(p)
    axis = "xyz".index(face[0])
    return float(mn[axis] if face.endswith("min") else mx[axis])


# ============================================================
# MATING / PLACEMENT HELPERS
# ============================================================
def mate_face_to_face(
    moving_part: dict,
    fixed_part: dict,
    moving_face: str,
    fixed_face: str,
    clearance: float = 0.0,
) -> None:
    """Translate moving_part along one world axis so AABB faces touch."""
    axis = "xyz".index(moving_face[0])
    if axis != "xyz".index(fixed_face[0]):
        raise ValueError("Face-to-face AABB mating requires faces on the same axis")
    fixed_value = face_coordinate(fixed_part, fixed_face)
    moving_value = face_coordinate(moving_part, moving_face)
    sign = 1.0 if fixed_face.endswith("max") else -1.0
    delta = np.zeros(3)
    delta[axis] = fixed_value - moving_value + sign * clearance
    translate_part(moving_part, delta)


def overlap_amount(a: dict, b: dict) -> np.ndarray:
    amin, amax = aabb(a)
    bmin, bmax = aabb(b)
    return np.maximum(0.0, np.minimum(amax, bmax) - np.maximum(amin, bmin))


def check_overlaps(parts: list[dict], tolerance: float = 1e-6) -> list[str]:
    warnings: list[str] = []
    for i, pa in enumerate(parts):
        for pb in parts[i + 1:]:
            ov = overlap_amount(pa, pb)
            if float(np.prod(ov)) > tolerance:
                warnings.append(f"{pa['id']} overlaps {pb['id']} by {ov.round(3).tolist()} mm")
    return warnings


# ============================================================
# BILL OF MATERIALS OUTPUT
# ============================================================
def bom_rows(parts: list[dict]) -> list[dict]:
    rows = []
    for p in parts:
        lx, ly, lz = p["size"]
        vol = lx * ly * lz / 1_000_000_000.0
        rows.append({
            "id": p["id"],
            "name": p["name"],
            "material": p["material"],
            "profile": p["profile"],
            "quantity": 1,
            "length_x_mm": lx,
            "width_y_mm": ly,
            "height_z_mm": lz,
            "volume_m3_each": round(vol, 6),
            "origin_mm": p["origin"],
            "rotation_deg": p["rotation"],
            "cut_notes": "; ".join(c.get("note", "cut") for c in p.get("cuts", [])) or "none",
            "notes": p.get("notes", ""),
        })
    return rows


def write_bom_csv(parts: list[dict], path: Path) -> None:
    rows = bom_rows(parts)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


# ============================================================
# PLOTTING HELPERS
# ============================================================
def add_cuboid(ax, p: dict) -> None:
    v = world_vertices(p)
    poly = Poly3DCollection(
        box_faces(v), facecolors=p.get("color", "0.8"), edgecolors=COLORS["wood_edge"],
        linewidths=0.55, alpha=p.get("alpha", 0.95)
    )
    ax.add_collection3d(poly)
    c = v.mean(axis=0)
    ax.text(c[0], c[1], c[2], p["id"], ha="center", va="center", fontsize=7)


def add_rect(ax, x0: float, x1: float, y0: float, y1: float, fc: str, ec: str | None = None, lw: float = 1.1, alpha: float = 1.0) -> None:
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, facecolor=fc, edgecolor=ec or COLORS["wood_edge"], linewidth=lw, alpha=alpha))


def dim(ax, p0, p1, txt: str, offset=(0, 0), color="black") -> None:
    ax.annotate("", xy=p0, xytext=p1, arrowprops=dict(arrowstyle="<->", lw=1.0, color=color))
    ax.text((p0[0] + p1[0]) / 2 + offset[0], (p0[1] + p1[1]) / 2 + offset[1], txt, ha="center", va="center", fontsize=8.5, color=color)


def wood_grain(ax, x0, x1, y0, y1, orientation="v", n=4) -> None:
    if orientation == "v":
        for i in range(n):
            xx = x0 + (i + 1) * (x1 - x0) / (n + 1)
            ax.plot([xx, xx], [y0 + 10, y1 - 10], color=COLORS["wood_dark"], lw=0.45, alpha=0.55)
    else:
        for i in range(n):
            yy = y0 + (i + 1) * (y1 - y0) / (n + 1)
            ax.plot([x0 + 10, x1 - 10], [yy, yy], color=COLORS["wood_dark"], lw=0.45, alpha=0.55)


def corrugated_lines(ax, x0, x1, y0, y1, pitch=28, color="#333333") -> None:
    y = y0
    while y <= y1:
        ax.plot([x0, x1], [y, min(y + pitch / 2, y1)], color=color, lw=0.8, alpha=0.8)
        y += pitch


def plot_structure(parts: list[dict], d: dict, png_path: Path, pdf_path: Path) -> None:
    fig = plt.figure(figsize=FIGSIZE)

    ax3 = fig.add_subplot(2, 2, 1, projection="3d")
    for p in parts:
        add_cuboid(ax3, p)
    ax3.set_xlim(-40, d["frame_w"] + 40)
    ax3.set_ylim(-40, d["frame_h"] + 40)
    ax3.set_zlim(0, d["frame_t"] + 25)
    ax3.view_init(elev=22, azim=-58)
    ax3.set_box_aspect((d["frame_w"], d["frame_h"], 290))
    ax3.set_title("3D: layered shutter, mm")
    ax3.set_axis_off()

    axf = fig.add_subplot(2, 2, 2)
    for i in range(int(d["front_board_count"])):
        x0 = i * d["front_board_w"]
        x1 = x0 + d["front_board_w"]
        add_rect(axf, x0, x1, d["y0"], d["y1"], COLORS["wood_front"])
        wood_grain(axf, x0, x1, d["y0"], d["y1"], "v", 3)
        axf.text((x0 + x1) / 2, d["frame_h"] / 2, f"W{i+1:02d}", ha="center", va="center", fontsize=7)
    for i in range(1, int(d["front_board_count"])):
        xx = i * d["front_board_w"]
        axf.plot([xx, xx], [d["y0"], d["y1"]], color=COLORS["wood_edge"], lw=1.1)
    dim(axf, (0, d["frame_h"] + 55), (d["frame_w"], d["frame_h"] + 55), f"{int(d['frame_w'])} mm", (0, 18))
    dim(axf, (-55, 0), (-55, d["frame_h"]), f"{int(d['frame_h'])} mm", (-25, 0))
    dim(axf, (0, -45), (d["front_board_w"], -45), f"{int(d['front_board_w'])} mm", (0, -14))
    axf.set_aspect("equal")
    axf.set_xlim(-110, d["frame_w"] + 60)
    axf.set_ylim(-80, d["frame_h"] + 100)
    axf.axis("off")
    axf.set_title("Front view: 7 wooden boards")

    axs = fig.add_subplot(2, 2, 3)
    add_rect(axs, d["poly_z0"], d["poly_z1"], d["y0"], d["y1"], COLORS["polycarbonate"], "steelblue", alpha=0.55)
    add_rect(axs, d["solar_z0"], d["solar_z1"], d["y0"], d["y1"], COLORS["solar"], "black")
    add_rect(axs, d["steel_z0"], d["steel_z1"], d["y0"], d["y1"], COLORS["steel"], "black")
    corrugated_lines(axs, d["steel_z0"], d["steel_z1"], d["y0"], d["y1"])
    add_rect(axs, d["front_z0"], d["front_z1"], d["y0"], d["y1"], COLORS["wood_front"])
    add_rect(axs, d["side_z0"], d["side_z1"], d["side_y0"], d["side_y1"], COLORS["wood_side"])
    add_rect(axs, d["side_z0"], d["side_z1"], d["top_side_y0"], d["top_side_y1"], COLORS["wood_side"])
    dim(axs, (d["poly_z0"], -50), (d["poly_z1"], -50), "PC 10", (0, -13))
    dim(axs, (d["solar_z0"], -50), (d["solar_z1"], -50), "solar 20", (0, -13))
    dim(axs, (d["steel_z0"], -50), (d["steel_z1"], -50), "steel 50", (0, -13))
    dim(axs, (d["front_z0"], -50), (d["front_z1"], -50), "wood 10", (0, -13))
    dim(axs, (d["side_z0"], -50), (d["side_z1"], -50), "100 depth", (0, -13))
    dim(axs, (0, -95), (d["frame_t"], -95), f"{int(d['frame_t'])} mm total", (0, -15))
    dim(axs, (-45, 0), (-45, d["frame_h"]), f"{int(d['frame_h'])} mm", (-25, 0))
    axs.set_aspect("equal")
    axs.set_xlim(-100, d["frame_t"] + 90)
    axs.set_ylim(-140, d["frame_h"] + 70)
    axs.axis("off")
    axs.set_title("Side view: outside -> inside layer stack")

    axt = fig.add_subplot(2, 2, 4)
    add_rect(axt, 0, d["frame_w"], d["poly_z0"], d["poly_z1"], COLORS["polycarbonate"], "steelblue", alpha=0.55)
    add_rect(axt, 0, d["frame_w"], d["solar_z0"], d["solar_z1"], COLORS["solar"], "black")
    add_rect(axt, 0, d["frame_w"], d["steel_z0"], d["steel_z1"], COLORS["steel"], "black")
    add_rect(axt, 0, d["frame_w"], d["front_z0"], d["front_z1"], COLORS["wood_front"])
    for i in range(int(d["front_board_count"]) + 1):
        xx = i * d["front_board_w"]
        axt.plot([xx, xx], [d["front_z0"], d["front_z1"]], color=COLORS["wood_edge"], lw=0.8)
    add_rect(axt, d["x0"], d["x0"] + d["side_board_t"], d["side_z0"], d["side_z1"], COLORS["wood_side"])
    add_rect(axt, d["x1"] - d["side_board_t"], d["x1"], d["side_z0"], d["side_z1"], COLORS["wood_side"])
    add_rect(axt, 0, d["frame_w"], d["side_z0"], d["side_z1"], COLORS["wood_side"], lw=1.4, alpha=0.40)
    dim(axt, (0, d["frame_t"] + 45), (d["frame_w"], d["frame_t"] + 45), f"{int(d['frame_w'])} mm", (0, 15))
    dim(axt, (-45, d["poly_z0"]), (-45, d["poly_z1"]), "PC 10", (-30, 0))
    dim(axt, (-45, d["solar_z0"]), (-45, d["solar_z1"]), "solar 20", (-30, 0))
    dim(axt, (-45, d["steel_z0"]), (-45, d["steel_z1"]), "steel 50", (-30, 0))
    dim(axt, (-45, d["front_z0"]), (-45, d["front_z1"]), "wood 10", (-30, 0))
    dim(axt, (-45, d["side_z0"]), (-45, d["side_z1"]), "100 depth", (-30, 0))
    dim(axt, (0, -35), (d["front_board_w"], -35), f"{int(d['front_board_w'])} mm", (0, -12))
    axt.set_aspect("equal")
    axt.set_xlim(-130, d["frame_w"] + 40)
    axt.set_ylim(-70, d["frame_t"] + 90)
    axt.axis("off")
    axt.set_title("Top view: layer stack and side frame")

    fig.suptitle("Parametric layered shutter frame: PC + solar panel + steel + wooden box", fontsize=14, fontweight="bold")
    plt.tight_layout()
    fig.savefig(png_path, dpi=DPI, bbox_inches="tight")
    fig.savefig(pdf_path, bbox_inches="tight")
    plt.close(fig)


# ============================================================
# MAIN
# ============================================================
def main() -> None:
    warnings = check_overlaps(PARTS)
    for warning in warnings:
        # Intentional layer overlap is not expected. Touching faces have zero volume and are OK.
        print(f"Warning: {warning}")
    plot_structure(PARTS, D, PNG_PATH, PDF_PATH)
    write_bom_csv(PARTS, BOM_CSV_PATH)
    print(f"Wrote {PNG_PATH}")
    print(f"Wrote {PDF_PATH}")
    print(f"Wrote {BOM_CSV_PATH}")


if __name__ == "__main__":
    main()
