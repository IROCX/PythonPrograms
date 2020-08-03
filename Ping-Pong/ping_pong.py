# ping pong game

import turtle
import time
import winsound

score_a = 0
score_b = 0

window = turtle.Screen()
window.title("Fx Ping-Pong")
window.bgcolor('black')
window.setup(width=800, height=600)
window.tracer(0)


# paddle A
paddle_a = turtle.Turtle()
paddle_a.speed(0)
paddle_a.shape('square')
paddle_a.color('white')
paddle_a.penup()
paddle_a.shapesize(stretch_wid=4, stretch_len=0.8)
paddle_a.goto(-380, 0)


# paddle B
paddle_b = turtle.Turtle()
paddle_b.speed(0)
paddle_b.shape('square')
paddle_b.color('white')
paddle_b.penup()
paddle_b.shapesize(stretch_wid=4, stretch_len=0.8)
paddle_b.goto(+370, 0)

# Ball
ball = turtle.Turtle()
ball.speed(0)
ball.shape('circle')
ball.color('white')
ball.penup()
ball.goto(0, 0)
ball.dx = 0.3
ball.dy = 0.3

# scoring module - pen
pen = turtle.Turtle()
pen.speed(0)
pen.color('white')
pen.penup()
pen.hideturtle()
pen.goto(0, 250 )
pen.write(f"{score_a}:{score_b}", align='center', font=('Courier', 24, 'normal') )

def move_paddle_a_up():
    y = paddle_a.ycor()
    if y < 260:
        y = y+20
        paddle_a.sety(y)


def move_paddle_a_down():
    y = paddle_a.ycor()
    if y > -260:
        y = y-20
        paddle_a.sety(y)


def move_paddle_b_up():
    y = paddle_b.ycor()
    if y < 260:
        y = y+20
        paddle_b.sety(y)


def move_paddle_b_down():
    y = paddle_b.ycor()
    if y > -260:
        y = y-20
        paddle_b.sety(y)

# keyboard binding


window.listen()
window.onkeypress(move_paddle_a_up, 'w')
window.onkeypress(move_paddle_a_down, 's')
window.onkeypress(move_paddle_b_up, 'Up')
window.onkeypress(move_paddle_b_down, 'Down')

# main game loop
while True:
    window.update()

    # move the ball
    ball.setx(ball.xcor()+ball.dx)
    ball.sety(ball.ycor()+ball.dy)

    # border checking
    if (ball.ycor() > 290):
        ball.sety(290)
        ball.dy = ball.dy*-1
        winsound.PlaySound('Ball_Bounce.wav', winsound.SND_ASYNC)
    if (ball.ycor() < -290):
        ball.sety(-290)
        ball.dy = ball.dy*-1
        winsound.PlaySound('Ball_Bounce.wav', winsound.SND_ASYNC)

    # paddle bounce check
    if  ball.xcor() > 365:
        if (paddle_b.ycor()-40) < ball.ycor() < (paddle_b.ycor()+40):
            ball.setx(360)
            ball.dx = ball.dx*-1
            winsound.PlaySound('Ball_Bounce.wav', winsound.SND_ASYNC)
        else:
            score_a+=1
            ball.goto(0,0)
            pen.clear()
            pen.write(f"{score_a}:{score_b}", align='center', font=('Courier', 24, 'normal') )
            time.sleep(2)

    if  ball.xcor() < -365:
        if (paddle_a.ycor()-40)<ball.ycor()<(paddle_a.ycor()+40):
            ball.setx(-360)
            ball.dx = ball.dx*-1
            winsound.PlaySound('Ball_Bounce.wav', winsound.SND_ASYNC)
        else:
            score_b+=1
            ball.goto(0,0)
            pen.clear()
            pen.write(f"{score_a}:{score_b}", align='center', font=('Courier', 24, 'normal') )
            time.sleep(2)
