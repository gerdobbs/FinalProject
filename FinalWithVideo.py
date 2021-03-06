from bokeh.models import Text, ColumnDataSource, DataRange1d, Range1d, Plot, LinearAxis, Grid, SingleIntervalTicker, \
    ResetTool, BoxSelectTool, CrosshairTool, HoverTool, BoxZoomTool, WheelPanTool, WheelZoomTool, TapTool, PanTool, \
    CustomJS, ZoomInTool, ZoomOutTool, Button, Div, Tabs, WheelPanTool,WheelZoomTool
from bokeh.models.glyphs import Rect, HBar
from bokeh.io import curdoc, output_notebook, show
from bokeh.plotting import figure, curdoc, output_file, show
from bokeh.layouts import gridplot, column, row
from bokeh import events
import xml.etree.ElementTree as etree
import cv2

Video_file = 'IrevCan.mp4'
file = 'IREvNZL Events.xml'
team1 = file[0:3]
team2 = file[4:7]
title = file[0:7]
# pp = pprint.PrettyPrinter(indent=4)
root = etree.parse(file)
doc = root.getroot()
rootInstance = root.find('ALL_INSTANCES')
codes_set = set()
codes_list = []
codes_count = []
start = []
end = []
all_info = {}
count = 0  # Used to store how mant times each code appears
code_list = []
entire_codes = []
temp_dict = {}
each_code = []  # Will include a list of each code x number of times it appears
all_codes = []
all_counts = []  # Will include the number assigned to the code x how many times that code appears
colors = []
overall_code_count = 0
all_starts = []
all_ends = []
plot_start = 200000
plot_end = 0
team_list = []
team_color = ['Lime', 'Black']
counts_list = []
count1 = 0
position = 0
home_team = []
home_start = []
home_end = []
home_code_count = []
home_exclusive = []
away_team = []
away_start = []
away_end = []
away_code_count = []
away_exclusive = []
neither_team = []
neither_start = []
neither_end = []
neither_code_count = []
neither_exclusive = []
new_all_code_list = []
temp_list = []
temp_pos =0


# Get centre point between start and end times. Used to plot rect
def centre(a, b):
    list = [(float(a[i]) + float(b[i])) / 2 for i in range(len(a))]
    return list


# Get the width of each rect by subtracting end time from start time
def get_width(a, b):
    list = [(float(b[i]) - float(a[i])) / 1 for i in range(len(a))]
    return list


# Creare a list for the team associated with each event and a colour for that team
def assign_team_colors(t1, t2):
    for code in all_codes:
        if t2 in code:
            colors.append("Black")
            team_list.append(team2)
        elif t1 in code:
            colors.append("Lime")
            team_list.append(team1)
        else:
            colors.append(("White"))
            team_list.append('Neither')


# Make a list of the total number of each code
def create_list_of_codes(all_codes, position, count1):
    for code in all_codes:
        check_code = code  # g is the code to check through resr of list for in order to count
        for code1 in all_codes[position:len(all_codes)]:  # loop through rest of list for same code
            if code1 == check_code:  # if code matches count it
                count1 += 1
        position = position + count1
        counts_list.extend([count1] * count1)
        count1 = 0


# Get the count of how many distinctive codes there are
for i in rootInstance.iterfind('instance'):
    if i.findtext('code') not in codes_set:
        codes_set.add(i.findtext('code'))  # First time to see code
        overall_code_count += 1
codes_set = set()
# Extract all relevant data from xml file
for i in rootInstance.iterfind('instance'):
    if i.findtext('code') not in codes_set:  # First time to see code
        codes_set.add(i.findtext('code'))
        temp_dict['code'] = i.findtext('code')  # Add new code to dictionary
        codes_list.append(i.findtext('code'))
        for j in rootInstance.iterfind('instance'):  # Loop through codes again
            if i.findtext('code') == j.findtext('code'):  # Code == one in outer loop
                count += 1
                start.append(round(float(j.findtext('start'))))  # Add start time to list of starts for that code
                if float(j.findtext('start')) < plot_start:
                    plot_start = float(j.findtext('start'))
                end.append(round(float(j.findtext('end'))))
                if float(j.findtext('end')) > plot_end:
                    plot_end = float(j.findtext('end'))
            each_code = [i.findtext('code')] * count  # Make list of the code x number of times it appears
        all_codes.extend(each_code)  # Add the list of each code to list of all codes
        temp_dict['count'] = count
        codes_count.append(count)
        temp_dict['start'] = start  # Add list of start times as value to start key in dict
        temp_dict['end'] = end
        code_list.append(temp_dict.copy())  # Add full dict to list
        temp_dict.clear()  # Clear for next iteration
        all_starts.extend(start)
        all_ends.extend((end))
        start = []
        end = []
        all_counts.extend([overall_code_count] * count)
        count = 0
        overall_code_count -= 1

