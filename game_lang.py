import pygame
from random import randrange


JAPANES_PATH = r"C:\WINDOWS\FONTS\MSGOTHIC.TTC"
WIDTH = 800
HEIGHT = 600
FPS = 120
RENDER_INT = 10
PLAY_RENDER_INT = 10

WORDS_DICT = {
    "駅": {"True": "駅", "False": ["口", "十", "人", "七"]},
    "口": {"True": "口", "False": ["駅", "十", "人", "七"]},
    
}


class Display:
    width = WIDTH
    height = HEIGHT
    fps_int = FPS
    pygame_md = pygame
    display = pygame.display
    fps_md = pygame.time.Clock
    size = width, height

    def __init__(self) -> None:
        self.surface = self.display.set_mode(self.size, self.pygame_md.RESIZABLE)
        self.fps = self.fps_md()

    def update(self) -> None:
        self.fps.tick(self.fps_int)
        self.rect = self.surface.get_rect()

        self.surface.blit(self.surface, self.rect)
        self.display.flip()
        self.surface.fill((0, 0, 0))

    def resize_disp(self):
        self.size = self.surface.get_size()
        self.width, self.height = self.size


class Player(pygame.sprite.Sprite):
    pygame_md = pygame
    words_dict = WORDS_DICT
    jap_font = JAPANES_PATH
    render_int = PLAY_RENDER_INT
    speed = 4
    finish_game = False

    def __init__(self, width: int = WIDTH, height: int = HEIGHT) -> None:
        super(Player, self).__init__()
        self.first_start = True

        if self.first_start:
            self.width = width
            self.height = height
            self.word_list = list(self.words_dict.keys())
            self.get_word()

        else:
            return False

    def get_word(self):
        try:
            word_index = randrange(len(self.word_list))
        except ValueError:
            self.finish_game = True
            return

        font_size = self.width // self.render_int
        word_font = self.pygame_md.font.Font(self.jap_font, font_size)

        self.key_player = self.word_list.pop(word_index)
        self.image = word_font.render(self.key_player, True, "red")

        if self.first_start:
            self.rect = self.image.get_rect(center=(self.width / 2, self.height))
            self.first_start = False
            return

        self.rect = self.image.get_rect(center=(self.rect.center))

    def update(self, width: int = WIDTH, height: int = HEIGHT) -> None:
        self.width = width
        self.height = height

        self.pressed_key = self.pygame_md.key.get_pressed()

        if (
            self.pressed_key[self.pygame_md.K_UP]
            or self.pressed_key[self.pygame_md.K_w]
        ):
            self.rect.move_ip(0, -self.speed)
        if (
            self.pressed_key[self.pygame_md.K_DOWN]
            or self.pressed_key[self.pygame_md.K_s]
        ):
            self.rect.move_ip(0, self.speed)
        if (
            self.pressed_key[self.pygame_md.K_LEFT]
            or self.pressed_key[self.pygame_md.K_a]
        ):
            self.rect.move_ip(-self.speed, 0)
        if (
            self.pressed_key[self.pygame_md.K_RIGHT]
            or self.pressed_key[self.pygame_md.K_d]
        ):
            self.rect.move_ip(self.speed, 0)

        if self.pressed_key[self.pygame_md.K_c]:
            self.get_word()

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.width:
            self.rect.right = self.width
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= self.height:
            self.rect.bottom = self.height

    def resize(self, place_len, width: int = WIDTH, height: int = HEIGHT):
        
        resize_ind = self.width / width

        self.width = width
        self.height = height

        font_size = self.width // self.render_int

        word_font = self.pygame_md.font.Font(self.jap_font, font_size)
        self.image = word_font.render(self.key_player, True, "red")
        self.rect = self.image.get_rect(center=(self.rect.centerx / resize_ind, self.rect.centery))


class FakeWords(pygame.sprite.Sprite):
    pygame_md = pygame
    words_dict = WORDS_DICT
    jap_font = JAPANES_PATH
    render_int = RENDER_INT

    def __init__(
        self,
        fake_word: str,
        place_x: int,
        width: int = WIDTH,
        height: int = HEIGHT,
        speed=[0, 1],
    ) -> None:
        super(FakeWords, self).__init__()

        self.width = width
        self.height = height

        self.speed = speed
        self.speed_x, self.speed_y = self.speed

        self.place_x = place_x

        font_size = self.width // self.render_int
        self.fake_word = fake_word

        word_font = self.pygame_md.font.Font(self.jap_font, font_size)

        self.image = word_font.render(self.fake_word, True, "blue")
        self.rect = self.image.get_rect(
            center=(self.place_x, -self.image.get_height()),
            height=self.image.get_height() // 2,
        )


    def resize(self, place_len, width: int = WIDTH, height: int = HEIGHT):
        resize_ind = self.width / width

        self.width = width
        self.height = height
        self.place_len = place_len

        font_size = self.width // self.render_int
        word_font = self.pygame_md.font.Font(self.jap_font, font_size)


        self.image = word_font.render(self.fake_word, True, "blue")
        self.rect = self.image.get_rect(
            center=(self.rect.centerx / resize_ind, self.rect.centery),
            height=self.image.get_height() // 2,
        )

    def update(self, width: int = WIDTH, height: int = HEIGHT):
        self.width = width
        self.height = height

        self.rect.move_ip(self.speed_x, self.speed_y)
        if self.rect.bottom >= self.image.get_height() + self.height:
            self.kill()


