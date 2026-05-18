import pygame
import sys
import math
import os
from main import solve_puzzle, update_used_words, update_full_dictionary

# Constants
WIDTH, HEIGHT = 900, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (247, 218, 33)
GRAY = (220, 220, 220)
DARK_GRAY = (169, 169, 169)
HEX_RADIUS = 60

def get_hexagon_points(center, radius):
    points = []
    for i in range(6):
        # Flat top: vertices at 0, 60, 120, 180, 240, 300 degrees
        angle_deg = 60 * i
        angle_rad = math.pi / 180 * angle_deg
        points.append((center[0] + radius * math.cos(angle_rad),
                       center[1] + radius * math.sin(angle_rad)))
    return points

def draw_hexagon(screen, center, radius, color, text="", font=None, is_selected=False):
    points = get_hexagon_points(center, radius)
    pygame.draw.polygon(screen, color, points)
    if is_selected:
        pygame.draw.polygon(screen, BLACK, points, 3)
    else:
        pygame.draw.polygon(screen, DARK_GRAY, points, 1)
    
    if text and font:
        text_surf = font.render(text.upper(), True, BLACK)
        text_rect = text_surf.get_rect(center=center)
        screen.blit(text_surf, text_rect)

def is_point_in_hexagon(point, center, radius):
    dist = math.sqrt((point[0] - center[0])**2 + (point[1] - center[1])**2)
    return dist < radius * 0.85

class Button:
    def __init__(self, x, y, w, h, text, color, font):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.font = font

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=5)
        pygame.draw.rect(screen, BLACK, self.rect, 1, border_radius=5)
        text_surf = self.font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

