import pygame
import json
from collections import deque

#----------------------상수 정의역-----------------------#
SCREEN_WIDTH = 600 # 가로
SCREEN_HEIGHT = 800 # 세로

RECORD_SCALE = 390 # 음반 사진 스케일

INTRO_BACKGROUND_PATH = "./resources/intro_background.jpg"
INTRO_START_PATH = "./resources/intro_start.png"
ARROW_PATH = "./resources/arrow.png"
PLAY_PATH = "./resources/play.png"
BACK_PATH = "./resources/back.png"

AEGUK_NOTE_IMAGE_PATH = "./resources/aeguk_note.png"
TAKEDOWN_NOTE_IMAGE_PATH = "./resources/takedown_note.png"
VIRUS_NOTE_IMAGE_PATH = "./resources/virus_note.png"

SETTING_PATH = "./resources/setting.png"
TO_MAIN_PATH = "./resources/to_main.png"
SELECT_ARROW_PATH = "./resources/select_arrow.png"
EXIT_PATH = "./resources/exit.png"

GALMURI_FONT_PATH = "./resources/fonts/Galmuri11-Bold.ttf"

AEGUK_MUSIC_PATH = "./resources/musics/aegukMusic.mp3"
TAKEDOWN_MUSIC_PATH = "./resources/musics/takedownMusic.mp3"
VIRUS_MUSIC_PATH = "./resources/musics/virusMusic.mp3"

AEGUK_RECORD_PATH = "./resources/aeguk_record.png"
TAKEDOWN_RECORD_PATH = "./resources/takedown_record.png"
VIRUS_RECORD_PATH = "./resources/virus_record.png"

INTRO_BGM_PATH = "./resources/bgms/introSceneBgm.mp3"
SELECT_BGM_PATH = "./resources/bgms/selectSceneBgm.mp3"

AEGUK_NOTE_PATH = "./resources/notemap/aeguk_notemap.json"
TAKEDOWN_NOTE_PATH = "./resources/notemap/takedown_notemap.json"
VIRUS_NOTE_PATH = "./resources/notemap/virus_notemap.json"

JUDGE_LINE = SCREEN_HEIGHT - 200 # 판정선 y좌표
SPEED = [230, 400, 950] # 초당 움직이는 픽셀(노트 속도) --> 난이도 조절 가능

JUDGE_TEXT_LONG = 35

JUDGE_STANDARD = [
    {
        "PERFECT" : 0.1, # 100ms
        "GREAT" : 0.15, # 150ms
        "GOOD" : 0.2, # 200ms
    },
    {
        "PERFECT" : 0.15, # 150ms
        "GREAT" : 0.2, # 200ms
        "GOOD" : 0.25 # 250ms
    },
    {
        "PERFECT" : 0.15,
        "GREAT" : 0.2,
        "GOOD" : 0.25
    }
]


SLIDE_ANIMATION_RECT = (0, (SCREEN_HEIGHT - RECORD_SCALE - 25) / 3.5, SCREEN_WIDTH, RECORD_SCALE + 185)

FRAME_PER_SECOND = 80 # fps

#------------------------------창 설정------------------------------------------#
pygame.init() #초기화
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # 일정한 크기로 창 띄우기
pygame.display.set_caption("리 듬 게 임") # 창 타이틀 설정
#------------------------------기타 변수 정의역-----------------------------------#
clock = pygame.time.Clock()

intro_background = pygame.image.load(INTRO_BACKGROUND_PATH) # 인트로 배경 불러오기

aeguk_record = pygame.image.load(AEGUK_RECORD_PATH) # 애국가 음반 사진 불러오기
aeguk_record = pygame.transform.scale(aeguk_record, (RECORD_SCALE, RECORD_SCALE))
takedown_record = pygame.image.load(TAKEDOWN_RECORD_PATH)
takedown_record = pygame.transform.scale(takedown_record, (RECORD_SCALE, RECORD_SCALE))
virus_record = pygame.image.load(VIRUS_RECORD_PATH)
virus_record = pygame.transform.scale(virus_record, (RECORD_SCALE, RECORD_SCALE))

