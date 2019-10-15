import dash_html_components as html


def get_global_stat_view(df):
    if df is not None:
        return html.Div(
            [
                html.P("Number of variales: {}".format(df.shape[1])),
                html.P("Number of observations: {}".format(df.shape[0])),
                html.P(
                    "Total missing values: {}%".format(
                        round(
                            100
                            * (len(df) - df.count()).sum()
                            / (df.shape[0] * df.shape[1]),
                            2,
                        )
                    )
                ),
                html.Hr(),
            ]
        )
    else:
        return []
