#include <algorithm>
#include <chrono>
#include <cmath>
#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <vector>

struct SoilConfig {
  double cohesion;
  double friction_angle_deg;
  double compaction_rate;
  double blade_coupling;
  double spillover_rate;
};

struct BladeState {
  double x;
  double y;
  double width;
  double depth;
};

class TerrainGrid {
 public:
  TerrainGrid(double x_min, double x_max, double y_min, double y_max, int nx, int ny)
      : nx_(nx), ny_(ny), xs_(nx), ys_(ny), heights_(nx * ny, 0.0) {
    if (nx < 2 || ny < 2) {
      throw std::invalid_argument("terrain resolution must have at least two cells per axis");
    }
    for (int i = 0; i < nx; ++i) {
      xs_[i] = x_min + (x_max - x_min) * static_cast<double>(i) / static_cast<double>(nx - 1);
    }
    for (int j = 0; j < ny; ++j) {
      ys_[j] = y_min + (y_max - y_min) * static_cast<double>(j) / static_cast<double>(ny - 1);
    }
  }

  void add_pile(double cx, double cy, double radius, double height) {
    for (int i = 0; i < nx_; ++i) {
      for (int j = 0; j < ny_; ++j) {
        const double dx = xs_[i] - cx;
        const double dy = ys_[j] - cy;
        const double r = std::sqrt(dx * dx + dy * dy);
        const double pile = std::max(0.0, 1.0 - r / radius);
        at(i, j) = height * pile * pile;
      }
    }
  }

  double volume() const {
    return std::accumulate(heights_.begin(), heights_.end(), 0.0) * cell_area();
  }

  double cell_area() const {
    return (xs_[1] - xs_[0]) * (ys_[1] - ys_[0]);
  }

  double& at(int i, int j) {
    return heights_[static_cast<size_t>(i * ny_ + j)];
  }

  double at(int i, int j) const {
    return heights_[static_cast<size_t>(i * ny_ + j)];
  }

  int nx() const { return nx_; }
  int ny() const { return ny_; }
  double x(int i) const { return xs_[i]; }
  double y(int j) const { return ys_[j]; }

 private:
  int nx_;
  int ny_;
  std::vector<double> xs_;
  std::vector<double> ys_;
  std::vector<double> heights_;
};

double apply_blade_segment(TerrainGrid& terrain, const BladeState& start, const BladeState& end, const SoilConfig& soil) {
  const double dx = end.x - start.x;
  const double dy = end.y - start.y;
  const double distance = std::hypot(dx, dy);
  if (distance <= 1e-9) {
    return 0.0;
  }

  const double fx = dx / distance;
  const double fy = dy / distance;
  const double lx = -fy;
  const double ly = fx;
  const double resistance = 1.0 + soil.cohesion + std::tan(soil.friction_angle_deg * M_PI / 180.0) * 0.25;
  const double coupling = std::clamp(soil.blade_coupling / resistance, 0.0, 1.0);
  const double cut_height = std::max(0.0, end.depth);
  std::vector<double> removed(static_cast<size_t>(terrain.nx() * terrain.ny()), 0.0);
  double removed_volume = 0.0;
  double transported_volume = 0.0;

  for (int i = 0; i < terrain.nx(); ++i) {
    for (int j = 0; j < terrain.ny(); ++j) {
      const double rx = terrain.x(i) - end.x;
      const double ry = terrain.y(j) - end.y;
      const double along = rx * fx + ry * fy;
      const double cross = rx * lx + ry * ly;
      const bool in_blade = std::abs(cross) <= end.width * 0.5 && along >= -distance && along <= distance * 0.35;
      if (!in_blade) {
        continue;
      }
      const double cut = std::max(0.0, terrain.at(i, j) - cut_height) * coupling;
      terrain.at(i, j) -= cut;
      removed[static_cast<size_t>(i * terrain.ny() + j)] = cut;
      removed_volume += cut * terrain.cell_area();
      transported_volume += cut * (1.0 - std::clamp(soil.compaction_rate, 0.0, 0.9)) * terrain.cell_area();
    }
  }

  if (transported_volume <= 0.0) {
    return removed_volume;
  }

  const double spread_x = std::max(distance * (1.2 + soil.spillover_rate), 1e-6);
  const double spread_y = std::max(end.width * (0.45 + soil.spillover_rate), 1e-6);
  const double deposit_center = distance * 0.9;
  std::vector<double> weights(static_cast<size_t>(terrain.nx() * terrain.ny()), 0.0);
  double weight_integral = 0.0;
  for (int i = 0; i < terrain.nx(); ++i) {
    for (int j = 0; j < terrain.ny(); ++j) {
      const double rx = terrain.x(i) - end.x;
      const double ry = terrain.y(j) - end.y;
      const double along = rx * fx + ry * fy - deposit_center;
      const double cross = rx * lx + ry * ly;
      if (along < -spread_x * 0.5) {
        continue;
      }
      const double weight = std::exp(-0.5 * ((along / spread_x) * (along / spread_x) + (cross / spread_y) * (cross / spread_y)));
      weights[static_cast<size_t>(i * terrain.ny() + j)] = weight;
      weight_integral += weight * terrain.cell_area();
    }
  }
  for (int i = 0; i < terrain.nx(); ++i) {
    for (int j = 0; j < terrain.ny(); ++j) {
      terrain.at(i, j) += weights[static_cast<size_t>(i * terrain.ny() + j)] * transported_volume / weight_integral;
    }
  }
  return removed_volume;
}

struct KernelResult {
  double start_volume;
  double end_volume;
  double moved_volume;
};

KernelResult run_kernel_once() {
  TerrainGrid terrain(-0.55, 0.75, -0.35, 0.35, 72, 40);
  terrain.add_pile(-0.18, 0.0, 0.22, 0.12);
  const double start_volume = terrain.volume();
  const SoilConfig soil{0.12, 30.0, 0.06, 0.8, 0.22};
  const std::vector<BladeState> path{{-0.42, 0.0, 0.2, 0.014}, {-0.14, 0.0, 0.2, 0.014}, {0.14, 0.0, 0.2, 0.014}, {0.44, 0.0, 0.2, 0.014}};
  double moved_volume = 0.0;
  for (size_t i = 1; i < path.size(); ++i) {
    moved_volume += apply_blade_segment(terrain, path[i - 1], path[i], soil);
  }
  return KernelResult{start_volume, terrain.volume(), moved_volume};
}

int main(int argc, char** argv) {
  const int repeats = argc > 1 ? std::max(1, std::atoi(argv[1])) : 1;
  KernelResult result{};
  const auto start = std::chrono::steady_clock::now();
  for (int index = 0; index < repeats; ++index) {
    result = run_kernel_once();
  }
  const auto end = std::chrono::steady_clock::now();
  const double elapsed_ms = std::chrono::duration<double, std::milli>(end - start).count();
  std::cout << std::fixed << std::setprecision(8)
            << "repeats=" << repeats << "\n"
            << "elapsed_ms=" << elapsed_ms << "\n"
            << "mean_ms=" << elapsed_ms / static_cast<double>(repeats) << "\n"
            << "start_volume=" << result.start_volume << "\n"
            << "end_volume=" << result.end_volume << "\n"
            << "moved_volume=" << result.moved_volume << "\n";
  return result.moved_volume > 0.0 ? 0 : 2;
}
