# Visbox charting function documentation

### Common Function Parameters
1. svgSelector
- Type: string
- Description: A CSS style sector for the already existing SVG element on the page. 
- Example: If you have an SVG with the ID "bar_chart" a valid svgSelector would be "#bar_chart"

2. config
- Type: Object
- Description: An object containing configuration options for the charts
- Example: 
```json
{"y_label": "US $ billions (constant 2015 prices)", "y_axis_ticks": 5, "y_maximum": "auto", "x_text_rotation": 0, "padding_right": 60, "labels_on_chart": true, "y_maximum_value": null, "title": "Donor FPRH billions", "x_label": " ", "padding_bottom": 30, "label_font_size": 10, "unit_divisor": 1000000000, "group_by": "Purpose", "filter_by": "Donor", "padding_left": 55, "template": 1, "save_as_template": true, "x_indicator": "Year", "sort": "xasc", "legend_position": "cr", "inject_css": null, "height": 300, "filter_selection": "United States", "colour": "#e84439,#f8c1b2,#f0826d,#bc2629,#8f1b13", "label_format": ",.1f", "padding_top": 20, "y_indicator": "Value", "width": 500}
```

3. csvDat
- Type: Array of objects
- Description: Data to drive the chart, formatted as if you were to read a csv using the d3.csv function
- Example: 
```json
[{"Country":"USA","Value":100},{"Country":"Uganda","Value":200}]
```

### Underlying model

Underneath these functions is a single Django model that holds all of the configuration options for each chart. This model contains information about the data types of each configuration option, as well as any defaults. Not all options are used on all of the charts, and some options are just for the internal operation of Visbox itself ('title', 'dataset', 'creator', 'created', and 'save_as_template'). Please see below for the full model, and even further below for which charts use which options specifically.
```python
title = models.CharField(null=True,blank=True,max_length=255)
chart_type = models.CharField(max_length=255)
dataset = models.ForeignKey(Dataset)
creator = models.ForeignKey(User, editable=False)
created = models.DateTimeField(auto_now_add=True)
width = models.IntegerField(default=960)
height = models.IntegerField(default=500)
padding_top = models.IntegerField(default=20)
padding_right = models.IntegerField(default=100)
padding_bottom = models.IntegerField(default=100)
padding_left = models.IntegerField(default=100)
x_indicator = models.CharField(null=True,blank=True,max_length=255)
y_indicator = models.CharField(null=True,blank=True,max_length=255)
z_indicator = models.CharField(null=True,blank=True,max_length=255)
c_indicator = models.CharField(null=True,blank=True,max_length=255)
group_by = models.CharField(null=True,blank=True,max_length=255)
sort = models.CharField(null=True,blank=True,max_length=255)
y_maximum = models.CharField(null=True,blank=True,max_length=255,default="auto")
y_maximum_value = models.DecimalField(null=True,blank=True,max_digits=99,decimal_places=5)
x_maximum = models.CharField(null=True,blank=True,max_length=255,default="auto")
x_maximum_value = models.DecimalField(null=True,blank=True,max_digits=99,decimal_places=5)
colour = models.CharField(null=True,blank=True,max_length=255,default="#e84439")
x_label = models.CharField(null=True,blank=True,max_length=255)
y_label = models.CharField(null=True,blank=True,max_length=255)
y_axis_ticks = models.IntegerField(null=True,blank=True)
x_text_rotation = models.IntegerField(default=45)
save_as_template = models.BooleanField(default=False)
labels_on_chart = models.BooleanField(default=False)
label_font_size = models.IntegerField(default=10)
label_format = models.CharField(default=",.2f",max_length=255)
unit_divisor = models.IntegerField(default=1)
filter_by = models.CharField(default="None",max_length=255)
filter_selection = models.CharField(null=True,blank=True,max_length=255)
legend_position = models.CharField(default='tr',max_length=2)
bubble_minimum = models.IntegerField(default=0)
bubble_maximum = models.IntegerField(default=20)
inject_css = models.TextField(null=True,blank=True)
```

### Chart types

#### 1. (Stacked) area chart
- Location: area.js
- Function: vb_area(svgSelector,config,csvDat)
- Accepted configuration parameters:
    - 'title', 'dataset', 'width', 'height', 'padding_top', 'padding_right', 'padding_bottom', 'padding_left', 'x_indicator', 'y_indicator', 'group_by', 'sort', 'y_maximum', 'y_maximum_value', 'unit_divisor', 'filter_by', 'filter_selection', 'colour', 'x_label', 'y_label', 'y_axis_ticks', 'x_text_rotation', 'labels_on_chart', 'label_font_size', 'label_format', 'legend_position', 'inject_css', 'save_as_template'
- Parameter choices ('value', ' label'):
    - sort = [('yasc', ' Y ascending'),('ydes', ' Y descending'),('xasc', ' X ascending'),('xdes', ' X descending')]
    - y_maximum = [('auto', ' Automatic'),('manual', ' Manual (define below)')]
    - legend_position = [('tr', ' Top right'),('tl', ' Top left'),('cr', ' Center right')]
