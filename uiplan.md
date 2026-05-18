# Pygame UI for Spelling Bee Solver

## Objective
Create a local desktop application using Pygame that provides a graphical interface for the Spelling Bee solver. The UI will mimic the NYT game layout with interactive hexagons for entering letters, and include controls to update word dictionaries, solve the puzzle, and reset the board.

## Scope & Impact
- **New Dependency:** Pygame will be added to `requirements.txt`.
- **New File:** A new file (e.g., `gui.py`) will be created to contain all Pygame rendering and event loop logic.
- **Refactoring:** Minor adjustments may be needed in `main.py`'s `solve_puzzle` function to return raw lists (or an object) of matched words instead of only a formatted string, making it easier to render results in the UI. 
- **Existing Logic:** The core trie, scraping, and solving logic will remain intact and be imported by the UI script.

## Proposed Solution
We will use Pygame to handle rendering and events.
1. **Layout:** 
   - **Left Side:** The 7 hexagons (1 yellow center, 6 gray surrounding).
   - **Right Side / Bottom:** A scrollable text area or simple list view to display the solved words, categorized into Used Words, Pangrams, and Remaining Words.
   - **Top/Bottom Controls:** Buttons for "Solve", "Reset", "Update Used Words", and "Update Full Dictionary".
2. **Interaction:**
   - The user can click on a hexagon to select it.
   - Typing on the keyboard will insert the letter into the selected hexagon.
   - The center hexagon will automatically be treated as the mandatory capital letter required by the solver.
3. **Integration:**
   - The "Solve" button will read the letters from the hexagons and call `solve_puzzle()`.
   - The "Update" buttons will trigger `update_used_words()` and `update_full_dictionary()` from `main.py`, showing a "Loading..." state in the UI while they run.

## Implementation Plan

### Phase 1: Setup and Pygame Scaffolding
- Add `pygame` to `requirements.txt`.
- Create `gui.py` and set up the basic Pygame event loop, window initialization, and color constants (Yellow, Gray, White, Black).

### Phase 2: Drawing the Hexagons
- Implement a function to calculate the vertices of a hexagon given a center coordinate and radius.
- Draw the 7 hexagons in a honeycomb pattern.
- Add text rendering inside the hexagons to display entered letters.

### Phase 3: User Input and State Management
- Add click detection to select which hexagon is currently active.
- Handle `KEYDOWN` events to capture letter input [A-Z] for the active hexagon.
- Add a "Reset" button that clears all hexagons.

### Phase 4: Integration with Solver
- Refactor `solve_puzzle` in `main.py` slightly to return the tuple `(used_word_matches, full_word_matches, pangrams)` so the UI can format it, or have `gui.py` parse the returned formatted string.
- Create a "Solve" button in Pygame. When clicked, it gathers the 7 letters (ensuring the center is treated as the required letter), validates the input, and calls the solver.
- Render the results on the screen (using a simple vertical text layout).

### Phase 5: Update Dictionary Controls
- Add buttons for "Update Used Words" and "Update Full Dictionary".
- Wire these buttons to call the respective functions in `main.py`. Provide visual feedback (e.g., changing text to "Updating...") during the process.

## Verification
- Verify that clicking each hexagon and typing works correctly.
- Verify that the center hexagon correctly acts as the mandatory letter.
- Test the "Solve" functionality with known puzzles to ensure output matches the CLI version.
- Verify that the dictionary update functions run successfully from within the Pygame app.
- Ensure the app can be closed gracefully.