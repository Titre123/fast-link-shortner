from fasthtml.common import *
import dub
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Dub with the API key from the environment variables
d = dub.Dub(token=os.getenv('DUB_API_KEY'))

# Initialize the FastHTML app
app, rt = fast_app()

@rt("/")
def index():
    # This function defines the home page of the application, which includes a form to input URLs for shortening.
    return Titled(
        "AI Link Shortener",
        Article(
            Form(method="post", action="/shorten")(
                Label("Enter URL: ", Input(name="url", type="url", required=True)),
                Button("Shorten", type="submit")
            ),
            Div(id="result")
        )
    )

@rt("/shorten")
async def shorten(url: str):
    # This function handles the shortening of URLs. It attempts to shorten the URL using Dub.co and returns the result.
    try:
        response = d.links.create(request={"url": url})
        short_link = response.short_link
    except Exception as e:
        short_link = f"Error: {e}"

    # This returns the result of the shortening process, including the original URL, the shortened URL, and a link to shorten another URL.
    return Titled(
        "Shortened Link",
        Article(
            P(f"Original URL: {url}"),
            P(f"Shortened URL: ", A(href=short_link)(short_link)),
            A(href="/")("Shorten another link")
        )
    )

# This starts the FastHTML application server.
serve()