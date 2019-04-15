from wordcloud import WordCloud


def create_wordcloud(text, user_id, *, background_color="white", additional_stopwords=[],
                  max_words=2000, save=False, ret=True, **kwargs):

    wc = WordCloud(width=700,
                   height=500,
                   background_color=background_color,
                   max_words=max_words,
                   font_step=2,
                   **kwargs)
    wc.generate(text)

    wc.to_file(f"static/images/{user_id}_wordcloud.png")