arrow = pygame.image.load(ARROW_PATH) # 화살표 불러오기
arrow = pygame.transform.scale(arrow, (125, 125))
to_main = pygame.image.load(TO_MAIN_PATH) # 메인으로 버튼 이미지 불러오기
to_main = pygame.transform.scale(to_main, (to_main.get_size()[0] / 4, to_main.get_size()[1] / 4))
to_main_hovered = to_main.copy()
to_main_hovered.fill((50, 50, 50), special_flags = pygame.BLEND_RGB_SUB)
setting = pygame.image.load(SETTING_PATH) # 설정 버튼 이미지 불러오기
setting = pygame.transform.scale(setting, (setting.get_size()[0] / 3, setting.get_size()[1] / 3))
setting_hovered = setting.copy()
setting_hovered.fill((50, 50, 50), special_flags = pygame.BLEND_RGB_SUB)
exit = pygame.image.load(EXIT_PATH)
exit = pygame.transform.scale(exit, (exit.get_size()[0] / 4, exit.get_size()[1] / 4))
exit_hovered = exit.copy()
exit_hovered.fill((50, 50, 50), special_flags = pygame.BLEND_RGB_SUB)
back = pygame.image.load(BACK_PATH)
back = pygame.transform.scale(back, (back.get_size()[0] / 5, back.get_size()[1] / 5))
back_hovered = back.copy()
back_hovered.fill((50, 50, 50), special_flags = pygame.BLEND_RGB_SUB)
intro_start = pygame.image.load(INTRO_START_PATH) # 인트로 시작 버튼 불러오기
intro_start = pygame.transform.scale(intro_start, (intro_start.get_size()[0] * 1.5, intro_start.get_size()[1] * 1.5))
intro_start_hovered = intro_start.copy() # 인트로 시작 버튼 호버 설정
intro_start_hovered.fill((50, 50, 50), special_flags = pygame.BLEND_RGB_SUB)
play = pygame.image.load(PLAY_PATH)
play = pygame.transform.scale(play, (play.get_size()[0] / 5, play.get_size()[1] / 5))
play_hovered = play.copy()
play_hovered.fill((50, 50, 50), special_flags = pygame.BLEND_RGB_SUB)

select_arrow_r = pygame.image.load(SELECT_ARROW_PATH)
select_arrow_r = pygame.transform.scale(select_arrow_r, (select_arrow_r.get_size()[0] / 5, select_arrow_r.get_size()[1] / 5))
select_arrow_hovered_r = select_arrow_r.copy()
select_arrow_hovered_r.fill((50, 50, 50), special_flags = pygame.BLEND_RGB_SUB)
select_arrow_l = pygame.transform.rotate(select_arrow_r, 180)
select_arrow_hovered_l = pygame.transform.rotate(select_arrow_hovered_r, 180)

aeguk_note_image = pygame.image.load(AEGUK_NOTE_IMAGE_PATH)
aeguk_note_image = pygame.transform.scale(aeguk_note_image, (aeguk_note_image.get_size()[0] / 6.7, aeguk_note_image.get_size()[1] / 10))
takedown_note_image = pygame.image.load(TAKEDOWN_NOTE_IMAGE_PATH)
takedown_note_image = pygame.transform.scale(takedown_note_image, (takedown_note_image.get_size()[0] / 6.7, takedown_note_image.get_size()[1] / 10))
virus_note_image = pygame.image.load(VIRUS_NOTE_IMAGE_PATH)
virus_note_image = pygame.transform.scale(virus_note_image, (virus_note_image.get_size()[0] / 6.7, virus_note_image.get_size()[1] / 10))

galmuriFont = pygame.font.Font(GALMURI_FONT_PATH, 135)
judgeFont = pygame.font.Font(GALMURI_FONT_PATH, 30)
scoreFont = pygame.font.Font(GALMURI_FONT_PATH, 25)
keyFont = pygame.font.Font(GALMURI_FONT_PATH, 19)
mediumFont = pygame.font.Font(GALMURI_FONT_PATH , 70)

recordPhoto = [aeguk_record, takedown_record, virus_record] # 음반 사진 리스트
recordTitle = ["애국가", "Takedown", "베토벤 바이러스"] # 음반 제목 리스트
music = [AEGUK_MUSIC_PATH, TAKEDOWN_MUSIC_PATH, VIRUS_MUSIC_PATH] # 음악 리스트
noteMapFiles = [AEGUK_NOTE_PATH, TAKEDOWN_NOTE_PATH, VIRUS_NOTE_PATH] # 노트맵 파일 리스트

