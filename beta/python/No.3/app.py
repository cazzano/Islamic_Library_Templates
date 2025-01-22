import dash
from dash import html, dcc, Input, Output, callback
import pandas as pd
import dash_bootstrap_components as dbc

# Initialize Dash App
app = dash.Dash(__name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap",
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"
    ]
)

# Books Dataset with Strategic Color Coding
books_data = [
    {
        "id": 1,
        "title": "The Noble Quran",
        "author": "Divine Revelation",
        "category": "Holy Book",
        "description": "The foundational text of Islam, providing divine guidance",
        "icon": "book-quran",
        "primary_color": "primary",
        "rating": 5.0,
        "difficulty": "Advanced"
    },
    {
        "id": 2,
        "title": "Sahih Al-Bukhari",
        "author": "Imam Al-Bukhari",
        "category": "Hadith",
        "description": "Authentic collection of Prophet Muhammad's sayings",
        "icon": "scroll",
        "primary_color": "success",
        "rating": 4.9,
        "difficulty": "Intermediate"
    },
    {
        "id": 3,
        "title": "Riyad us-Saliheen",
        "author": "Imam An-Nawawi",
        "category": "Islamic Teachings",
        "description": "A comprehensive guide to Islamic ethics and morality",
        "icon": "mosque",
        "primary_color": "danger",
        "rating": 4.7,
        "difficulty": "Beginner"
    }
]

# App Layout
app.layout = html.Div([
    # Navbar
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
        color="dark",
        dark=True
    ),

    # Main Container
    dbc.Container([
        # Search and Filter Section
        dbc.Row([
            dbc.Col([
                html.Div([
                    dbc.Label("Search Books", className="mb-2"),
                    dbc.InputGroup([
                        dbc.Input(
                            id="search-input",
                            placeholder="Enter book title or author...",
                            type="text"
                        ),
                        dbc.Button(
                            html.I(className="fas fa-search"),
                            id="search-button",
                            color="primary",
                            className="ms-2"
                        )
                    ])
                ])
            ], width=6),
            dbc.Col([
                html.Div([
                    dbc.Label("Filter by Category", className="mb-2"),
                    dbc.Select(
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
            ], width=6)
        ], className="my-4"),

        # Books Grid
        html.Div(id="books-grid", className="row g-4")
    ], fluid=True)
])

# Book Card Component
def create_book_card(book):
    return dbc.Col(
        dbc.Card(
            [
                # Card Header with Colored Icon
                html.Div(
                    html.I(className=f"fas fa-{book['icon']} fa-3x text-white text-center w-100 py-3"),
                    className=f"bg-{book['primary_color']} text-center"
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
                            html.Strong("Difficulty: "),
                            book['difficulty']
                        ])
                    ], flush=True),

                    # Description
                    html.P(
                        book['description'],
                        className="text-muted mt-3"
                    ),

                    # Rating and Action Buttons
                    dbc.Row([
                        dbc.Col([
                            dbc.Badge(
                                f"Rating: {book['rating']}/5",
                                color=book['primary_color']
                            )
                        ]),
                        dbc.Col([
                            dbc.Button(
                                [html.I(className="fas fa-info-circle me-2"), "Details"],
                                color=book['primary_color'],
                                size="sm"
                            )
                        ], className="text-end")
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
