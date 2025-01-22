import dash
from dash import html, dcc, Input, Output, callback
import pandas as pd
import dash_bootstrap_components as dbc

# Initialize Dash App
app = dash.Dash(__name__,
    external_stylesheets=[
        dbc.themes.FLATLY,
        "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap",
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"
    ]
)

# Books Dataset with Enhanced Metadata
books_data = [
    {
        "id": 1,
        "title": "The Noble Quran",
        "author": "Divine Revelation",
        "category": "Holy Book",
        "description": "The foundational sacred text of Islam, providing comprehensive guidance.",
        "tags": ["Spiritual", "Guidance", "Divine"],
        "published": 610,
        "languages": ["Arabic", "Translations"],
        "icon": "book-quran",
        "color": "primary"
    },
    {
        "id": 2,
        "title": "Sahih Al-Bukhari",
        "author": "Imam Al-Bukhari",
        "category": "Hadith",
        "description": "Comprehensive collection of authenticated sayings of Prophet Muhammad.",
        "tags": ["Prophetic", "Authentic", "Tradition"],
        "published": 870,
        "languages": ["Arabic", "Translations"],
        "icon": "scroll",
        "color": "success"
    },
    {
        "id": 3,
        "title": "Riyad us-Saliheen",
        "author": "Imam An-Nawawi",
        "category": "Islamic Teachings",
        "description": "A profound compilation of ethical and moral teachings in Islam.",
        "tags": ["Ethics", "Morality", "Guidance"],
        "published": 1277,
        "languages": ["Arabic", "Translations"],
        "icon": "mosque",
        "color": "info"
    }
]

# App Layout
app.layout = dbc.Container([
    # Top Navigation
    dbc.Navbar(
        dbc.Container([
            dbc.NavbarBrand([
                html.I(className="fas fa-book-open me-2"),
                "Islamic Library"
            ], href="/"),
            dbc.Nav([
                dbc.NavItem(dbc.NavLink("Home", href="/")),
                dbc.NavItem(dbc.NavLink("Books", href="/books")),
                dbc.NavItem(dbc.NavLink("Categories", href="/categories"))
            ], className="ms-auto")
        ]),
        color="white",
        light=True,
        className="mb-4 shadow-sm"
    ),

    # Main Content Area
    dbc.Row([
        # Sidebar Filters
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Explore Books"),
                dbc.CardBody([
                    # Search Input
                    dbc.Label("Search"),
                    dbc.InputGroup([
                        dbc.Input(
                            id="search-input",
                            placeholder="Search books...",
                            type="text"
                        ),
                        dbc.Button(
                            html.I(className="fas fa-search"),
                            id="search-button",
                            color="primary",
                            className="ms-2"
                        )
                    ], className="mb-3"),

                    # Category Dropdown
                    dbc.Label("Categories"),
                    dcc.Dropdown(
                        id="category-select",
                        options=[
                            {"label": "All Categories", "value": "All"},
                            {"label": "Holy Book", "value": "Holy Book"},
                            {"label": "Hadith", "value": "Hadith"},
                            {"label": "Islamic Teachings", "value": "Islamic Teachings"}
                        ],
                        placeholder="Select Category"
                    )
                ])
            ], className="mb-4")
        ], width=3),

        # Books Grid
        dbc.Col([
            html.Div(id="books-grid", className="row g-4")
        ], width=9)
    ])
], fluid=True, className="p-4")

# Book Card Component
def create_book_card(book):
    return dbc.Col(
        dbc.Card(
            [
                # Card Header with Minimal Icon
                html.Div(
                    html.I(className=f"fas fa-{book['icon']} fa-3x text-white text-center w-100 py-3"),
                    className=f"bg-{book['color']} text-center"
                ),

                # Card Body
                dbc.CardBody([
                    # Book Title
                    html.H4(
                        book['title'],
                        className="card-title mb-3"
                    ),

                    # Book Details
                    dbc.ListGroup([
                        dbc.ListGroupItem([
                            html.Strong("Author: "),
                            book['author']
                        ]),
                        dbc.ListGroupItem([
                            html.Strong("Category: "),
                            book['category']
                        ]),
                        dbc.ListGroupItem([
                            html.Strong("Published: "),
                            book['published']
                        ])
                    ], flush=True),

                    # Tags
                    html.Div(
                        [dbc.Badge(tag, color="light", text_color="dark", className="me-1")
                         for tag in book['tags']],
                        className="mt-3 mb-3"
                    ),

                    # Description
                    html.P(
                        book['description'],
                        className="text-muted"
                    ),

                    # Action Buttons
                    dbc.Row([
                        dbc.Col([
                            dbc.Button(
                                [html.I(className="fas fa-info-circle me-2"), "Details"],
                                color=book['color'],
                                outline=True,
                                size="sm"
                            )
                        ])
                    ])
                ])
            ],
            className="h-100 shadow-sm"
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
