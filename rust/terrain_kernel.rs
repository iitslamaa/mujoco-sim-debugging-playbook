use std::env;
use std::time::Instant;

#[derive(Clone, Copy)]
struct SoilConfig {
    cohesion: f64,
    friction_angle_deg: f64,
    compaction_rate: f64,
    blade_coupling: f64,
    spillover_rate: f64,
}

#[derive(Clone, Copy)]
struct BladeState {
    x: f64,
    y: f64,
    width: f64,
    depth: f64,
}

struct TerrainGrid {
    nx: usize,
    ny: usize,
    xs: Vec<f64>,
    ys: Vec<f64>,
    heights: Vec<f64>,
}

struct KernelResult {
    start_volume: f64,
    end_volume: f64,
    moved_volume: f64,
}

impl TerrainGrid {
    fn new(x_min: f64, x_max: f64, y_min: f64, y_max: f64, nx: usize, ny: usize) -> Self {
        assert!(nx >= 2 && ny >= 2, "terrain resolution must have at least two cells per axis");
        let xs = (0..nx)
            .map(|i| x_min + (x_max - x_min) * i as f64 / (nx - 1) as f64)
            .collect();
        let ys = (0..ny)
            .map(|j| y_min + (y_max - y_min) * j as f64 / (ny - 1) as f64)
            .collect();
        Self {
            nx,
            ny,
            xs,
            ys,
            heights: vec![0.0; nx * ny],
        }
    }

    fn add_pile(&mut self, cx: f64, cy: f64, radius: f64, height: f64) {
        for i in 0..self.nx {
            for j in 0..self.ny {
                let dx = self.xs[i] - cx;
                let dy = self.ys[j] - cy;
                let r = (dx * dx + dy * dy).sqrt();
                let pile = (1.0 - r / radius).max(0.0);
                let index = self.index(i, j);
                self.heights[index] = height * pile * pile;
            }
        }
    }

    fn volume(&self) -> f64 {
        self.heights.iter().sum::<f64>() * self.cell_area()
    }

    fn cell_area(&self) -> f64 {
        (self.xs[1] - self.xs[0]) * (self.ys[1] - self.ys[0])
    }

    fn index(&self, i: usize, j: usize) -> usize {
        i * self.ny + j
    }
}

fn apply_blade_segment(terrain: &mut TerrainGrid, start: BladeState, end: BladeState, soil: SoilConfig) -> f64 {
    let dx = end.x - start.x;
    let dy = end.y - start.y;
    let distance = dx.hypot(dy);
    if distance <= 1e-9 {
        return 0.0;
    }

    let fx = dx / distance;
    let fy = dy / distance;
    let lx = -fy;
    let ly = fx;
    let resistance = 1.0 + soil.cohesion + (soil.friction_angle_deg.to_radians()).tan() * 0.25;
    let coupling = (soil.blade_coupling / resistance).clamp(0.0, 1.0);
    let cut_height = end.depth.max(0.0);
    let mut removed_volume = 0.0;
    let mut transported_volume = 0.0;

    for i in 0..terrain.nx {
        for j in 0..terrain.ny {
            let rx = terrain.xs[i] - end.x;
            let ry = terrain.ys[j] - end.y;
            let along = rx * fx + ry * fy;
            let cross = rx * lx + ry * ly;
            let in_blade = cross.abs() <= end.width * 0.5 && along >= -distance && along <= distance * 0.35;
            if !in_blade {
                continue;
            }
            let index = terrain.index(i, j);
            let cut = (terrain.heights[index] - cut_height).max(0.0) * coupling;
            terrain.heights[index] -= cut;
            removed_volume += cut * terrain.cell_area();
            transported_volume += cut * (1.0 - soil.compaction_rate.clamp(0.0, 0.9)) * terrain.cell_area();
        }
    }

    if transported_volume <= 0.0 {
        return removed_volume;
    }

    let spread_x = (distance * (1.2 + soil.spillover_rate)).max(1e-6);
    let spread_y = (end.width * (0.45 + soil.spillover_rate)).max(1e-6);
    let deposit_center = distance * 0.9;
    let mut weights = vec![0.0; terrain.nx * terrain.ny];
    let mut weight_integral = 0.0;
    for i in 0..terrain.nx {
        for j in 0..terrain.ny {
            let rx = terrain.xs[i] - end.x;
            let ry = terrain.ys[j] - end.y;
            let along = rx * fx + ry * fy - deposit_center;
            let cross = rx * lx + ry * ly;
            if along < -spread_x * 0.5 {
                continue;
            }
            let weight = (-0.5 * ((along / spread_x).powi(2) + (cross / spread_y).powi(2))).exp();
            let index = terrain.index(i, j);
            weights[index] = weight;
            weight_integral += weight * terrain.cell_area();
        }
    }

    if weight_integral > 0.0 {
        for i in 0..terrain.nx {
            for j in 0..terrain.ny {
                let index = terrain.index(i, j);
                terrain.heights[index] += weights[index] * transported_volume / weight_integral;
            }
        }
    }

    removed_volume
}

fn run_kernel_once() -> KernelResult {
    let mut terrain = TerrainGrid::new(-0.55, 0.75, -0.35, 0.35, 72, 40);
    terrain.add_pile(-0.18, 0.0, 0.22, 0.12);
    let start_volume = terrain.volume();
    let soil = SoilConfig {
        cohesion: 0.12,
        friction_angle_deg: 30.0,
        compaction_rate: 0.06,
        blade_coupling: 0.8,
        spillover_rate: 0.22,
    };
    let path = [
        BladeState { x: -0.42, y: 0.0, width: 0.2, depth: 0.014 },
        BladeState { x: -0.14, y: 0.0, width: 0.2, depth: 0.014 },
        BladeState { x: 0.14, y: 0.0, width: 0.2, depth: 0.014 },
        BladeState { x: 0.44, y: 0.0, width: 0.2, depth: 0.014 },
    ];
    let mut moved_volume = 0.0;
    for window in path.windows(2) {
        moved_volume += apply_blade_segment(&mut terrain, window[0], window[1], soil);
    }
    KernelResult {
        start_volume,
        end_volume: terrain.volume(),
        moved_volume,
    }
}

fn main() {
    let repeats = env::args()
        .nth(1)
        .and_then(|value| value.parse::<usize>().ok())
        .unwrap_or(1)
        .max(1);
    let start = Instant::now();
    let mut result = KernelResult {
        start_volume: 0.0,
        end_volume: 0.0,
        moved_volume: 0.0,
    };
    for _ in 0..repeats {
        result = run_kernel_once();
    }
    let elapsed_ms = start.elapsed().as_secs_f64() * 1000.0;
    println!("repeats={}", repeats);
    println!("elapsed_ms={:.8}", elapsed_ms);
    println!("mean_ms={:.8}", elapsed_ms / repeats as f64);
    println!("start_volume={:.8}", result.start_volume);
    println!("end_volume={:.8}", result.end_volume);
    println!("moved_volume={:.8}", result.moved_volume);
}
