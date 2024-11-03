import pygame
import numpy as np
import json
from datetime import datetime

# Configuration de la grille
CELL_SIZE = 10
GRID_WIDTH, GRID_HEIGHT = 800, 600
GRID_COLS = GRID_WIDTH // CELL_SIZE
GRID_ROWS = GRID_HEIGHT // CELL_SIZE

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (220, 220, 220)
HIGHLIGHT = (150, 150, 150)

class GameOfLife:
    """Classe pour gérer la logique du jeu de la vie."""
    def __init__(self, rows: int, cols: int, no_window_boundaries: bool):
        self.rows = rows
        self.cols = cols
        self.grid = np.zeros((rows, cols), dtype=int)
        self.no_window_boundaries = no_window_boundaries

    def update(self):
        """Met à jour l'état de chaque cellule en fonction des règles du jeu."""
        new_grid = np.copy(self.grid)
        for row in range(self.rows):
            for col in range(self.cols):
                if self.no_window_boundaries:
                    live_neighbors = self.count_live_neighbors_nolimits(row, col)
                else:
                    live_neighbors = self.count_live_neighbors(row, col)
                if self.grid[row, col] == 1:
                    if live_neighbors < 2 or live_neighbors > 3:
                        new_grid[row, col] = 0
                else:
                    if live_neighbors == 3:
                        new_grid[row, col] = 1
        self.grid = new_grid

    def count_live_neighbors(self, row, col):
        """Compte les voisins vivants autour de la cellule (row, col)."""
        total = 0
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if (i == row and j == col) or i < 0 or j < 0 or i >= self.rows or j >= self.cols:
                    continue
                total += self.grid[i, j]
        return total

    def count_live_neighbors_nolimits(self, row, col):
        """Compte les voisins vivants autour de la cellule (row, col) avec effet de bord cyclique."""
        total = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                # On évite de compter la cellule elle-même
                if i == 0 and j == 0:
                    continue
                # Calcul en utilisant le modulo pour créer l'effet cyclique
                neighbor_row = (row + i) % self.rows
                neighbor_col = (col + j) % self.cols
                total += self.grid[neighbor_row, neighbor_col]
        return total

    def toggle_cell(self, row, col):
        """Inverse l'état d'une cellule donnée."""
        self.grid[row, col] = 1 if self.grid[row, col] == 0 else 0

    def reset_grid(self):
        """Réinitialise la grille en mettant toutes les cellules à zéro."""
        self.grid = np.zeros((self.rows, self.cols), dtype=int)

    def save_initial_state(self, pattern_name):
        """Sauvegarde l'état initial avec un nom et les dimensions de la grille en format JSON."""
        live_cells = [(row, col) for row in range(self.rows) for col in range(self.cols) if self.grid[row, col] == 1]
        data = {
            "timestamp": datetime.now().isoformat(),
            "name": pattern_name,
            "rows": self.rows,
            "cols": self.cols,
            "live_cells": live_cells
        }
        # Chargement et sauvegarde de l'historique
        try:
            with open("initial_states.json", "r") as f:
                history = json.load(f)
        except FileNotFoundError:
            history = []
        history.append(data)
        # Sauvegarde sans saut de ligne entre les éléments
        with open("initial_states.json", "w") as f:
            json.dump(history, f, separators=(',', ':'))

    def load_initial_state(self, index):
        """Charge un état initial simplifié en JSON."""
        try:
            with open("initial_states.json", "r") as f:
                history = json.load(f)
                selected_state = history[index]["live_cells"]
                self.grid = np.zeros((self.rows, self.cols), dtype=int)
                for row, col in selected_state:
                    self.grid[row, col] = 1
        except (FileNotFoundError, IndexError):
            print("Aucun état initial valide trouvé.")

    def get_saved_states(self):
        """Retourne une liste des timestamps des états enregistrés."""
        try:
            with open("initial_states.json", "r") as f:
                history = json.load(f)
                return [entry["name"] for entry in history]
        except FileNotFoundError:
            return []

