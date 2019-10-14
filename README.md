# Data Quality Dashboard

Data Quality Dashboard developped using [dash](https://dash.plot.ly/) and [pandas-profiling](https://github.com/pandas-profiling/pandas-profiling)

To launch the project:

```
pip install -r requirements.txt
cd dash
python app.py
```

Or using docker:
```
docker build -t data-quality .
docker run --name data-quality p 8050:8050 data-quality
```

You can then access the app at [http://localhost:8050/](http://localhost:8050/)

And you can try uploading the [titanic dataset](data-titanic.csv) as an example.
