import pygame

pygame.init()

screen = pygame.display.set_mode((800,800))
clock = pygame.time.Clock()

rect1 = pygame.Surface((50,50))
rect1.fill("maroon")


player_pos_x = screen.get_width()/2
player_pos_y = screen.get_height()/2

rect1_rect = rect1.get_rect(topleft = (0,0))

rect2_surf = pygame.Surface((200,200))
rect2_surf.fill("orange")
rect2_rect = rect2_surf.get_rect(center=(40,40))


running=True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")
    
    screen.blit(rect2_surf, rect2_rect)

    screen.blit(rect1, rect1_rect)

    pygame.draw.line(screen,"blue", (0,0),(800,800))

    if rect2_rect.colliderect(rect1_rect): 
        rect2_surf.fill("green")
    else:
        rect2_surf.fill("orange")
    
    key = pygame.key.get_pressed()
    if rect1_rect.left <0: rect1_rect.right = screen.get_width()
    if rect1_rect.right >screen.get_width(): rect1_rect.left = 0
    if rect1_rect.top < 0: rect1_rect.bottom = screen.get_height()
    if rect1_rect.bottom > screen.get_height(): rect1_rect.top = 0

    if key[pygame.K_w]:
        rect1_rect.y -= 5
    if key[pygame.K_s]:
        rect1_rect.y += 5
    if key[pygame.K_a]:
        rect1_rect.x -= 5
    if key[pygame.K_d]:
        rect1_rect.x += 5


    pygame.display.update()
    clock.tick(60)


pygame.quit()