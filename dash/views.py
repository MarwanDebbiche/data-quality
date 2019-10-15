import dash_html_components as html
import dash_table


def get_global_stat_view(data_manager):
    if data_manager.data is not None:
        df_stats = data_manager.get_dataset_stats()
        return html.Div(
            [
                html.Div(
                    [
                        html.P(f"Number of variales: {df_stats['n_var']}"),
                        html.P(f"Number of observations: {df_stats['n_obs']}"),
                        html.P(
                            f"Total missing values: {df_stats['missing_count']} "
                            f"({round(df_stats['missing_count_percent'], 2)} %)"
                        )
                    ],
                    className="six columns"
                )
            ],
            className="row flex-display"
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