scene = "introScene" # 현재 화면
item = 0 # 선택된 음악의 인덱스
itemCount = len(recordPhoto)

noteImages = [aeguk_note_image, takedown_note_image, virus_note_image]

noteMapObjects = [] # 객체로 불러온 json 노트맵 데이터

firstKeyValue = 'D'
secondKeyValue = 'F'
thirdKeyValue = 'J'
fourthKeyValue = 'K'

perfectLong = 0
greatLong = 0
goodLong = 0
missLong = 0

isSetting = False
isPause = False

score = 0
#---------------------------클래스 정의역-------------------------------------#
class Button: # 버튼 클래스 정의
    def __init__(self, img, img_hovered, x, y, action):
        self.x = x
        self.y = y
        self.rect = img.get_rect(topleft = (self.x, self.y))
        self.action = action
        self.img = img
        self.img_hovered = img_hovered
        
    def draw(self):
        mouse = pygame.mouse.get_pos() # 마우스 위치 겟

        if self.rect.collidepoint(mouse): # 버튼 호버 처리
            screen.blit(self.img_hovered, (self.x, self.y))
        else:
            screen.blit(self.img, (self.x, self.y))    

    def clicked(self, event): # 좌클릭 처리
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.action()

class InputField:
    def __init__(self, width, height, x, y, var):
        self.width = width
        self.height= height
        self.x = x
        self.y = y
        self.var = var
        self.rect = pygame.Rect(x, y, width, height)
        self.long = 0
        self.activated = False

    def input(self, event):
        if self.activated:
            if event.type == pygame.KEYDOWN:
                if event.key >= 97 and event.key <= 122:
                    self.var = chr(event.key - 32)
                elif event.key >= 48 and event.key <= 57:
                    self.var = chr(event.key - 32)
    def draw(self):
        mouse = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse):
            pygame.draw.rect(screen, (0, 205, 205), (self.x, self.y, self.width, self.height), 0, 15)
        else:
            pygame.draw.rect(screen, (0, 255, 255), (self.x, self.y, self.width, self.height), 0, 15)
        if self.activated:
            if self.long == -45:
                self.long = 45
            self.long -= 1
            if self.long > 0:
                pygame.draw.line(screen, (0, 0, 0), (self.x + 5, self.y + 10), (self.x + 5, self.y + self.height - 10))

        keyText = keyFont.render(self.var, True, (0, 0, 0))
        screen.blit(keyText, (self.x + 10, self.y + (self.height - 19) / 2))
    def clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.long = 0
                self.activated = True
            else:
                self.activated = False

class Note: # 노트
    def __init__(self, direction, spawnY, timing):
        self.spawnY = spawnY
        self.y = spawnY
        self.direction = direction
        self.timing = timing
        if direction == 1:
            self.spawnX = 0
        elif direction == 2:
            self.spawnX = 150
        elif direction == 3:
            self.spawnX = 300
        else:
            self.spawnX = 450
        self.out = False

    def fall(self):
        global missLong, greatLong, perfectLong, goodLong, score
        self.y = self.spawnY + SPEED[item] * pygame.mixer.music.get_pos() / 1000
        if self.y > JUDGE_LINE:
            self.out = True
            perfectLong = 0
            missLong = JUDGE_TEXT_LONG
            greatLong = 0
            goodLong = 0
            score -= 250
            print(pygame.mixer.music.get_pos())

#---------------------------함수 정의역---------------------------------------#
def coord(s, a): # 글자 중앙 좌표 계산
    r = 0
    for i in range(0, len(s)):
        if s[i] == ' ' or (ord(s[i]) >= 48 and ord(s[i]) <= 57):
            r += a / 2
        elif ord(s[i]) >= 65 and ord(s[i]) <= 97:
            r -= a / 2
        else:
            r += a
    return (SCREEN_WIDTH - r) / 2

def changeItem(direction):
    global item
    if direction: # 오른 화살표
        if item == itemCount - 1:
            item = 0
        else:
            item += 1
    else: # 왼 화살표
        if item == 0:
            item = itemCount - 1
        else:
            item -= 1

def changeScene(sc): # 화면 전환
    global scene
    scene = sc

def settingPanel():
    global isSetting
    isSetting = not isSetting

def pausedPanel():
    global isPause
    isPause = not isPause
    pygame.mixer.music.unpause()

