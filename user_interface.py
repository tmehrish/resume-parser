from dash import Dash, dcc, html, Input, Output
from doc_conversion import tokenize, convert_pdf_to_text, get_dates, find_grad, find_latest, get_eligibility, get_matches, get_strength
import base64
import io


app = Dash(__name__)

app.layout = html.Div([
      # Header Section
    html.Div([
        html.H1('Resume Analysis', style={"textAlign": "center", "color": "black", "background-color": "lightblue", "padding": "20px"})
    ], style={"margin-bottom": "20px"}),

    # Content Section
    html.Div([
        dcc.Upload(id='upload_resume', children=html.Button('Upload Resume'), style={"margin-bottom": "20px"}),

        dcc.Input(id='upload_description',
                  type='text',
                  placeholder='Enter job description...',
                  style={'width': '100%', "margin-bottom": "20px"}),
    ], style={"padding": "20px", "border": "1px solid #ccc", "border-radius": "5px", "background-color": "#f9f9f9"}),

    # Results Section
    html.Div([
        html.Div(id='eligibility_output', children='Eligibility', style={"margin-bottom": "20px"}),
        
        html.Div(id='matches_output', children='Matches', style={"margin-bottom": "20px"}),
        
        html.Div(id='strength_output', children='Strength', style={"margin-bottom": "20px"}),
    ], style={"padding": "20px", "border": "1px solid #ccc", "border-radius": "5px", "background-color": "#f9f9f9"})
], style={"max-width": "800px", "margin": "auto", "font-family": "Arial, sans-serif"})

@app.callback(
    Output('upload_resume', 'children'),
    [Input('upload_resume', 'contents')]
)
# Update the button text
def update_output(contents):
    if contents is not None:
        return html.Button('Resume Uploaded')
    else:
        return html.Button('Upload Resume')

@app.callback(
    [Output('eligibility_output', 'children'),
     Output('matches_output', 'children'),
     Output('strength_output', 'children')],
    [Input('upload_resume', 'contents'),
     Input('upload_description', 'value')]
)
# Update the results section to display the eligibility, matches, and strength
def update_output(upload_resume, upload_description):
    if upload_resume is None or upload_description is None:
        return 'Please upload a resume or enter a job description.', '', ''
    
    # Decode the base64 string
    content_type,content_string = upload_resume.split(',')
    decoded = base64.b64decode(content_string)
    pdf_content = io.BytesIO(decoded)

    resume_text = convert_pdf_to_text(pdf_content) 

    tokens = tokenize(resume_text)
    description_tokens = tokenize(upload_description)

    formatted_dates = get_dates(tokens)
    formatted_description_dates = get_dates(description_tokens)

    grad_date = find_grad(formatted_dates)
    latest_date = find_latest(formatted_description_dates)

    # Check if there is a latest date in the job description
    if latest_date is None:
        eligibility_output = None
    else:
        eligibility_output = get_eligibility(grad_date, latest_date)
    # Create an HTML unordered list
    matches = get_matches(tokens, description_tokens)
    # Create an HTML table
    matches_output = html.Table([
        html.Thead(html.Tr([html.Th("Matches")])),
        html.Tbody([html.Tr([html.Td(match)]) for match in matches])
    ]) 
    strength_output = "Strength: " + get_strength(matches)
    
    return eligibility_output, matches_output, strength_output
    

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)