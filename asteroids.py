import pygame
import random
import math

pygame.init()
pygame.key.set_repeat(600,600)
MIN_AST_ZERO=45
MAX_AST_ZERO=75
MIN_AST_ONE=30
MAX_AST_ONE=43
MIN_AST_TWO=10
MAX_AST_TWO=15
ASTEROID_SCORES=[10,20,30]
black = (0,0,0)
white = (255,255,255)
green = (0,255,0)
blue= (0,0,255)
red= (255,0,0)
pi = math.pi
ast_vect_len=9
ship_scale=15
clockspeed=20
SHOT_SCALE=4
ROTAT_DELTA=3
ACCEL_DELTA=0.1

def rdm(least,most):
    return random.randrange(least,most+1)
# draws a polygon with approx given side length
def draw_asteroid(screen,x,y,size):
    #draw a polygon with semi random corners
    pygame.draw.polygon(screen,white,[(x,y),(x+size,y),(x+size,y+size),(x,y+size)],5)

#returns an (x,y) pair between -2 and 2
def get_rdm_dir():
    return (rdm(-2,2),rdm(-2,2))
def create_ast_vector(type,xy):
    '''
    Returns a vector with the vertices of the asteroid, and its center point (centered at given xy vector..
    '''
    vertices=[]
    #define the scale ranges
    if type==0 :
        scale_min=MIN_AST_ZERO
        scale_max=MAX_AST_ZERO
    else:
        if type==1 :
            scale_min=MIN_AST_ONE
            scale_max=MAX_AST_ONE
        else:
            if type==2 :
                scale_min = MIN_AST_TWO
                scale_max = MAX_AST_TWO
            else:
                # something's gone wrong, only three kinds of ast exist
                print("Ast_vector TYPE ERROR, type = ",type)
    #so we'll just default to type 0.
        scale_min=15 
        scale_max=45 
    '''for i in range(0,3):
        theta=rdm(30*i,30*i+30)
        scale= rdm(5*i,(i+3)*5)
        vertices.append((theta,scale))
        '''
    for i in [0,1,2,3]:
        for k in range(2):
            theta=rdm(k*45,45*k+45)+i*90 
            scale= rdm(scale_min,scale_max)
            vertices.append((theta,scale))
    x=xy[0]
    y=xy[1]
    vertices.append((x,y))
 #   print("asteroid vector:")
  #  print(vertices)
    return vertices

def draw_ast_vector(ast_vector,rotation):
 
    verts=[]
    x0=ast_vector[len(ast_vector)-1][0]
    y0=ast_vector[len(ast_vector)-1][1]
    for i in range(len(ast_vector)-1):
        x=ast_vector[i][1]*math.cos(math.radians(ast_vector[i][0]+rotation))
        y=ast_vector[i][1]*math.sin(math.radians(ast_vector[i][0]+rotation))
        verts.append((x0+x,y0+y))
    #now verts has the coordinates of each one with rotations..and its a vector.. so
    
    pygame.draw.polygon(screen,white,verts,3)
    return verts
        
def draw_asteroidV(l):
    draw_asteroid(l[0],l[1],l[2],l[3])
#takes a centre point of where the ship is, and its current rotation
    # and draws the ship centered at x,y pointing in the given rotation
def draw_ship(screen,x,y,theta):
    t1=math.radians(theta) # tip is at v1 let's say....
    t2= math.radians((theta+138)%360) 
    t3=math.radians((theta-138)%360)
    #calculate the vertices based on the theta and stuff
    #v1= (ship_scale*(x+math.cos(v1)),ship_scale*(y+math.sin(v1)))
    v1= (x+ship_scale*math.cos(t1),y+ship_scale*math.sin(t1))
    
    v2= (x+ship_scale*math.cos(t2),y+ship_scale*math.sin(t2))
    v3= (x+ship_scale*math.cos(t3),y+ship_scale*math.sin(t3))
    A_v2= (x+0.6*ship_scale*math.cos(t2),y+0.6*ship_scale*math.sin(t2))
    A_v3= (x+0.6*ship_scale*math.cos(t3),y+0.6*ship_scale*math.sin(t3))
    #pygame.draw.polygon(screen,white,[v1,v2,v3],2)
    pygame.draw.line(screen,white,v1,v2,2)
    pygame.draw.line(screen,white,v1,v3,2)
    pygame.draw.line(screen,white,A_v2,A_v3,2)
def new_shot(ship, theta):
    x0=ship[0]
    y0=ship[1]
    x1=x0+SHOT_SCALE*math.cos(math.radians(theta))
    y1=y0+SHOT_SCALE*math.sin(math.radians(theta))
   # print("Pew pew")
    return [(x0,y0),(x1,y1),theta]


