import pandas as pd
from bokeh.charts import Line, show, output_file
from bokeh.layouts import gridplot
from bokeh.plotting import figure, show, output_file
import configparser

config = configparser.ConfigParser()
config.read('my_config.ini')

FILE_NAME = config.get("Waka", "fileName")

df = pd.DataFrame.from_csv(FILE_NAME, header=0)
project_names_set = set(df["project"])

projects_duration_dict = {}
for project_name in project_names_set:
    durations_per_project = df[df["project"] == project_name].values
    project_duration_dict = {}
    for date, name, duration in durations_per_project:
        project_duration_dict[date] = duration
    projects_duration_dict[project_name] = project_duration_dict

TOOLS = "pan,wheel_zoom,box_zoom,reset,save,box_select"
p2 = figure(title="Another Legend Example", tools=TOOLS)

for key in projects_duration_dict:
    asd_x = []
    asd_y = []
    for k,v in projects_duration_dict[key].items():
        asd_x.append(k)
        asd_y.append(v)
    print(asd_x)
