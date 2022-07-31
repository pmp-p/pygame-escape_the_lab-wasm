    def free_play_normal(segment):
        global bullet_y
        global bullet_x
        bullet_picture = pygame.transform.scale(pygame.image.load("Images/bullet.png"), (64, 32)).convert_alpha()
        background = pygame.transform.scale(pygame.image.load("Images/Background_images/menu_background.png"),
                                            (1280, 736)).convert_alpha()

        pygame.init()
        screen = pygame.display.set_mode(SCREEN_SIZE.size)
        pygame.display.set_caption("Level Mode")
        timer = pygame.time.Clock()

        platforms = pygame.sprite.Group()
        player = Player(platforms, (TILE_SIZE, TILE_SIZE))
        level_width = MAP_BORDER[0] * TILE_SIZE
        level_height = MAP_BORDER[1] * TILE_SIZE
        entities = CameraAwareLayeredUpdates(player, pygame.Rect(0, 0, level_width, level_height))

        # build the map_border
        x = y = 0
        for row in segment:
            for col in row:
                if col == "=":
                    PlatLevelEnd((x, y), platforms, entities)
                if col == "P":
                    PlatBasic((x, y), platforms, entities)
                if col == "D":
                    PlatEnemy((x, y), platforms, entities)
                if col == "E":
                    PlatExitNorm((x, y), platforms, entities)
                if col == "F":
                    PlatSpeedF((x, y), platforms, entities)
                if col == "H":
                    PlatSpeedH((x, y), platforms, entities)
                if col == "M":
                    PlatSpeedM((x, y), platforms, entities)
                if col == "L":
                    PlatSpeedL((x, y), platforms, entities)
                if col == "N":
                    PlatNormNorm((x, y), platforms, entities)
                if col == "J":
                    PlatJumpH((x, y), platforms, entities)
                if col == "G":
                    PlatJumpM((x, y), platforms, entities)
                if col == "2":
                    PlatLevel2((x, y), platforms, entities)
                if col == "3":
                    PlatLevel3((x, y), platforms, entities)
                if col == "4":
                    PlatLevel4((x, y), platforms, entities)
                if col == "5":
                    PlatLevel5((x, y), platforms, entities)
                if col == "6":
                    PlatLevel6((x, y), platforms, entities)
                if col == "7":
                    PlatLevel3((x, y), platforms, entities)
                if col == "0":
                    PlatMoving((x, y), platforms, entities)
                if col == "C":
                    PlatCoinsNorm((x, y), platforms, entities)
                if col == "S":
                    PlatFreeStick((x, y), platforms, entities)
                if col == "0":
                    PlatMoving((x, y), platforms, entities)
                x += TILE_SIZE
            y += TILE_SIZE
            x = 0

        free_play_music()

        previous_time = pygame.time.get_ticks()
        enemy_list = []

        while 1:

            dead = False

            for e in pygame.event.get():
                if e.type == QUIT:
                    return
                if e.type == KEYDOWN and e.key == K_ESCAPE:
                    level_music(level=0)
                    remove_bullets()
                    return

            bullet_x = player.rect[0]
            bullet_y = player.rect[1]

            current_time = pygame.time.get_ticks()

            entities.update()
            screen.blit(background, (0, 0))
            for bullet in BULLETS:
                SCREEN.blit(bullet_picture, pygame.Rect(bullet[0] + entities.cam[0], bullet[1] + entities.cam[1], 32, 32))
            for bullet in ENEMY_BULLETS:
                SCREEN.blit(pygame.transform.rotate(bullet_picture, -180),
                            pygame.Rect(bullet[0] + entities.cam[0], bullet[1] + entities.cam[1], 32, 32))

            for b in range(len(ENEMY_BULLETS)):
                ENEMY_BULLETS[b][0] -= 6

            for p in platforms:
                temp = str(p)
                if "PlatEnemy" in temp:
                    if p not in enemy_list:
                        enemy_list.append(p)

                for bullet in ENEMY_BULLETS:
                    if bullet.colliderect(p.rect):
                        ENEMY_BULLETS.remove(bullet)
                    if bullet.colliderect(player):
                        dead = True

                for bullet in BULLETS:
                    for bullet2 in ENEMY_BULLETS:
                        if bullet2.colliderect(bullet):
                            ENEMY_BULLETS.remove(bullet2)
                            BULLETS.remove(bullet)
                    if bullet.colliderect(p.rect):
                        BULLETS.remove(bullet)
                        if "PlatEnemy" in temp:
                            enemy_list.remove(p)
                            p.kill()

                if current_time - previous_time > 4000:
                    for enemy in enemy_list:
                        ENEMY_BULLETS.append(pygame.Rect(enemy.rect[0] - 100, enemy.rect[1], 32, 32))
                        shoot_sound()
                    previous_time = current_time

                if (p.rect[0] - player.rect[0]) < -1300:
                    if "PlatMoving" in temp:
                        continue
                    else:
                         p.kill()






            entities.draw(screen)
            pygame.display.update()

            if dead == True:
                wasted()
                free_play_window()

            timer.tick(60)