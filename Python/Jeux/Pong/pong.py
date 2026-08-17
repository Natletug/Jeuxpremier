import random
import pygame
import time
from math import sqrt, cos, sin, acos, asin
from pathlib import Path
from PIL import Image
DOSSIER_JEU = Path(__file__).resolve().parent
pygame.init()


image = ["bgpong","Rkt","bll","ponglvlupR","ponglvlupV","ponglvlupB","ponglvlupJ","gover1","gover2","rtry","fondscore"]
name = ["background","rkt","bll","brk1","brk2","brk3","brk4","gover2","gover1","rtry","fndsc"]
images_pygame = {}
for i in range(len(image)):
    img = Image.open(DOSSIER_JEU / "images" / f"{image[i]}.png").convert("RGBA")
    images_pygame[name[i]] = pygame.image.fromstring(img.tobytes(),img.size,"RGBA")


pygame.display.set_caption("Pong")
screen = pygame.display.set_mode((800, 600))
font = pygame.font.Font(None , 36)
plyy = 275
plyv = 5
blly = 280
bllx = 33
bllvi = 2.75
bllvmax = 6
bllvmin = 2
bllvx =  bllvi
bllvy = bllvi * 2 * (random.randint(0, 1) - 0.5 )
lbll = 16
brk = []
hbox = 1
verif = 0
score = 0
bestscore = 0
vbrk = 33
timing = 0
bouton = pygame.Rect(350, 380, 100, 100)
hbox = 0
n = 1000
dejax = 0
dejay = 0
nbclln = 0
effet = .5
signevx = 1
signevy = 2 * (random.randint(0, 1) - 0.5 )


try:
    with open("meilleur_score.txt", "r") as fichier:
        meilleur_score = int(fichier.read())
except FileNotFoundError:
    meilleur_score = 0


#loop
running = True
while running:
    screen.blit(images_pygame["background"], (0, 0))
#controle
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if bouton.collidepoint(event.pos) and verif != 0:
                plyy = 275
                plyv = 5
                blly = 280
                bllx = 33
                bllvi = 2.75
                bllvmax = 6
                bllvmin = 2
                bllvx =  bllvi
                bllvy = bllvi * 2 * (random.randint(0, 1) - 0.5 )
                lbll = 16
                brk = []
                verif = 0
                score = 0
                bestscore = 0
                vbrk = 33
                timing = 0
                effet = .5
                bouton = pygame.Rect(-100, -100, 100, 100)
                n = 1000
                nbclln = 0
    if event.type in (pygame.KEYDOWN, pygame.KEYUP):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                plyy += -plyv
            if event.key == pygame.K_DOWN:
                plyy += plyv
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                plyy += 0

#plus de brik
    n += 1 
    if n > 10000 / vbrk :
        for i in range (6):
            if random.randint(1,2) == 1:
                brk.insert(0 , random.randint(1,4))
            
            else :
                brk.insert(0,0)
        n = 0 
        nbclln += 1 

#wall
    if plyy > 500:
        plyy = 500
    if 0 > plyy:
        plyy = 0
    if blly > 594:
        blly = 594
        signevy *= -1
    if 0 > blly :
        blly = 0
        signevy *= -1
    if bllx > 794:
        bllx = 794
        signevx *= -1
    if 30 > bllx > 30 - bllvmax and plyy +lbll + 100 > blly > plyy -lbll :
        bllx = 30
        signevx *= -1
        score += 1
        effet = abs( blly - plyy -50 + lbll/2 ) / (50 + lbll )
        signevy *=  (-blly - lbll/2 + plyy + 50 ) / abs( blly - plyy -50 + lbll/2 )

        if effet > 0.9:
            effet = 0.9
        if 0.436 > effet:
            effet = 0.436


            
        """
        bllvy = bllvmax * effet
        bllvx = sqrt(bllvmax**2 - bllvx**2)
        if 0 > signevy and 0 > bllvy:
            bllvy *= -1
        print(bllvx,bllvy)"""

#continuer effet ... (grosse défaite ce soir) mais frr j'crois que c'est aléatoire enft jamis ca fait 2 fois pareil -J'abbandone faut faire des bails avec la trigonométrie "je suis pas venu ici pour souffrir OK"