- Considerations: At the moment, the area chart needs some indicator to "group by" even if you're only visualizing a single area. This can be solved by appending a column of 1s to any dataset. At the moment, the chart is hardcoded to have a linear scale. "colour" parameter can accept multiple values via comma separation.

#### 2. Bar chart
- Location: bar.js
- Function: vb_bar(svgSelector,config,csvDat)
- Accepted configuration parameters:
    - 'title', 'dataset', 'width', 'height', 'padding_top', 'padding_right', 'padding_bottom', 'padding_left', 'x_indicator', 'y_indicator', 'sort', 'x_maximum', 'x_maximum_value', 'filter_by', 'filter_selection', 'colour', 'x_label', 'y_label', 'x_text_rotation', 'labels_on_chart', 'label_font_size', 'label_format', 'inject_css', 'save_as_template'
- Parameter choices ('value', ' label'):
    - sort = [('yasc', ' Y ascending'),('ydes', ' Y descending'),('xasc', ' X ascending'),('xdes', ' X descending')]
    - x_maximum = [('auto', ' Automatic'),('manual', ' Manual (define below)')]
- Considerations: At the moment, the chart is hardcoded to have a linear scale.

#### 3. Bubble chart
- Location: bubble.js
- Function: vb_bubble(svgSelector,config,csvDat)
- Accepted configuration parameters:
    - 'title', 'dataset', 'width', 'height', 'padding_top', 'padding_right', 'padding_bottom', 'padding_left', 'x_indicator', 'y_indicator', 'z_indicator', 'c_indicator', 'sort', 'y_maximum', 'y_maximum_value', 'bubble_minimum', 'bubble_maximum', 'unit_divisor', 'filter_by', 'filter_selection', 'colour', 'x_label', 'y_label', 'y_axis_ticks', 'x_text_rotation', 'labels_on_chart', 'label_font_size', 'label_format', 'legend_position', 'inject_css', 'save_as_template'
- Parameter choices ('value', ' label'):
    - sort = [('yasc', ' Y ascending'),('ydes', ' Y descending'),('xasc', ' X ascending'),('xdes', ' X descending')]
    - y_maximum = [('auto', ' Automatic'),('manual', ' Manual (define below)')]
    - legend_position = [('tr', ' Top right'),('tl', ' Top left'),('cr', ' Center right')]
- Considerations: At the moment, the chart is hardcoded to have a linear scale. "colour" parameter can accept multiple values via comma separation.

#### 4. Column chart
- Location: column.js
- Function: vb_column(svgSelector,config,csvDat)
- Accepted configuration parameters:
    - 'title', 'dataset', 'width', 'height', 'padding_top', 'padding_right', 'padding_bottom', 'padding_left', 'x_indicator', 'y_indicator', 'sort', 'y_maximum', 'y_maximum_value', 'filter_by', 'filter_selection', 'colour', 'x_label', 'y_label', 'y_axis_ticks', 'x_text_rotation', 'labels_on_chart', 'label_font_size', 'label_format', 'inject_css', 'save_as_template'
- Parameter choices ('value', ' label'):
    - sort = [('yasc', ' Y ascending'),('ydes', ' Y descending'),('xasc', ' X ascending'),('xdes', ' X descending')]
    - y_maximum = [('auto', ' Automatic'),('manual', ' Manual (define below)')]
- Considerations:  At the moment, the chart is hardcoded to have a linear scale.

#### 5. Donut chart
- Location: donut.js
- Function: vb_donut(svgSelector,config,csvDat)
- Accepted configuration parameters:
    - 'title', 'dataset', 'width', 'height', 'padding_top', 'padding_right', 'padding_bottom', 'padding_left', 'x_indicator', 'y_indicator', 'sort', 'filter_by', 'filter_selection', 'colour', 'label_font_size', 'label_format', 'inject_css', 'save_as_template'
- Parameter choices ('value', ' label'):
    - sort = [('native', ' Native ordering'),('avoid', ' Avoid text collisions'),('yasc', ' Y ascending'),('ydes', ' Y descending'),('xasc', ' X ascending'),('xdes', ' X descending')]
- Considerations: Given slice angles, it's common for text labels to overlap. I prefer pie charts because the labels will pop into the slice when they fit, but Comms prefers donuts. Choose "avoid" for sort to try and avoid text collisions to the best of my ability. "colour" parameter can accept multiple values via comma separation.

#### 6. Grouped column chart
- Location: grouped_column.js
- Function: vb_grouped_column(svgSelector,config,csvDat)
- Accepted configuration parameters:
    - 'title', 'dataset', 'width', 'height', 'padding_top', 'padding_right', 'padding_bottom', 'padding_left', 'x_indicator', 'y_indicator', 'group_by', 'sort', 'y_maximum', 'y_maximum_value', 'unit_divisor', 'filter_by', 'filter_selection', 'colour', 'x_label', 'y_label', 'y_axis_ticks', 'x_text_rotation', 'labels_on_chart', 'label_font_size', 'label_format', 'legend_position', 'inject_css', 'save_as_template'
