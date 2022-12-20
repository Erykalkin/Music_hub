import pygame
import os
import random
import mutagen


# определение текущей рабочей директории
music = []
path = os.getcwd()
print(path + '\music')
# чтение записей
with os.scandir(path + '\music') as listOfEntries:
    for entry in listOfEntries:
        # печать всех записей, являющихся файлами
        if entry.is_file():
            music.append(path + '\music\/' + entry.name)

def shuffle(list):
    random.shuffle(list)

print(music)
pygame.mixer.init()


class Track:
    def __init__(self, track_name, track_num):
        self.num = track_num
        pygame.mixer.music.load(track_name)
        self.volume = 0.5
        pygame.mixer.music.set_volume(self.volume)
        self.length = mutagen.File(music[self.num]).info.length
        self.time = 0
        self.pos = 0

    def upd_time(self):
        self.time = pygame.mixer.music.get_pos()/1000 + self.pos

    def play(self):
        '''Start the track'''
        pygame.mixer.music.play()
        print(music[self.num + 1])
        #pygame.mixer.music.queue(music[self.num + 1])
        #pygame.mixer.music.queue(music[self.num: ])
        self.num += 1
        #print(pygame.mixer.music.queue)
        return self.num + 1
    def stop(self):
        '''Stop the music'''
        pygame.mixer.music.stop()
    def resume(self):
        '''Continue playing'''
        pygame.mixer.music.unpause()
    def pause(self):
        '''Pause the track'''
        pygame.mixer.music.pause()
    def set_volume(self, vol):
        '''Change the volume'''
        self.volume = vol
        pygame.mixer.music.set_volume(self.volume)
    def rewind(self, pos):
        '''Rewinds the track to given position'''
        pygame.mixer.music.stop()
        self.pos = pos
        #pygame.mixer.music.set_pos(pos)
        pygame.mixer.music.play(start=pos)
        pygame.mixer.music.queue(music[self.num + 1])


'''
track1 = Track('morgenshtern-eldzhej-kadillak-mp3.mp3')
track2 = Track('morgenshtern-novyj-merin-mp3.mp3')
print('Choose the track')
song = input()
if song == '1':
    track = Track('morgenshtern-eldzhej-kadillak-mp3.mp3')
if song == '2':
    track = Track('morgenshtern-novyj-merin-mp3.mp3')
'''
global i

i = 0

track = Track(music[0], i)

#print(length)

i += 1

while True:
    '''
    if not pygame.mixer.music.get_busy():
        track = Track(music[i], i)
        track.play()
        i += 1
    '''
    com = ''
    '''
    if track.time >= track.length - 1:
        track = Track(music[i], i)
        track.play()
        i += 1
        print('YA gavno')
    '''

    com = input()
    #print(pygame.mixer.music.get_pos())

    print(i)
    print(pygame.mixer.music.get_pos())
    track.upd_time()
    print(track.time)

    if com == 'shuffle':
        track.stop()
        shuffle(music)
        i = 0
        track = Track(music[i], i)
        i += 1
        #print(music)
        print('Shuffled!')
        print(i)

    if com == 'play':
        track.play()
    if com == 'pause':
        track.pause()
    if com == 'resume':
        track.resume()
    if com == 'skip':
        track.stop()
        track = Track(music[i], i)
        i += 1
        track.play()
    if com == 'rewind':
        print('Enter the time')
        time = float(input())
        #track.stop()
        track.rewind(time)
        #track.play()
    if com == 'stop':
        track.stop()
        '''
        print('What do you want to play next')
        song = input()
        if song == '1':
            track = Track('morgenshtern-eldzhej-kadillak-mp3.mp3')
        if song == '2':
            track = Track('morgenshtern-novyj-merin-mp3.mp3')
        '''
    if com == 'volume':
        print('Введите громкость')
        vol = float(input())
        track.set_volume(vol)
        print(track.volume)