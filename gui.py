import math
import tkinter as tk

# Translation : Graph coordinate to UI coordinate
coordinates = {
    0: {
        0: (50, 75),
        1: (50, 125),
        2: (50, 175),
        3: (50, 225),
        4: (50, 275),
        5: (50, 325)
    },
    1: {
        -1: (95, 50),
        0: (95, 100),
        1: (95, 150),
        2: (95, 200),
        3: (95, 250),
        4: (95, 300),
    },
    2: {
        -1: (140, 75),
        0: (140, 125),
        1: (140, 175),
        2: (140, 225),
        3: (140, 275),
        4: (140, 325)
    },
    3: {
        -2: (185, 50),
        -1: (185, 100),
        0: (185, 150),
        1: (185, 200),
        2: (185, 250),
        3: (185, 300)
    },
    4: {
        -2: (230, 75),
        -1: (230, 125),
        0: (230, 175),
        1: (230, 225),
        2: (230, 275),
        3: (230, 325)
    },
    5: {
        -3: (275, 50),
        -2: (275, 100),
        -1: (275, 150),
        0: (275, 200),
        1: (275, 250),
        2: (275, 300)
    },
    6: {
        -3: (320, 75),
        -2: (320, 125),
        -1: (320, 175),
        0: (320, 225),
        1: (320, 275),
        2: (320, 325)
    },
    7: {
        -4: (365, 50),
        -3: (365, 100),
        -2: (365, 150),
        -1: (365, 200),
        0: (365, 250),
        1: (365, 300)
    },
    8: {
        -4: (410, 75),
        -3: (410, 125),
        -2: (410, 175),
        -1: (410, 225),
        0: (410, 275),
        1: (410, 325)
    }
}


def draw_hexagon(canvas, x, y):
    size = 30
    points = []
    for i in range(6):
        angle_deg = 60 * i
        angle_rad = math.radians(angle_deg)
        point_x = x + size * math.cos(angle_rad)
        point_y = y + size * math.sin(angle_rad)
        points.append((point_x, point_y))

    canvas.create_polygon(points, outline="black", fill="#E7E8D1")


def draw_rubbish(canvas, x, y, color):
    size = 20
    points = []
    for i in range(6):
        angle_deg = 60 * i
        angle_rad = math.radians(angle_deg)
        point_x = x + size * math.cos(angle_rad)
        point_y = y + size * math.sin(angle_rad)
        points.append((point_x, point_y))

    return canvas.create_polygon(points, outline="black", fill=color)


# Create the main window
window = tk.Tk()
window.title("Shortest Path using A* Algorithm")

# Create a canvas widget
canvas = tk.Canvas(window, width=800, height=500, background="#A7BEAE")
canvas.pack()

# Print the hexagonal map


def printMap():
    for i in range(5):
        for j in range(6):
            draw_hexagon(canvas, 50+(90*i), 75+(50*j))

    for i in range(4):
        for j in range(6):
            draw_hexagon(canvas, 95 + (90*i), 50+(50*j))


printMap()

binWeight = 0
binVolume = 0
disposalRoomCoordinates = [(275, 50), (140, 325), (410, 325)]


def clearRubbish(x, y):
    for i in range(len(disposalRoomCoordinates)):
        if (x == disposalRoomCoordinates[i][0] and y == disposalRoomCoordinates[i][1]):
            global binWeight
            global binVolume
            binWeight = 0
            binVolume = 0
            canvas.itemconfigure(binWeightIndex, text=str(binWeight) + "  kg")
            canvas.itemconfigure(binVolumeIndex, text=str(binVolume) + "  m^3")
            canvas.itemconfigure(conditon, text="Disposal Room")


iter = 0
# Function to print path


# Print rubbsih and disposal rooms
rubbish1 = draw_rubbish(canvas, 50, 325, "green")
rubbish2 = draw_rubbish(canvas, 140, 175, "orange")
rubbish3 = draw_rubbish(canvas, 230, 175, "green")
rubbish4 = draw_rubbish(canvas, 230, 275, "blue")
rubbish5 = draw_rubbish(canvas, 320, 125, "green")
rubbish6 = draw_rubbish(canvas, 320, 275, "orange")
rubbish7 = draw_rubbish(canvas, 410, 125, "green")
rubbish8 = draw_rubbish(canvas, 95, 200, "purple")
rubbish9 = draw_rubbish(canvas, 185, 100, "orange")
rubbish10 = draw_rubbish(canvas, 185, 250, "orange")
rubbish11 = draw_rubbish(canvas, 365, 50, "purple")
rubbish12 = draw_rubbish(canvas, 365, 200, "blue")
canvas.create_line(140, 325, 140, 350, arrow=tk.LAST, fill="orange", width=2)
canvas.create_line(275, 50, 290, 30, arrow=tk.LAST, fill="orange", width=2)
canvas.create_line(410, 325, 430, 340, arrow=tk.LAST, fill="orange", width=2)