'''
collision detection methods
'''
def collision_complicated(shot,asteroid):
    return True
def collision_player_complex(ship, theta, asteroid):
    return True
def collision_shot_simple(shot, boundary): 
     # we simply check start and end of shot.. which is a pair of xy pairs since it's a line... so
    #return collision_simple(shot[0],boundary) or collision_simple(shot[1],boundary)
    c_shot = shot[0]
    r_shot=SHOT_SCALE
    r_bound=boundary[1]
    ctr_bound=boundary[0]
   # print(c_shot)
    return collision_simple(r_shot,c_shot,r_bound,ctr_bound)
def collision_simple(r1,c1,r2,c2):
     dist = math.sqrt(math.pow((c2[0]-c1[0]),2)+math.pow((c2[1]-c1[1]),2))
     return dist <(r1+r2)
def collision_player_simple(xy,theta,boundary):
     # since we know the scale of the ship, we can simply consider it to be a circle... so
     r_player= ship_scale
     r_bound=boundary[1]
     ctr_bound=boundary[0]
     #calculate distance between ctr_bound and xy
     #dist = sqrt((x2-x1)^2+(y2-y1)^2)
     #dist = math.sqrt(math.pow((ctr_bound[0]-xy[0]),2)+math.pow((ctr_bound[1]-xy[1]),2))
     #return dist <(r_player+r_bound)
     return collision_simple(r_player,xy,r_bound,ctr_bound)
def create_ast_bound(vertices, rotation, direction,ast_type):
    # get the centre points from the vertice vector
    x0 = vertices[len(vertices)-1][0] 
    y0= vertices[len(vertices)-1][1] 
    #get the angles (theta) of each point..
    theta0= math.radians(45+rotation)
    theta1= math.radians(135+rotation)
    theta2 = math.radians(225+rotation)
    theta3= math.radians(315 +rotation)

    # we don't actually need  direction.
    # but we will use ast_type
    sidelength=0 # square will have lengths larger than the maximum size of any vertex..
    if ast_type == 0:
        sidelength=MAX_AST_ZERO
    else:
        if ast_type==1:
            sidelength=MAX_AST_ONE
        else:
            if ast_type==2:
                sidelength=MAX_AST_TWO
            else:
                print("Bound type error with type=",ast_type)
    r= sidelength # changed from a bounding square to a circle for ease...
   # verts=[(x0+math.cos(theta0),y0+math.sin(theta0)),(x0+math.cos(theta1),y0+math.sin(theta1)),(x0+math.cos(theta2),y0+math.sin(theta2)),(x0+math.cos(theta3),y0+math.sin(theta3))]
    #return the centrepoint and radius of the bounding circle..
    return [(x0,y0),r]

def draw_explosion(ctr, dist):
    # we will draw a dozen random dots at the dist away from the ctr point...
    angles=[]
    for i in range(5):
        angles.append(rdm(0,360))
    for a in angles:
        x=int(ctr[0]+dist*math.cos(math.radians(a)))
        y= int(ctr[1]+dist*math.sin(math.radians(a)))
        pygame.draw.circle(screen,white,(x,y),1,0)
def draw_shot(screen,shot):
   # print(shot)
    x0y0=shot[0]
    ctr= (int(x0y0[0]),int(x0y0[1]))
    #x1y1=shot[1]
    pygame.draw.circle(screen, white,ctr,2,0)
def calculateMovement(xy,theta, dist):
    # moves the xy pair  the dist distance in theta direction...
    # returns the new location xy
 #   print(xy)
    newX= (xy[0]+ dist*math.cos(theta))%size[0]
    newY= (xy[1]+dist*math.sin(theta)) % size[1]
    return (newX,newY)    
    # return a list of vertices, centered at the same place as the asteroid vector...
def calculate_shot_movement(xy,theta,dist):
    newX= (xy[0]+ dist*math.cos(theta))
    newY= (xy[1]+dist*math.sin(theta)) 
    return (newX,newY)    
    
# polygon(screen,color,[(x1,y1),(x2,y2)...],width=0 (filled))
size = (700,500)
# we use set_mode b/c it allows us to do more then just make a window, also allows
# for mouse control, full screen, etc. 
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Asteroids!")

#now, we'll need a state variable
done = False

