from pathlib import Path
import argparse
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import PillowWriter


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate an animated demo GIF from a trace.")
    parser.add_argument("--trace", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--title", default="MuJoCo reaching demo")
    args = parser.parse_args()

    trace = json.loads(Path(args.trace).read_text())
    ee_points = trace["ee_xy"]
    target = trace["target_xy"][0]

    fig, axis = plt.subplots(figsize=(5, 5))
    axis.set_xlim(0.0, 0.35)
    axis.set_ylim(0.0, 0.32)
    axis.set_title(args.title)
    axis.set_xlabel("x")
    axis.set_ylabel("y")
    axis.grid(True, alpha=0.3)
    target_artist = axis.scatter([target[0]], [target[1]], color="red", s=80, label="target")
    line, = axis.plot([], [], color="#2D6CDF", linewidth=2, label="trajectory")
    point = axis.scatter([], [], color="#0F9D58", s=70, label="end effector")
    axis.legend(loc="upper right")

    writer = PillowWriter(fps=12)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with writer.saving(fig, str(output_path), dpi=120):
        xs: list[float] = []
        ys: list[float] = []
        for ee in ee_points:
            xs.append(ee[0])
            ys.append(ee[1])
            line.set_data(xs, ys)
            point.set_offsets([[ee[0], ee[1]]])
            writer.grab_frame()
    plt.close(fig)
    print(f"Demo GIF written to {output_path}")


if __name__ == "__main__":
    main()

