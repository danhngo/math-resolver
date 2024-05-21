import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import base64
import requests

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Math Solver"), className="text-center mt-4")
    ]),
    dbc.Row([
        dbc.Col(html.Button("Take a Picture", id="camera-button", n_clicks=0), className="text-center mt-4")
    ]),
    dbc.Row([
        dbc.Col(dcc.Loading(id="loading-1", children=[
            html.Div(id="output-image"),
            html.Div(id="output-solution")
        ], type="default"), className="text-center mt-4")
    ]),
    dcc.Store(id="image-store"),
    dcc.Input(id='input-on-submit', type='hidden'),
    html.Script(src='/assets/camera.js')
])
@app.callback(
    Output('output-image', 'children'),
    Output('image-store', 'data'),
    Input('input-on-submit', 'value')
)
def update_output_image(image_data):
    if image_data is None:
        return dash.no_update, dash.no_update

    image_data = image_data.split(",")[1]
    return html.Img(src='data:image/png;base64,' + image_data, style={'width': '100%'}), image_data

@app.callback(
    Output('output-solution', 'children'),
    Input('image-store', 'data')
)
def process_image(image_data):
    if image_data is None:
        return dash.no_update

    # Call GPT-4V API to solve the math problem
    solution = solve_math_problem(image_data)
    
    return f"Solution: {solution}"

def solve_math_problem(image_data):
    api_key = "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"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4-vision",
        "prompt": "Solve the math problem in the provided image.",
        "image": image_data,
        "max_tokens": 200
    }
    response = requests.post("https://api.openai.com/v1/images/generations", headers=headers, json=data)
    response_json = response.json()
    
    return response_json["choices"][0]["text"].strip()

if __name__ == '__main__':
    app.run_server(host="0.0.0.0", debug=True)