def introScene(): # 인트로 화면 처리
    global scene, isSetting, firstKeyValue, secondKeyValue, thirdKeyValue, fourthKeyValue
    
    pygame.mixer.music.load(INTRO_BGM_PATH) # 배경음악 인트로 브금으로 초기화
    pygame.mixer.music.play(-1)
    
    title = galmuriFont.render("리듬게임", True, (0, 255, 0))

    firstKeyInput = InputField(250, 45, 125, 130, firstKeyValue)
    secondKeyInput = InputField(250, 45, 125, 185, secondKeyValue)
    thirdKeyInput = InputField(250, 45, 125, 240, thirdKeyValue)
    fourthKeyInput = InputField(250, 45, 125, 295, fourthKeyValue)

    firstKeyText = scoreFont.render("키1", True, (0, 0, 0))
    secondKeyText = scoreFont.render("키2", True, (0, 0, 0))
    thirdKeyText = scoreFont.render("키3", True, (0, 0, 0))
    fourthKeyText = scoreFont.render("키4", True, (0, 0, 0))

    exitButton = Button(exit, exit_hovered, 550 - exit.get_size()[0], 100, lambda: settingPanel())
    settingButton = Button(setting, setting_hovered, SCREEN_WIDTH - setting.get_size()[0], 0, lambda: settingPanel())
    startButton = Button(intro_start, intro_start_hovered, 155, 570, lambda: changeScene("selectScene")) # (155, 570) 불러온 시작 버튼 띄우기
    while scene == "introScene":
        screen.blit(intro_background, (0, 0)) # 불러온 배경 화면에 띄우기
        screen.blit(pygame.transform.rotate(arrow, -15), (350, 425))
        screen.blit(pygame.transform.rotate(arrow, 135), (0, 500))

        screen.blit(pygame.font.Font(GALMURI_FONT_PATH, 140).render("리듬게임", True, (0, 100, 0)), (SCREEN_WIDTH * 0.08, SCREEN_HEIGHT * 0.15))
        screen.blit(title, (SCREEN_WIDTH * 0.06, SCREEN_HEIGHT * 0.14))
        startButton.draw()
        if isSetting:
            pygame.draw.rect(screen, (255, 255, 255), (50, 100,  500, 600), 0, 15)
            firstKeyInput.draw()
            secondKeyInput.draw()
            thirdKeyInput.draw()
            fourthKeyInput.draw()

            screen.blit(firstKeyText, (70, 140))
            screen.blit(secondKeyText, (70, 195))
            screen.blit(thirdKeyText, (70, 250))
            screen.blit(fourthKeyText, (70, 305))
        if not isSetting:
            settingButton.draw()
        else:
            exitButton.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # 창 닫기 누르면 닫혀라
                return "quit"
            if not isSetting:
                startButton.clicked(event)
                settingButton.clicked(event)
            else:
                exitButton.clicked(event)

                firstKeyInput.clicked(event)
                secondKeyInput.clicked(event)
                thirdKeyInput.clicked(event)
                fourthKeyInput.clicked(event)

                firstKeyInput.input(event)
                secondKeyInput.input(event)
                thirdKeyInput.input(event)
                fourthKeyInput.input(event)
        pygame.display.update()
        clock.tick(FRAME_PER_SECOND) # fps 제한 적용
    firstKeyValue = firstKeyInput.var
    secondKeyValue = secondKeyInput.var
    thirdKeyValue = thirdKeyInput.var
    fourthKeyValue = fourthKeyInput.var
    return scene