# just a clock. tick tock
clock = pygame.time.Clock()
#initialise the polygons
ship = (size[0]/2,size[1]/2)
asteroids=[] # see AST_VECTOR_DESCRIPTION for explanation of what goes in here
ast_bounds=[] # see AST_BOUND_SHAPES for description
shots=[] # |contains two points (a line) and an angle that the shot is moving at...
player_velocity=[]
lives=3
font = pygame.font.Font(None,25) # we'll use that for drawing the score
explosions = [] # will store xy vectors  and lifetimesto draw explosions at...
theta_changed=False
#player_acceleration=0
player_theta=0 # stored in degrees
score=0
k=0
diff_level=0
ship_resetting=-1
while done == False:
# HANDLE EVENTS    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            done=True
        if event.type==pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                #then player shoots
                shots.append(new_shot(ship,player_theta))
            if event.key == pygame.K_UP:
                #if we've turned, or not moved we'll add a new vector...
                if theta_changed or len(player_velocity)==0:
                    player_velocity.append((ACCEL_DELTA,player_theta))
                    theta_changed=False
                else: # if not changed, remove the last vector added and increase it a bit
                    player_velocity.append((player_velocity.pop()[0]+ACCEL_DELTA,player_theta))
            if event.key == pygame.K_DOWN:
                #if we've turned or not accelerated, we'll add a new vector...
                if theta_changed or len(player_velocity)==0:
                    player_velocity.append((-ACCEL_DELTA,player_theta))
                    theta_changed=False
                else: # if not changed, remove the last vector added and decrease it a bit
                    player_velocity.append((player_velocity.pop()[0]-ACCEL_DELTA,player_theta))
            if event.key == pygame.K_RIGHT:
                player_theta-=ROTAT_DELTA
                theta_changed=True
            if event.key == pygame.K_LEFT:
                player_theta+=ROTAT_DELTA
                theta_changed=False
#        if event.type==pygame.KEYUP:
        # we don't handle keyups, because we really wanted to be handling repeated press...
    #would also add more shots if player fired, change player theta if necessary
            #and change player_velocity

# HANDLE MOVEMENTS
        #change player velocity based on acceleration
    #player_acceleration
        # we need to factor in the angle.. velocity should have a direction
        # right now, turning is instant, but it should rotate the ship.
        #first for asteroids...
    for i in range(len(asteroids)):
        currX=(asteroids[i][0][ast_vect_len-1][0])
        currY=(asteroids[i][0][ast_vect_len-1][1])
        #print(asteroids[i])
        dirX=asteroids[i][2][0]
        dirY=asteroids[i][2][1]
        #need to store a direction too...
        asteroids[i][0][ast_vect_len-1]= (((currX+dirX)%size[0]),(currY+dirY)%size[1])
        asteroids[i]= (asteroids[i][0],asteroids[i][1]+(rdm(3,6)),asteroids[i][2],asteroids[i][3])

    # second for player:
    #ship= calculateMovement(ship,player_theta,player_velocity)
    #player_velocity is a collection of vetors and angles, so we move the player for each one
    for vel in player_velocity:
        ship=calculateMovement(ship,vel[1],vel[0])
    
    # third for shots (pew pew pew)
    shotsToPop=[]# a list of indices to remove from shots
    for i in range(len(shots)):
        theta = shots[i][2]
        xy1= shots[i][0]
        xy2=shots[i][1]
       # print("theta=",
        shots[i]=[(calculate_shot_movement(xy1,theta,SHOT_SCALE)),calculate_shot_movement(xy2,theta,SHOT_SCALE),theta]
       #cleanup shots that have moved off screen:
        x0=shots[i][0][0]
        x1=shots[i][1][0]
        y0=shots[i][0][1]
        y1=shots[i][1][1]
        if (x0<0 or x0>size[0]) and (x1<0 or x0>size[0]):
            shotsToPop.append(i)
    for k in shotsToPop:
        shots.pop(k)
    


#HANDLE COLLISIONS(happens after movements b/c what if asteroid dodges a bullet!
    # we'll set up bounding shapes, and tehn delete them later...


    for k in range(len(asteroids)):
       ast_bounds.append((create_ast_bound(asteroids[k][0],asteroids[k][1],asteroids[k][2],asteroids[k][3])))
       # this is just passing all info about the asteroid.
    '''

               AST_BOUNDS DESCRIPTION:
               each element simply describes a circle,
               with a centre point as a vector (ast_bound[0]) and a radius (ast_bound[1])
            '''

 # check shot collisions first, player might just survive if they managed to shoot the asteroid at the last moment...
    shots_to_pop=[]
    ast_to_pop=[]
    for shot in shots:
        i=0 # so we can correspond to the asteroids list
        for bound in ast_bounds:
            if collision_shot_simple(shot,bound):
                if collision_complicated(shot,asteroids[i][0]):
                    old_asteroid=asteroids.pop(i)
                    i-=1 # decr i since we removed an asteroid
