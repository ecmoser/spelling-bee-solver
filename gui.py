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

# Simplistic but elegant font choice with Linux fallbacks
MAIN_FONT = ["Verdana", "DejaVu Sans", "Liberation Sans", "Arial"]

def get_hexagon_points(center, radius):
    points = []
    for i in range(6):
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
    y += 35
    
    curr_x = 10
    row_h = 0
    pill_font = pygame.font.SysFont(MAIN_FONT, 14)
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
    pygame.draw.rect(screen, WHITE, (x, y, width, height))
    pygame.draw.rect(screen, GRAY, (x, y, width, height), 1)
    
    virt_surface = pygame.Surface((width - 20, 5000))
    virt_surface.fill(WHITE)
    
    curr_y = 10
    header_font = pygame.font.SysFont(MAIN_FONT, 18, bold=True)
    
    if pangrams:
        curr_y = render_section(virt_surface, f"PANGRAMS ({len(pangrams)})", pangrams, header_font, curr_y, width - 20, True)
    
    if used:
        curr_y = render_section(virt_surface, f"USED WORDS ({len(used)})", used, header_font, curr_y, width - 20)
        
    if full:
        curr_y = render_section(virt_surface, f"OTHER WORDS ({len(full)})", full, header_font, curr_y, width - 20)

    screen.blit(virt_surface, (x + 10, y + 10), (0, scroll_y, width - 20, height - 20))
    return curr_y

def draw_help_overlay(screen, font, small_font):
    # Dim the background
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((255, 255, 255, 230))
    screen.blit(overlay, (0, 0))
    
    box_w, box_h = 600, 420
    box_rect = pygame.Rect((WIDTH - box_w) // 2, (HEIGHT - box_h) // 2, box_w, box_h)
    pygame.draw.rect(screen, WHITE, box_rect)
    pygame.draw.rect(screen, BLACK, box_rect, 2)
    
    title = font.render("HOW TO USE", True, BLACK)
    screen.blit(title, (box_rect.centerx - title.get_width() // 2, box_rect.y + 30))
    
    instructions = [
        "1. Click a hexagon and type a letter to fill it.",
        "2. The center (Yellow) hexagon is the required letter.",
        "3. Press Backspace to clear a letter.",
        "4. Click 'SOLVE' to find all possible words.",
        "5. Use your mouse wheel to scroll through the results.",
        "6. Use 'UPDATE' buttons to download latest word lists.",
        "7. 'RESET' clears the entire board.",
        "8. Click anywhere to close this guide."
    ]
    
    curr_y = box_rect.y + 100
    for line in instructions:
        txt = small_font.render(line, True, BLACK)
        screen.blit(txt, (box_rect.x + 50, curr_y))
        curr_y += 35

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Spelling Bee Solver")
    clock = pygame.time.Clock()
    
    # Fonts
    font = pygame.font.SysFont(MAIN_FONT, 40, bold=True)
    small_font = pygame.font.SysFont(MAIN_FONT, 16)
    button_font = pygame.font.SysFont(MAIN_FONT, 18, bold=True)
    title_font = pygame.font.SysFont(MAIN_FONT, 38, bold=True)

    letters = [""] * 7
    selected_hex = 0
    results = None 
    status_msg = "Enter puzzle letters. All hexagons are required."
    scroll_y = 0
    max_scroll = 0
    show_help = False

    cx, cy = 250, 310
    h_dist = HEX_RADIUS * 1.5
    v_dist = HEX_RADIUS * math.sqrt(3) / 2
    gap = 1.05
    h_dist *= gap
    v_dist *= gap

    hex_centers = [
        (cx, cy), (cx, cy - v_dist * 2), (cx + h_dist, cy - v_dist),
        (cx + h_dist, cy + v_dist), (cx, cy + v_dist * 2),
        (cx - h_dist, cy + v_dist), (cx - h_dist, cy - v_dist)
    ]

    buttons = [
        Button(50, 520, 100, 40, "Reset", GRAY, button_font),
        Button(160, 520, 100, 40, "Solve", YELLOW, button_font),
        Button(500, 520, 180, 40, "Update Used", GRAY, button_font),
        Button(700, 520, 180, 40, "Update Full Dict", GRAY, button_font),
        Button(WIDTH - 100, 20, 80, 35, "Help", GRAY, small_font),
    ]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                
                if show_help:
                    show_help = False
                    continue

                if event.button == 4: # Scroll Up
                    scroll_y = max(0, scroll_y - 40)
                elif event.button == 5: # Scroll Down
                    scroll_y = min(max_scroll, scroll_y + 40)
                
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
                        solve_res = solve_puzzle(puzzle)
                        scroll_y = 0
                        if solve_res[0] is None:
                            status_msg = solve_res[3]
                            results = None
                        else:
                            results = solve_res
                            status_msg = f"Found {len(results[0]) + len(results[1]) + len(results[2])} words!"
                elif buttons[2].is_clicked(pos):
                    status_msg = "Updating Used Words..."
                    screen.fill(WHITE)
                    loading_surf = title_font.render("UPDATING...", True, BLACK)
                    screen.blit(loading_surf, (WIDTH // 2 - loading_surf.get_width() // 2, HEIGHT // 2 - 50))
                    msg_surf = small_font.render("Please wait, this may take a minute.", True, DARK_GRAY)
                    screen.blit(msg_surf, (WIDTH // 2 - msg_surf.get_width() // 2, HEIGHT // 2 + 20))
                    pygame.display.flip()
                    pygame.event.pump()
                    update_used_words()
                    status_msg = "Used words updated!"
                elif buttons[3].is_clicked(pos):
                    status_msg = "Updating Full Dictionary..."
                    screen.fill(WHITE)
                    loading_surf = title_font.render("UPDATING...", True, BLACK)
                    screen.blit(loading_surf, (WIDTH // 2 - loading_surf.get_width() // 2, HEIGHT // 2 - 50))
                    msg_surf = small_font.render("Downloading dictionary...", True, DARK_GRAY)
                    screen.blit(msg_surf, (WIDTH // 2 - msg_surf.get_width() // 2, HEIGHT // 2 + 20))
                    pygame.display.flip()
                    pygame.event.pump()
                    update_full_dictionary()
                    status_msg = "Full dictionary updated!"
                elif buttons[4].is_clicked(pos):
                    show_help = True

            if event.type == pygame.KEYDOWN and not show_help:
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
        
        # Draw Title
        title_surf = title_font.render("SPELLING BEE SOLVER", True, BLACK)
        screen.blit(title_surf, (cx - title_surf.get_width() // 2, 45))

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
        screen.blit(status_surf, (50, 485))

        if show_help:
            draw_help_overlay(screen, font, small_font)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
