import dash
from dash import html, dcc, Input, Output, callback
import pandas as pd
import dash_bootstrap_components as dbc

# Initialize Dash App
app = dash.Dash(__name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap",
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"
    ]
)

# Enhanced Books Dataset
books_data = [
    {
        "id": 1,
        "title": "The Noble Quran",
        "author": "Divine Revelation",
        "category": "Holy Book",
        "description": "The ultimate source of divine guidance for humanity.",
        "tags": ["Spiritual", "Wisdom", "Universal"],
        "difficulty": "Advanced",
        "cover_color": "#3498db"
    },
    {
        "id": 2,
        "title": "Sahih Al-Bukhari",
        "author": "Imam Al-Bukhari",
        "category": "Hadith",
        "description": "Comprehensive collection of Prophetic traditions.",
        "tags": ["Authentic", "Historical", "Prophetic"],
        "difficulty": "Intermediate",
        "cover_color": "#e74c3c"
    },
    {
        "id": 3,
        "title": "Riyad us-Saliheen",
        "author": "Imam An-Nawawi",
        "category": "Islamic Teachings",
        "description": "Profound compilation of ethical and moral teachings.",
        "tags": ["Ethics", "Moral", "Guidance"],
        "difficulty": "Beginner",
        "cover_color": "#2ecc71"
    }
]

# App Layout
app.layout = dbc.Container([
    # Modern Header
    html.Div([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.I(className="fas fa-book-open me-3 text-primary"),
                    html.H1("Islamic Library", className="display-6 fw-bold"),
                    html.P("Discover Wisdom, Explore Knowledge", className="lead text-muted")
                ], className="text-center py-4")
            ])
        ])
    ], className="bg-light mb-4 shadow-sm"),

    # Advanced Search and Filter Section
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col(md=6, className="mb-3 mb-md-0", children=[
                            dbc.InputGroup([
                                dbc.Input(
                                    id="search-input",
                                    placeholder="Search books...",
                                    type="text",
                                    className="form-control-lg"
                                ),
                                dbc.Button(
                                    html.I(className="fas fa-search"),
                                    id="search-button",
                                    color="primary",
                                    className="btn-lg"
                                )
                            ])
                        ]),
                        dbc.Col(md=6, children=[
                            dcc.Dropdown(
                                id="category-select",
                                options=[
                                    {"label": "All Categories", "value": "All"},
                                    {"label": "Holy Book", "value": "Holy Book"},
                                    {"label": "Hadith", "value": "Hadith"},
                                    {"label": "Islamic Teachings", "value": "Islamic Teachings"}
                                ],
                                placeholder="Select Category",
                                className="form-control-lg"
                            )
                        ])
                    ])
                ])
            ], className="shadow-sm")
        ], width=10, className="mx-auto")
    ], className="mb-4"),

    # Books Grid
    html.Div(id="books-grid", className="row g-4")
], fluid=True, className="p-4 bg-white")

# Book Card Component
def create_book_card(book):
    return dbc.Col(
        dbc.Card(
            [
                # Stylized Cover Header
                html.Div(
                    html.Div(
                        html.I(className="fas fa-book fa-2x"),
                        className="d-flex justify-content-center align-items-center h-100 text-white"
                    ),
                    className="book-cover",
                    style={
                        "backgroundColor": book['cover_color'],
                        "height": "150px",
                        "display": "flex",
                        "justifyContent": "center",
                        "alignItems": "center"
                    }
                ),

                # Card Body
                dbc.CardBody([
                    # Book Title
                    html.H4(
                        book['title'],
                        className="card-title mb-3",
                        style={"color": book['cover_color']}
                    ),

                    # Book Details
                    dbc.ListGroup([
                        dbc.ListGroupItem([
                            html.I(className="fas fa-user me-2"),
                            html.Strong("Author: "),
                            book['author']
                        ]),
                        dbc.ListGroupItem([
                            html.I(className="fas fa-layer-group me-2"),
                            html.Strong("Category: "),
                            book['category']
                        ]),
                        dbc.ListGroupItem([
                            html.I(className="fas fa-chart-line me-2"),
                            html.Strong("Difficulty: "),
                            book['difficulty']
                        ])
                    ], flush=True),

                    # Description
                    html.P(
                        book['description'],
                        className="text-muted mt-3"
                    ),

                    # Tags
                    html.Div(
                        [
                            html.Span(
                                tag,
                                className="badge me-2",
                                style={
                                    "backgroundColor": f"{book['cover_color']}20",
                                    "color": book['cover_color']
                                }
                            )
                            for tag in book['tags']
                        ],
                        className="mb-3"
                    ),

                    # Action Buttons
                    dbc.Button(
                        [html.I(className="fas fa-info-circle me-2"), "Explore"],
                        color="outline-primary",
                        size="sm",
                        className="w-100"
                    )
                ])
            ],
            className="h-100 shadow-sm overflow-hidden"
        ),
        lg=4, md=6, sm=12
    )

# Callback for Dynamic Book Filtering
@app.callback(
    Output("books-grid", "children"),
    [Input("search-button", "n_clicks"),
     Input("search-input", "value"),
     Input("category-select", "value")]
)
def update_book_grid(n_clicks, search_term, category):
    df_books = pd.DataFrame(books_data)

    # Filter by search term
    if search_term:
        df_books = df_books[
            df_books['title'].str.contains(search_term, case=False, na=False) |
            df_books['author'].str.contains(search_term, case=False, na=False)
        ]

    # Filter by category
    if category and category != "All":
        df_books = df_books[df_books['category'] == category]

    # Create book cards
    book_cards = [
        create_book_card(book.to_dict())
        for _, book in df_books.iterrows()
    ]

    return book_cards

# Server configuration
if __name__ == '__main__':
    app.run_server(debug=True)
