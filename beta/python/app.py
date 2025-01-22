import dash
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import pandas as pd

# Initialize Dash App with CDN stylesheets
app = dash.Dash(__name__,
    external_stylesheets=[
        "https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css",
        "https://cdn.jsdelivr.net/npm/daisyui@3.9.4/dist/full.css",
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css",
        dbc.themes.BOOTSTRAP
    ]
)

# Islamic Books Dataset with Icons
books_data = [
    {
        "id": 1,
        "title": "The Noble Quran",
        "author": "Allah (Revealed to Prophet Muhammad)",
        "category": "Holy Book",
        "description": "The central religious text of Islam",
        "icon": "fas fa-book-quran",
        "icon_color": "text-green-600",
        "rating": 5.0
    },
    {
        "id": 2,
        "title": "Sahih Al-Bukhari",
        "author": "Imam Al-Bukhari",
        "category": "Hadith",
        "description": "Most authentic hadith collection",
        "icon": "fas fa-scroll",
        "icon_color": "text-blue-600",
        "rating": 4.9
    },
    {
        "id": 3,
        "title": "Riyad us-Saliheen",
        "author": "Imam An-Nawawi",
        "category": "Islamic Teachings",
        "description": "Gardens of the Righteous",
        "icon": "fas fa-mosque",
        "icon_color": "text-purple-600",
        "rating": 4.7
    }
]

# Create DataFrame
df_books = pd.DataFrame(books_data)

# Navbar Component
def create_navbar():
    return dbc.Navbar(
        dbc.Container([
            dbc.NavbarBrand([
                html.I(className="fas fa-library mr-2"),
                "Islamic Library"
            ], href="/"),
            dbc.Nav([
                dbc.NavItem(dbc.NavLink([
                    html.I(className="fas fa-home mr-1"),
                    "Home"
                ], href="/")),
                dbc.NavItem(dbc.NavLink([
                    html.I(className="fas fa-book mr-1"),
                    "Books"
                ], href="/books")),
                dbc.NavItem(dbc.NavLink([
                    html.I(className="fas fa-tags mr-1"),
                    "Categories"
                ], href="/categories"))
            ], className="ml-auto")
        ])
    )

# Book Card Component
def create_book_card(book):
    return dbc.Card(
        [
            html.Div(
                html.I(className=f"{book['icon']} {book['icon_color']} text-6xl mx-auto my-4"),
                className="flex justify-center items-center"
            ),
            dbc.CardBody([
                html.H4(book['title'], className="card-title text-center"),
                html.P(f"Author: {book['author']}", className="card-text text-center"),
                html.P(f"Category: {book['category']}", className="card-text text-center"),
                html.Div(
                    dbc.Badge(
                        [
                            html.I(className="fas fa-star mr-1"),
                            f"Rating: {book['rating']}/5"
                        ],
                        color="success",
                        className="mx-auto"
                    ),
                    className="flex justify-center"
                )
            ])
        ],
        className="mb-3 shadow-lg text-center"
    )

# App Layout
app.layout = html.Div([
    create_navbar(),
    dbc.Container([
        html.H1(
            [
                html.I(className="fas fa-book-open mr-3"),
                "Islamic Library Collection"
            ],
            className="text-center my-4 flex justify-center items-center"
        ),

        # Search and Filter Section
        dbc.Row([
            dbc.Col([
                dbc.InputGroup([
                    dbc.InputGroupText(html.I(className="fas fa-search")),
                    dbc.Input(
                        id="search-input",
                        placeholder="Search books...",
                        type="text"
                    )
                ]),
            ], width=6),
            dbc.Col([
                dbc.InputGroup([
                    dbc.InputGroupText(html.I(className="fas fa-filter")),
                    dbc.Select(
                        id="category-select",
                        options=[
                            {"label": "All Categories", "value": "All"},
                            {"label": "Holy Book", "value": "Holy Book"},
                            {"label": "Hadith", "value": "Hadith"},
                            {"label": "Islamic Teachings", "value": "Islamic Teachings"}
                        ],
                        value="All"
                    )
                ])
            ], width=6)
        ], className="mb-4"),

        # Books Grid
        html.Div(id="books-grid", className="row")
    ])
])

# Callback for Dynamic Book Filtering
@app.callback(
    Output("books-grid", "children"),
    [Input("search-input", "value"),
     Input("category-select", "value")]
)
def update_book_grid(search_term, category):
    filtered_books = df_books.copy()

    # Filter by search term
    if search_term:
        filtered_books = filtered_books[
            filtered_books['title'].str.contains(search_term, case=False) |
            filtered_books['author'].str.contains(search_term, case=False)
        ]

    # Filter by category
    if category and category != "All":
        filtered_books = filtered_books[filtered_books['category'] == category]

    # Create book cards
    book_cards = [
        dbc.Col(create_book_card(book.to_dict()), width=4)
        for _, book in filtered_books.iterrows()
    ]

    return dbc.Row(book_cards)

# Server configuration
if __name__ == '__main__':
    app.run_server(debug=True)
