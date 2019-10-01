# 为线程定义一个函数
import pygame,time
def PlaySound_time():
    # pygame.mixer.init()
    # pygame.display.set_mode([300,300])
    # track = pygame.mixer.music.load("pythonSound.wav")
    # pygame.mixer.music.play()
    # time.sleep(100)
    # pygame.mixer.music.stop()
    # count = 0
    # while count < 5:
    #     time.sleep(delay)
    #     count += 1
    #     print("%s: %s" % (threadName, time.ctime(time.time())))

    pygame.init()
    intNumber = 0
    while 1:
        if pygame.mixer.music.get_busy() == False:
            if intNumber == 3:
                break
            else:
                intNumber = intNumber + 1
                print('is playing!' + str(intNumber))
                # screen = pygame.display.set_mode([640, 480])
                pygame.mixer.music.load('Wav/outgoing.wav')
                pygame.mixer.music.play()
        else:
            time.sleep(1)
            print("ffff")
    return