def selectScene(): # 선택 화면 처리
    global scene
    global item

    item = 0

    screen.fill((0, 0, 0))
    title = pygame.font.Font(GALMURI_FONT_PATH, 70).render("음악 선택", True, (255, 255, 255))
    screen.blit(title, ((SCREEN_WIDTH - 315) / 2, SCREEN_HEIGHT * 0.015))
    pygame.draw.rect(screen, (255, 255, 255), ((SCREEN_WIDTH - RECORD_SCALE - 25) / 2, (SCREEN_HEIGHT - RECORD_SCALE - 25) / 3.5, RECORD_SCALE + 25, RECORD_SCALE + 25), 0, 15) # 앨범
    screen.blit(recordPhoto[item], ((SCREEN_WIDTH - RECORD_SCALE) / 2, (SCREEN_HEIGHT - RECORD_SCALE + 25) / 3.5))

    playButton = Button(play, play_hovered, (SCREEN_WIDTH - play.get_size()[0]) / 2, RECORD_SCALE + 270, lambda: changeScene("playScene"))
    rightButton = Button(select_arrow_r, select_arrow_hovered_r, SCREEN_WIDTH - select_arrow_r.get_size()[0] - 70, RECORD_SCALE + 150, lambda: changeItem(1))
    leftButton = Button(select_arrow_l, select_arrow_hovered_l, 70, RECORD_SCALE + 150, lambda: changeItem(0))

    backButton = Button(back, back_hovered, 20, 20, lambda: changeScene("introScene"))

    pygame.mixer.music.load(SELECT_BGM_PATH)
    pygame.mixer.music.play(-1)

    while scene == "selectScene":
        screen.fill((0, 0, 0), SLIDE_ANIMATION_RECT)
        playButton.draw()
        rightButton.draw()
        leftButton.draw()
        backButton.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            playButton.clicked(event)
            rightButton.clicked(event)
            leftButton.clicked(event)
            backButton.clicked(event)
        songName = pygame.font.Font(GALMURI_FONT_PATH, 45).render(recordTitle[item], True, (255, 255, 255)) # 곡 이름
        screen.blit(songName, (coord(recordTitle[item], 45), RECORD_SCALE + 160))
        pygame.draw.rect(screen, (255, 255, 255), ((SCREEN_WIDTH - RECORD_SCALE - 25) / 2, (SCREEN_HEIGHT - RECORD_SCALE - 25) / 3.5, RECORD_SCALE + 25, RECORD_SCALE + 25), 0, 15)
        screen.blit(recordPhoto[item], ((SCREEN_WIDTH - RECORD_SCALE) / 2, (SCREEN_HEIGHT - RECORD_SCALE + 25) / 3.5))
        pygame.display.update()
        clock.tick(FRAME_PER_SECOND)
    return scene

def judge(timing):
    time = pygame.mixer.music.get_pos() / 1000
    if JUDGE_STANDARD[item]["PERFECT"] >= abs(timing - time):
        return 0
    elif JUDGE_STANDARD[item]["GREAT"] >= abs(timing - time):
        return 1
    elif JUDGE_STANDARD[item]["GOOD"] >= abs(timing - time):
        return 2
    else:
        return 3
    
def resultScene():
    global scene, score

    screen.fill((0, 0, 0))
    scoreText = judgeFont.render("스코어 : " + str(score), True, (255, 255, 255))
    screen.blit(scoreText, (coord("스코어 : " + str(score), 30), 500))

    homeButton = Button(to_main, to_main_hovered, (SCREEN_WIDTH - (to_main.get_size()[0])) / 2, 600, lambda: changeScene("introScene"))

    while scene == "resultScene":
        homeButton.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            homeButton.clicked(event)
        pygame.display.update()
        clock.tick(FRAME_PER_SECOND)
    return scene

