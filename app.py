import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import base64
import requests
import io
import json
from PIL import Image
from openai import OpenAI 
import os

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Math Solver"), className="text-center mt-4")
    ]),
    dbc.Row([
        dbc.Col(dcc.Upload(
            id='upload-image',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select a File')
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },
            # Allow multiple files to be uploaded
            multiple=False
        ), className="text-center mt-4")
    ]),
    dbc.Row([
        dbc.Col(dcc.Loading(id="loading-1", children=[
            html.Div(id="output-image"),
            html.Div(id="output-solution")
        ], type="default"), className="text-center mt-4")
    ]),
    dcc.Store(id="image-store")
])

@app.callback(
    Output('output-image', 'children'),
    Output('image-store', 'data'),
    Input('upload-image', 'contents')
)
def update_output_image(contents):
    if contents is None:
        return dash.no_update, dash.no_update

    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    image = Image.open(io.BytesIO(decoded))

    # Save image as base64
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    image_data = base64.b64encode(buffered.getvalue()).decode('utf-8')

    return html.Img(src='data:image/png;base64,' + image_data, style={'width': '100%'}), image_data

@app.callback(
    Output('output-solution', 'children'),
    Input('image-store', 'data')
)
def process_image(image_data):
    if image_data is None:
        return dash.no_update

    # Call GPT-4V API to solve the math problem
    solution = solve_math(image_data)
    
    return f"Solution: {solution}"

def solve_math(base64_image):
    ## Set the API key and model name
    MODEL="gpt-4o"
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "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"))

    
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that responds in simple text. Help me with my math homework!"},
            {"role": "user", "content": [
                {"type": "text", "text": "pls help to do math or verify the answer"},
                {"type": "image_url", "image_url": {
                    "url": f"data:image/png;base64,{base64_image}"}
                }
            ]}
        ],
        temperature=0.0,
    )
    return response.choices[0].message.content

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
    
    try:
        response_json = response.json()
        print("Response JSON:", json.dumps(response_json, indent=2))  # Debugging line
        return response_json["choices"][0]["text"].strip()
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        print("Error processing response:", e)
        return "Error: Unable to process the image."


if __name__ == '__main__':
    app.run_server(host="0.0.0.0", debug=True)
