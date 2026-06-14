import turtle


def koch_snowflake(t, length, depth):
    if depth == 0:
        t.forward(length)
    else:
        length /= 3.0
        koch_snowflake(t, length, depth - 1)
        t.left(60)
        koch_snowflake(t, length, depth - 1)
        t.right(120)
        koch_snowflake(t, length, depth - 1)
        t.left(60)
        koch_snowflake(t, length, depth - 1)


def draw_branch(t, length, depth, angle):
    if depth == 0:
        return
    t.forward(length)
    t.left(angle)
    draw_branch(t, length * 0.65, depth - 1, angle)
    t.right(angle * 2)
    draw_branch(t, length * 0.65, depth - 1, angle)
    t.left(angle)
    t.backward(length)


def draw_koch():
    screen = turtle.Screen()
    screen.setup(700, 700)
    screen.bgcolor("#0a1628")
    screen.title("Koch Snowflake")
    screen.tracer(0)

    t = turtle.Turtle()
    t.speed(0)
    t.hideturtle()
    t.pensize(2)

    depth = 4
    size = 200
    start_x = -size / 2
    start_y = size * 0.288

    colors = ["#88ccff", "#aaeeff", "#6699dd", "#ffffff"]
    for i in range(3):
        t.penup()
        t.goto(start_x, start_y)
        t.setheading(i * 120)
        t.pendown()
        t.pencolor(colors[i])
        koch_snowflake(t, size, depth)

    screen.tracer(1)

    t2 = turtle.Turtle()
    t2.speed(0)
    t2.hideturtle()
    for angle in range(0, 360, 30):
        t2.penup()
        t2.goto(0, 10)
        t2.setheading(angle)
        t2.pencolor("#ffffff")
        t2.pensize(1)
        t2.pendown()
        draw_branch(t2, 50, 4, 25)

    screen.update()
    screen.mainloop()


if __name__ == "__main__":
    draw_koch()