#colisions ...
    dejax -= 1
    dejay -= 1
    if verif == 0:
        bllx += bllvx*signevx
        for i in range (nbclln):
            for j in range (6):
                #Y
                if j*100 +100 > blly - lbll/2 > j*100 - lbll and brk[(i)*6 + j] != 0:
                    #X
                    if 800 - 30*i > bllx - lbll/2 > 770 -30*i -lbll:
                        if 0 >= dejax:
                            brk[(i)*6 + j] = 0
                            score += 1   
                            signevx *= -1
                            bllx += bllvx
                            dejax = 3
        
    
        blly += bllvy*signevy
        for i in range (int(round(len(brk))/6)):
            for j in range (6):
                #Y
                if j*100 +100 > blly - lbll/2 > j*100 - lbll and brk[(i)*6 + j] != 0:
                    #X
                    if 800 - 30*i > bllx - lbll/2 > 770 -30*i -lbll:
                        if 0 >= dejay:
                            brk[(i)*6 + j] = 0
                            score += 1   
                            signevy *= -1
                            blly += bllvy
                            dejay =3
                 
    if hbox == 1:
        for i in range (nbclln):
            for j in range (6):
                if brk[(i)*6 + j] != 0:
                    screen.blit(images_pygame["red"],(800 - 30*i +lbll/2, j*100 +100+lbll/2))
                    screen.blit(images_pygame["red"],(800 - 30*i +lbll/2, j*100 - lbll+lbll/2 ))
                    screen.blit(images_pygame["red"],(770 -30*i -lbll +lbll/2 , j*100 +100+lbll/2))
                    screen.blit(images_pygame["red"],(770 -30*i -lbll +lbll/2, j*100 - lbll+lbll/2))
#score et game over
    if 0 > bllx:
        verif = 1000
        debut = pygame.time.get_ticks()
        vbrk = 0.000000001
        bllx = 900
        bouton = pygame.Rect(350, 380, 100, 100)
        if score > meilleur_score:
            meilleur_score = score
            with open("meilleur_score.txt", "w") as fichier:
                fichier.write(str(meilleur_score))
    t = 0
    if len(brk) == 0:
        for i in range (6):
            brk.append(0)
        nbclln += 1
    if verif == 0:
        for i in range (6):
            if brk[len(brk)-1-i] == 0:
                t += 1
        if t == 6 and len(brk) > 11:
            for i in range (6):
                brk.pop()
            nbclln += -1

    if len(brk) > 150:
        for i in range (6):
            verif += brk[-1]
            brk.pop()
        if verif != 0:
            debut = pygame.time.get_ticks()
            vbrk = 0.00000001
            bouton = pygame.Rect(350, 380, 100, 100)
            if score > meilleur_score:
                meilleur_score = score
                with open("meilleur_score.txt", "w") as fichier:
                    fichier.write(str(meilleur_score))

#affichage
    screen.blit(images_pygame["rkt"], (20, plyy))
    screen.blit(images_pygame["fndsc"], (308 , 485))
    texte = font.render(f"Score : {score}  Best : {meilleur_score}", True, (255, 255, 255))
    screen.blit(texte, ( 300 , 500))
    screen.blit(images_pygame["bll"], (bllx, blly))
    for i in range (nbclln):
            for j in range (6):
                if 0 > i*6 + j or i*6 +j > len(brk) -1 :
                    debut = pygame.time.get_ticks()
                    vbrk = 0.0000001
                    bouton = pygame.Rect(350, 380, 100, 100)
                    if score > meilleur_score:
                        meilleur_score = score
                        with open("meilleur_score.txt", "w") as fichier:
                            fichier.write(str(meilleur_score))
                elif brk[(i)*6 + j] == 1:
                    screen.blit(images_pygame["brk1"], ((770 - 30*i) , (j)*100 ))
                elif brk[(i)*6 + j] == 2:
                    screen.blit(images_pygame["brk2"], ((770 - 30*i) , (j)*100 ))
                elif brk[(i)*6 + j] == 3:
                    screen.blit(images_pygame["brk3"], ((770 - 30*i) , (j)*100 ))
                elif brk[(i)*6 + j] == 4:
                    screen.blit(images_pygame["brk4"], ((770 - 30*i) , (j)*100 ))
                else:
                    ()
    if verif != 0 :
        screen.blit((images_pygame["rtry"]), (368 , 380))
        screen.blit(images_pygame["fndsc"], (308 , 485))
        texte = font.render(f"Score : {score}  Best : {meilleur_score}", True, (255, 255, 255))
        screen.blit(texte, ( 300 , 500))
        timing = round((pygame.time.get_ticks() - debut) / 1000)
        if round(timing/2) == timing / 2 :
            screen.blit(images_pygame["gover1"], (50 , 100))
            pygame.display.update()
        else : 
            screen.blit(images_pygame["gover2"], (50 , 100))
            pygame.display.update()

    pygame.display.update()