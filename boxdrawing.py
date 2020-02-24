import cv2
import math


# corners
# 1 ––– 2
# |     |
# 3 ––– 4

# draw a rectangle with rounded corners
def rounded_rectangle(src, topLeft, bottomRight, lineColor, thickness, lineType, cornerRadiuses):
    cr1, cr2, cr3, cr4 = cornerRadiuses

    topRight = (bottomRight[0], topLeft[1])
    bottomLeft = (topLeft[0], bottomRight[1])

    # draw corners
    cv2.ellipse(src, (topLeft[0] + cr1, topLeft[1] + cr1), (cr1, cr1), 180, 0, 90, lineColor, thickness)
    cv2.ellipse(src, (topRight[0] - cr2, topRight[1] + cr2), (cr2, cr2), 270, 0, 90, lineColor, thickness)
    cv2.ellipse(src, (bottomLeft[0] + cr3, bottomLeft[1] - cr3), (cr3, cr3), 90, 0, 90, lineColor, thickness)
    cv2.ellipse(src, (bottomRight[0] - cr4, bottomRight[1] - cr4), (cr4, cr4), 0, 0, 90, lineColor, thickness)

    # draw borders
    if thickness >= 0:
        cv2.line(src, (topLeft[0], topLeft[1] + cr1), (bottomLeft[0], bottomLeft[1] - cr3), lineColor, thickness,
                 lineType)
        cv2.line(src, (topLeft[0] + cr1, topLeft[1]), (topRight[0] - cr2, topRight[1]), lineColor, thickness, lineType)
        cv2.line(src, (topRight[0], topRight[1] + cr2), (bottomRight[0], bottomRight[1] - cr4), lineColor, thickness,
                 lineType)
        cv2.line(src, (bottomLeft[0] + cr3, bottomLeft[1]), (bottomRight[0] - cr4, bottomRight[1]), lineColor,
                 thickness, lineType)

    # fill rectangle, if thickness < 0
    else:
        # middle rectangle
        cv2.rectangle(src, (topLeft[0] + cr1, topLeft[1] + cr1), (bottomRight[0] - cr4, bottomRight[1] - cr4),
                      lineColor, thickness, lineType)
        # top rectangle
        if cr1 < cr2:
            cv2.rectangle(src, (topLeft[0] + cr1, topLeft[1]), (topRight[0] - cr2, topRight[1] + cr2),
                          lineColor, thickness, lineType)
        else:
            cv2.rectangle(src, (topRight[0] - cr2, topRight[1]), (topLeft[0] + cr1, topLeft[1] + cr1),
                          lineColor, thickness, lineType)
        # left rectangle
        if cr1 < cr3:
            cv2.rectangle(src, (topLeft[0], topLeft[1] + cr1), (bottomLeft[0] + cr3, bottomLeft[1] - cr3),
                          lineColor, thickness, lineType)
        else:
            cv2.rectangle(src, (bottomLeft[0], bottomLeft[1] - cr3), (topLeft[0] + cr1, topLeft[1] + cr1),
                          lineColor, thickness, lineType)
        # right rectangle
        if cr2 < cr4:
            cv2.rectangle(src, (topRight[0], topRight[1] + cr2), (bottomRight[0] - cr4, bottomRight[1] - cr4),
                          lineColor, thickness, lineType)
        else:
            cv2.rectangle(src, (bottomRight[0], bottomRight[1] - cr4), (topRight[0] - cr2, topRight[1] + cr2),
                          lineColor, thickness, lineType)
        # bottom rectangle
        if cr3 < cr4:
            cv2.rectangle(src, (bottomLeft[0] + cr3, bottomLeft[1]), (bottomRight[0] - cr4, bottomRight[1] - cr4),
                          lineColor, thickness, lineType)
        else:
            cv2.rectangle(src, (bottomRight[0] - cr4, bottomRight[1]), (bottomLeft[0] + cr3, bottomLeft[1] - cr3),
                          lineColor, thickness, lineType)


# draws a rectangle with text in the middle. all required data is stored in rec and txt dictionaries
def draw_rectangle(src, rec, txt):
    output = src.copy()

    p1 = rec["p1"]
    p2 = (p1[0] + rec["width"], p1[1] + rec["height"])
    rounded_rectangle(src, rec["p1"], p2, rec["color"], rec["thickness"], rec["lineType"], rec["corners"])

    cv2.addWeighted(src, rec["alpha"], output, 1 - rec["alpha"], 0, src)  # make transparent

    if txt:
        text_size = cv2.getTextSize(txt["text"], txt["font"], txt["scale"], txt["thickness"])[0]
        text_X = int(p1[0] + ((p2[0] - p1[0] - text_size[0]) / 2))
        text_Y = int(p1[1] + text_size[1] + (p2[1] - p1[1] - text_size[1]) / 2)
        cv2.putText(src, txt["text"], (text_X, text_Y), txt["font"], txt["scale"], txt["color"], txt["thickness"],
                    cv2.LINE_AA)