def playScene():
    global isPause, score, scene, item, perfectLong, greatLong, goodLong, missLong, score, firstKeyValue, secondKeyValue, thirdKeyValue, fourthKeyValue
    
    isPause = False
    exitButton = Button(exit, exit_hovered, 550 - exit.get_size()[0], 100, lambda: pausedPanel())
    homeButton = Button(to_main, to_main_hovered, (SCREEN_WIDTH - (to_main.get_size()[0])) / 2, 600, lambda: changeScene("introScene"))

    perfectText = judgeFont.render("완벽!!!", True, (172, 194, 255))
    greatText = judgeFont.render("훌륭", True, (0, 255, 0))
    goodText = judgeFont.render("아슬아슬", True, (255, 255, 255))
    missText = judgeFont.render("놓침!!!", True, (255, 0, 0))

    pausePanel = pygame.Surface((500, 600))
    pausePanel.set_alpha(128)
    pausePanel.fill((0, 0, 0))

    pygame.draw.rect(pausePanel, (0, 0, 201), (0, 0,  500, 600), 0, 15)
    pauseText = mediumFont.render("일시정지", True, (255, 0, 0))
    pausePanel.blit(pauseText, (110, 0))

    score = 0

    firstKey = ord(firstKeyValue) + 32
    secondKey = ord(secondKeyValue) + 32
    thirdKey = ord(thirdKeyValue) + 32
    fourthKey = ord(fourthKeyValue) + 32

    one_pressed = False
    two_pressed = False
    three_pressed = False
    four_pressed = False

    perfectLong = 0
    greatLong = 0
    goodLong = 0
    missLong = 0

    #-------노트 생성--------#
    notes = deque()
    for note in noteMapObjects[item]["notes"]:
        spawnY = JUDGE_LINE - SPEED[item] * note["timing"]
        notes.append(Note(note["direction"], spawnY, note["timing"]))
    #-------끝---------------#
    end = pygame.USEREVENT + 1

    pygame.mixer.music.set_endevent()
    pygame.event.clear(end)

    pygame.mixer.music.stop()
    pygame.mixer.music.load(music[item])
    pygame.mixer.music.play()
    pygame.mixer.music.set_endevent(end)
    while scene == "playScene":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == end:
                scene = "resultScene"
                break
            if isPause:
                exitButton.clicked(event)
                homeButton.clicked(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if not isPause:
                        pygame.mixer.music.pause()
                        isPause = True
                    else:
                        pygame.mixer.music.unpause()
                        isPause = False
                if not isPause:
                    if event.key == firstKey:
                        one_pressed = True
                        for note in notes:
                            if note.direction != 1:
                                continue
                            judgment = judge(note.timing)
                            if judgment == 0:
                                perfectLong = JUDGE_TEXT_LONG
                                score += 500
                                greatLong = 0
                                goodLong = 0
                                missLong = 0
                                note.out = True
                            elif judgment == 1:
                                greatLong = JUDGE_TEXT_LONG
                                score += 100
                                perfectLong = 0
                                goodLong = 0
                                missLong = 0
                                note.out = True
                            elif judgment == 2:
                                goodLong = JUDGE_TEXT_LONG
                                score += 50
                                perfectLong = 0
                                greatLong = 0
                                missLong = 0
                                note.out = True
                            else:
                                missLong = JUDGE_TEXT_LONG
                                score -= 250
                                perfectLong = 0
                                greatLong = 0
                                goodLong = 0
                            break
                    elif event.key == secondKey:
                        two_pressed = True
                        for note in notes:
                            if note.direction != 2:
                                continue
                            judgment = judge(note.timing)
                            if judgment == 0:
                                perfectLong = JUDGE_TEXT_LONG
                                score += 500
                                greatLong = 0
                                goodLong = 0
                                missLong = 0
                                note.out = True
                            elif judgment == 1:
                                greatLong = JUDGE_TEXT_LONG
                                score += 100
                                perfectLong = 0
                                goodLong = 0
                                missLong = 0
                                note.out = True
                            elif judgment == 2:
                                goodLong = JUDGE_TEXT_LONG
                                score += 50
                                perfectLong = 0
                                greatLong = 0
                                missLong = 0
                                note.out = True
                            else:
                                missLong = JUDGE_TEXT_LONG
                                score -= 250
                                perfectLong = 0
                                greatLong = 0
                                goodLong = 0
                            break
                    elif event.key == thirdKey:
                        three_pressed = True
                        for note in notes:
                            if note.direction != 3:
                                continue
                            judgment = judge(note.timing)
                            if judgment == 0:
                                perfectLong = JUDGE_TEXT_LONG
                                score += 500
                                greatLong = 0
                                goodLong = 0
                                missLong = 0
                                note.out = True
                            elif judgment == 1:
                                greatLong = JUDGE_TEXT_LONG
                                score += 100
                                perfectLong = 0
                                goodLong = 0
                                missLong = 0
                                note.out = True
                            elif judgment == 2:
                                goodLong = JUDGE_TEXT_LONG
                                score += 50
                                perfectLong = 0
                                greatLong = 0
                                missLong = 0
                                note.out = True
                            else:
                                missLong = JUDGE_TEXT_LONG
                                score -= 250
                                perfectLong = 0
                                greatLong = 0
                                goodLong = 0
                            break
                    elif event.key == fourthKey:
                        four_pressed = True
                        for note in notes:
                            if note.direction != 4:
                                continue
                            judgment = judge(note.timing)
                            if judgment == 0:
                                perfectLong = JUDGE_TEXT_LONG
                                score += 500
                                greatLong = 0
                                goodLong = 0
                                missLong = 0
                                note.out = True
                            elif judgment == 1:
                                greatLong = JUDGE_TEXT_LONG
                                score += 100
                                perfectLong = 0
                                goodLong = 0
                                missLong = 0
                                note.out = True
                            elif judgment == 2:
                                goodLong = JUDGE_TEXT_LONG
                                score += 50
                                perfectLong = 0
                                greatLong = 0
                                missLong = 0
                                note.out = True
                            else:
                                missLong = JUDGE_TEXT_LONG
                                score -= 250
                                perfectLong = 0
                                greatLong = 0
                                goodLong = 0
                            break
            elif event.type == pygame.KEYUP:
                if event.key == firstKey:
                    one_pressed = False
                elif event.key == secondKey:
                    two_pressed = False
                elif event.key == thirdKey:
                    three_pressed = False
                elif event.key == fourthKey:
                    four_pressed = False
        screen.fill((0, 0, 0))
        for note in notes:
            note.fall()
            screen.blit(noteImages[item], (note.spawnX, note.y))
        while notes and notes[0].out:
            notes.popleft()
        
        scoreText = scoreFont.render("스코어 : " + str(score), True, (255, 255, 255))
        screen.blit(scoreText, (0, JUDGE_LINE + 27))

        if perfectLong > 0:
            screen.blit(perfectText, (coord("완벽!!!", 30), JUDGE_LINE - 40))
            perfectLong -= 1
        elif greatLong > 0:
            screen.blit(greatText, (coord("훌륭", 30), JUDGE_LINE - 40))
            greatLong -= 1
        elif goodLong > 0:
            screen.blit(goodText, (coord("아슬아슬", 30), JUDGE_LINE - 40))
            goodLong -= 1
        elif missLong > 0:
            screen.blit(missText, (coord("놓침!!!", 30), JUDGE_LINE - 40))
            missLong -= 1
        for i in range(SCREEN_WIDTH // 4, SCREEN_WIDTH, SCREEN_WIDTH // 4): # 라인
            pygame.draw.line(screen, (255, 255, 255), (i, 0), (i, JUDGE_LINE))
        for i in range(0, SCREEN_WIDTH, SCREEN_WIDTH // 4): # 키보드 입력 표시선
            pygame.draw.lines(screen, (255, 0, 0), True, [(i, JUDGE_LINE + 90), (i + SCREEN_WIDTH / 4, JUDGE_LINE + 90), (i + SCREEN_WIDTH / 4, SCREEN_HEIGHT - 10), (i, SCREEN_HEIGHT - 10)], 10)
        pygame.draw.line(screen, (0, 255, 0), (0, JUDGE_LINE), (SCREEN_WIDTH, JUDGE_LINE), 10) # 판정선
        if one_pressed:
            pygame.draw.rect(screen, (255, 255, 255), (10, SCREEN_HEIGHT - 100, SCREEN_WIDTH / 4 - 20, 80))
        if two_pressed:
            pygame.draw.rect(screen, (255, 255, 255), (SCREEN_WIDTH / 4 + 10, SCREEN_HEIGHT - 100, SCREEN_WIDTH / 4 - 20, 80))
        if three_pressed:
            pygame.draw.rect(screen, (255, 255, 255), (SCREEN_WIDTH / 4 * 2 + 10, SCREEN_HEIGHT - 100, SCREEN_WIDTH / 4 - 20, 80))
        if four_pressed:
            pygame.draw.rect(screen, (255, 255, 255), (SCREEN_WIDTH / 4 * 3 + 10, SCREEN_HEIGHT - 100, SCREEN_WIDTH / 4 - 20, 80))

        if isPause:
            screen.blit(pausePanel, (50, 100))
            exitButton.draw()
            homeButton.draw()
        pygame.display.update()
        clock.tick(FRAME_PER_SECOND)
    return scene

#--------------------------노트맵 파일 파싱------------------------------------#
for i in noteMapFiles:
    with open(i, 'r') as f:
        noteMapObjects.append(json.load(f))

#--------------------------사실상 메인 코드임----------------------------------#
while True:
    if scene == "introScene":
        scene = introScene()
    elif scene == "selectScene":
        scene = selectScene()
    elif scene == "playScene":
        scene = playScene()
    elif scene == "resultScene":
        scene = resultScene()
    elif scene == "quit":
        break
    clock.tick(FRAME_PER_SECOND)
pygame.quit()