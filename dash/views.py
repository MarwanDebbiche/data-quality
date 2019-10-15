import dash_html_components as html
import dash_table

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
                )
            ]
        )
    else:
        return []


def get_head_view(df):
    return html.Div(
        [
            html.H5("Head :"),
            dash_table.DataTable(
                data=df.head(5).to_dict("rows"),
                columns=[{"name": i, "id": i} for i in df.columns],
            )
        ]
    )
