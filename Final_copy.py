from bokeh.models import Text, ColumnDataSource, DataRange1d, Range1d, Plot, LinearAxis, Grid, SingleIntervalTicker, \
    ResetTool, BoxSelectTool, CrosshairTool, HoverTool, BoxZoomTool, WheelPanTool, WheelZoomTool, TapTool, PanTool, \
    CustomJS, ZoomInTool, ZoomOutTool, Button, Div, Tabs, WheelPanTool, WheelZoomTool, BoxAnnotation
from bokeh.models.glyphs import Rect, HBar
from bokeh.plotting import figure, curdoc, output_file, show
from bokeh.layouts import gridplot, column, row
from bokeh import events
import xml.etree.ElementTree as etree

Video_file = 'FRAvJAP.mp4'
file = 'IREvNZL Events.xml'
team1 = file[0:3]
team2 = file[4:7]
title = file[0:7]
tree = etree.ElementTree(file=file)
root = tree.getroot()
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
temp_pos = 0
team_color = ['Lime', 'Black']
all_list = []
label_list = []
list_of_all_labels = []
for child in root:
    if child.tag == 'ALL_INSTANCES':
        for child2 in child:  # instance
            for child3 in child2:  # ID,start,end, code, label
                if child3.tag == 'ID':
                    key = child3.text
                elif child3.tag == 'start':
                    all_list.append(child3.text)
                elif child3.tag == 'end':
                    all_list.append(child3.text)
                elif child3.tag == 'code':
                    all_list.append(child3.text)
                elif child3.tag == 'label':
                    for child4 in child3:  # group,text
                        label_list.append(child4.text)
            list_of_all_labels.append(label_list)
            label_list = []

"""Make a list of the total number of each code"""


def create_list_of_codes(all_codes, position, count1):
    for code in all_codes:
        check_code = code  # g is the code to check through rest of list for in order to count
        for code1 in all_codes[position:len(all_codes)]:  # loop through rest of list for same code
            if code1 == check_code:  # if code matches count it
                count1 += 1
        position = position + count1
        counts_list.extend([count1] * count1)
        count1 = 0


"""Function to convert seconds to h:m:s"""


