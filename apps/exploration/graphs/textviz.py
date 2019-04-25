"""
This module collects functions and utilities for text visualizations.

Functions:
    - create_wordcloud: Generate a wordcloud and save it to a file.

Notes to others:
    Feel free to write code here either to improve current or to add
    new functionality. Avoid word vectors visualizations at this stage
    of development as it will simply increase (re)load times for the app.
"""

from wordcloud import WordCloud


def create_wordcloud(text, user_id, *, background_color="white",
                     additional_stopwords=[], max_words=2000,
                     save=False, ret=True, **kwargs):
    """
    Generate a wordcloud and save it to a file.

    Args:
        text (str): Raw text for the word cloud.
        user_id (str): Session/user id. Needed to save the image.
        background_color (str):  Color as accepted by wordcloud / matplotlib.
        additional_stopwords (list(str)): Stopwords to remove along \
                                          with the predefined ones.
        max_words (int): Max number of words to include in the wordcloud.
        save (bool): Whether to save the figure. Currently unimportant.
        ret (bool): Whether to return a value. Currently unimportant.
        **kwargs: Anything that `wordcloud.WordCloud` accepts.

    Returns:
        None
    """
    wc = WordCloud(width=700,
                   height=500,
                   background_color=background_color,
                   max_words=max_words,
                   font_step=2,
                   **kwargs)
    wc.generate(text)

    wc.to_file(f"static/images/{user_id}_wordcloud.png")