# draws an outlier. all required data is stored in outlier dictionary
def draw_outlier(src, outlier):
    p1 = outlier["p1"]
    p2 = (p1[0] + outlier["width"], p1[1] + outlier["height"])
    rounded_rectangle(src, p1, p2, outlier["color"], outlier["thickness"], outlier["lineType"], outlier["corners"])

    
# calculates indent between center and box; box top-left point; and the point where line connects to the box
def calculate_points(src, box, m_corners, center):
    h, w = src.shape[0:2]
    
    corner = ("middle", "middle")
    
    if box["width"] + 10 < center[0] < w / 2:
        corner = ("left", corner[1])
    elif w/2 <= center[0] < w - box["width"] - 10:
        corner = ("right", corner[1])

    if box["height"] + 10 < center[1] < h/2:
        corner = (corner[0], "top")
    elif h/2 <= center[1] < h - box["height"] - 10:
        corner = (corner[0], "bottom")

    if corner[0] == "left":
        indent = ((center[0] - box["width"]) * (1 / 3), None)
        point = (int(center[0] - box["width"] - indent[0]), None)
        line_point = (int(point[0] + box["width"] - (m_corners[3] - m_corners[3] / math.sqrt(2))), None)
    elif corner[0] == "right":
        indent = ((w - center[0] - box["width"]) * (1 / 3), None)
        point = (int(center[0] + indent[0]), None)
        line_point = (int(point[0] + (m_corners[3] - m_corners[3] / math.sqrt(2))), None)
    else:
        indent = (box["width"] / 2, None)
        point = (int(center[0] - indent[0]), None)
        line_point = (center[0], None)

    if corner[1] == "top":
        indent = (indent[0], (center[1] - box["height"]) * (2 / 3))
        point = (point[0], int(center[1] - box["height"] - indent[1]))
        line_point = (line_point[0], int(point[1] + box["height"] - (m_corners[3] - m_corners[3] / math.sqrt(2))))
    elif corner[1] == "bottom":
        indent = (indent[0], (h - center[1] - box["height"]) * (2 / 3))
        point = (point[0], int(center[1] + indent[1]))
        line_point = (line_point[0], int(point[1] + (m_corners[3] - m_corners[3] / math.sqrt(2))))
    else:
        indent = (indent[0], box["height"] / 2)
        point = (point[0], int(center[1] - indent[1]))
        line_point = (line_point[0], center[1])

    return point, line_point


# draws whole box with main section, header, text, outlier and line connecting box to detected center point
def draw_box(src, center, n, text):
    # box details
    box = {"width": 210, "height": 140, "corner": 30, "indent": (1 / 3)}
    h_corners = (box["corner"], box["corner"], 0, 0)  # header corners
    m_corners = (0, 0, box["corner"], box["corner"])  # main corners
    o_corners = (box["corner"], box["corner"], box["corner"], box["corner"])  # outlier corners

    # if required point is detected draw box and line
    if center is not None:
        point, line_point = calculate_points(src, box, m_corners, center)

        # draw transparent circle around detected point
        output = src.copy()
        alpha = 0.5
        cv2.circle(src, center, 10, (51, 56, 237), -1)
        cv2.addWeighted(src, alpha, output, 1 - alpha, 0, src)

        # draw line between point and box
        cv2.line(src, line_point, center, (0, 0, 0), 2)

    # else draw box on the left side of the video
    else:
        position = {"xPos": 30, "yPos": 30, "space": 20}
        point = (position["xPos"], position["yPos"] + position["space"] * (n - 1) + box["height"] * (n - 1))

    # more box details
    box["p1"] = point
    header_height = int(box["height"] * (4 / 10))
    main_height = int(box["height"] * (6 / 10))
    main_p1 = (box["p1"][0], int(box["p1"][1] + header_height))

    header_rec = {"p1": box["p1"], "width": box["width"], "height": header_height, "corners": h_corners,
                  "color": (255, 255, 255), "thickness": -1, "lineType": 0, "alpha": 1}
    main_rec = {"p1": main_p1, "width": box["width"], "height": main_height, "corners": m_corners,
                "color": (156, 98, 37), "thickness": -1, "lineType": 0, "alpha": 0.8}
    header_text = {"text": text[0], "font": cv2.FONT_HERSHEY_DUPLEX, "scale": 1, "thickness": 1, "color": (0, 0, 0)}
    main_text = {"text": text[1], "font": cv2.FONT_HERSHEY_DUPLEX, "scale": 1, "thickness": 1, "color": (0, 0, 0)}
    outlier = {"p1": box["p1"], "width": box["width"], "height": box["height"], "corners": o_corners,
               "color": (0, 0, 0), "thickness": 2, "lineType": 0}

    # draw box
    draw_rectangle(src, header_rec, header_text)
    draw_rectangle(src, main_rec, main_text)
    draw_outlier(src, outlier)