def convertTime(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "%d:%02d:%02d" % (h, m, s)


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


"""Get the count of how many distinctive codes there are"""
for i in rootInstance.iterfind('instance'):
    if i.findtext('code') not in codes_set:
        codes_set.add(i.findtext('code'))  # First time to see code
        overall_code_count += 1
codes_set = set()
count_used_for_title_height = overall_code_count

"""Extract all relevant data from xml file"""
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

"""Reorder the data lists to enable events to be ordered according to teams"""
pos = 0
for team in all_codes:
    if team1 in team:
        home_team.append(team)
        home_start.append(all_starts[pos])
        home_end.append(all_ends[pos])
    elif team2 in team:
        away_team.append(team)
        away_start.append(all_starts[pos])
        away_end.append(all_ends[pos])
    else:
        neither_team.append(team)
        neither_start.append(all_starts[pos])
        neither_end.append(all_ends[pos])
    pos += 1
total_codes = []
total_codes.extend(home_team)
total_codes.extend(away_team)
total_codes.extend(neither_team)
total_starts = []
total_starts.extend(home_start)
total_starts.extend(away_start)
total_starts.extend(neither_start)
total_ends = []
total_ends.extend(home_end)
total_ends.extend(away_end)
total_ends.extend(neither_end)

exclusive_codes_list = []
for code in total_codes:
    if code not in exclusive_codes_list:
        exclusive_codes_list.append(code)

total_codes = []
total_codes.extend(home_team)
total_codes.extend(away_team)
total_codes.extend(neither_team)
total_starts = []
total_starts.extend(home_start)
total_starts.extend(away_start)
total_starts.extend(neither_start)
total_ends = []
total_ends.extend(home_end)
total_ends.extend(away_end)
total_ends.extend(neither_end)

exclusive_codes_list = []
count_each_code = 0

temp_list1 = []
for code in total_codes:
    if code not in exclusive_codes_list:
        exclusive_codes_list.append(code)
list_index_of_each_code = []
code_number = len(exclusive_codes_list)
for code in exclusive_codes_list:
    for code1 in total_codes:
        if code1 == code:
            count_each_code += 1
            list_index_of_each_code.append(count_each_code)

    temp_list1.extend([code_number] * count_each_code)
    count_each_code = 0
    code_number -= 1
colors.extend(["white"] * len(total_codes))

pos_count = 0
for code in total_codes:
    if team1 in code:
        pos_count += 1
top_lower = int(temp_list1[pos_count])

pos_count = 0
for code in total_codes:
    if team2 in code or team1 in code:
        pos_count += 1
bottom_higher = int(temp_list1[pos_count])
print("pos_count", pos_count)
print("BottomHigher", bottom_higher)

# Make a list of the total number of each code
create_list_of_codes(total_codes, position, count1)
print("left: ", total_starts)
print("x: ", total_ends)
print("y: ", temp_list1)

print("all_codes: ", total_codes)
print("x: ", counts_list)

"""Convert start and end times from seconds to h:m:s"""
converted_start_times = []
converted_end_times = []
time_length = []
converted_time_length = []
for diff in range(0, len(total_ends)):
    time_length.append(int(total_ends[diff]) - int(total_starts[diff]))
for t in total_starts:
    converted_start_times.append(convertTime(t))
for t in total_ends:
    converted_end_times.append(convertTime(t))
for t in time_length:
    converted_time_length.append(convertTime(t))

data = {'x': total_ends, 'y': temp_list1, 'left': total_starts, 'colors': colors, 'all_codes': total_codes,
        'counts_list': counts_list, 'list_index_of_each_code': list_index_of_each_code,
        'list_of_all_labels': list_of_all_labels, 'converted_start_times': converted_start_times,
        'converted_end_times': converted_end_times, 'converted_time_length': converted_time_length}
source = ColumnDataSource(data)

"""Create a html Div to contain the video"""
div = Div(text="""<video id="myVideo" width="540" height="310" controls>
            <source id="mySrc" src="IREvNZL.mp4" type="video/mp4">Your browser does not support HTML5 video.
            </video>""", width=840, height=310)
"""Create a html Div to contain details of the event on screen as video plays"""
div1 = Div(width=121)
hoverDiv = Div(height=10, width=650, text="THE TOOL TIPS WILL BE DISPLAYED HERE")

"""The event that will be called to play the video on hbar click"""
""" Function to build a suitable CustomJS to display the current event in the div model."""


def display_event(div, attributes=[]):
    style = 'float:left;clear:left;font_size=32.5pt'
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
            selected_list_index_of_each_code = data['list_index_of_each_code'][selected[0]]
            selected_counts_list = data['counts_list'][selected[0]]
            selected_converted_start_times = data['converted_start_times'][selected[0]]
            selected_converted_end_times = data['converted_end_times'][selected[0]]
            if(data['list_of_all_labels'][selected[0]]=="")
                selected_list_of_all_labels = "NO LABELS";
            else
                selected_list_of_all_labels = data['list_of_all_labels'][selected[0]];
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
            selected_left_hours = selected_left/(60);

            var date = new Date(null);
            date.setSeconds(selected_left); // specify value for SECONDS here
            start = date.toISOString().substr(11, 8);
            var date = new Date(null);
            date.setSeconds(selected_x); // specify value for SECONDS here
            end = date.toISOString().substr(11, 8); 
            var date = new Date(null);
            date.setSeconds(selected_x); // specify value for SECONDS here
            end = date.toISOString().substr(11, 8);

           lines = "Start = "+start+"   ";
           lines = lines + "End = "+end+"   ";
           lines = lines + selected_code + "\\n\\n";
           lines = lines + "Event No."+selected_list_index_of_each_code+" of "+ selected_counts_list+"  "
           lines = lines + " Labels: "  + "\\n" + selected_list_of_all_labels;

           div1.text = lines;

        }
        var attrs = %s;
        var args = [];
        for (var i=0; i<attrs.length; i++ ) {
            val = JSON.stringify(cb_obj[attrs[i]], function(key, val) {
                return val.toFixed ? Number(val.toFixed(2)) : val;
            })
            args.push(attrs[i] + '=' + val)
        }
        var line = "<span style=%r><b>" + cb_obj.event_name + "</b>(" + args.join(", ") + ")</span>\\n";
        var text = div1.text.concat(line);

        var lines = text.split("\\n")
        if ( lines.length > 35 ) { lines.shift(); }
        //Get start & end times of video from left & right values of hbar (4266)
        var startInt = parseInt(selected_left);
        var start = ((parseInt(selected_left))).toString();
        var duration = (parseInt(selected_x)-parseInt(selected_left));
        var end = ((parseInt(selected_x))).toString();
        //var srce = document.getElementById("mySrc");
        //srce.src="IREvNZL.mp4#t="+start+","+end;
        var vid = document.getElementById("myVideo");
        //vid.load();
        vid.currentTime = start;
        vid.play();
        vid.addEventListener("timeupdate", function() {
            if (vid.currentTime >= end) {
                vid.pause();
                start = 0;
                end = 90000;
            }
        }, false);
    """ % (attributes, style))


hover = HoverTool(tooltips="""
        <style>.zoom:hover{transform:scale(1.5);}</style>
        <div bgcolor="#E6E6FA" class = "zoom">
            <span style="font-size: 10px; font-weight: bold;">Code = @all_codes</span></br>
            <span style="font-size: 10px; font-weight: bold;">Total number = @list_index_of_each_code/@counts_list</span></br>
            <span style="font-size: 8px; color: #966;">Start = @converted_start_times</span></br>
            <span style="font-size: 8px; color: #966;">End = @converted_end_times</span></br>
            <span style="font-size: 8px; color: #966;">Duration: = @converted_time_length</span></br>
            

        </div>
    """)

xdr = DataRange1d()
ydr = DataRange1d()
plot_height = 550
plot = Plot(
    title=None, x_range=xdr, y_range=ydr, plot_width=1100
    , plot_height=plot_height - 200,
    h_symmetry=False, v_symmetry=False, min_border=0,
    toolbar_location="right", background_fill_color="green")

low_box = BoxAnnotation(top=bottom_higher, fill_alpha=0.3, fill_color='Green')
mid_box = BoxAnnotation(bottom=bottom_higher, top=top_lower, fill_alpha=0.5, fill_color='#00CC00')
high_box = BoxAnnotation(bottom=top_lower, fill_alpha=0.4, fill_color='Lime')

plot.add_layout(low_box)
plot.add_layout(mid_box)
plot.add_layout(high_box)
taptool = TapTool(callback=display_event(div))
plot.add_tools(taptool)
plot.add_tools(ResetTool())
plot.add_tools(hover)
plot.add_tools(WheelPanTool())
plot.add_tools(BoxZoomTool())
plot.add_tools(CrosshairTool())
plot.add_tools(ZoomOutTool())
plot.add_tools(ZoomInTool())
plot.add_tools(WheelZoomTool())
glyph = HBar(y="y", right="x", left="left", height=0.5, fill_color="colors")
plot.add_glyph(source, glyph)

xaxis = LinearAxis()
yaxis = LinearAxis()
plot.add_layout(Grid(dimension=0, ticker=xaxis.ticker))
plot.add_layout(Grid(dimension=1, ticker=yaxis.ticker))

yaxis_offset = 0.5
code_index = len(codes_list) - 1
for code in exclusive_codes_list:
    text = Text(x=-470, y=yaxis_offset, text=[exclusive_codes_list[code_index][0:30]], text_font_size="5pt",
                text_font_style="normal",
                text_color="White", text_baseline="alphabetic")
    plot.add_glyph(text)
    yaxis_offset += 1.01
    code_index -= 1
home_title = Text(x=-470, y=count_used_for_title_height + 2, text=[team1], text_font_size="8pt", text_font_style="bold",
                  text_alpha=1.0, text_font='helvetica', text_color=team_color[0], text_baseline="alphabetic")
versus = Text(x=-330, y=count_used_for_title_height + 2, text=['v'], text_font_size="8pt", text_font_style="bold",
              text_alpha=1.0, text_font='helvetica', text_color='White', text_baseline="alphabetic")
away_title = Text(x=-280, y=count_used_for_title_height + 2, text=[team2], text_font_size="8pt", text_font_style="bold",
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

layout = column(row(div, div1), plot)
show(layout)
