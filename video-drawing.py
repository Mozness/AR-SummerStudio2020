# Import Python packages
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
from flask import Flask, Response
import cv2
import plotly

# Import project packages
import dbfunction as db
import loground_B as lt
from shapedetection import ShapeDetector
from boxdrawing import draw_box

# AR code
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

        # tape colours
        yellow_hsv = ((20, 50, 50), (40, 200, 255))  # (26, 161, 128)       (30, 93, 225)
        purple_hsv = ((120, 50, 50), (140, 200, 200))  # (132, 140, 95)      (131, 91, 174)
        blue_hsv = ((100, 100, 100), (120, 200, 200))  # (111, 149, 115)      (112, 113, 196,
        green_hsv = ((80, 50, 100), (100, 150, 255))  # (92, 87, 144)        (88, 78, 232)

        # box 1 – yellow
        center1 = ShapeDetector(image, yellow_hsv)
        draw_box(image, center1, 1, ("Pressure", db.getPressure()))

        # box 2 – purple
        center2 = ShapeDetector(image, purple_hsv)
        draw_box(image, center2, 2, ("Temperature", db.getWTemp()))

        # box 3 – blue
        center3 = ShapeDetector(image, blue_hsv)
        draw_box(image, center3, 3, ("Humidity", db.getHum()))

        # box 4 – green
        center4 = ShapeDetector(image, green_hsv)
        draw_box(image, center4, 4, ("W Temp", db.getWTemp()))

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
    dcc.ConfirmDialog(
        id='confirm',
        message='Are you sure you want to export to CSV?',
    ),
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
        ),
    html.Div(
        html.H2("Export table to CSV")
    ),
    html.Div(html.P("Select data to export to a CSV file for use in programs such as Excel")),
    html.Div(
        dcc.Dropdown(
            options=[
                {'label': i, 'value': i}
                for i in ['Temperature and Humidity', 'Pressure']
            ],
            placeholder='Select table...', id='dropdown', style={'width': '400px', 'margin': '10px'},
        ),
    ),
    html.Div(id='output-confirm')

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
