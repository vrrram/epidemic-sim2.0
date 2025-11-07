"""
Spatial hash grid for efficient particle collision detection
Reduces infection checking from O(n²) to O(n) complexity
"""
from collections import defaultdict


class SpatialGrid:
    """
    2D spatial hash grid for efficient nearest-neighbor queries

    Maps continuous 2D space into discrete grid cells for fast proximity checks.
    Essential for performance when checking infection between particles.
    """

    def __init__(self, cell_size=0.2):
        """
        Initialize spatial grid

        Args:
            cell_size: Size of each grid cell (smaller = more cells, more precision)
        """
        self.cell_size = cell_size
        self.grid = defaultdict(list)

    def clear(self):
        """Clear all particles from the grid"""
        self.grid.clear()

    def _hash(self, x, y):
        """
        Hash continuous coordinates to discrete grid cell

        Args:
            x, y: Continuous coordinates

        Returns:
            tuple: (cell_x, cell_y) grid coordinates
        """
        return (int(x / self.cell_size), int(y / self.cell_size))

    def insert(self, particle):
        """
        Insert a particle into the grid

        Args:
            particle: Particle object with x, y attributes
        """
        cell = self._hash(particle.x, particle.y)
        self.grid[cell].append(particle)

    def get_nearby(self, x, y, radius=1):
        """
        Get all particles in nearby grid cells

        Args:
            x, y: Query position
            radius: Number of cells to search in each direction

        Returns:
            list: All particles in nearby cells
        """
        cell_x, cell_y = self._hash(x, y)
        nearby = []
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                nearby.extend(self.grid.get((cell_x + dx, cell_y + dy), []))
        return nearby