rubbish = {
    (50, 325): (rubbish1, 10, 1),
    (140, 175): (rubbish2, 5, 1),
    (230, 175): (rubbish3, 10, 2),
    (230, 275): (rubbish4, 20, 1),
    (320, 125): (rubbish5, 10, 2),
    (320, 275): (rubbish6, 5, 2),
    (410, 125): (rubbish7, 10, 3),
    (95, 200): (rubbish8, 30, 3),
    (185, 100): (rubbish9, 5, 1),
    (185, 250): (rubbish10, 5, 3),
    (365, 50): (rubbish11, 30, 1),
    (365, 200): (rubbish12, 20, 2),
}


solution = [(0, 0), (0, 1), (0, 2), (1, 2), (2, 1), (2, 0), (3, -1), (4, -2), (5, -3), (5, -2), (6, -2), (5, -1), (4, 0), (4, 1), (4, 2), (3, 3), (2, 4), (1, 4), (0, 5), (1, 4),
            (2, 4), (2, 3), (3, 2), (4, 2), (5, 2), (6, 1), (7, 1), (8, 1), (8, 0), (8, -1), (7, -1), (7, -2), (8, -3), (7, -3), (6, -3), (5, -3), (6, -3), (7, -4), (6, -3), (5, -3)]


# Display Bin capacity
rectangle = canvas.create_rectangle(
    490, 40, 700, 170, outline="black", fill="#B85042")

rectangle2 = canvas.create_rectangle(
    490, 200, 700, 350, outline="black", fill="#B85042")

rectangle3 = canvas.create_rectangle(
    40, 380, 400, 480, outline="black", fill="#B85042"
)

canvas.create_text(600, 100, text="Bin Current Capacity : \n\nWeight  \n\nVolume ",
                   fill="black", font=("Times New Roman", 14, "bold"))

binWeightIndex = canvas.create_text(
    650, 100, fill="black", text="0  kg", font=("Times New Roman", 12))

binVolumeIndex = canvas.create_text(
    650, 140, fill="black", text="0  m^3", font=("Times New Roman", 12))

canvas.create_text(560, 270, text="Coordinates :\n\nCurrent \n\nPrevious",
                   fill="black", font=("Times New Roman", 14, "bold"))
currentCoord = canvas.create_text(
    650, 270, fill="black", text="(0, 0)", font=("Times New Roman", 12))

previousCoord = canvas.create_text(
    650, 310, fill="black", text="(0, 0)", font=("Times New Roman", 12))

canvas.create_text(120, 400, text="Room Condition :",
                   fill="black", font=("Times New Roman", 14, "bold"))

conditon = canvas.create_text(
    250, 430, text="Clean",
    fill="black", font=("Times New Roman", 12)
)


def runAnimation(solution):
    def footPrint(x, y):
        global iter
        canvas.itemconfigure(currentCoord, text=str(solution[iter]))

        footprint1 = canvas.create_oval(
            x-15, y-10, x-5, y + 10, outline='black', fill="yellow")
        footprint2 = canvas.create_oval(
            x, y-10, x+10, y+10, outline="black", fill="yellow")

        # Make footprint appear
        canvas.itemconfigure(footprint1, state="normal")
        canvas.itemconfigure(footprint2, state="normal")
        window.update()
        canvas.after(500)

        # If inside of a dirty room
        if (x, y) in rubbish:
            key = (x, y)
            shape, weight, volume = rubbish[key]

            # Update the bin current capacity
            global binWeight
            global binVolume
            binWeight += weight
            binVolume += volume
            canvas.itemconfigure(binWeightIndex, text=str(binWeight) + "  kg")
            canvas.itemconfigure(binVolumeIndex, text=str(binVolume) + "  m^3")
            canvas.itemconfigure(conditon, text="Dirty with rubbish of " +
                                 str(weight) + "  kg " + " and " + str(volume) + " m^3")

            # Remove the rubbish
            canvas.delete(shape)
            rubbish.pop(key)

        else:
            canvas.itemconfigure(conditon, text="Clean")

        clearRubbish(x, y)
        # Make footprint disappear
        canvas.itemconfigure(footprint1, state="hidden")
        canvas.itemconfigure(footprint2, state="hidden")
        window.update()
        canvas.after(500)

        # Make footprint appear
        canvas.itemconfigure(footprint1, state="normal")
        canvas.itemconfigure(footprint2, state="normal")
        canvas.itemconfigure(footprint1, fill="grey")
        canvas.itemconfigure(footprint2, fill="grey")
        window.update()
        canvas.after(500)

        if iter > 0 and iter < len(solution) - 1:
            canvas.itemconfigure(previousCoord, text=str(solution[iter]))

        iter = iter + 1
    for i in range(len(solution)):
        graph_x = solution[i][0]
        graph_y = solution[i][1]
        UI = coordinates[graph_x][graph_y]
        x = UI[0]
        y = UI[1]
        footPrint(x, y)

    # Start the main window's event loop
    window.mainloop()
