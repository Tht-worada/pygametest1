import pygame
import random

def run_game():
    pygame.init()

    # --- หน้าจอหลัก ---
    width, height = 1280,720
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Taankhun888 so fat")

    # --- Colors ---
    lightbrown = (179, 138, 102)
    white = (255, 255, 255)
    blue = (56, 182, 255)
    red = (255, 87, 87)

    # --- โหลดภาพพื้นหลัง ---
    bg = pygame.image.load("ImgAsset/ingame.png").convert()
    bg = pygame.transform.scale(bg, (width, height))

    # --- ตั้งค่า font ---
    font = pygame.font.SysFont("Montserrat", 40)
    big_font = pygame.font.SysFont("Montserrat", 80, bold=True)

    # --- ฟังก์ชันสร้าง Bingo Board ---
    def generate_bingo_numbers():
        numbers = random.sample(range(1, 76), 25)
        board = [numbers[i * 5:(i + 1) * 5] for i in range(5)]
        board[2][2] = None  # ช่อง Free
        return board
    
    # --- ฟังก์ชันตรวจ Bingo ---
    def check_bingo(selected):
        # แนวนอน
        for r in range(5):
            if all((r, c) in selected for c in range(5)):
                return True
        # แนวตั้ง
        for c in range(5):
            if all((r, c) in selected for r in range(5)):
                return True
        # ทแยงมุมหลัก
        if all((i, i) in selected for i in range(5)):
            return True
        # ทแยงมุมรอง
        if all((i, 4 - i) in selected for i in range(5)):
            return True
        return False

    # --- ฟังก์ชันแสดงเลขบนกระดาน ---
    def draw_board(board, selected_cells, cursor_pos, start_x, start_y,
                cell_width=70, cell_height=70, color=white, cursor_color=red):
        for row in range(5):
            for col in range(5):
                x = start_x + col * cell_width
                y = start_y + row * cell_height
                rect = pygame.Rect(x - cell_width/2, y - cell_height/2, cell_width, cell_height)

                # --- วาด selected ก่อน ---
                if (row, col) in selected_cells:
                    pygame.draw.rect(screen, white, rect)

                # --- วาดกรอบเคอร์เซอร์ **หลัง selected** ---
                if (row, col) == cursor_pos:
                    pygame.draw.rect(screen, cursor_color, rect, 4)  # ขอบหนา 4 px

                # --- วาดตัวเลข ---
                num = board[row][col]
                if num is not None:
                    text = font.render(str(num), True, color)
                    text_rect = text.get_rect(center=(x, y))
                    screen.blit(text, text_rect)
                else:
                    text = font.render(str('O'), True, color)
                    text_rect = text.get_rect(center=(x, y))
                    screen.blit(text, text_rect)
    # --- สร้างกระดานทั้งสอง ---
    player1_board = generate_bingo_numbers()
    player2_board = generate_bingo_numbers()

    # ช่อง Free (กลาง)
    player1_selected = {(2, 2)}
    player2_selected = {(2, 2)}

    # --- ตำแหน่งของกระดาน ---
    player1_origin = (400, 390)
    player2_origin = (1370, 505)

    # --- ตัวแปรเวลา ---
    countdown = 3
    show_start = False
    show_number = False
    current_number = None
    numbers_list = list(range(1, 76)) #1-75
    random.shuffle(numbers_list)
    number_index = 0

    # --- ตัวแปรการควบคุมผู้เล่น ---
    player1_cursor = [0, 0]
    player2_cursor = [0, 0]

    # --- สถานะชนะ ---
    p1_bingo = False
    p2_bingo = False

    # --- ตัวนับช่องที่เลือกถูกต้อง ---
    player1_points = 0
    player2_points = 0

    # --- ตัวนับเลขที่สุ่ม ---
    draw_count = 0
    
    unused_numbers = set(range(1, 76))

    # --- สถานะชนะ ---
    p1_bingo = False
    p2_bingo = False
    game_over = False

    # --- Timer Events ---
    COUNTDOWN_EVENT = pygame.USEREVENT + 1
    GO_DONE_EVENT = pygame.USEREVENT + 2
    SHOW_NUMBER_EVENT = pygame.USEREVENT + 3

    pygame.time.set_timer(COUNTDOWN_EVENT, 1000)

    # --- ตัวแปร Mini Game ---
    mini_game_active = False
    player1_press = 0
    player2_press = 0
    mini_winner = None
    last_mini_trigger = 0   # ป้องกันไม่ให้ซ้ำรอบเดิม

    # --- sfx ---
    choose_sfx = pygame.mixer.Sound("SFX/choose.mp3")
    bingo_sfx = pygame.mixer.Sound("SFX/bingo_sfx.mp3")
    bgmusic = pygame.mixer.Sound("SFX/bgmusic.mp3")
    wowclap = pygame.mixer.Sound("SFX/wowclap.mp3")
    alert = pygame.mixer.Sound("SFX/alert.mp3")
    cookeddog = pygame.mixer.Sound("SFX/cookeddog.mp3")
    omg = pygame.mixer.Sound("SFX/omg.mp3")

    alert.set_volume(0.5)
    wowclap.set_volume(0.6)
    bgmusic.set_volume(0.7)
    bgmusic.play(-1, 0)

    bingo_winner_sound = False

    # --- ลูปหลัก ----------------------------------------------------------------------
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                bgmusic.stop()
                running = False
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: # กด ESC เพื่อกลับเมนู
                bgmusic.stop()
                return

            # --- Countdown ---
            if event.type == COUNTDOWN_EVENT:
                if countdown > 0:
                    countdown -= 1
                elif countdown == 0:
                    show_start = True
                    countdown = -1
                    pygame.time.set_timer(COUNTDOWN_EVENT, 0)
                    pygame.time.set_timer(GO_DONE_EVENT, 3000)

            if event.type == GO_DONE_EVENT:
                show_start = False
                pygame.time.set_timer(GO_DONE_EVENT, 0)
                pygame.time.set_timer(SHOW_NUMBER_EVENT, 2000)
            
            # --- สุ่มเลขใหม่ทุก 8 วิ ---
            if event.type == SHOW_NUMBER_EVENT and not game_over:
                show_number = True
                pygame.time.set_timer(SHOW_NUMBER_EVENT, 0)
                pygame.time.set_timer(SHOW_NUMBER_EVENT, 8000)
                draw_count += 1

                # ทุก 2 ครั้ง ให้เลขช่วยผู้เล่น
                # กรณี Lucky Draw (ช่วยผู้เล่น)
                if draw_count % 2 == 0 and draw_count > 0:
                    lucky_player = random.choice([1, 2])

                    board = player1_board if lucky_player == 1 else player2_board
                    selected = player1_selected if lucky_player == 1 else player2_selected

                    # เลือกเฉพาะเลขใน board ที่ยังไม่เลือกและยังอยู่ใน unused_numbers
                    remaining_numbers = [
                        board[r][c]
                        for r in range(5) for c in range(5)
                        if board[r][c] is not None
                        and (r, c) not in selected
                        and board[r][c] in unused_numbers
                    ]

                    if remaining_numbers:
                        current_number = random.choice(remaining_numbers)
                        unused_numbers.remove(current_number)
                    else:
                        current_number = None

                # กรณีสุ่มปกติ
                else:
                    if unused_numbers:
                        current_number = random.choice(list(unused_numbers))
                        unused_numbers.remove(current_number)
                    else:
                        current_number = None

                

            # --- การควบคุมเคอร์เซอร์ ---
            if event.type == pygame.KEYDOWN:
                # Player1: WASD
                if event.key == pygame.K_w: player1_cursor[0] = (player1_cursor[0] - 1) % 5
                if event.key == pygame.K_s: player1_cursor[0] = (player1_cursor[0] + 1) % 5
                if event.key == pygame.K_a: player1_cursor[1] = (player1_cursor[1] - 1) % 5
                if event.key == pygame.K_d: player1_cursor[1] = (player1_cursor[1] + 1) % 5

                # Player2: IJKL
                if event.key == pygame.K_i: player2_cursor[0] = (player2_cursor[0] - 1) % 5
                if event.key == pygame.K_k: player2_cursor[0] = (player2_cursor[0] + 1) % 5
                if event.key == pygame.K_j: player2_cursor[1] = (player2_cursor[1] - 1) % 5
                if event.key == pygame.K_l: player2_cursor[1] = (player2_cursor[1] + 1) % 5

                # --- เมื่ออยู่ใน Mini Game ---
                if mini_game_active and not mini_winner:
                    if event.key == pygame.K_e:
                        player1_press += 1
                    if event.key == pygame.K_o:
                        player2_press += 1

                    # ใครครบ 20 ครั้งก่อนเป็นผู้ชนะ
                    if player1_press >= 20:
                        mini_winner = 1
                    elif player2_press >= 20:
                        mini_winner = 2


                if not game_over:
                    # Player1 เลือกด้วย E
                    if event.key == pygame.K_e and current_number is not None:
                        r, c = player1_cursor
                        # ป้องกันการเลือกซ้ำ
                        if (r, c) not in player1_selected:
                            if player1_board[r][c] == current_number:
                                player1_selected.add((r, c))
                                player1_points += 1
                                choose_sfx.play()
                                print(f"Player 1 Points: {player1_points}")

                                if player1_points % 3 == 0:
                                    print("3 point player 1!")

                                if check_bingo(player1_selected):
                                    p1_bingo = True
                                    game_over = True
                                    pygame.time.set_timer(SHOW_NUMBER_EVENT, 0)
                                    print("Player 1: BINGO!")


                    # Player2 เลือกด้วย O
                    if event.key == pygame.K_o and current_number is not None:
                        r, c = player2_cursor
                        # ป้องกันการเลือกซ้ำ
                        if (r, c) not in player2_selected:
                            if player2_board[r][c] == current_number:
                                player2_selected.add((r, c))
                                player2_points += 1
                                choose_sfx.play()
                                print(f"Player 2 Points: {player2_points}")

                                if player2_points % 3 == 0:
                                    print("3 point player 2!")

                                if check_bingo(player2_selected):
                                    p2_bingo = True
                                    game_over = True
                                    pygame.time.set_timer(SHOW_NUMBER_EVENT, 0)
                                    print("Player 2: BINGO!")

        
        # --- เริ่ม Mini Game เมื่อแต้มรวม %6 == 0 และยังไม่เล่นรอบนี้ ---
        total_points = player1_points + player2_points
        if total_points > 0 and total_points % 6 == 0 and total_points != last_mini_trigger and not game_over:
            mini_game_active = True
            last_mini_trigger = total_points
            pygame.time.set_timer(SHOW_NUMBER_EVENT, 0)  # หยุดสุ่มเลข
            current_number = None
            player1_press = 0
            player2_press = 0
            mini_winner = None
            alert.play()

        # --- เมื่อ mini-game มีผู้ชนะ ---
        if mini_winner:
            board = player1_board if mini_winner == 1 else player2_board
            selected = player1_selected if mini_winner == 1 else player2_selected

            # หา cell ที่ยังไม่ได้เลือก
            available_cells = [(r, c) for r in range(5) for c in range(5)
                            if board[r][c] is not None and (r, c) not in selected]

            if available_cells:
                random_cell = random.choice(available_cells)

                # เอฟเฟกต์กระพริบช่องฟรี 3 ครั้ง
                for i in range(3):
                    screen.blit(bg, (0, 0))
                    draw_board(player1_board, player1_selected, tuple(player1_cursor),
                            player1_origin[0] - 203, player1_origin[1] - 160,
                            cell_width=76, cell_height=81, color=red, cursor_color=red)
                    draw_board(player2_board, player2_selected, tuple(player2_cursor),
                            player2_origin[0] - 590, player2_origin[1] - 275,
                            cell_width=76, cell_height=81, color=blue, cursor_color=blue)

                    start_x, start_y = (player1_origin if mini_winner == 1 else player2_origin)
                    offset_x = -203 if mini_winner == 1 else -590
                    offset_y = -160 if mini_winner == 1 else -275
                    x = start_x + (random_cell[1] * 76) + offset_x
                    y = start_y + (random_cell[0] * 81) + offset_y
                    rect = pygame.Rect(x - 38, y - 40, 76, 81)

                    color = white if i % 2 == 0 else bg.get_at((int(x), int(y)))
                    pygame.draw.rect(screen, color, rect)
                    pygame.display.flip()
                    pygame.time.delay(500)

                # หลังจากกระพริบครบ 3 ครั้ง ค่อยให้ช่องนั้นเป็นของจริง
                selected.add(random_cell)
                used_num = board[random_cell[0]][random_cell[1]]
                if used_num in unused_numbers:
                    unused_numbers.remove(used_num)
                print(f"Mini-game winner: Player {mini_winner} gained a free cell {used_num}")

                # --- เพิ่มตรงนี้ เช็ก Bingo หลังได้ช่องฟรี ---
                if mini_winner == 1:
                    if check_bingo(player1_selected):
                        p1_bingo = True
                        game_over = True
                        pygame.time.set_timer(SHOW_NUMBER_EVENT, 0)
                        print("Player 1: BINGO!")
                else:
                    if check_bingo(player2_selected):
                        p2_bingo = True
                        game_over = True
                        pygame.time.set_timer(SHOW_NUMBER_EVENT, 0)
                        print("Player 2: BINGO!")

            # รีเซ็ตสถานะ mini-game แล้วกลับเข้าสู่เกมหลัก
            mini_game_active = False
            mini_winner = None
            pygame.time.set_timer(SHOW_NUMBER_EVENT, 8000)



        # --- วาดพื้นหลัง ---
        screen.blit(bg, (0, 0))

        # --- วาดกระดาน ---
        draw_board(player1_board, player1_selected, tuple(player1_cursor),
                player1_origin[0] - 203, player1_origin[1] - 160, #0 right left -- 1 up down 
                cell_width=76, cell_height=81, color=red, cursor_color=red)
        
        draw_board(player2_board, player2_selected, tuple(player2_cursor),
                player2_origin[0] - 590, player2_origin[1] - 275,  #0 right left -- 1 up down 
                cell_width=76, cell_height=81, color=blue, cursor_color=blue)

        
        # --- แสดง Countdown / GO / เลขสุ่ม ---
        text = None
        if countdown > 0:
            text = big_font.render(str(countdown), True, white)
        elif show_start:
            text = big_font.render("GO", True, white)
        elif show_number and current_number is not None:
            text = big_font.render(str(current_number), True, white)
        if text:
            rect = text.get_rect(center=(width // 2, height // 2))
            screen.blit(text, rect)
        
        # --- เมื่อเกมจบ แสดงปุ่มกลับเมนู ---
        if game_over:
            # --- Overlay มืดโปร่งใส ---
            overlay = pygame.Surface((width, height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))

            # --- ข้อความผู้ชนะ ---
            if p1_bingo:
                win_text = big_font.render("PLAYER 1 BINGO!", True, red)
            elif p2_bingo:
                win_text = big_font.render("PLAYER 2 BINGO!", True, blue)
            else:
                win_text = big_font.render("BINGO!", True, white)

            win_rect = win_text.get_rect(center=(width // 2, height // 2 - 100))
            screen.blit(win_text, win_rect)
            
            # --- ปุ่ม BACK TO MENU ---
            button_font = pygame.font.SysFont("Montserrat", 50, bold=True)
            button_text = button_font.render("BACK TO MENU", True, white)
            button_rect = button_text.get_rect(center=(width // 2, height // 2 + 100))

            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()

            # สีปุ่มตามผู้ชนะ
            if button_rect.collidepoint(mouse_pos):
                if p1_bingo:
                    pygame.draw.rect(screen, red, button_rect.inflate(40, 20), border_radius=10)
                elif p2_bingo:
                    pygame.draw.rect(screen, blue, button_rect.inflate(40, 20), border_radius=10)
                else:
                    pygame.draw.rect(screen, lightbrown, button_rect.inflate(40, 20), border_radius=10)

                if mouse_click[0]:
                    return  # กลับเมนู
            else:
                pygame.draw.rect(screen, lightbrown, button_rect.inflate(40, 20), border_radius=10)

            # เล่นเสียงหลังจบเกม
            if not bingo_winner_sound:
                bgmusic.stop()
                omg.play()
                wowclap.play()
                bingo_sfx.play()
                cookeddog.play()
                bingo_winner_sound = True

            screen.blit(button_text, button_rect)



        # --- แสดง Mini Game ---
        if mini_game_active:
            overlay = pygame.Surface((width, height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))

            mini_text = big_font.render("Mini Game!", True, white)
            inst_text = font.render("Press E (P1) or O (P2) - First to 20 wins!", True, white)
            p1_text = font.render(f"P1: {player1_press}", True, red)
            p2_text = font.render(f"P2: {player2_press}", True, blue)

            screen.blit(mini_text, mini_text.get_rect(center=(width//2, height//2 - 100)))
            screen.blit(inst_text, inst_text.get_rect(center=(width//2, height//2)))
            screen.blit(p1_text, p1_text.get_rect(center=(width//2 - 150, height//2 + 100)))
            screen.blit(p2_text, p2_text.get_rect(center=(width//2 + 150, height//2 + 100)))

        pygame.display.flip()
    
    pygame.display.quit()
    return

#del it if want to test mainmenu full version
# run_game()