import turtle as t

t.speed(0)
t.bgcolor("black")
t.title("玫瑰花")

def draw_petal(radius, color):
    t.fillcolor(color)
    t.begin_fill()
    t.circle(radius, 60)
    t.left(120)
    t.circle(radius, 60)
    t.left(120)
    t.end_fill()

def draw_flower():
    t.penup()
    t.goto(0, 0)
    t.pendown()

    colors = ["#ff0040", "#ff1240", "#ff2440", "#ff3650", "#ff4860"]

    for layer in range(5):
        t.pencolor(colors[layer])
        t.left(18)
        for _ in range(12):
            draw_petal(80 + layer * 15, colors[layer])
            t.left(360 / 12)

    # 花心
    t.penup()
    t.goto(0, 170)
    t.pendown()
    t.fillcolor("#ffcc00")
    t.pencolor("#ffcc00")
    t.begin_fill()
    t.circle(30)
    t.end_fill()

def draw_stem():
    t.penup()
    t.goto(0, 0)
    t.pendown()
    t.pensize(6)
    t.pencolor("#228B22")
    t.setheading(270)
    t.forward(180)

    t.pensize(4)

    # 左叶子
    t.penup()
    t.goto(0, -80)
    t.pendown()
    t.setheading(150)
    t.fillcolor("#228B22")
    t.begin_fill()
    t.forward(80)
    t.left(90)
    t.forward(30)
    t.left(90)
    t.forward(80)
    t.end_fill()

    # 右叶子
    t.penup()
    t.goto(0, -130)
    t.pendown()
    t.setheading(30)
    t.fillcolor("#228B22")
    t.begin_fill()
    t.forward(80)
    t.right(90)
    t.forward(30)
    t.right(90)
    t.forward(80)
    t.end_fill()

draw_stem()
draw_flower()

t.hideturtle()
t.done()
