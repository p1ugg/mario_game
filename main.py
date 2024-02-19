import pygame

import sys
import os

FPS = 60


def load_image(name, colorkey=-1):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey == -1:
        colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon.jpg'), size)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
player_image = load_image('mar.png')

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.pos = (pos_x, pos_y)

    def move(self, x, y):
        camera.dx -= tile_width * (x - self.pos[0])
        camera.dy -= tile_height * (y - self.pos[1])
        self.pos = (x, y)
        for sprite in tiles_group:
            camera.apply(sprite)


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy
        if obj.rect.y < 0:
            obj.rect.y = max_y - tile_width
        if obj.rect.x < 0:
            obj.rect.x = max_x - tile_width

        if obj.rect.y > max_y:
            obj.rect.y = tile_width
        if obj.rect.x > max_x:
            obj.rect.x = tile_width

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = 0
        self.dy = 0


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    max_y = len(level) * tile_height
    max_x = len(level[0]) * tile_width
    return new_player, x, y, max_y, max_x


def load_level(filename):
    filename = "data/" + filename
    try:
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]
    except FileNotFoundError:
        exit('Такого файла не существует')

    max_width = max(map(len, level_map))

    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def move(player, movement):
    x, y = player.pos
    if movement == "up":
        if y > 0 and level_map[y - 1][x] in [".", "@"]:
            player.move(x, y - 1)
    elif movement == "down":
        if y < level_y - 1 and level_map[y + 1][x] in [".", "@"]:
            player.move(x, y + 1)
    elif movement == "left":
        if x > 0 and level_map[y][x - 1] in [".", "@"]:
            player.move(x - 1, y)
    elif movement == "right":
        if x < level_x and level_map[y][x + 1] in [".", "@"]:
            player.move(x + 1, y)


if __name__ == '__main__':
    pygame.init()
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Марио')
    fps = 10
    clock = pygame.time.Clock()
    running = True
    all_sprites = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()

    start_screen()
    camera = Camera()
    level_map = load_level("map.txt")
    player, level_x, level_y, max_y, max_x = generate_level(level_map)

    while running:
        screen.fill('black')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    move(player, "up")
                elif event.key == pygame.K_s:
                    move(player, "down")
                elif event.key == pygame.K_a:
                    move(player, "left")
                elif event.key == pygame.K_d:
                    move(player, "right")
        camera.update(player)
        tiles_group.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()
