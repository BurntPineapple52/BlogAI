import time
import sys
import os
import math
import random
from datetime import datetime

# --- Helper for ANSI Colors ---
class Colors:
    RESET = "\033[0m"
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    BRIGHT_BLACK = "\033[90m"  # Grey
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"

    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"
    BG_BRIGHT_BLACK = "\033[100m"
    BG_BRIGHT_RED = "\033[101m"
    BG_BRIGHT_GREEN = "\033[102m"
    BG_BRIGHT_YELLOW = "\033[103m"
    BG_BRIGHT_BLUE = "\033[104m"
    BG_BRIGHT_MAGENTA = "\033[105m"
    BG_BRIGHT_CYAN = "\033[106m"
    BG_BRIGHT_WHITE = "\033[107m"

    ALL_FG_COLORS = [
        RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE,
        BRIGHT_RED, BRIGHT_GREEN, BRIGHT_YELLOW, BRIGHT_BLUE, BRIGHT_MAGENTA, BRIGHT_CYAN, BRIGHT_WHITE
    ]
    RAINBOW_COLORS = [RED, YELLOW, GREEN, CYAN, BLUE, MAGENTA]

def clear_screen():
    """Clears the terminal screen."""
    # For Windows
    if os.name == 'nt':
        _ = os.system('cls')
    # For macOS and Linux
    else:
        _ = os.system('clear')
    # Alternative using ANSI:
    # sys.stdout.write("\033[2J\033[H")
    # sys.stdout.flush()

def show_message_before_anim(message, color=Colors.BRIGHT_YELLOW):
    clear_screen()
    print(f"{color}{message}{Colors.RESET}")
    print(f"{Colors.BRIGHT_BLACK}(Press Ctrl+C to stop and return to menu){Colors.RESET}\n")
    time.sleep(1.5) # Give time to read message

# --- ANIMATIONS ---

def anim_braille_spinner_colorized(delay=0.07, message="Processing"):
    show_message_before_anim("Animation: Colorized Braille Spinner")
    frames = ["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⣀"]
    colors = [Colors.BRIGHT_RED, Colors.BRIGHT_YELLOW, Colors.BRIGHT_GREEN, Colors.BRIGHT_CYAN,
              Colors.BRIGHT_BLUE, Colors.BRIGHT_MAGENTA, Colors.BRIGHT_WHITE, Colors.BRIGHT_BLACK]
    idx = 0
    try:
        while True:
            frame = frames[idx % len(frames)]
            color = colors[idx % len(colors)]
            text = f"\r{message}... {color}{frame}{Colors.RESET}  "
            sys.stdout.write(text)
            sys.stdout.flush()
            time.sleep(delay)
            idx += 1
    except KeyboardInterrupt:
        sys.stdout.write("\r" + " " * (len(message) + 10) + "\r") # Clear line
        sys.stdout.flush()
        return

def anim_filling_bar_gradient(delay=0.1, message="Loading", width=20):
    show_message_before_anim("Animation: Gradient Filling Bar")
    gradient_chars = ['░', '▒', '▓', '█']
    gradient_colors = [Colors.BLUE, Colors.CYAN, Colors.GREEN, Colors.YELLOW, Colors.RED]

    try:
        while True: # Loop the whole animation
            for i in range(width + 1):
                bar = ""
                for j in range(width):
                    if j < i:
                        # Determine color based on position in the filled part
                        color_idx = (j * (len(gradient_colors) -1)) // width
                        char_idx = (j * (len(gradient_chars) -1)) // width # less variation for char
                        bar += f"{gradient_colors[color_idx]}{gradient_chars[char_idx]}"
                    else:
                        bar += f"{Colors.BRIGHT_BLACK}." # Unfilled part
                percent = (i * 100) // width
                sys.stdout.write(f"\r{message}: [{bar}{Colors.RESET}] {percent}% ")
                sys.stdout.flush()
                time.sleep(delay)
            time.sleep(0.5) # Pause at 100%
            # Emptying (optional, or just restart)
            for i in range(width, -1, -1):
                bar = ""
                for j in range(width):
                    if j < i:
                        color_idx = (j * (len(gradient_colors) -1)) // width
                        char_idx = (j * (len(gradient_chars) -1)) // width
                        bar += f"{gradient_colors[color_idx]}{gradient_chars[char_idx]}"
                    else:
                        bar += f"{Colors.BRIGHT_BLACK}."
                percent = (i * 100) // width
                sys.stdout.write(f"\r{message}: [{bar}{Colors.RESET}] {percent}% ")
                sys.stdout.flush()
                time.sleep(delay/2) # Faster emptying
    except KeyboardInterrupt:
        sys.stdout.write("\r" + " " * (len(message) + width + 10) + "\r")
        sys.stdout.flush()
        return