class GameView:
    """Classe pour gérer l'affichage du jeu de la vie."""
    def __init__(self, game):
        pygame.init()
        self.screen = pygame.display.set_mode((GRID_WIDTH, GRID_HEIGHT))
        pygame.display.set_caption("Jeu de la Vie")
        self.game = game
        self.font = pygame.font.SysFont(None, 24)
        self.speed = 10  # Vitesse initiale

    def draw_grid(self):
        """Dessine la grille de cellules et les lignes de la grille."""
        self.screen.fill(WHITE)
        for row in range(self.game.rows):
            for col in range(self.game.cols):
                color = BLACK if self.game.grid[row, col] == 1 else WHITE
                pygame.draw.rect(self.screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
        for x in range(0, GRID_WIDTH, CELL_SIZE):
            pygame.draw.line(self.screen, GRAY, (x, 0), (x, GRID_HEIGHT))
        for y in range(0, GRID_HEIGHT, CELL_SIZE):
            pygame.draw.line(self.screen, GRAY, (0, y), (GRID_WIDTH, y))

    def draw_instructions(self):
        """Affiche les instructions pour l'utilisateur."""
        instructions = [
            "Clique gauche : Ajouter / Supprimer une cellule",
            "Espace : Démarrer / Mettre en pause",
            "Flèche Haut / Bas : Augmenter / Diminuer la vitesse",
            "Raccourci [R] : Réinitialiser la grille",
            "Raccourci [S] : Sauvegarder l'état initial",
            "Raccourci [L] : Charger un état initial",
        ]
        y_offset = GRID_HEIGHT - len(instructions) * 20 - 10
        for line in instructions:
            text = self.font.render(line, True, BLACK)
            self.screen.blit(text, (10, y_offset))
            y_offset += 20


    def prompt_for_pattern_name(self):
        """Affiche une invite pour saisir le nom du pattern à sauvegarder."""
        pattern_name = ""
        input_active = True

        while input_active:
            self.screen.fill(WHITE)
            prompt_text = self.font.render("Nom du pattern : ", True, BLACK)
            name_text = self.font.render(pattern_name, True, BLACK)

            self.screen.blit(prompt_text, (10, 10))
            self.screen.blit(name_text, (10, 40))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        pattern_name = pattern_name[:-1]
                    else:
                        pattern_name += event.unicode
        return pattern_name

    def display_state_selection(self):
        """Affiche une fenêtre de sélection d'état avec un menu scrollable, y compris avec la molette de la souris."""
        saved_states = self.game.get_saved_states()
        if not saved_states:
            print("Aucun état enregistré trouvé.")
            return

        # Configuration du menu
        menu_width, menu_height = 400, 300
        menu_x, menu_y = (GRID_WIDTH - menu_width) // 2, (GRID_HEIGHT - menu_height) // 2
        menu_surface = pygame.Surface((menu_width, menu_height))
        menu_surface.fill(LIGHT_GRAY)

        # Configuration des boutons
        button_height = 30
        max_visible_buttons = menu_height // (button_height + 10)  # Nombre max de boutons visibles
        scroll_offset = 0  # Décalage de défilement initial

        selecting = True
        while selecting:
            # Gestion des événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Clic gauche seulement
                    # Gestion du clic sur un bouton
                    for i in range(scroll_offset, min(len(saved_states), scroll_offset + max_visible_buttons)):
                        rect = pygame.Rect(10, 10 + (i - scroll_offset) * (button_height + 10), menu_width - 20, button_height)
                        if rect.collidepoint(event.pos[0] - menu_x, event.pos[1] - menu_y):
                            self.game.load_initial_state(i)
                            selecting = False
                elif event.type == pygame.KEYDOWN:
                    # Défilement avec les flèches haut et bas
                    if event.key == pygame.K_DOWN and scroll_offset < len(saved_states) - max_visible_buttons:
                        scroll_offset += 1
                    elif event.key == pygame.K_UP and scroll_offset > 0:
                        scroll_offset -= 1
                    elif event.key == pygame.K_ESCAPE:
                        # Fermer le menu de sélection sur Échap
                        selecting = False
                elif event.type == pygame.MOUSEWHEEL:
                    # Défilement avec la molette de la souris sans sélection d'option
                    if event.y < 0 and scroll_offset < len(saved_states) - max_visible_buttons:
                        scroll_offset += 1
                    elif event.y > 0 and scroll_offset > 0:
                        scroll_offset -= 1

            # Dessin du menu
            menu_surface.fill(LIGHT_GRAY)  # Effacer le menu pour redessiner
            for i in range(scroll_offset, min(len(saved_states), scroll_offset + max_visible_buttons)):
                rect = pygame.Rect(10, 10 + (i - scroll_offset) * (button_height + 10), menu_width - 20, button_height)
                pygame.draw.rect(menu_surface, HIGHLIGHT if rect.collidepoint(pygame.mouse.get_pos()[0] - menu_x,
                                                                            pygame.mouse.get_pos()[1] - menu_y) else GRAY, rect)
                text = self.font.render(saved_states[i], True, BLACK)
                menu_surface.blit(text, (rect.x + 5, rect.y + 5))

            # Affichage du menu sur l'écran
            self.screen.blit(menu_surface, (menu_x, menu_y))
            pygame.display.flip()

    def update_display(self):
        """Met à jour l'affichage et gère les événements."""
        running = True
        clock = pygame.time.Clock()
        is_paused = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        is_paused = not is_paused
                    elif event.key == pygame.K_r:
                        self.game.reset_grid()
                        is_paused = True
                    elif event.key == pygame.K_s:
                        pattern_name = self.prompt_for_pattern_name()
                        if pattern_name:
                            self.game.save_initial_state(pattern_name)
                    elif event.key == pygame.K_l:
                        self.display_state_selection()
                    elif event.key == pygame.K_UP:
                        self.speed = min(60, self.speed + 1)
                    elif event.key == pygame.K_DOWN:
                        self.speed = max(1, self.speed - 1)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    col, row = x // CELL_SIZE, y // CELL_SIZE
                    self.game.toggle_cell(row, col)

            if not is_paused:
                self.game.update()

            self.draw_grid()
            self.draw_instructions()
            pygame.display.flip()
            clock.tick(self.speed)

        pygame.quit()

# Initialisation et démarrage du jeu
if __name__ == "__main__":
    game = GameOfLife(GRID_ROWS, GRID_COLS, True)
    view = GameView(game)
    view.update_display()
