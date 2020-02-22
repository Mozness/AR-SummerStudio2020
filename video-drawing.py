import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
from imutils.video import VideoStream
from flask import Flask, Response
import cv2
import colourdetection
import boxdrawing
import dbfunction as db
import shapedetection as sd

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        # Sets the height and width of the video
        self.video.set(cv2.CAP_PROP_FRAME_WIDTH, 1200)
        self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, 675)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()

        # highilighers colours
        blue_hsv = ((90, 100, 140), (120, 200, 255))  # blue      (190, 130, 75)      [[[106 154 190]]]
        purple_hsv = ((128, 30, 100), (148, 120, 200))  # purple    (150, 100, 130)     [[[138  85 150]]]
        pink_hsv = ((158, 50, 150), (178, 200, 255))  # pink      (145, 100, 215)     [[[168 136 215]]]

        # box 1 – blue
        center1 = sd.ShapeDetector(image, blue_hsv)
        boxdrawing.draw_box(image, center1, ("left", "top"), ("Pressure", db.getPressure()))

        # box 2 – purple
        center2 = sd.ShapeDetector(image, purple_hsv)
        boxdrawing.draw_box(image, center2, ("right", "top"), ("Temperature", db.getTemp()))

        # box 3 – pink
        center3 = sd.ShapeDetector(image, pink_hsv)
        boxdrawing.draw_box(image, center3, ("left", "bottom"), ("Humidity", db.getHum()))

        ret, jpeg = cv2.imencode('.jpg', image)

        return jpeg.tobytes()


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

server = Flask(__name__)
app = dash.Dash(__name__, server=server)

@server.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

app.layout = html.Div([
    dcc.ConfirmDialog(
        id='confirm',
        message='Are you sure you want to export to CSV?',
    ),
    html.H1("Webcam Test", className="header"),
    html.Div(
        children=[
            html.Img(src="/video_feed", className="video"),
        ],
        className="center_body"
    ),
    html.Div(
        html.H2("Export table to CSV", className="header"),
        className="center_body"
    ),
    html.Div(html.P("Select data to export to a CSV file for use in programs such as Excel"), className="center_body"),
    html.Div(
        dcc.Dropdown(
            options=[
                {'label': i, 'value': i}
                for i in ['Temperature and Humidity', 'Pressure']
            ],
            placeholder='Select table...', id='dropdown', style={'width': '400px', 'margin': '10px'},
        ),
        className="center_body"
    ),
    html.Div(id='output-confirm', className="center_body")
])

# Handles export to CSV function
global table

@app.callback(Output('confirm', 'displayed'),
              [Input('dropdown', 'value')])
def display_confirm(value):
    global table
    if value == 'Pressure':
        table = 'p_data'
        return True
    elif value == 'Temperature and Humidity':
        table = 't_data'
        return True

@app.callback(Output('output-confirm', 'children'),
              [Input('confirm', 'submit_n_clicks')])
def update_output(submit_n_clicks):
    global table
    if submit_n_clicks:
        if table == 'p_data':
            db.exportCSV(table)
            return 'Export successful. Available on your Desktop'
        elif table == 't_data':
            db.exportCSV(table)
            return 'Export successful. Available on your Desktop'

if __name__ == '__main__':
    app.run_server(debug=True)