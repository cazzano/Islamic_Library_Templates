import dash
from dash import html, dcc, Input, Output, callback
import pandas as pd
import dash_bootstrap_components as dbc

# Initialize Dash App
app = dash.Dash(__name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600&display=swap",
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"
    ]
)

# Enhanced Books Dataset with Multi-Color Palette
books_data = [
    {
        "id": 1,
        "title": "The Noble Quran",
        "author": "Divine Revelation",
        "category": "Holy Book",
        "description": "The ultimate source of divine guidance, providing comprehensive wisdom for humanity.",
        "language": "Arabic & Translations",
        "complexity": "Advanced",
        "spiritual_focus": ["Guidance", "Wisdom", "Spiritual Growth"],
        "icon": "book-quran",
        "accent_color": "#3498db",  # Blue
        "text_color": "#ffffff"
    },
    {
        "id": 2,
        "title": "Sahih Al-Bukhari",
        "author": "Imam Al-Bukhari",
        "category": "Hadith",
        "description": "A comprehensive collection of authenticated sayings and practices of Prophet Muhammad.",
        "language": "Arabic & Translations",
        "complexity": "Intermediate",
        "spiritual_focus": ["Prophetic Traditions", "Historical Context", "Authentic Practices"],
        "icon": "scroll",
        "accent_color": "#e74c3c",  # Red
        "text_color": "#ffffff"
    },
    {
        "id": 3,
        "title": "Riyad us-Saliheen",
        "author": "Imam An-Nawawi",
        "category": "Islamic Teachings",
        "description": "A profound compilation of ethical principles and moral teachings in Islam.",
        "language": "Arabic & Translations",
        "complexity": "Beginner",
        "spiritual_focus": ["Ethical Living", "Moral Development", "Practical Guidance"],
        "icon": "mosque",
        "accent_color": "#2ecc71",  # Green
        "text_color": "#ffffff"
    },
    {
        "id": 4,
        "title": "Tafsir Ibn Kathir",
        "author": "Ibn Kathir",
        "category": "Quranic Interpretation",
        "description": "Comprehensive Quranic exegesis providing deep insights into Quranic verses.",
        "language": "Arabic & Translations",
        "complexity": "Advanced",
        "spiritual_focus": ["Interpretation", "Scholarly Analysis", "Detailed Explanation"],
        "icon": "book-open",
        "accent_color": "#f39c12",  # Orange
        "text_color": "#ffffff"
    },
    {
        "id": 5,
        "title": "Muwatta Malik",
        "author": "Imam Malik",
        "category": "Hadith",
        "description": "A foundational text of Islamic jurisprudence and prophetic traditions.",
        "language": "Arabic & Translations",
        "complexity": "Intermediate",
        "spiritual_focus": ["Jurisprudence", "Legal Principles", "Prophetic Guidance"],
        "icon": "scroll",
        "accent_color": "#FFD700",  # Yellow
        "text_color": "#333"
    }
]

# App Layout with Multi-Color Design
app.layout = dbc.Container([
    # Colorful Gradient Header
    html.Div([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.I(className="fas fa-book-open me-3"),
                    html.Span("Islamic Library", className="display-6 fw-bold")
                ], className="d-flex align-items-center justify-content-center text-white")
            ])
        ])
    ], className="bg-gradient p-4 text-center mb-4", style={
        "background": "linear-gradient(135deg, #3498db, #e74c3c, #2ecc71, #f39c12, #FFD700)",
        "backgroundSize": "400% 400%"
    }),

    # Search and Filter Section
    dbc.Row([
        dbc.Col([
            dbc.InputGroup([
                dbc.Input(
                    id="search-input",
                    placeholder="Search books by title or author...",
                    type="text",
                    className="form-control-lg"
                ),
                dbc.Button(
                    html.I(className="fas fa-search"),
                    id="search-button",
                    color="primary",
                    className="btn-lg"
                )
            ], className="mb-3"),

            dcc.Dropdown(
                id="category-select",
                options=[
                    {"label": "All Categories", "value": "All"},
                    {"label": "Holy Book", "value": "Holy Book"},
                    {"label": "Hadith", "value": "Hadith"},
                    {"label": "Islamic Teachings", "value": "Islamic Teachings"},
                    {"label": "Quranic Interpretation", "value": "Quranic Interpretation"}
                ],
                placeholder="Filter by Category",
                className="mb-3"
            )
        ], width=8, className="mx-auto")
    ]),

    # Books Grid
    html.Div(id="books-grid", className="row g-4")
], fluid=True, className="p-0")

# Book Card Component with Multi-Color Theme
def create_book_card(book):
    return dbc.Col(
        dbc.Card(
            [
                # Iconic Header with Gradient
                html.Div(
                    html.I(className=f"fas fa-{book['icon']} fa-3x text-white text-center w-100 py-3"),
                    className="text-center",
                    style={
                        "background": book['accent_color'],
                        "color": book['text_color'],
                        "borderTopLeftRadius": "0.25rem",
                        "borderTopRightRadius": "0.25rem"
                    }
                ),

                # Card Body
                dbc.CardBody([
                    # Book Title
                    html.H4(
                        book['title'],
                        className="card-title mb-3",
                        style={"color": book['accent_color']}
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
                            html.I(className="fas fa-language me-2"),
                            html.Strong("Language: "),
                            book['language']
                        ])
                    ], flush=True),

                    # Description
                    html.P(
                        book['description'],
                        className="text-muted mt-3"
                    ),

                    # Spiritual Focus Tags
                    html.Div(
                        [
                            html.Span(
                                [html.I(className="fas fa-tag me-1"), focus],
                                className="badge",
                                style={
                                    "backgroundColor": book['accent_color'],
                                    "color": book['text_color'],
                                    "marginRight": "0.5rem"
                                }
                            )
                            for focus in book['spiritual_focus']
                        ],
                        className="mb-3"
                 ),

                    # Action Buttons
                    dbc.Row([
                        dbc.Col([
                            dbc.Button(
                                [html.I(className="fas fa-info-circle me-2"), "Details"],
                                color="primary",
                                size="sm"
                            )
                        ])
                    ])
                ])
            ],
            className="h-100 shadow-sm",
            style={"backgroundColor": "#f8f9fa"}
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