class TrueWord(pygame.sprite.Sprite):
    pygame_md = pygame

    words_dict = WORDS_DICT
    jap_font = JAPANES_PATH
    render_int = RENDER_INT

    def __init__(
        self,
        player_word: str,
        place_x: int,
        width: int = WIDTH,
        height: int = HEIGHT,
        speed=[0, 1],
    ) -> None:
        super(TrueWord, self).__init__()
        self.width = width
        self.height = height

        self.speed = speed
        self.speed_x, self.speed_y = self.speed

        self.player_word = player_word
        self.place_x = place_x

        font_size = self.width // self.render_int
        true_words = self.words_dict[self.player_word]["True"]
        word_font = self.pygame_md.font.Font(self.jap_font, font_size)

        self.image = word_font.render(true_words, True, "blue")
        self.rect = self.image.get_rect(
            center=(self.place_x, -self.image.get_height()),
            height=self.image.get_height() // 2,
        )

    def update(self, width: int = WIDTH, height: int = HEIGHT) -> None:
        self.width = width
        self.height = height

        self.rect.move_ip(self.speed_x, self.speed_y)
        if self.rect.bottom >= self.image.get_height() + self.height:
            self.kill()


    def resize(self, place_len, width: int = WIDTH, height: int = HEIGHT):
        resize_ind = self.width / width

        self.width = width
        self.height = height
        self.place_len = place_len

        font_size = self.width // self.render_int

        word_font = self.pygame_md.font.Font(self.jap_font, font_size)
        true_words = self.words_dict[self.player_word]["True"]

        self.image = word_font.render(true_words, True, "blue")
        self.rect = self.image.get_rect(
            center=(self.rect.centerx / resize_ind, self.rect.centery),
            height=self.image.get_height() // 2,
        )


class Game(pygame.sprite.Sprite):
    display_md = Display
    player_md = Player
    fake_word_md = FakeWords
    true_word_md = TrueWord

    pygame_md = pygame
    fake_words_dict = {}
    work_game = True
    g_over = False

    words_dict = WORDS_DICT

    def __init__(self) -> None:
        super(Game, self).__init__()
        self.false_sprite = pygame.sprite.Group()
        self.true_sprite = pygame.sprite.Group()
        self.all_sprite = pygame.sprite.Group()

        self.display = self.display_md()
        self.player = self.player_md(*self.display.size)
        self.all_sprite.add(self.player)

    def resize(self) -> None:
        self.display.resize_disp()

        for sprite in self.all_sprite:
            sprite.resize(self.place_len, *self.display.size)

    def event_loop(self) -> None:
        for event in self.pygame_md.event.get():
            if event.type == self.pygame_md.QUIT:
                self.work_game = False

            if event.type == self.pygame_md.VIDEORESIZE:
                self.resize()
                self.get_place_x()

            if event.type == self.ADD_WORDS:
                if not len(self.all_sprite.sprites()) > 1:
                    self.get_place_x()
                    self.create_trure_words()
                    self.create_false_word()

    def get_place_x(self):
        self.place_len = (len(self.words_dict[self.player.key_player]["False"]) + 1) * 2
        num = self.display.width // self.place_len

        list_x = []
        x_num = 0

        for _ in range(0, self.place_len):
            x_num += num
            list_x.append(x_num)

        self.list_x = list_x[::2]

    def create_trure_words(self):
        indx = randrange(len(self.list_x))
        plase_x = self.list_x.pop(indx)

        true_key = self.words_dict[self.player.key_player]["True"]
        true_word = self.true_word_md(true_key, plase_x, *self.display.size)
        self.true_sprite.add(true_word)
        self.all_sprite.add(true_word)

        return

    def create_false_word(self):
        false_list = self.words_dict[self.player.key_player]["False"]

        for false_word in false_list:
            indx = randrange(len(self.list_x))
            plase_x = self.list_x.pop(indx)

            fake_word = self.fake_word_md(false_word, plase_x, *self.display.size)
            self.false_sprite.add(fake_word)
            self.all_sprite.add(fake_word)

    def create_event(self):
        self.ADD_WORDS = pygame.USEREVENT + 1
        pygame.time.set_timer(self.ADD_WORDS, 1000)

    def create_obj(self):
        self.all_sprite.draw(self.display.surface)

    def chose_true(self):
        true_word = self.pygame_md.sprite.spritecollideany(
            self.player, self.true_sprite
        )
        if true_word:
            for false_word in self.false_sprite:
                false_word.kill()
            true_word.kill()
            self.player.get_word()

    def chose_false(self):
        false_word = self.pygame_md.sprite.spritecollideany(
            self.player, self.false_sprite
        )
        if false_word:
            for true_word in self.true_sprite:
                true_word.kill()

            for false_word in self.false_sprite:
                false_word.kill()
            # self.g_over = True

    def create_objects(self):
        self.g_over = False
        self.event_loop()
        self.create_obj()
        self.all_sprite.update(*self.display.size)
        self.chose_true()
        self.chose_false()

        if self.player.finish_game or self.g_over:
            return False
        return True

    def play(self) -> None:
        self.create_event()
        while self.work_game:
            self.display.update()

            if self.work_game:
                if not self.create_objects():
                    self.work_game = False


class GameApp:
    pygame_md = pygame
    game_md = Game

    def __init__(self) -> None:
        self.pygame_md.init()

    def run(self) -> None:
        self.game_md = self.game_md().play()
        pygame.quit()
        quit()

# if __name__ == "__main__":
#     a = GameApp()
#     a.run()
