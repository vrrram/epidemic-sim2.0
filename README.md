Rebuilding Epidemic Simulation in Python
 
## Quick Overview
This .NET WPF simulation can be rebuilt in Python with similar functionality but simpler deployment.
 
## Python Requirements
 
### Core Stack
```
Python 3.8+
pygame==2.5.0        # For visualization and particle rendering
numpy==1.24.0        # For efficient particle calculations
```
 
### Optional
```
matplotlib==3.7.0    # For statistics charts
pandas==2.0.0        # For data analysis
```
 
## Why Python is Better for This Project
 
### Advantages
- **No compilation**: Run directly with `python main.py`
- **Simpler distribution**: Single Python file vs .NET installer
- **Cross-platform**: Works on Windows/Mac/Linux (WPF is Windows-only)
- **Easier for students**: More accessible language
- **Faster prototyping**: Test changes instantly
 
### Disadvantages
- **Performance**: ~3x slower for 500+ particles (but fine for 200)
- **UI polish**: Less professional looking than WPF
- **Type safety**: No compile-time type checking (use type hints)
 
## Key Issues When Porting
 
### 1. **Particle Rendering**
**Issue**: WPF uses ItemsControl with data binding; Pygame uses direct drawing.
 
**Solution**:
```python
# Instead of XAML binding
for particle in particles:
    pygame.draw.circle(screen, particle.color,
                      (int(particle.x), int(particle.y)), 3)
```
 
### 2. **MVVM Pattern**
**Issue**: Python doesn't have built-in property change notification.
 
**Solution**: Skip MVVM, use simple classes:
```python
class Simulation:
    def __init__(self, params):
        self.particles = []
        self.stats = Statistics()
 
    def update(self):
        # All logic here
```
 
### 3. **Real-time Updates**
**Issue**: WPF uses DispatcherTimer; Pygame uses game loop.
 
**Solution**:
```python
clock = pygame.time.Clock()
while running:
    simulation.step()
    draw()
    clock.tick(30)  # 30 FPS
```
 
### 4. **UI Controls**
**Issue**: No XAML sliders/buttons.
 
**Solution**: Use pygame-gui library OR simple text UI:
```python
# Option 1: pygame-gui (recommended)
import pygame_gui
slider = pygame_gui.elements.UIHorizontalSlider(...)
 
# Option 2: Simple terminal + Pygame window
print("Press SPACE to start, R to reset")
```
 
## Lessons Learned
 
### Architecture
1. **Keep models separate**: `Particle`, `Boundary`, `SimulationEngine` classes work identically in Python
2. **Avoid over-engineering**: Python doesn't need interfaces/converters/MVVM boilerplate
3. **Use dataclasses**: Replace verbose C# properties with Python `@dataclass`
 
### Performance
1. **Vectorize with NumPy**: Calculate distances for all particles at once
2. **Spatial partitioning**: Grid-based neighbor finding (already in .NET code)
3. **Profile first**: `cProfile` reveals bottlenecks
 
### Code Structure
```
epidemic_sim/
├── main.py              # Entry point + game loop (100 lines)
├── models.py            # Particle, Boundary, SimulationParams (150 lines)
├── engine.py            # SimulationEngine (200 lines)
├── renderer.py          # Pygame drawing (50 lines)
├── ui.py                # Simple controls (optional, 100 lines)
└── requirements.txt
```
 
**Total: ~500-600 lines vs 2000+ in .NET**
 
## Quick Port Checklist
 
- [ ] Install pygame, numpy
- [ ] Port `Particle` class (use `@dataclass`)
- [ ] Port `SimulationEngine` (same logic, simpler syntax)
- [ ] Create Pygame window (800x600)
- [ ] Implement game loop with `clock.tick(30)`
- [ ] Draw particles with `pygame.draw.circle()`
- [ ] Add keyboard controls (SPACE=start/pause, R=reset, ESC=quit)
- [ ] Display stats with `pygame.font`
- [ ] Optional: Add pygame-gui sliders for parameters
 
## Minimal Example
 
```python
import pygame
import random
 
# Initialize
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
 
# Simple particle
class Particle:
    def __init__(self, x, y, infected=False):
        self.x, self.y = x, y
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)
        self.infected = infected
 
    def update(self):
        self.x += self.vx
        self.y += self.vy
        # Bounce off walls
        if self.x < 0 or self.x > 800: self.vx *= -1
        if self.y < 0 or self.y > 600: self.vy *= -1
 
# Create particles
particles = [Particle(random.randint(0, 800),
                      random.randint(0, 600),
                      i < 2) for i in range(100)]
 
# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
 
    # Update
    for p in particles:
        p.update()
 
    # Draw
    screen.fill((0, 0, 0))
    for p in particles:
        color = (255, 100, 50) if p.infected else (0, 191, 255)
        pygame.draw.circle(screen, color, (int(p.x), int(p.y)), 3)
 
    pygame.display.flip()
    clock.tick(30)
```
 
**This 40-line example shows the core concept. Extend with infection logic, stats, and controls.**
 
## Performance Tips
 
### For 200 particles (smooth):
- Direct Python loops are fine
- Update at 30 FPS
 
### For 500+ particles (optimization needed):
```python
import numpy as np
 
# Store all particle positions in numpy array
positions = np.array([[p.x, p.y] for p in particles])
 
# Calculate all pairwise distances at once (vectorized)
from scipy.spatial.distance import cdist
distances = cdist(positions, positions)
 
# Find infections (where distance < infection_radius)
infected_idx = np.where(state == INFECTED)[0]
susceptible_idx = np.where(state == SUSCEPTIBLE)[0]
# ...vectorized infection logic
```
 
## Deployment Comparison
 
### .NET WPF
```
- Requires .NET 6.0 Runtime (50+ MB download)
- Windows only
- Executable: ~100 MB (self-contained) or needs runtime
```
 
### Python
```
- Requires Python + pygame (~30 MB)
- Cross-platform (Windows/Mac/Linux)
- Distribute as .py files or use PyInstaller for .exe
```
 
## Final Recommendation
 
**For your school project**: Python is likely better because:
- ✅ Easier to demonstrate and modify during presentation
- ✅ Works on school computers with Python installed
- ✅ Simpler to understand and extend
- ✅ Better for adding charts/data export with matplotlib/pandas
 
**Stick with .NET if**:
- ❌ School requires Windows desktop apps specifically
- ❌ You need professional UI polish
- ❌ Performance with 1000+ particles matters
 
## Getting Started
 
```bash
# Install dependencies
pip install pygame numpy
 
# Create main.py with game loop (see example above)
# Port Particle and SimulationEngine classes from .NET code
# Keep the same logic, just simpler syntax
 
# Run
python main.py
```
 
---
 
**Bottom line**: Python version = same simulation logic, 1/4 the code, no compilation, cross-platform. Perfect for school projects.