def anim_bouncing_dots_rainbow(delay=0.15, message="Thinking", length=10):
    show_message_before_anim("Animation: Rainbow Bouncing Dots")
    positions = [" "] * length
    colors = Colors.RAINBOW_COLORS
    current_dot = 0
    direction = 1
    try:
        while True:
            # Place dot
            temp_positions = list(positions) # Create a mutable copy
            color_idx = (current_dot * len(colors)) // length
            temp_positions[current_dot] = f"{colors[color_idx]}●{Colors.RESET}"
            
            output = "".join(temp_positions)
            sys.stdout.write(f"\r{message} [{output}]")
            sys.stdout.flush()
            
            # Move dot
            current_dot += direction
            if current_dot >= length -1 :
                direction = -1
                current_dot = length -1 
            elif current_dot <= 0:
                direction = 1
                current_dot = 0
            
            time.sleep(delay)
    except KeyboardInterrupt:
        sys.stdout.write("\r" + " " * (len(message) + length + 5) + "\r")
        sys.stdout.flush()
        return

def anim_shuttle_with_stars(delay=0.15, message="Traveling", width=30):
    show_message_before_anim("Animation: Shuttle with Starry Background")
    shuttle_frames = [f"{Colors.BRIGHT_CYAN}<=>", f"{Colors.CYAN}-=-", f"{Colors.BRIGHT_CYAN}O=O"]
    shuttle_idx = 0
    position = 0
    direction = 1
    
    # Pre-generate a starry background string for efficiency
    star_chars = ['.', '*', '+', "'"]
    star_colors = [Colors.WHITE, Colors.BRIGHT_WHITE, Colors.BRIGHT_BLACK, Colors.YELLOW]
    
    background_line = list(" " * width)
    for i in range(width):
        if random.random() < 0.15: # 15% chance of a star
            background_line[i] = f"{random.choice(star_colors)}{random.choice(star_chars)}{Colors.RESET}"

    try:
        while True:
            current_shuttle = shuttle_frames[shuttle_idx % len(shuttle_frames)]
            shuttle_len = 3 # len("<=>") without colors

            # Create current frame
            frame_list = list(background_line) # Start with stars

            # Place shuttle, overwriting stars
            for i in range(shuttle_len):
                if 0 <= position + i < width:
                    # This is tricky with ANSI codes. A simpler approach:
                    # just replace characters at the shuttle's position.
                    # For now, let's place the shuttle directly.
                    pass # Shuttle will be placed on top

            # Construct the line with shuttle
            display_line = list(background_line)
            for i in range(len(current_shuttle)): # Iterate through visible chars + ANSI codes
                # This is still simplified as ANSI codes mess with simple string slicing/indexing for length
                # A better way would be to rebuild the string segment by segment.
                # For this example, let's assume shuttle length is fixed in display chars.
                pass
            
            # Simpler placement:
            prefix = "".join(display_line[:position])
            suffix = "".join(display_line[position + shuttle_len:])
            output_line = prefix + current_shuttle + suffix
            
            # Trim or pad to ensure consistent line width
            # (This is still hard due to invisible ANSI codes)
            # For now, we'll rely on \r and hope for the best or pad with spaces.
            actual_display_len = width + 20 # Estimate extra length for ANSI
            
            sys.stdout.write(f"\r{message}: [{output_line[:width]}] {Colors.RESET}      ") # Pad with spaces
            sys.stdout.flush()

            # Randomly "twinkle" some stars
            for i in range(width):
                 if background_line[i] != " " and random.random() < 0.05: # 5% chance to twinkle
                    background_line[i] = f"{random.choice(star_colors)}{random.choice(star_chars)}{Colors.RESET}"
                 elif background_line[i] == " " and random.random() < 0.01: # new star
                    background_line[i] = f"{random.choice(star_colors)}{random.choice(star_chars)}{Colors.RESET}"


            position += direction
            if position + shuttle_len > width or position < 0:
                direction *= -1
                position += direction * 2 # Correct overshoot
            
            shuttle_idx += 1
            time.sleep(delay)
    except KeyboardInterrupt:
        sys.stdout.write("\r" + " " * (len(message) + width + 20) + "\r")
        sys.stdout.flush()
        return

