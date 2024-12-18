import unittest
import numpy as np
import sys

sys.path.append('..')
sys.path.append('../..')

from src.app.app import GameOfLife

class TestGameOfLife(unittest.TestCase):

    def setUp(self):
        self.config = {
            'CELL_SIZE': 10,
            'GRID_WIDTH': 100,
            'GRID_HEIGHT': 100,
            'colors': {
                'WHITE': [255, 255, 255],
                'BLACK': [0, 0, 0],
                'GRAY': [128, 128, 128],
                'LIGHT_GRAY': [211, 211, 211],
                'HIGHLIGHT': [255, 0, 0]
            }
        }
        self.game = GameOfLife(self.config, no_window_boundaries=False)

    def test_initial_grid(self):
        self.assertEqual(self.game.grid.shape, (10, 10))
        self.assertTrue(np.array_equal(self.game.grid, np.zeros((10, 10), dtype=int)))

    def test_toggle_cell(self):
        self.game.toggle_cell(1, 1)
        self.assertEqual(self.game.grid[1, 1], 1)
        self.game.toggle_cell(1, 1)
        self.assertEqual(self.game.grid[1, 1], 0)

    def test_reset_grid(self):
        self.game.toggle_cell(1, 1)
        self.game.reset_grid()
        self.assertTrue(np.array_equal(self.game.grid, np.zeros((10, 10), dtype=int)))

    def test_count_live_neighbors(self):
        self.game.toggle_cell(1, 1)
        self.game.toggle_cell(1, 2)
        self.game.toggle_cell(2, 1)
        self.assertEqual(self.game.count_live_neighbors(1, 1), 2)
        self.assertEqual(self.game.count_live_neighbors(0, 0), 1)

    def test_count_live_neighbors_nolimits(self):
        self.game = GameOfLife(self.config, no_window_boundaries=True)
        self.game.toggle_cell(0, 0)
        self.game.toggle_cell(0, 9)
        self.game.toggle_cell(9, 0)
        self.assertEqual(self.game.count_live_neighbors_nolimits(0, 0), 2)
        self.assertEqual(self.game.count_live_neighbors_nolimits(9, 9), 3)

    def test_update(self):
        self.game.toggle_cell(1, 1)
        self.game.toggle_cell(1, 2)
        self.game.toggle_cell(2, 1)
        self.game.update()
        self.assertEqual(self.game.grid[1, 1], 1)
        self.assertEqual(self.game.grid[1, 2], 1)
        self.assertEqual(self.game.grid[2, 1], 1)
        self.assertEqual(self.game.grid[2, 2], 1)

    def test_save_and_load_initial_state(self):
        self.game.toggle_cell(1, 1)
        self.game.save_initial_state("test_pattern")
        self.game.reset_grid()
        self.game.load_initial_state(0)
        self.assertEqual(self.game.grid[1, 1], 0)

    def test_get_saved_states(self):
        self.game.save_initial_state("test_pattern")
        saved_states = self.game.get_saved_states()
        self.assertIn("test_pattern", saved_states)

if __name__ == '__main__':
    unittest.main()