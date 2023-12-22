import pygame
import sys
import os


def load_image(name, colorkey=None):
    fullname = os.path.join(r'C:\Users\Schwannenvogel\Desktop\pygame_task', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


fname = str(input())
if not os.path.isfile(os.path.join(r'C:\Users\Schwannenvogel\Desktop\pygame_task', fname)):
    print(f'Ошибка, файла {fname} не существует!')
    sys.exit(0)

pygame.init()
size = WIDTH, HEIGHT = 550, 550
screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
player_image = load_image('mario.png')

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
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(tile_width * self.pos[0] + 15,
                                               tile_height * self.pos[1] + 5)


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    FPS = 50

    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
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
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename):
    filename = r"C:\Users\Schwannenvogel\Desktop\pygame_task/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r', encoding='utf-8') as mapFile:
        level_map = [line.strip() for line in mapFile]
        level_map[0] = level_map[0][1:]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


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
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


def mmove(player, direction):
    x, y = player.pos
    if direction == 'up':
        if y > 0 and lev_map[y - 1][x] != '#':
            player.move(x, y - 1)
    elif direction == 'down':
        if y < level_y - 1 and lev_map[y + 1][x] != '#':
            player.move(x, y + 1)
    elif direction == 'left':
        if x > 0 and lev_map[y][x - 1] != '#':
            player.move(x - 1, y)
    elif direction == 'right':
        if x < level_x - 1 and lev_map[y][x + 1] != '#':
            player.move(x + 1, y)


if __name__ == '__main__':
    pygame.display.set_caption('Перемещение героя')

    # основной персонаж
    player = None

    running = True

    start_screen()
    lev_map = load_level(fname)
    player, level_x, level_y = generate_level(lev_map)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    mmove(player, 'up')
                if event.key == pygame.K_DOWN:
                    mmove(player, 'down')
                if event.key == pygame.K_RIGHT:
                    mmove(player, 'right')
                if event.key == pygame.K_LEFT:
                    mmove(player, 'left')

        screen.fill(pygame.Color('#000000'))

        tiles_group.draw(screen)
        player_group.draw(screen)

        pygame.display.flip()
