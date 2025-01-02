import pcbnew
from pcbnew import FromMM, ToMM


def draw_segment(board, layer, start, end):
    line = pcbnew.PCB_SHAPE(board)
    line.SetShape(pcbnew.S_SEGMENT)
    print(start, end)
    line.SetStart(start)
    line.SetEnd(end)
    line.SetLayer(layer)
    board.Add(line)

# Define the square size (14mm)
square_size = 14

keySwitchLength = 19.05

# Get the current board
board = pcbnew.GetBoard()

# Get the user layer (layer 1 is typically user.1 in KiCad)
user_layer = pcbnew.GetBoard().GetLayerID("User.1")

# Iterate over all components
for component in board.Footprints():
    # Check if the component reference is 'SW_CHERRY_MX'
    if 'Cherry MX keyswitch' in component.GetKeywords():
        pad = None
        # find the pad with no name
        for pad in component.Pads():
            if pad.GetName() == '':
                break

        if pad is None:
            print('No pad found for component', component.GetReference())
            break

        # Get the component's position
        position = pad.GetPosition()
        print(position)

        # convert to mm
        position = ToMM(position)
        print(position)

        center_x = position[0]
        center_y = position[1]

        pts = [
            (center_x - square_size / 2, center_y - square_size / 2),
            (center_x + square_size / 2, center_y - square_size / 2),
            (center_x + square_size / 2, center_y + square_size / 2),
            (center_x - square_size / 2, center_y + square_size / 2),
        ]

        pts = [(FromMM(x), FromMM(y)) for (x,y) in pts]

        # Draw the square
        draw_segment(board, user_layer, pcbnew.VECTOR2I(pts[0][0], pts[0][1]), pcbnew.VECTOR2I(pts[1][0], pts[1][1]))
        draw_segment(board, user_layer, pcbnew.VECTOR2I(pts[1][0], pts[1][1]), pcbnew.VECTOR2I(pts[2][0], pts[2][1]))
        draw_segment(board, user_layer, pcbnew.VECTOR2I(pts[2][0], pts[2][1]), pcbnew.VECTOR2I(pts[3][0], pts[3][1]))
        draw_segment(board, user_layer, pcbnew.VECTOR2I(pts[3][0], pts[3][1]), pcbnew.VECTOR2I(pts[0][0], pts[0][1]))

# Save the board
pcbnew.Refresh()