pos=0
for team in all_codes:
    if team1 in team:
        home_team.append(team)
        home_start.append(all_starts[pos])
        home_end.append(all_ends[pos])
        #home_code_count.append(all_counts[pos])
    elif team2 in team:
        away_team.append(team)
        away_start.append(all_starts[pos])
        away_end.append(all_ends[pos])
        #away_code_count.append(all_counts[pos])
    else:
        neither_team.append(team)
        neither_start.append(all_starts[pos])
        neither_end.append(all_ends[pos])
       # neither_code_count.append(all_counts[pos])

    pos +=1

total_codes= []
total_codes.extend(home_team)
total_codes.extend(away_team)
total_codes.extend(neither_team)
print("TotalCodes",len(total_codes),total_codes)
total_starts = []
total_starts.extend(home_start)
total_starts.extend(away_start)
total_starts.extend(neither_start)
print("Starts",len(total_starts),total_starts)
total_ends = []
total_ends.extend(home_end)
total_ends.extend(away_end)
total_ends.extend(neither_end)
print("Ends",len(total_ends),total_ends)
exclusive_codes_list = []
for code in total_codes:
    if code not in exclusive_codes_list:
        exclusive_codes_list.append(code)
print("ExclusiveCodes",len(exclusive_codes_list),exclusive_codes_list)

total_codes= []
total_codes.extend(home_team)
total_codes.extend(away_team)
total_codes.extend(neither_team)
print("TotalCodes",len(total_codes),total_codes)
total_starts = []
total_starts.extend(home_start)
total_starts.extend(away_start)
total_starts.extend(neither_start)
print("Starts",len(total_starts),total_starts)
total_ends = []
total_ends.extend(home_end)
total_ends.extend(away_end)
total_ends.extend(neither_end)
print("Ends",len(total_ends),total_ends)

exclusive_codes_list = []
count_each_code = 0

temp_list1=[]
for code in total_codes:
    if code not in exclusive_codes_list:
        exclusive_codes_list.append(code)

print("ExclusiveCodes",len(exclusive_codes_list),exclusive_codes_list)
code_number = len(exclusive_codes_list)
for code in exclusive_codes_list:
    for code1 in total_codes:
        if code1 == code:
            count_each_code+=1

    temp_list1.extend([code_number] * count_each_code)
    count_each_code = 0
    code_number -= 1
print("TempList",len(temp_list1),temp_list1)

assign_team_colors(team1, team2)
# Make a list of the total number of each code
create_list_of_codes(all_codes, position, count1)
# Set up ColumnDataSource to be used in plotting graph
data = {'x': all_ends, 'y': all_counts, 'left': all_starts, 'colors': colors, 'all_codes': all_codes,
        'counts_list': counts_list,
        'team_list': team_list}
source = ColumnDataSource(data)
# Create a html Div to contain the video
div = Div(text="""<video id="myVideo" width="540" height="310" controls>
  <source id="mySrc" src="IREvNZL.mp4" type="video/mp4">Your browser does not support HTML5 video.
</video>""", width=840, height=310)
div1 = Div(width=800)


# The event that will be called to play the video on hbar click
def display_event(div, attributes=[]):
    """
    Function to build a suitable CustomJS to display the current event
    in the div model.
    """
    style = 'float:left;clear:left;font_size=0.5pt'
    return CustomJS(args=dict(div=div, div1=div1, source=source), code="""

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

       lines = "Start = "+selected_left+"ms ,";
       
       //div1.text = lines;
        //div1.text = "Start = "+selected_left+"ms ," +"/n"+ "End = "+selected_x+"ms , Code = " + selected_code+" , Team = "+selected_team
        //window.alert("Start = "+selected_left+"ms , End = "+selected_x+"ms , Code = " + selected_code+" , Team = "+selected_team)
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
   /////////////////////////////////////////////////////////////////////////////////////////////
        var attrs = %s;
        var args = [];
        for (var i=0; i<attrs.length; i++ ) {
            val = JSON.stringify(cb_obj[attrs[i]], function(key, val) {
                return val.toFixed ? Number(val.toFixed(2)) : val;
            })
            args.push(attrs[i] + '=' + val)
        }
        var line = "<span style=%r><b>" + cb_obj.event_name + "</b>(" + args.join(", ") + ")</span>\\n";
        var text = div.text.concat(line);
        var lines = text.split("\\n")
        if ( lines.length > 35 ) { lines.shift(); }
        //Get start & end times of video from left & right values of hbar (4266)
        var start = ((parseInt(selected_left))).toString();
        // duration = 10;
        var duration = (parseInt(selected_x)-parseInt(selected_left));
        //var end = ((parseInt(selected_left))+ duration).toString();
        var end = ((parseInt(selected_x))).toString();
        
        //div1.text = selected_left;
        var srce = document.getElementById("mySrc");
        srce.src="IREvNZL.mp4#t="+start+","+end;
        //srce.currentTime = 50;
        var vid = document.getElementById("myVideo");
        vid.load();
        vid.play();



    """ % (attributes, style))


