import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64
from matplotlib.patches import Circle, Rectangle, Arc
from matplotlib import rcParams

def get_image():
    #creates a bytes buffer for the image to save
    buffer = BytesIO()
    #create the plot with the use of the BytesIO object as its 'file'
    plt.savefig(buffer,format='png')
    #set the cursor the beginning of the stream
    buffer.seek(0)
    #retrieve the entire content of the stream 
    image_png = buffer.getvalue()

    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')


    #free the memory of the buffer
    buffer.close()

    return graph


def get_correlation_plot(title,*args,**kwargs):
    plt.switch_backend('AGG')
    data = kwargs.get('data')
    x = kwargs.get('x')
    y = kwargs.get('y')
    x_label = kwargs.get('x_label')
    y_label = kwargs.get('y_label')

    corr = round(data[x].corr(data[y]),2)
    sns.jointplot(x=x,
                  y=y,
                  kind='reg',
                  data=data).set_axis_labels(x_label,y_label)

    plt.tight_layout()

    graph = get_image()

    return graph, corr

def draw_court(ax=None, color='black', lw=2, outer_lines=False):
    # If an axes object isn't provided to plot onto, just get current one
    if ax is None:
        ax = plt.gca()

    # Create the various parts of an NBA basketball court

    # Create the basketball hoop
    # Diameter of a hoop is 18" so it has a radius of 9", which is a value
    # 7.5 in our coordinate system
    hoop = Circle((0, 0), radius=7.5, linewidth=lw, color=color, fill=False)

    # Create backboard
    backboard = Rectangle((-30, -7.5), 60, -1, linewidth=lw, color=color)

    # The paint
    # Create the outer box 0f the paint, width=16ft, height=19ft
    outer_box = Rectangle((-80, -47.5), 160, 190, linewidth=lw, color=color,
                          fill=False)
    # Create the inner box of the paint, widt=12ft, height=19ft
    inner_box = Rectangle((-60, -47.5), 120, 190, linewidth=lw, color=color,
                          fill=False)

    # Create free throw top arc
    top_free_throw = Arc((0, 142.5), 120, 120, theta1=0, theta2=180,
                         linewidth=lw, color=color, fill=False)
    # Create free throw bottom arc
    bottom_free_throw = Arc((0, 142.5), 120, 120, theta1=180, theta2=0,
                            linewidth=lw, color=color, linestyle='dashed')
    # Restricted Zone, it is an arc with 4ft radius from center of the hoop
    restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw,
                     color=color)

    # Three point line
    # Create the side 3pt lines, they are 14ft long before they begin to arc
    corner_three_a = Rectangle((-220, -47.5), 0, 140, linewidth=lw,
                               color=color)
    corner_three_b = Rectangle((220, -47.5), 0, 140, linewidth=lw, color=color)
    # 3pt arc - center of arc will be the hoop, arc is 23'9" away from hoop
    # I just played around with the theta values until they lined up with the 
    # threes
    three_arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw,
                    color=color)

    # Center Court
    center_outer_arc = Arc((0, 422.5), 120, 120, theta1=180, theta2=0,
                           linewidth=lw, color=color)
    center_inner_arc = Arc((0, 422.5), 40, 40, theta1=180, theta2=0,
                           linewidth=lw, color=color)

    # List of the court elements to be plotted onto the axes
    court_elements = [hoop, backboard, outer_box, inner_box, top_free_throw,
                      bottom_free_throw, restricted, corner_three_a,
                      corner_three_b, three_arc, center_outer_arc,
                      center_inner_arc]

    if outer_lines:
        # Draw the half court line, baseline and side out bound lines
        outer_lines = Rectangle((-250, -47.5), 500, 470, linewidth=lw,
                                color=color, fill=False)
        court_elements.append(outer_lines)

    # Add the court elements onto the axes
    for element in court_elements:
        ax.add_patch(element)

    return ax

def get_pie_chart(data):
    plt.switch_backend('Agg')
    fig, ax = plt.subplots()
    fig.set_size_inches(4, 4)
    pie = data['action_type'].value_counts()[:5].plot.pie(labels=['','','','',''],  ax=ax, autopct='%.2f%%')
    ax.legend(loc=8, labels=data['action_type'].value_counts().index,bbox_to_anchor=(0.5, 1))
    plt.axis('off')

    return pie

def get_bar_plot(data,color='#1f77b4'):
    # plt.switch_backend('Agg')
    fig, ax = plt.subplots()
    fig.set_size_inches(6.75, 4)
    bar = data['action_type'].value_counts()[:5].plot.barh(color=color)
    data = data.loc[data['action_type'].isin(data['action_type'].value_counts()[:5].index)]
    max_value = data['action_type'].value_counts()[1]
    
    
    for i, v in enumerate(data['action_type'].value_counts()):
        ax.text(v+1, i, str(v), color=color)
    plt.xlim(0,max_value+30)
    rcParams.update({'figure.autolayout': True})

    return bar

def get_pct(made,attempted):
    return (made/attempted) * 100

def percentage(a, b):
    return round(a / b * 100, 2)