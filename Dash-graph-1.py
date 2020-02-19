import dash
from dash.dependencies import Output, Input, State
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objects
from collections import deque

X = deque(maxlen=20)
X.append(1)
Y = deque(maxlen=20)
Y.append(1)

app = dash.Dash(__name__)
app.layout = html.Div([dcc.Graph(id='live-graph',animate=True), dcc.Interval(id='graph-update',interval=1*1000, n_intervals=1)])

@app.callback(Output('live-graph', 'figure'), [Input('graph-update', 'n_intervals')])
def update_graph_scatter(n):
    X.append(X[-1]+1)
    Y.append(Y[-1] + Y[-1] * random.uniform(-0.1, 0.1))

    data = plotly.graph_objects.Scatter(x=list(X), y=list(Y), name = 'scatter', mode = 'lines+markers')

    return {'data':[data], 'layout': plotly.graph_objects.Layout(xaxis=dict(range=[min(X),max(X)]), yaxis=dict(range=[min(Y),max(Y)]),)}


if __name__ == '__main__':
    app.run_server(debug=True)


print('hello ')