def anim_pulsing_star_color_shift(delay=0.1, message="Energizing"):
    show_message_before_anim("Animation: Pulsing Star with Color Shift")
    star_chars = ['.', 'o', 'O', '*', 'O', 'o']
    colors = Colors.RAINBOW_COLORS
    char_idx = 0
    color_idx = 0
    try:
        while True:
            char = star_chars[char_idx % len(star_chars)]
            color = colors[color_idx % len(colors)]
            
            output = f"{message}: {color}{char}{Colors.RESET}"
            # Pad to overwrite previous, longer frames if any (e.g. if message changes)
            sys.stdout.write(f"\r{output:<30}") 
            sys.stdout.flush()
            
            char_idx += 1
            if char_idx % len(star_chars) == 0: # Cycle color after one pulse cycle
                color_idx +=1
            
            time.sleep(delay)
    except KeyboardInterrupt:
        sys.stdout.write("\r" + " " * 35 + "\r")
        sys.stdout.flush()
        return

def anim_text_glitch_color(text="LLM THINKING", delay=0.05):
    show_message_before_anim("Animation: Colorful Text Glitch")
    original_text = list(text)
    text_len = len(original_text)
    glitch_chars = ['#', '$', '%', '&', '*', '@', '!', '?', '~', '/', '\\', '|', '_', '+', '-']
    
    try:
        while True:
            display_text_list = list(original_text)
            num_glitches = random.randint(1, max(1, text_len // 3)) 

            for _ in range(num_glitches):
                idx_to_glitch = random.randint(0, text_len - 1)
                if original_text[idx_to_glitch] != ' ': 
                    chosen_color = random.choice(Colors.ALL_FG_COLORS)
                    if random.random() < 0.6: 
                        display_text_list[idx_to_glitch] = f"{chosen_color}{random.choice(glitch_chars)}{Colors.RESET}"
                    else:
                        display_text_list[idx_to_glitch] = f"{chosen_color}{original_text[idx_to_glitch]}{Colors.RESET}"
            
            output = "\r" + "".join(display_text_list) + "..."
            # Pad generously to overwrite previous line content
            sys.stdout.write(output.ljust(text_len + 25)) 
            sys.stdout.flush()
            time.sleep(delay)
    except KeyboardInterrupt:
        sys.stdout.write("\r" + " " * (text_len + 25) + "\r")
        sys.stdout.flush()
        return

def anim_dna_helix(delay=0.15, width=20, height=5):
    show_message_before_anim("Animation: Twisting DNA Helix (Multi-line)")
    # Helix patterns: /, \, X, |
    # Colors for strands
    color1 = Colors.BRIGHT_CYAN
    color2 = Colors.BRIGHT_MAGENTA
    offset = 0
    try:
        while True:
            clear_screen() # Clear screen for multi-line
            print(f"{Colors.BRIGHT_YELLOW}DNA Helix Twisting... (Ctrl+C to stop){Colors.RESET}\n")
            for y in range(height):
                line = ""
                for x in range(width):
                    # Create a wave pattern for each strand
                    pos1 = (x + y + offset) % width
                    pos2 = (x - y + offset + width // 2) % width # Offset second strand

                    char = " "
                    # Strand 1
                    if abs(math.sin((x + y + offset) * 0.3) * (width / 4) + width / 2 - (width - 1 - x)) < 1.5 : # Adjust for density
                         char = f"{color1}/{Colors.RESET}" if (x + y + offset) % 4 < 2 else f"{color1}\\{Colors.RESET}"
                    # Strand 2
                    if abs(math.sin((x - y + offset + width//2) * 0.3) * (width / 4) + width / 2 - (width -1 -x)) < 1.5 :
                        # If char is already set by strand 1, make it 'X'
                        if char != " ":
                            char = f"{Colors.WHITE}X{Colors.RESET}"
                        else:
                            char = f"{color2}\\{Colors.RESET}" if (x - y + offset) % 4 < 2 else f"{color2}/{Colors.RESET}"
                    
                    # Simplified version (less "wavy", more direct)
                    # Determine character based on x, y, and offset to simulate twist
                    val = (x + offset + y*2) % 10 # Simple pattern
                    char_s = " "
                    if val < 2 : char_s = f"{color1}/{Colors.RESET}"
                    elif val < 4: char_s = f"{color1}-{Colors.RESET}"
                    elif val < 5: char_s = f"{color1}\\{Colors.RESET}"
                    
                    val2 = (x + offset - y*2 + 5) % 10
                    if val2 < 2 : char_s = f"{color2}\\{Colors.RESET}" if char_s == " " else f"{Colors.WHITE}X{Colors.RESET}"
                    elif val2 < 4: char_s = f"{color2}-{Colors.RESET}" if char_s == " " else f"{Colors.WHITE}#{Colors.RESET}"
                    elif val2 < 5: char_s = f"{color2}/{Colors.RESET}" if char_s == " " else f"{Colors.WHITE}X{Colors.RESET}"
                    
                    line += char_s if char_s != " " else " "


                # More robust simplified helix for this example
                line_render = ""
                for x_coord in range(width):
                    char_to_print = " "
                    # Strand 1: /-\
                    # Strand 2: \-/
                    # Combined: X =
                    s1_y = (math.sin( (x_coord + offset) * math.pi / (width/2) ) * (height/2.5) + height/2)
                    s2_y = (math.cos( (x_coord + offset) * math.pi / (width/2) ) * (height/2.5) + height/2)

                    on_s1 = abs(s1_y - y) < 0.8
                    on_s2 = abs(s2_y - y) < 0.8
                    
                    if on_s1 and on_s2:
                        line_render += f"{Colors.WHITE}X{Colors.RESET}"
                    elif on_s1:
                        line_render += f"{color1}o{Colors.RESET}"
                    elif on_s2:
                        line_render += f"{color2}o{Colors.RESET}"
                    else:
                        line_render += " "
                print(line_render)
            
            offset += 1
            sys.stdout.flush()
            time.sleep(delay)
    except KeyboardInterrupt:
        clear_screen()
        return

def anim_matrix_rain(height=20, width=60, delay=0.05):
    show_message_before_anim("Animation: Matrix Digital Rain (Multi-line)")
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789アァカサタナハマヤャラワガザダバパイィキシチニヒミリヰギジヂビピウゥクスツヌフムユュルグズブヅプエェケセテネヘメレヱゲゼデベペオォコソトノホモヨョロヲゴゾドボポヴッン"
    columns = [0] * width # Stores the y-coordinate of the head of the rain drop
    col_speeds = [random.uniform(0.2, 1.0) for _ in range(width)] # How many steps to advance
    col_progress = [0.0] * width # Fractional progress for speed
    col_lengths = [random.randint(height // 3, height - 2) for _ in range(width)]
    col_colors = [random.choice([Colors.GREEN, Colors.BRIGHT_GREEN]) for _ in range(width)]

    # Pre-allocate screen buffer for faster updates
    screen_buffer = [[' ' for _ in range(width)] for _ in range(height)]

    try:
        while True:
            # Update screen buffer first
            for r in range(height):
                for c in range(width):
                    # Fade existing characters
                    if screen_buffer[r][c] != ' ':
                        if random.random() < 0.15 : # Chance to fade or disappear
                           screen_buffer[r][c] = f"{Colors.GREEN}{screen_buffer[r][c].replace(Colors.BRIGHT_WHITE, '').replace(Colors.BRIGHT_GREEN, '').replace(Colors.GREEN, '').strip()}{Colors.RESET}" if random.random() > 0.3 else ' '
                        if screen_buffer[r][c].strip() == '': screen_buffer[r][c] = ' '


            for c in range(width):
                col_progress[c] += col_speeds[c]
                if col_progress[c] >= 1.0:
                    col_progress[c] = 0.0 # Reset progress

                    # Existing trail fades slightly
                    for r_idx in range(height):
                        if screen_buffer[r_idx][c] != ' ' and Colors.BRIGHT_WHITE in screen_buffer[r_idx][c]: # If it was a head
                            screen_buffer[r_idx][c] = f"{col_colors[c]}{random.choice(chars)}{Colors.RESET}"
                        elif screen_buffer[r_idx][c] != ' ': # Dim others
                             screen_buffer[r_idx][c] = f"{Colors.GREEN}{random.choice(chars)}{Colors.RESET}"


                    # New head character
                    head_y = columns[c]
                    if 0 <= head_y < height:
                        screen_buffer[head_y][c] = f"{Colors.BRIGHT_WHITE}{random.choice(chars)}{Colors.RESET}"
                    
                    # Move head down
                    columns[c] += 1

                    # Reset column if it goes off screen or length is met
                    if columns[c] >= height or columns[c] > col_lengths[c]:
                        if random.random() < 0.1: # Chance to restart a column
                            columns[c] = 0
                            col_lengths[c] = random.randint(height // 3, height - 2)
                            col_speeds[c] = random.uniform(0.1, 0.7)
                            col_colors[c] = random.choice([Colors.GREEN, Colors.BRIGHT_GREEN])
                        else: # Keep it off for a bit
                             columns[c] = height + random.randint(5, 20) # Delay restart

            # Print screen buffer
            sys.stdout.write("\033[H") # Move cursor to home position
            for r in range(height):
                sys.stdout.write("".join(screen_buffer[r]) + "\n")
            sys.stdout.flush()
            time.sleep(delay)

    except KeyboardInterrupt:
        clear_screen()
        return

def anim_fireplace(width=40, height=10, delay=0.1):
    show_message_before_anim("Animation: Cozy Fireplace (Multi-line)")
    flame_chars = [' ', '.', ':', '^', '*', '#', '@']
    flame_colors = [Colors.BLACK, Colors.RED, Colors.BRIGHT_RED, Colors.YELLOW, Colors.BRIGHT_YELLOW, Colors.WHITE] # From cool to hot

    # Initialize fire buffer
    fire = [[0 for _ in range(width)] for _ in range(height)]

    try:
        while True:
            # 1. Cool down existing fire
            for r in range(height):
                for c in range(width):
                    decay = random.randint(0, 2)
                    fire[r][c] = max(0, fire[r][c] - decay)
            
            # 2. Heat up the base
            for c in range(width // 4, 3 * width // 4): # Hotter in the middle base
                fire[height - 1][c] = random.randint(len(flame_colors) * 2 // 3, len(flame_colors) -1)
                if random.random() < 0.3: # Sparks
                     fire[height - 2][c] = random.randint(len(flame_colors)//2, len(flame_colors)-1)


            # 3. Propagate fire upwards (simple average blur and upward movement)
            for r in range(height - 2, -1, -1): # Iterate from bottom up
                for c in range(1, width - 1):
                    # Average with neighbors below, slightly biased upwards
                    avg_heat = (fire[r+1][c-1] + fire[r+1][c] + fire[r+1][c+1] + fire[r][c]) // 4
                    fire[r][c] = min(len(flame_colors) -1, avg_heat + random.randint(-1,1)) # Add some randomness

            # 4. Render
            sys.stdout.write("\033[H") # Move cursor to home
            print(f"{Colors.BRIGHT_BLACK}Fireplace (Ctrl+C to stop){Colors.RESET}\n")
            for r in range(height):
                line = ""
                for c in range(width):
                    heat_val = fire[r][c]
                    char_idx = min(heat_val, len(flame_chars) -1)
                    color_idx = min(heat_val, len(flame_colors) -1)
                    if heat_val == 0:
                        line += " "
                    else:
                        line += f"{flame_colors[color_idx]}{flame_chars[char_idx]}{Colors.RESET}"
                print(line)
            
            # Logs (static part)
            log_color = Colors.YELLOW # Represents wood color, not burning part
            print(f"{log_color}{'~' * (width // 2):^{width}}{Colors.RESET}")
            print(f"{log_color}{'=' * width}{Colors.RESET}")

            sys.stdout.flush()
            time.sleep(delay)
    except KeyboardInterrupt:
        clear_screen()
        return

def anim_clock(delay=1.0): # Update every second
    show_message_before_anim("Animation: Analog ASCII Clock (Multi-line)")
    size = 10 # Radius of the clock face
    
    def plot_line(x0, y0, x1, y1):
        """Bresenham's line algorithm to find points on the line."""
        points = []
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy

        while True:
            points.append((x0, y0))
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy
        return points

    try:
        while True:
            now = datetime.now()
            hour = now.hour % 12
            minute = now.minute
            second = now.second

            # Create clock face grid
            grid_size = size * 2 + 3
            grid = [[' ' for _ in range(grid_size)] for _ in range(grid_size)]
            center_x, center_y = size + 1, size + 1

            # Draw clock outline (circle)
            for angle_deg in range(0, 360, 10): # Draw circle points
                angle_rad = math.radians(angle_deg)
                x = int(center_x + size * math.cos(angle_rad))
                y = int(center_y + size * math.sin(angle_rad) / 2) # Adjust for char aspect ratio
                if 0 <= x < grid_size and 0 <= y < grid_size:
                    grid[y][x] = f"{Colors.BRIGHT_BLACK}.{Colors.RESET}"
            
            # Draw hour markers
            for h in range(12):
                angle_rad = math.radians(h * 30 - 90) # 0 degrees is 3 o'clock
                x_marker = int(center_x + (size-1) * math.cos(angle_rad))
                y_marker = int(center_y + (size-1) * math.sin(angle_rad)/2)
                if 0 <= x_marker < grid_size and 0 <= y_marker < grid_size:
                    grid[y_marker][x_marker] = f"{Colors.WHITE}o{Colors.RESET}"


            # Hour hand
            hour_angle = math.radians((hour + minute / 60) * 30 - 90)
            hour_len = size * 0.5
            hx = int(center_x + hour_len * math.cos(hour_angle))
            hy = int(center_y + hour_len * math.sin(hour_angle) / 2)
            for px, py in plot_line(center_x, center_y, hx, hy):
                 if 0 <= px < grid_size and 0 <= py < grid_size: grid[py][px] = f"{Colors.RED}H{Colors.RESET}"

            # Minute hand
            minute_angle = math.radians((minute + second / 60) * 6 - 90)
            minute_len = size * 0.7
            mx = int(center_x + minute_len * math.cos(minute_angle))
            my = int(center_y + minute_len * math.sin(minute_angle) / 2)
            for px, py in plot_line(center_x, center_y, mx, my):
                 if 0 <= px < grid_size and 0 <= py < grid_size: grid[py][px] = f"{Colors.GREEN}M{Colors.RESET}"

            # Second hand
            second_angle = math.radians(second * 6 - 90)
            second_len = size * 0.9
            sx = int(center_x + second_len * math.cos(second_angle))
            sy = int(center_y + second_len * math.sin(second_angle) / 2)
            for px, py in plot_line(center_x, center_y, sx, sy):
                 if 0 <= px < grid_size and 0 <= py < grid_size: grid[py][px] = f"{Colors.BLUE}s{Colors.RESET}"
            
            grid[center_y][center_x] = f"{Colors.WHITE}@{Colors.RESET}" # Center pivot

            # Print the clock
            sys.stdout.write("\033[H") # Move cursor to home
            print(f"{Colors.BRIGHT_YELLOW}ASCII Clock (Ctrl+C to stop){Colors.RESET}")
            digital_time = now.strftime("%H:%M:%S")
            print(f"{Colors.CYAN}{digital_time:^{grid_size*2}}{Colors.RESET}\n") # Digital time above

            for row in grid:
                print("".join(f"{char}" for char in row)) # Each char might have ANSI
            sys.stdout.flush()
            time.sleep(delay)

    except KeyboardInterrupt:
        clear_screen()
        return


# --- STATIC ASCII ART ---
def art_dragon():
    clear_screen()
    print(f"{Colors.BRIGHT_GREEN}Static Art: Dragon{Colors.RESET}")
    print(f"{Colors.BRIGHT_BLACK}(Press Enter to return to menu){Colors.RESET}\n")
    art = r"""
                      🐲
                    .--""--.
                   /        \
                  |  O  _  O |
                  |   (/ \/ \)|
                 राजा \ `--` /🐉
                 /    `----`    \
                /  DAVID          \
               PREETHAM       .--""--.
              /  .--""--.  /        \
             (REQUESTED  )(  O  _  O )
              \  `----`  / \ ( / \/ \) /
               `.______.'   \ `-----` /
                             `._____.'
    """ # Using emojis too!
    print(f"{Colors.GREEN}{art}{Colors.RESET}")
    input()

def art_computer_cat():
    clear_screen()
    print(f"{Colors.BRIGHT_CYAN}Static Art: Computer Cat{Colors.RESET}")
    print(f"{Colors.BRIGHT_BLACK}(Press Enter to return to menu){Colors.RESET}\n")
    art = rf"""
{Colors.BRIGHT_BLACK}  __________________________________________________
 /                                                 \\
|    _________________________________________    |
|   |                                         |   |
|   |  {Colors.CYAN}Terminal App Loading Screen Fun!{Colors.RESET}{Colors.BRIGHT_BLACK}     |   |
|   |                                         |   |
|   |  {Colors.GREEN}* Colorized Braille Spinner{Colors.RESET}{Colors.BRIGHT_BLACK}             |   |
|   |  {Colors.YELLOW}* Gradient Filling Bar{Colors.RESET}{Colors.BRIGHT_BLACK}                |   |
|   |  {Colors.MAGENTA}* Rainbow Bouncing Dots{Colors.RESET}{Colors.BRIGHT_BLACK}               |   |
|   |  {Colors.RED}* And many more...{Colors.RESET}{Colors.BRIGHT_BLACK}                  |   |
|   |_________________________________________|   |
|                                                   |
 \_________________________________________________/
        \___________________________________/
     {Colors.WHITE}___________________________________________( )รีวิวสล็อตเว็บนอก{Colors.BRIGHT_BLACK}
  {Colors.WHITE} /___________________________________________/ \{Colors.BRIGHT_BLACK}
 {Colors.WHITE}(___________ขายบ้านศรีราชา_______________________){Colors.BRIGHT_BLACK}

      /\_/\           -----
     ( o.o )        / Hello \
      > ^ <         |  User!|
     /  `'\          \  -----
    |     |           -----
   (_M_M_|)
    """
    print(art) # Colors are embedded
    input()

def art_hello_world_banner():
    clear_screen()
    print(f"{Colors.BRIGHT_MAGENTA}Static Art: Hello World Banner{Colors.RESET}")
    print(f"{Colors.BRIGHT_BLACK}(Press Enter to return to menu){Colors.RESET}\n")
    art_lines = [
        "██╗  ██╗███████╗██╗     ██╗      ██████╗     ██╗    ██╗ ██████╗ ██╗     ██████╗ ██╗   ██╗",
        "██║  ██║██╔════╝██║     ██║     ██╔═══██╗    ██║    ██║██╔═══██╗██║     ██╔══██╗╚██╗ ██╔╝",
        "███████║█████╗  ██║     ██║     ██║   ██║    ██║ █╗ ██║██║   ██║██║     ██████╔╝ ╚████╔╝ ",
        "██╔══██║██╔══╝  ██║     ██║     ██║   ██║    ██║███╗██║██║   ██║██║     ██╔═══╝   ╚██╔╝  ",
        "██║  ██║███████╗███████╗███████╗╚██████╔╝    ╚███╔███╔╝╚██████╔╝███████╗██║        ██║   ",
        "╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝ ╚═════╝      ╚══╝╚══╝  ╚═════╝ ╚══════╝╚═╝        ╚═╝   "
    ]
    colors = [Colors.RED, Colors.BRIGHT_RED, Colors.YELLOW, Colors.BRIGHT_YELLOW, Colors.GREEN, Colors.BRIGHT_GREEN]
    for i, line in enumerate(art_lines):
        print(f"{colors[i % len(colors)]}{line}{Colors.RESET}")
    input()


# --- Main Menu ---
def display_menu():
    clear_screen()
    print(f"{Colors.BRIGHT_YELLOW}--- ASCII Art & Animation Showcase ---{Colors.RESET}")
    print(f"{Colors.CYAN}Select an option:{Colors.RESET}")

    options = {
        "1": ("Colorized Braille Spinner", anim_braille_spinner_colorized),
        "2": ("Gradient Filling Bar", anim_filling_bar_gradient),
        "3": ("Rainbow Bouncing Dots", anim_bouncing_dots_rainbow),
        "4": ("Shuttle with Stars", anim_shuttle_with_stars), # Might be flickery
        "5": ("Pulsing Star Color Shift", anim_pulsing_star_color_shift),
        "6": ("Colorful Text Glitch", anim_text_glitch_color),
        "7": ("Twisting DNA Helix (Multi-line)", anim_dna_helix), # Complex
        "8": ("Matrix Digital Rain (Multi-line)", anim_matrix_rain),
        "9": ("Cozy Fireplace (Multi-line)", anim_fireplace),
        "10": ("Analog ASCII Clock (Multi-line)", anim_clock),
        "A1": ("Static: Dragon", art_dragon),
        "A2": ("Static: Computer Cat", art_computer_cat),
        "A3": ("Static: Hello World Banner", art_hello_world_banner),
        "Q": ("Quit", None)
    }

    for key, (name, _) in options.items():
        cat_color = Colors.GREEN if key.isdigit() else Colors.MAGENTA
        print(f"  {cat_color}{key}{Colors.RESET}) {name}")
    
    choice = input(f"\n{Colors.BRIGHT_WHITE}Enter your choice: {Colors.RESET}").upper()
    return options.get(choice)

if __name__ == "__main__":
    try:
        while True:
            selected_option = display_menu()
            if selected_option:
                name, func = selected_option
                if func:
                    func() # Call the animation or art function
                    if name.startswith("Static:"): # Static art returns to menu immediately after Enter
                        pass
                    else: # Animations loop until Ctrl+C, then return here
                        print(f"\n{Colors.BRIGHT_BLACK}Returning to menu...{Colors.RESET}")
                        time.sleep(1)
                elif name == "Quit":
                    print(f"{Colors.BRIGHT_YELLOW}Exiting showcase. Goodbye!{Colors.RESET}")
                    break
                else:
                    print(f"{Colors.RED}Invalid function for option. Returning to menu.{Colors.RESET}")
                    time.sleep(1.5)
            else:
                print(f"{Colors.RED}Invalid choice. Please try again.{Colors.RESET}")
                time.sleep(1.5)
    except KeyboardInterrupt: # Catch Ctrl+C from the menu itself
        print(f"\n{Colors.BRIGHT_YELLOW}Exiting showcase. Goodbye!{Colors.RESET}")
    finally:
        clear_screen() # Clean up screen on exit