import pygame


def load_level(filename):
    if filename == 'game_data/':
        filename = 'game_data/map1.txt'
    try:
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]
    except FileNotFoundError:
        exit('ФАЙЛ НЕ НАЙДЕН')
    print('ЗАГРУЗКА')
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Нажмите любую клавишу",
                  "Чтобы продолжить"]

    fon = pygame.transform.scale(pygame.image.load('game_data/fon.jpg'), (width, height))
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
                exit()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(30)


tile_images = {
    'wall': pygame.image.load('game_data/box.png'),
    'empty': pygame.image.load('game_data/grass.png')
}
player_image = pygame.image.load('game_data/mar.png')
tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__()
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)


def render():
    global player
    for y, i in enumerate(board):
        for x, j in enumerate(i):
            if j == '.':
                all_sprites.add(Tile('empty', x, y))
            elif j == '#':
                les_sprites.add(Tile('wall', x, y))
            else:
                all_sprites.add(Tile('empty', x, y))
                player = Player(x, y)


if __name__ == '__main__':
    filename = input("Введите имя файла в папке данных игры: ")
    clock = pygame.time.Clock()
    pygame.init()
    size = width, height = 450, 450
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Перемещение героя. Новый уровень')
    screen.fill(pygame.color.Color('black'))
    all_sprites = pygame.sprite.Group()
    les_sprites = pygame.sprite.Group()
    player = Player(0, 0)
    board = load_level(f'game_data/{filename}')
    render()
    start_screen()
    a_cords = (player.rect.x, player.rect.y)
    player.rect.x, player.rect.y = width//2-player.rect.width//2, height//2-player.rect.height//2
    b_cords = (player.rect.x, player.rect.y)
    for s in [all_sprites, les_sprites]:
        for i in s.sprites():
            i.rect.x += b_cords[0] - a_cords[0]
            i.rect.y += b_cords[1] - a_cords[1]
    while True:
        clock.tick(60)
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    for i in all_sprites.sprites():
                        i.rect.x += tile_width
                    for i in les_sprites.sprites():
                        i.rect.x += tile_width
                    if player.rect.collidelistall([i.rect for i in les_sprites.sprites()]):
                        for i in all_sprites.sprites():
                            i.rect.x -= tile_width
                        for i in les_sprites.sprites():
                            i.rect.x -= tile_width
                elif event.key == pygame.K_d:
                    for i in all_sprites.sprites():
                        i.rect.x -= tile_width
                    for i in les_sprites.sprites():
                        i.rect.x -= tile_width
                    if player.rect.collidelistall([i.rect for i in les_sprites.sprites()]):
                        for i in all_sprites.sprites():
                            i.rect.x += tile_width
                        for i in les_sprites.sprites():
                            i.rect.x += tile_width
                if event.key == pygame.K_w:
                    for i in all_sprites.sprites():
                        i.rect.y += tile_height
                    for i in les_sprites.sprites():
                        i.rect.y += tile_height
                    if player.rect.collidelistall([i.rect for i in les_sprites.sprites()]):
                        for i in all_sprites.sprites():
                            i.rect.y -= tile_height
                        for i in les_sprites.sprites():
                            i.rect.y -= tile_height
                elif event.key == pygame.K_s:
                    for i in all_sprites.sprites():
                        i.rect.y -= tile_height
                    for i in les_sprites.sprites():
                        i.rect.y -= tile_height
                    if player.rect.collidelistall([i.rect for i in les_sprites.sprites()]):
                        for i in all_sprites.sprites():
                            i.rect.y += tile_height
                        for i in les_sprites.sprites():
                            i.rect.y += tile_height
        for s in [all_sprites, les_sprites]:
            for i in s.sprites():
                if i.rect.x + i.rect.width > 450:
                    i.rect.x -= 500
                elif i.rect.x - i.rect.width < -100:
                    i.rect.x += 500
                if i.rect.y + i.rect.height > 500:
                    i.rect.y -= 500
                elif i.rect.y - i.rect.width < -50:
                    i.rect.y += 500
        all_sprites.draw(screen)
        les_sprites.draw(screen)
        screen.blit(player.image, (player.rect.x, player.rect.y))
        pygame.display.flip()
