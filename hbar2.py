from bokeh.models import ColumnDataSource, DataRange1d, Range1d,Plot, LinearAxis, Grid,SingleIntervalTicker,ResetTool,\
    BoxSelectTool,HoverTool, BoxZoomTool, WheelPanTool,WheelZoomTool, TapTool,PanTool,CustomJS
from bokeh.models.glyphs import Rect, HBar
from bokeh.io import curdoc, output_notebook,show
from bokeh.plotting import figure, curdoc,output_file,show
import pandas as pd
import xml.etree.ElementTree as etree
import pprint

pp = pprint.PrettyPrinter(indent=4)
root = etree.parse('IREvNZL Events.xml')
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
overall_code_count = 39
#TODO get count of codes
all_starts = []
all_ends = []
plot_start = 200000
plot_end = 0

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

for code in all_codes:
    if 'NZL' in code:
        colors.append("Black")
    elif 'IRE' in code:
        colors.append("Lime")
    else:
        colors.append(("White"))

def centre(a,b):
    list = [(float(a[i]) + float(b[i]))/2 for i in range(len(a))]
    return list

#Get the width of each rect by subtracting end time from start time
def get_width(a,b):
    list = [(float(b[i]) - float(a[i]))/1 for i in range(len(a))]
    return list

x=all_ends
code=all_counts
left = all_starts
data = {'x':x,'y':code,'left':left,'colors':colors}
print(data['y'])
source = ColumnDataSource(data)

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
        var country
        if (selected_color=='Lime'){
            country='Ireland'
        }
        else if (selected_color=='Black'){
            country="New Zealand"
        }
        else{
            country="Neither"
        }
        window.alert("Start = "+selected_left+"ms , End = "+selected_x+"ms , Code = " + selected_y+" , Country = "+country)
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

hover = HoverTool(tooltips="""
        <div bgcolor="#E6E6FA">
            <span style="font-size: 10px; font-weight: bold;">Code = @y</span></br>
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
    title=None, x_range= xdr, y_range=ydr, plot_width=900, plot_height=400,
    h_symmetry=False, v_symmetry=False, min_border=0, toolbar_location="above",background_fill_color="green")
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
plot.add_layout(yaxis, 'left')

plot.add_layout(Grid(dimension=0, ticker=xaxis.ticker))
plot.add_layout(Grid(dimension=1, ticker=yaxis.ticker))
plot.xgrid.grid_line_color = None
plot.ygrid.grid_line_color = None
curdoc().add_root(plot)

show(plot)

