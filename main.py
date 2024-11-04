from src.app.app import GameOfLife, GameView
from src.app.utils.config import load_config

if __name__ == "__main__":
    # Set the environment
    env = 'development'

    # Load the configuration
    config = load_config(f'{env}/settings.yaml')

    # Run the application
    game = GameOfLife(config, True)
    view = GameView(game, config)
    view.update_display()

