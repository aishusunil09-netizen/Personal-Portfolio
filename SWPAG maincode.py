import turtle
import random
import time


# --- Screen Setup ---
screen = turtle.Screen()
screen.setup(width=400, height=600)
screen.title("Flappy Bird Turtle Edition")
screen.bgcolor("sky blue")
screen.tracer(0)


# --- Global Variables ---
score = 0
bird_velocity = 0
game_active = False
pipes = []
clouds = []
pipe_speed = 4
gravity_val = 0.4


# --- Bird ---
bird = turtle.Turtle()
bird.shape("turtle")
bird.color("yellow")
bird.penup()
bird.goto(-150, 0)


# --- Background Clouds ---
def create_clouds():
    for _ in range(4):
        cluster = []
        base_x = random.randint(-200, 200)
        base_y = random.randint(100, 250)


        positions = [(0, 0), (25, 5), (15, -10)]
        for dx, dy in positions:
            cloud_part = turtle.Turtle()
            cloud_part.shape("circle")
            cloud_part.color("white")
            cloud_part.penup()
            cloud_part.goto(base_x + dx, base_y + dy)
            cloud_part.shapesize(stretch_wid=2, stretch_len=2.5)
            cluster.append(cloud_part)


        clouds.append(cluster)


def move_clouds():
    for cluster in clouds:
        for part in cluster:
            part.setx(part.xcor() - 0.5)


        if cluster[0].xcor() < -280:
            new_x = 280
            new_y = random.randint(100, 250)
            offsets = [(0, 0), (25, 5), (15, -10)]
            for i in range(len(cluster)):
                cluster[i].goto(new_x + offsets[i][0], new_y + offsets[i][1])


# --- Scoreboard ---
scoreboard = turtle.Turtle()
scoreboard.hideturtle()
scoreboard.penup()
scoreboard.color("white")
scoreboard.goto(0, 260)


writer = turtle.Turtle()
writer.hideturtle()
writer.penup()
writer.color("white")


def update_score():
    scoreboard.clear()
    scoreboard.write("Score: " + str(score), align="center", font=("Arial", 24, "bold"))


# --- Pipes ---
def create_pipes():
    for i in range(3):
        top = turtle.Turtle()
        top.shape("square")
        top.color("forest green")
        top.shapesize(stretch_wid=30, stretch_len=3)
        top.penup()


        bottom = turtle.Turtle()
        bottom.shape("square")
        bottom.color("forest green")
        bottom.shapesize(stretch_wid=30, stretch_len=3)
        bottom.penup()


        x_pos = 300 + (i * 250)
        gap_y = random.randint(-80, 80)


        top.goto(x_pos, gap_y + 380)
        bottom.goto(x_pos, gap_y - 380)


        pipes.append(top)
        pipes.append(bottom)


def move_pipes():
    global score


    for i in range(len(pipes)):
        pipes[i].setx(pipes[i].xcor() - pipe_speed)


        if pipes[i].xcor() < -250:
            pipes[i].setx(500)


            # Only update gap + score for top pipes
            if i % 2 == 0:
                new_gap = random.randint(-80, 80)
                pipes[i].sety(new_gap + 380)
                pipes[i+1].sety(new_gap - 380)
                score += 1
                update_score()


# --- Controls ---
def flap():
    global game_active, bird_velocity
    if not game_active:
        writer.clear()
        game_active = True
        update_score()
        main_loop()
    else:
        bird_velocity = 8


def apply_gravity():
    global bird_velocity
    bird_velocity -= gravity_val
    bird.sety(bird.ycor() + bird_velocity)


# --- Game Over ---
def end_game():
    global game_active
    game_active = False
    writer.goto(0, 0)
    writer.color("red")
    writer.write("GAME OVER! Score: " + str(score),
                 align="center", font=("Arial", 20, "bold"))
    writer.goto(0, -40)
    writer.write("Press 'R' to Restart",
                 align="center", font=("Arial", 14, "bold"))


def reset_game():
    global score, bird_velocity, game_active


    if not game_active:
        score = 0
        bird_velocity = 0
        bird.goto(-150, 0)
        writer.clear()
        scoreboard.clear()


        for i in range(0, len(pipes), 2):
            x_pos = 300 + (i // 2 * 250)
            gap_y = random.randint(-80, 80)
            pipes[i].goto(x_pos, gap_y + 380)
            pipes[i+1].goto(x_pos, gap_y - 380)


        show_start_message()


def show_start_message():
    writer.clear()
    writer.color("white")
    writer.goto(0, 0)
    writer.write("PRESS SPACE TO START", align="center", font=("Arial", 20, "bold"))
    screen.update()


# --- Main Game Loop ---


#the main game loop
def main_loop():
    while game_active:
        move_clouds()
        apply_gravity()
        move_pipes()


        #check for hitting the floor or ceiling
        if bird.ycor() > 290 or bird.ycor() < -290:
            print("Hit floor/ceiling")
            end_game()


        # --- FINAL COLLISION ATTEMPT ---
        for p in pipes:
            # We check if the bird's X is very close to the pipe's X
            # We use a wider range (45) to make sure it doesn't skip over
            if abs(bird.xcor() - p.xcor()) < 40:
               
                # Check TOP pipes
                if p.ycor() > 0:
                    # If bird is above the gap
                    if bird.ycor() > (p.ycor() - 310):
                        print("Hit top pipe!")
                        end_game()
               
                # Check BOTTOM pipes
                else:
                    # If bird is below the gap
                    if bird.ycor() < (p.ycor() + 310):
                        print("Hit bottom pipe!")
                        end_game()
       
        #refresh the screen to show the movement
        screen.update()
        time.sleep(0.015)




# --- Start Program ---
create_clouds()
create_pipes()
show_start_message()


screen.listen()
screen.onkeypress(flap, "space")
screen.onkeypress(reset_game, "r")


screen.mainloop()
