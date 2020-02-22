# Import Python Packages
import plotly.graph_objects
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
from dash.dependencies import Input, Output
from flask import Flask, Response
import cv2

# Import project packages
import dbfunction as db
import boxdrawing
import shapedetection as sd
import loground_B as lt

# AR Code
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
        boxdrawing.draw_box(image, center2, ("right", "top"), ("Temperature", db.getWTemp()))

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

# Dash Code
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
server = Flask(__name__)
app = dash.Dash(__name__, server=server, external_stylesheets=external_stylesheets)

@server.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# Dash Layout
app.layout = html.Div([
    html.H1('David.S', className="header"),
    html.H4('Data Acquisition & Visualisation Integrated DeSalination'),
    html.Div(
        children=[
            html.Img(src="/video_feed", className="video"),
        ],
        className="center_body",
    # style=margins
    ),
    html.H4('hello', style={'color':"white"}),
    html.H4('Live Data Plots'),
    # html.H6('hello', style={'color':"white"}),
    html.Div(
        children=[
            html.Button("Export to CSV", className="button", id="button"),
            html.Button("Button 2", className="button")
        ],
        className="center_body",
        # style=margins
    ),
    html.H6('hello', style={'color':"white"}),
    dcc.Slider(
            id='my-slider',
            min=0,
            max=3,
            marks={i: '{}'.format(10 ** i) for i in range(4)},
            step=0.1,
            value=1.8,
            # size=1000,
            # updatemode= 'drag',
    ),
    html.Div(id='slider-output-container'),
    dcc.Graph(id='live-update-graph'),
    dcc.Interval(
            id='interval-component',
            interval=1*1000, # in milliseconds
            n_intervals=0
        )

], style={'margin': '100px'})

# Slider update/function
@app.callback(
    dash.dependencies.Output('slider-output-container', 'children'),
    [dash.dependencies.Input('my-slider', 'value')])
def update_output(value):
    x = lt.rlog(value)
    return "     Viewing the last {} database inputs (slide bar to change).".format(x)


# Graph Update/Function
@app.callback(Output('live-update-graph', 'figure'),
              [Input('interval-component', 'n_intervals'), Input('my-slider', 'value')])
def update_graph_live(n, value):
    limx = int(lt.rlog(value))
    x_w, y_w = db.getdataset('w_data', limx)
    x_p, y_p = db.getdataset('p_data', limx)
    x_t, y_t = db.getdataset('t_data', limx, 3)

    # Create the graph with subplots
    fig = plotly.subplots.make_subplots(rows=3, cols=1, vertical_spacing=0.2, subplot_titles=('Water Temperature (°C)', 'Pressure (kPa)','Humidity (%RH)'))
    fig['layout']['margin'] = {
        'l': 50, 'r': 10, 'b': 30, 't': 50
    }
    # fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}

    fig['layout']['height'] = 700

    fig.append_trace({
        'x': x_w,
        'y': y_w,
        'text': '°C',
        'name': 'Water Temperature',
        'mode': 'lines+markers',
        'type': 'scatter',
        # 'yaxis': dict('title'='Water Temperature (°C)')
    }, 1, 1)
    fig.append_trace({
        'x': x_p,
        'y': y_p,
        'text': 'kPa',
        'name': 'Pressure',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 2, 1)
    fig.append_trace({
        'x': x_t,
        'y': y_t,
        'text': '%RH',
        'name': 'Humidity',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 3, 1)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)