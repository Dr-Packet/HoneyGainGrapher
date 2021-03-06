import plotly
import plotly.graph_objs as go
import json
import datetime  # import datetime
import time
import sys
from urllib.parse import unquote
f = open("data.json", "r")
json_string = "["
json_string += f.read()
json_string = json_string[:-2]
json_string += "]"
json_string = json_string.replace('\'', '"')
parsed_json = json.loads(json_string)

f = open("idmap.json", "r")
json_string = f.read()
json_string = json_string.replace('\'', '"')
idmap_json = json.loads(json_string)

list = [0]

time1 = [[]]
timeTotal = []
displayName = [[]]
total_traffic_delta = [[]]
all_total_traffic_delta = []
traficDeltaOrder = []
last_total_traffic = []
ids = []
idOrder = []
wusTrace = []
wusTrace = []
lastSampleTime=[]
lastTime = 0


def datetime_from_utc_to_local(utc_datetime):
    now_timestamp = time.time()
    offset = datetime.datetime.fromtimestamp(
        now_timestamp) - datetime.datetime.utcfromtimestamp(now_timestamp)
    return utc_datetime + offset


for b in parsed_json:
    if datetime.datetime.fromtimestamp(b['9']) != lastTime:
        lastTime = datetime.datetime.fromtimestamp(b['9'])
        idOrder = []
        traficDeltaOrder = []
        all_total_traffic_delta.append(0)
        timeTotal.append(datetime_from_utc_to_local(
            datetime.datetime.fromtimestamp(b['9']))
        )
    if b['1'] not in ids:
        ids.append(b['1'])
        total_traffic_delta.append([])
        last_total_traffic.append(b['7']/1000000)
        time1.append([])
        lastSampleTime.append(0)
    if b['1'] not in idOrder:
        idOrder.append(b['1'])
        traficDeltaOrder.append(
            (b['7']/1000000)-last_total_traffic[ids.index(b['1'])]
        )
    
    time1[ids.index(b['1'])].append(
        datetime_from_utc_to_local(
            datetime.datetime.fromtimestamp(
                b['9']
            )
        )
    ) 
    total_traffic_delta[ids.index(b['1'])].append(
        ((b['7']/1000000)-last_total_traffic[ids.index(b['1'])])/
        ((b['9']-lastSampleTime[ids.index(b['1'])])/3600)
    )
    all_total_traffic_delta[len(all_total_traffic_delta)-1] += (
        ((b['7']/1000000)-last_total_traffic[ids.index(b['1'])])/
        ((b['9']-lastSampleTime[ids.index(b['1'])])/3600)
    )

    last_total_traffic[ids.index(b['1'])] = b['7']/1000000
    lastSampleTime[ids.index(b['1'])]=b['9']
wusTrace.append(
    go.Scatter(
        x=timeTotal,
        y=all_total_traffic_delta,
        name="Total",
        visible='legendonly'
    )
)

Z = [x for _, x in sorted(zip(traficDeltaOrder, idOrder))]
for b in reversed(Z):
    wusTrace.append(
        go.Scatter(
            x=time1[ids.index(b)],
            y=total_traffic_delta[ids.index(b)],
            name=unquote(idmap_json[b]['title']),
            visible='legendonly'
        )
    )

data = [
    wusTrace,
]

dtnow = datetime.datetime.now()
unixnow = time.mktime(dtnow.timetuple())*1000

unix_two_day = 2*24*60*60*1000
unix_one_week = 7*24*60*60*1000
unix_ten_day = 10*24*60*60*1000

titlestrg1 = sys.argv[1]

layout_g1 = go.Layout(
    title=titlestrg1,
    xaxis=dict(
        range=[
            unixnow-unix_two_day,
            unixnow
        ],
        title='Time',
        tickformat='%m/%d/%Y, %I:%M %p',
        dtick=43200000,  # 86400000
        ticklen=8,
        tickwidth=4,
        gridwidth=2,
        automargin=True,
        type="date",
    ),

    yaxis=dict(
        title='Data MB/h'
    )
)


#print ("start ploting :HoneyGainDevicesDelta_plot")
fig_g1 = go.Figure(data=data[0], layout=layout_g1)
plotly.offline.plot(
    fig_g1, filename='www/HoneyGainDevicesDelta_plot.html', auto_open=False)
#print ("done ploting :HoneyGainDevicesDelta_plot")