# this section needs a try-catch in case the shot instantly hits an asteroid (?)
                    shots.remove(shot) # remove the shot since its used
                    explosions.append((bound[0],0)) #store the center of the asteroid we blew up
                    #new_bound=ast_bounds.remove(bound)
                    #create two new asteroids centered at old_ast...
                    if old_asteroid[3] <2:
                        # then we create 2 new asteroids... (and corresponding bounding shapes)
                        asteroids.append((create_ast_vector(old_asteroid[3]+1,old_asteroid[0][len(old_asteroid[0])-1]),rdm(0,360),get_rdm_dir(),old_asteroid[3]+1))
                        ast_bounds.append((create_ast_bound(asteroids[len(asteroids)-1][0],asteroids[len(asteroids)-1][1],asteroids[len(asteroids)-1][2],asteroids[len(asteroids)-1][3])))
                        asteroids.append((create_ast_vector(old_asteroid[3]+1,old_asteroid[0][len(old_asteroid[0])-1]),rdm(0,360),get_rdm_dir(),old_asteroid[3]+1))
                        ast_bounds.append((create_ast_bound(asteroids[len(asteroids)-1][0],asteroids[len(asteroids)-1][1],asteroids[len(asteroids)-1][2],asteroids[len(asteroids)-1][3])))
                        #now, we aren't changing i but i think that'll be okay...
                    #add to the score based on the type of asteroid
                    score+= ASTEROID_SCORES[old_asteroid[3]]
                    #lastly, since we removed the shot, we need to break from this loop (since we're done with this shot)
                    break
            i+=1 
   
    # now check if player collided
    if ship_resetting<0: # if the ship is not resetting, we'll handle collision for i
        for asteroid in ast_bounds:
            if collision_player_simple(ship,player_theta,asteroid):
                if collision_player_complex(ship,player_theta,asteroid):
                    explosions.append((ship,0))
                    lives-=1
                    # need to do a pause until ship resets..
                    ship=(-1000,--1000)
                    player_velocity=[]
                    player_theta=0
                    ship_resetting=80 # when that reaches 1, we'll reset..
                print("Player blew up!")
                #print(ship)
                #print(asteroid)
                #done=True # for now we just end the game. 
        
    else: #ship is still resetting...
        if ship_resetting==0: # on the last time, we'll redraw it
            ship=(size[0]/2,size[1]/2)
            #player_theta = 270
            #player_velocity=[]
            theta_changed=False
        #print("ship is resetting... ",ship_resetting)
    ast_bounds=[]
    #delete the bounds..

    
#draw stuff:
#first clear screen
    screen.fill(black)
    # draw the score!
    scoreString= "Score: "+str(score)
    text= font.render(scoreString,True,white)
    screen.blit(text,[10,10])
    # draw the lives remaining, as ships...
    for i in range(lives):
        draw_ship(screen,30+30*i,50,270)
    #draw player on screen!
    draw_ship(screen,ship[0],ship[1],player_theta) 
    #if no asteroids, draw some
    if len(asteroids)==0:
        for i in range(diff_level+2): 
            '''
               AST_VECTOR_DESCRIPTION:
               asteroids[i] = [vertices[], 0<=rotation<=360, direction (See get_rdm_dir() for range), type(0-3) ] 
            '''
            asteroids.append((create_ast_vector(0,[rdm(100,size[0]-100),rdm(100,size[1]-100)]),rdm(0,360),get_rdm_dir(),0))
        diff_level+=1 #next round will be harder!
            # adds a vector of all its vertices, and a rotation offset...
    #draw asteroids
    for i in range(len(asteroids)):
        vert=draw_ast_vector(asteroids[i][0],asteroids[i][1])
        #assignment allowed print for debugging

    #draw shots
    for s in shots:
        draw_shot(screen,s)

    #draw explosions
    explosions_to_pop=[]
    for k in range(len(explosions)):
        #draw the explosion:
        draw_explosion(explosions[k][0],3+explosions[k][1])
        print(explosions[k][1])
        explosions[k]= [ explosions[k][0],explosions[k][1]+1]
        #print(explosions[k][1])
        if explosions[k][1]>20:
            # we'll save it to remove later..
            explosions_to_pop.append(k)
    h=0 # this allows us to pop from old indices without getting messed up..
    for p in explosions_to_pop:
        explosions.pop(p-h)
        h+=1
        
    pygame.display.flip()

    clock.tick(clockspeed)
    k+=1
    ship_resetting-=1
   # if k%5==0:
#    player_theta+=1


# end while loop

pygame.quit()