- Parameter choices ('value', ' label'):
    - sort = [('yasc', ' Y ascending'),('ydes', ' Y descending'),('xasc', ' X ascending'),('xdes', ' X descending')]
    - y_maximum = [('auto', ' Automatic'),('manual', ' Manual (define below)')]
    - legend_position = [('tr', ' Top right'),('tl', ' Top left'),('cr', ' Center right')]
- Considerations: Must be used with "group_by." If you don't have anything to group by, just use vb_column. At the moment, the chart is hardcoded to have a linear scale. "colour" parameter can accept multiple values via comma separation.

#### 7. Line chart
- Location: line.js
- Function: vb_line(svgSelector,config,csvDat)
- Accepted configuration parameters:
    - 'title', 'dataset', 'width', 'height', 'padding_top', 'padding_right', 'padding_bottom', 'padding_left', 'x_indicator', 'y_indicator', 'sort', 'y_maximum', 'y_maximum_value', 'filter_by', 'filter_selection', 'colour', 'x_label', 'y_label', 'y_axis_ticks', 'x_text_rotation', 'labels_on_chart', 'label_font_size', 'label_format', 'inject_css', 'save_as_template'
- Parameter choices ('value', ' label'):
    - sort = [('yasc', ' Y ascending'),('ydes', ' Y descending'),('xasc', ' X ascending'),('xdes', ' X descending')]
    - y_maximum = [('auto', ' Automatic'),('manual', ' Manual (define below)')]
- Considerations: Just draws one line in a linear scale. Expect a multi-line chart in the future as needed.

#### 8. Pie chart
- Location: pie.js
- Function: vb_pie(svgSelector,config,csvDat)
- Accepted configuration parameters:
    - 'title', 'dataset', 'width', 'height', 'padding_top', 'padding_right', 'padding_bottom', 'padding_left', 'x_indicator', 'y_indicator', 'sort', 'filter_by', 'filter_selection', 'colour', 'label_font_size', 'label_format', 'inject_css', 'save_as_template'
- Parameter choices ('value', ' label'):
    - sort = [('native', ' Native ordering'),('avoid', ' Avoid text collisions'),('yasc', ' Y ascending'),('ydes', ' Y descending'),('xasc', ' X ascending'),('xdes', ' X descending')]
- Considerations: As with donut chart, "avoid" is the best sorting algorithm. When labels are small enough, they'll pop into the slice. "colour" parameter can accept multiple values via comma separation.

#### 9. Stacked column chart
- Location: stacked_column.js
- Function: vb_stacked_column(svgSelector,config,csvDat)
- Accepted configuration parameters:
    - 'title', 'dataset', 'width', 'height', 'padding_top', 'padding_right', 'padding_bottom', 'padding_left', 'x_indicator', 'y_indicator', 'group_by', 'sort', 'y_maximum', 'y_maximum_value', 'unit_divisor', 'filter_by', 'filter_selection', 'colour', 'x_label', 'y_label', 'y_axis_ticks', 'x_text_rotation', 'labels_on_chart', 'label_font_size', 'label_format', 'legend_position', 'inject_css', 'save_as_template'
- Parameter choices ('value', ' label'):
    - sort = [('yasc', ' Y ascending'),('ydes', ' Y descending'),('xasc', ' X ascending'),('xdes', ' X descending')]
    - y_maximum = [('auto', ' Automatic'),('manual', ' Manual (define below)')]
    - legend_position = [('tr', ' Top right'),('tl', ' Top left'),('cr', ' Center right')]
- Considerations: Must be used with "group_by." If you don't have anything to group by, just use vb_column. At the moment, the chart is hardcoded to have a linear scale. "colour" parameter can accept multiple values via comma separation.

#### 10. Tree chart
- Location: tree.js
- Function: vb_tree(svgSelector,config,csvDat)
- Accepted configuration parameters:
    - 'title', 'dataset', 'width', 'height', 'padding_top', 'padding_right', 'padding_bottom', 'padding_left', 'x_indicator', 'y_indicator', 'c_indicator', 'sort', 'unit_divisor', 'filter_by', 'filter_selection', 'colour', 'label_font_size', 'label_format', 'inject_css', 'save_as_template'
- Parameter choices ('value', ' label'):
    - sort = [('native', ' Native ordering'),('yasc', ' Y ascending'),('ydes', ' Y descending'),('xasc', ' X ascending'),('xdes', ' X descending'),('casc', ' C ascending'),('cdes', ' C descending')]
- Considerations: Just a single layered tree chart. Can be utilized as a 2D tree chart if you specify a C indicator (sized by y_indicator, coloured on a linear scale by c_indicator). "colour" parameter can accept multiple values via comma separation.