def draw_word_pill(surface, x, y, word, font, is_pangram=False):
    text_surf = font.render(word, True, BLACK)
    padding_x = 10
    padding_y = 4
    w = text_surf.get_width() + padding_x * 2
    h = text_surf.get_height() + padding_y * 2
    rect = pygame.Rect(x, y, w, h)
    color = YELLOW if is_pangram else GRAY
    pygame.draw.rect(surface, color, rect, border_radius=h//2)
    if is_pangram:
        pygame.draw.rect(surface, BLACK, rect, 1, border_radius=h//2)
    surface.blit(text_surf, (x + padding_x, y + padding_y))
    return w, h

def render_section(surface, title, words, font, y, width, is_pangram=False):
    title_surf = font.render(title, True, BLACK)
    surface.blit(title_surf, (10, y))
    y += 30
    
    curr_x = 10
    row_h = 0
    pill_font = pygame.font.SysFont("Arial", 16)
    for word in words:
        pill_w = pill_font.size(word)[0] + 20
        if curr_x + pill_w > width - 10:
            curr_x = 10
            y += row_h + 8
            row_h = 0
        
        w, h = draw_word_pill(surface, curr_x, y, word, pill_font, is_pangram)
        curr_x += w + 8
        row_h = max(row_h, h)
    
    return y + row_h + 20

def render_results(screen, used, full, pangrams, font, x, y, width, height, scroll_y):
    # Draw background and border
    pygame.draw.rect(screen, WHITE, (x, y, width, height))
    pygame.draw.rect(screen, GRAY, (x, y, width, height), 1)
    
    # Large virtual surface for scrolling
    virt_surface = pygame.Surface((width - 20, 5000))
    virt_surface.fill(WHITE)
    
    curr_y = 10
    header_font = pygame.font.SysFont("Arial", 20, bold=True)
    
    if pangrams:
        curr_y = render_section(virt_surface, f"Pangrams ({len(pangrams)})", pangrams, header_font, curr_y, width - 20, True)
    
    if used:
        curr_y = render_section(virt_surface, f"Used Words ({len(used)})", used, header_font, curr_y, width - 20)
        
    if full:
        curr_y = render_section(virt_surface, f"Other Words ({len(full)})", full, header_font, curr_y, width - 20)

    # Draw visible part
    screen.blit(virt_surface, (x + 10, y + 10), (0, scroll_y, width - 20, height - 20))
    
    return curr_y
    # Border
    pygame.draw.rect(screen, GRAY, (x, y, width, height), 1)
    
    return total_height

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Spelling Bee Solver")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 40, bold=True)
    small_font = pygame.font.SysFont("Arial", 18)
    button_font = pygame.font.SysFont("Arial", 20, bold=True)

    letters = [""] * 7
    selected_hex = 0
    results = None 
    status_msg = "Enter puzzle letters. Center hexagon is required."
    scroll_y = 0
    max_scroll = 0

    cx, cy = 250, 300
    # Spacing for flat-topped hexagons in a vertical arrangement
    h_dist = HEX_RADIUS * 1.5
    v_dist = HEX_RADIUS * math.sqrt(3) / 2
    
    # Add a small gap (5%)
    gap = 1.05
    h_dist *= gap
    v_dist *= gap

    hex_centers = [
        (cx, cy), # Center
        (cx, cy - v_dist * 2), # Top
        (cx + h_dist, cy - v_dist), # Top Right
        (cx + h_dist, cy + v_dist), # Bottom Right
        (cx, cy + v_dist * 2), # Bottom
        (cx - h_dist, cy + v_dist), # Bottom Left
        (cx - h_dist, cy - v_dist)  # Top Left
    ]

    buttons = [
        Button(50, 520, 100, 40, "Reset", GRAY, button_font),
        Button(160, 520, 100, 40, "Solve", YELLOW, button_font),
        Button(500, 520, 180, 40, "Update Used", GRAY, button_font),
        Button(700, 520, 180, 40, "Update Full Dict", GRAY, button_font),
    ]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if event.button == 4: # Scroll Up
                    scroll_y = max(0, scroll_y - 30)
                elif event.button == 5: # Scroll Down
                    scroll_y = min(max_scroll, scroll_y + 30)
                
                for i, center in enumerate(hex_centers):
                    if is_point_in_hexagon(pos, center, HEX_RADIUS):
                        selected_hex = i
                
                if buttons[0].is_clicked(pos):
                    letters = [""] * 7
                    results = None
                    scroll_y = 0
                    status_msg = "Board reset."
                elif buttons[1].is_clicked(pos):
                    if "" in letters:
                        status_msg = "Error: Please fill all 7 hexagons."
                    else:
                        puzzle = letters[0].upper() + "".join(letters[1:]).lower()
                        status_msg = "Solving..."
                        results = solve_puzzle(puzzle)
                        scroll_y = 0
                        if results[0] is None:
                            status_msg = results[3]
                            results = None
                        else:
                            status_msg = f"Found {len(results[0]) + len(results[1]) + len(results[2])} words!"
                elif buttons[2].is_clicked(pos):
                    status_msg = "Updating Used Words... Please wait."
                    screen.fill(WHITE)
                    btn_surf = button_font.render(status_msg, True, BLACK)
                    screen.blit(btn_surf, (50, 50))
                    pygame.display.flip()
                    update_used_words()
                    status_msg = "Used words updated!"
                elif buttons[3].is_clicked(pos):
                    status_msg = "Updating Full Dictionary..."
                    screen.fill(WHITE)
                    btn_surf = button_font.render(status_msg, True, BLACK)
                    screen.blit(btn_surf, (50, 50))
                    pygame.display.flip()
                    update_full_dictionary()
                    status_msg = "Full dictionary updated!"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    letters[selected_hex] = ""
                elif event.unicode.isalpha() and len(event.unicode) == 1:
                    letters[selected_hex] = event.unicode.upper()
                    for i in range(1, 8):
                        next_idx = (selected_hex + i) % 7
                        if letters[next_idx] == "":
                            selected_hex = next_idx
                            break

        screen.fill(WHITE)
        for i, center in enumerate(hex_centers):
            color = YELLOW if i == 0 else GRAY
            draw_hexagon(screen, center, HEX_RADIUS, color, letters[i], font, i == selected_hex)

        for btn in buttons:
            btn.draw(screen)

        if results:
            total_h = render_results(screen, results[0], results[1], results[2], small_font, 500, 50, 380, 450, scroll_y)
            max_scroll = max(0, total_h - 430)
        else:
            pygame.draw.rect(screen, GRAY, (500, 50, 380, 450), 1)
            res_title = small_font.render("Results will appear here...", True, DARK_GRAY)
            screen.blit(res_title, (510, 60))

        status_surf = small_font.render(status_msg, True, BLACK)
        screen.blit(status_surf, (50, 480))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