# Display details whwn graph bar is hovered over. Hover Tool.
hover = HoverTool(tooltips="""
        <div bgcolor="#E6E6FA">
            <span style="font-size: 10px; font-weight: bold;">Code = @all_codes</span></br>
            <span style="font-size: 10px; font-weight: bold;">Total number = @counts_list</span></br>
            <span style="font-size: 8px; color: #966;">Start = @left</span></br>
            <span style="font-size: 8px; color: #966;">End = @x</span></br>
        </div>
    """)

taptool = TapTool(callback=display_event(div))
xdr = DataRange1d()
ydr = DataRange1d()
# plot = Plot(
#  title=None, x_range= Range1d(plot_start-5,plot_end+5), y_range=Range1d(0,len(codes_set)+2), plot_width=900, plot_height=400,
# h_symmetry=False, v_symmetry=False, min_border=0, toolbar_location="above",background_fill_color="green")
plot_height = 550
plot = Plot(
    title=None, x_range=xdr, y_range=ydr, plot_width=650
    , plot_height=plot_height,
    h_symmetry=False, v_symmetry=False, min_border=0, toolbar_location="above", background_fill_color="green")

plot.add_tools(taptool)
plot.add_tools(ResetTool())
plot.add_tools(hover)
# plot.add_tools(BoxSelectTool(dimensions="width"))
plot.add_tools(WheelPanTool())
plot.add_tools(BoxZoomTool())
plot.add_tools(CrosshairTool())
plot.add_tools(ZoomOutTool())
plot.add_tools(ZoomInTool())
plot.add_tools(WheelZoomTool())
glyph = HBar(y="y", right="x", left="left", height=0.5, fill_color="colors")
plot.add_glyph(source, glyph)

xaxis = LinearAxis()
plot.add_layout(xaxis, 'below')
yaxis = LinearAxis()
plot.add_layout(Grid(dimension=0, ticker=xaxis.ticker))
plot.add_layout(Grid(dimension=1, ticker=yaxis.ticker))

yaxis_offset = 0.5
code_index = len(codes_list) - 1
for code in codes_list:
    text = Text(x=-150, y=yaxis_offset, text=[codes_list[code_index][0:30]], text_font_size="6pt",
                text_font_style="normal",
                text_color="Black", text_baseline="alphabetic")
    plot.add_glyph(text)
    yaxis_offset += 1
    code_index -= 1
home_title = Text(x=-150, y=40, text=[team1], text_font_size="8pt", text_font_style="bold",
                  text_alpha=1.0, text_font='helvetica', text_color=team_color[0], text_baseline="alphabetic")
versus = Text(x=0, y=40, text=['v'], text_font_size="8pt", text_font_style="bold",
              text_alpha=1.0, text_font='helvetica', text_color='White', text_baseline="alphabetic")
away_title = Text(x=70, y=40, text=[team2], text_font_size="8pt", text_font_style="bold",
                  text_alpha=1.0, text_font='helvetica', text_color=team_color[1], text_baseline="alphabetic")
plot.add_glyph(home_title)
plot.add_glyph(versus)
plot.add_glyph(away_title)
plot.ygrid.grid_line_color = "navy"
plot.ygrid.minor_grid_line_color = 'navy'
plot.ygrid.minor_grid_line_alpha = 0.1
plot.ygrid.grid_line_alpha = 0.1
plot.xgrid.grid_line_color = None
plot.axis.major_tick_out = 3
plot.axis.minor_tick_in = -3
plot.axis.minor_tick_out = 2



plot.ygrid.band_fill_alpha = 0.1
plot.ygrid.band_fill_color = "navy"
button = Button(label="Button", button_type="success")

layout = row(plot, column(div, div1))
button.js_on_event(events.ButtonClick, display_event(div))
show(layout)