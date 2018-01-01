from bokeh.models import ColumnDataSource, DataRange1d, Range1d,Plot, LinearAxis, Grid,SingleIntervalTicker,ResetTool,\
    BoxSelectTool,HoverTool, BoxZoomTool, WheelPanTool,WheelZoomTool, TapTool,PanTool,CustomJS
from bokeh.models.glyphs import Rect, HBar
from bokeh.io import curdoc, output_notebook,show
from bokeh.plotting import figure, curdoc,output_file,show
import pandas as pd
import xml.etree.ElementTree as etree
import pprint

file = 'IREvNZL Events.xml'
team1 = file[0:3]
team2 = file[4:7]
pp = pprint.PrettyPrinter(indent=4)
root = etree.parse(file)
doc = root.getroot()
rootInstance = root.find('ALL_INSTANCES')
codes_set = set()
codes_list = []
codes_count = []
start = []
end = []
all_info = {}
count = 0       # Used to store how mant times each code appears
code_list =[]
entire_codes = []
temp_dict = {}
each_code = [] #Will include a list of each code x number of times it appears
all_codes = []
all_counts = [] # Will include the number assigned to the code x how many times that code appears
colors = []
overall_code_count = 0
all_starts = []
all_ends = []
plot_start = 200000
plot_end = 0

#Get the count of how many distinctive codes there are
for i in rootInstance.iterfind('instance'):
    if i.findtext('code') not in codes_set:
        codes_set.add(i.findtext('code'))#First time to see code
        overall_code_count += 1
codes_set = set()
#Extract all relevant data from xml file
for i in rootInstance.iterfind('instance'):
    if i.findtext('code') not in codes_set:             #First time to see code
        codes_set.add(i.findtext('code'))
        temp_dict['code']=i.findtext('code')            #Add new code to dictionary
        codes_list.append(i.findtext('code'))
        for j in rootInstance.iterfind('instance'):     #Loop through codes again
            if i.findtext('code') == j.findtext('code'):#Code == one in outer loop
                count+=1
                start.append(round(float(j.findtext('start'))))       #Add start time to list of starts for that code
                if float(j.findtext('start'))<plot_start:
                    plot_start = float(j.findtext('start'))#round(2.675, 2)
                end.append(round(float(j.findtext('end'))))
                if float(j.findtext('end'))>plot_end:
                    plot_end = float(j.findtext('end'))
            each_code = [i.findtext('code')]*count      #Make list of the code x number of times it appears
        all_codes.extend(each_code)                     #Add the list of each code to list of all codes
        temp_dict['count']=count
        codes_count.append(count)
        temp_dict['start'] = start                      #Add list of start times as value to start key in dict
        temp_dict['end'] = end
        code_list.append(temp_dict.copy())              #Add full dict to list
        temp_dict.clear()                               #Clear for next iteration
        all_starts.extend(start)
        all_ends.extend((end))
        start = []
        end = []
        all_counts.extend([overall_code_count]*count)
        count = 0
        overall_code_count -= 1
#Creare a list for the team associated with each event and a colour for that team
team_list = []
for code in all_codes:
    if team2 in code:
        colors.append("Black")
        team_list.append(team2)
    elif team1 in code:
        colors.append("Lime")
        team_list.append(team1)
    else:
        colors.append(("White"))
        team_list.append('Neither')
#Get centre point between start and end times. Used to plot rect
def centre(a,b):
    list = [(float(a[i]) + float(b[i]))/2 for i in range(len(a))]
    return list
#Get the width of each rect by subtracting end time from start time
def get_width(a,b):
    list = [(float(b[i]) - float(a[i]))/1 for i in range(len(a))]
    return list
#Make a list of the total number of each code
counts_list = []
count1=0
position=0
for code in all_codes:
    g = code            #g is the code to check through resr of list for in order to count
    for code1 in all_codes[position:len(all_codes)]: # loop through rest of list for same code
        if code1 == g:                               # if code matches count it
            count1 += 1
            #position += position
    position = position + count1
    counts_list.extend([count1]*count1)
    count1 = 0
#Set up ColumnDataSource to be used in plotting graph
x=all_ends
code=all_counts
left = all_starts
data = {'x':x,'y':code,'left':left,'colors':colors,'all_codes':all_codes,'counts_list':counts_list,'team_list':team_list}
source = ColumnDataSource(data)
#Callbach function used when graph ber is clicked.
callback = CustomJS(args=dict(source=source), code="""
       var data = source.data,
        //gets id of selected point ie. index of point created
        selected = source.selected['1d']['indices'],
        select_inds = [selected[0]];
    if(selected.length == 1){
        // only consider case where one glyph is selected by user
        selected_x = data['x'][selected[0]]
        selected_y = data['y'][selected[0]]
        selected_left = data['left'][selected[0]]
        selected_color = data['colors'][selected[0]]
        selected_code = data['all_codes'][selected[0]]
        selected_team = data['team_list'][selected[0]]
        var team
        if (selected_color=='Lime'){
            team='Ireland'
        }
        else if (selected_color=='Black'){
            team="New Zealand"
        }
        else{
            team="Neither"
        }
        window.alert("Start = "+selected_left+"ms , End = "+selected_x+"ms , Code = " + selected_code+" , Team = "+selected_team)
        //for (var i = 0; i < data['x'].length; ++i){
           // if(data['left'][i] == selected_left){
                // add all points to selected if their ids coincide with original
                // glyph that was clicked.
               // select_inds.push(i)
            //}
       // }
    }
    //source.selected['1d']['indices'] = select_inds 
   // source.change.emit();

    """)
#Display details whwn graph bar is hovered over. Hover Tool.
hover = HoverTool(tooltips="""
        <div bgcolor="#E6E6FA">
            <span style="font-size: 10px; font-weight: bold;">Code = @all_codes</span></br>
            <span style="font-size: 10px; font-weight: bold;">Total number = @counts_list</span></br>
            <span style="font-size: 8px; color: #966;">Start = @left</span></br>
            <span style="font-size: 8px; color: #966;">End = @x</span></br>
        </div>
    """)

taptool = TapTool(callback=callback)
xdr = DataRange1d()
ydr = DataRange1d()

#plot = Plot(
  #  title=None, x_range= Range1d(plot_start-5,plot_end+5), y_range=Range1d(0,len(codes_set)+2), plot_width=900, plot_height=400,
   # h_symmetry=False, v_symmetry=False, min_border=0, toolbar_location="above",background_fill_color="green")
plot = Plot(
    title=None, x_range= xdr, y_range=ydr, plot_width=850, plot_height=300,
    h_symmetry=False, v_symmetry=False, min_border=0, toolbar_location="left",background_fill_color="green")
plot.add_tools(taptool)
plot.add_tools(ResetTool())
plot.add_tools(hover)
plot.add_tools(BoxSelectTool(dimensions="width"))
plot.add_tools(BoxZoomTool())
glyph = HBar(y="y", right="x", left="left", height=0.5, fill_color="colors")
plot.add_glyph(source, glyph)

xaxis = LinearAxis()
plot.add_layout(xaxis, 'below')
yaxis = LinearAxis()
#plot.add_layout(yaxis, 'left')
plot.add_layout(Grid(dimension=0, ticker=xaxis.ticker))
plot.add_layout(Grid(dimension=1, ticker=yaxis.ticker))
plot.xgrid.grid_line_color = None
plot.ygrid.grid_line_color = None
curdoc().add_root(plot)
show(plot)

