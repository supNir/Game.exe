import pygame
import os
import sys


pygame.init()
size = width, height = 1000, 1000
screen = pygame.display.set_mode(size)
screen.fill((255, 255, 255))


def load_image(name, colorkey=None):
    fullname = os.path.join("data", name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


tile_images = {"wall": load_image("wall_2.png"), "empty": load_image("ground.png")}
player_image = pygame.transform.scale(load_image("goose_3.png", colorkey=-1), (50, 50))
tile_width = tile_height = 50


def load_level(filename):
    filename = "data/" + filename
    with open(filename, "r") as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, "."), level_map))


def create_level():
    pass


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["ЗАСТАВКА",
                  "Правила игры",
                  "Есть в правилах несколько строк",
                  "Приходится выводить их построчно"]
    font = pygame.font.Font(None, 30)
    text_coord = 50
    sprite = pygame.sprite.Group()
    image = pygame.sprite.Sprite()
    image.image = load_image("fon.jpg")
    image.image = pygame.transform.scale(image.image, (550, 550))
    image.rect = image.image.get_rect()
    sprite.add(image)
    sprite.draw(screen)
    for line in intro_text:
        string_render = font.render(line, 1, pygame.Color(0, 0, 0))
        intro_rect = string_render.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_render, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                return
        pygame.display.flip()


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        if tile_type == "wall":
            super().__init__(tile_group, all_sprites)
        else:
            super().__init__(all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)

    def go(self, vx, vy):
        self.rect.x = (self.rect.x + vx) % width
        self.rect.y = (self.rect.y + vy) % height


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == ".":
                Tile("empty", x, y)
            elif level[y][x] == "#":
                Tile("wall", x, y)
            elif level[y][x] == "@":
                Tile("empty", x, y)
                new_player = Player(x, y)
    return new_player, x, y


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = width // 2 - (target.rect.x + target.rect.w // 2)
        self.dy = height // 2 - (target.rect.y + target.rect.h // 2)


start_screen()
player = None
all_sprites = pygame.sprite.Group()
tile_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
player, level_x, level_y = generate_level(load_level("level2.txt"))
camera = Camera()
del_x = 0
del_y = 0
running = True
xod = {pygame.K_DOWN: (0, 1), pygame.K_UP: (0, -1), pygame.K_LEFT: (-1, 0), pygame.K_RIGHT: (1, 0)}
camera.update(player)
for sprite in all_sprites:
    camera.apply(sprite)
camera.apply(player)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYUP:
            f = event.key
            if f in xod.keys():
                k = xod[event.key]
                del_x -= k[0]
                del_y -= k[1]
        if event.type == pygame.KEYDOWN:
            f = event.key
            if f in xod.keys():
                k = xod[event.key]
                del_x += k[0]
                del_y += k[1]
    if del_x != 0 or del_y != 0:
        player.go(del_x, del_y)
        if pygame.sprite.spritecollideany(player, tile_group):
            player.go(-del_x, -del_y)
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)
        camera.apply(player)
    screen.fill((255, 255, 255))
    all_sprites.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()
pygame.quit()