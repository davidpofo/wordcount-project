from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.transform import factor_cmap
from django.shortcuts import render, render_to_response
from bokeh.palettes import Spectral11
import operator

def homepage(request):
    return render(request, 'home.html')
def about(request):
    return render(request, 'about.html')
def count(request):
    # words list from full text
    fulltext = request.GET['fulltext']
    wordlist = [word.strip().replace(',', '').replace('.', '').replace('-', '') for word in fulltext.split()]

    # dictionary of words to ignore updates with articles
    ignorelist = {}
    try:
        ignoretext = request.GET['ignorelist']
        for key in ignoretext.split(','):
            ignorelist[key.strip()] = ''
    except Exception as ex:
        print("No words were entered here!{}".format(ex))

    articles = {'a': '', 'an': '', 'and': '', 'the': ''}
    ignorelist.update(articles)
    # Creating a dictionary of counts for each word in the word list
    worddictionary = {}
    for word in wordlist:
        if word in worddictionary:
            # increase by 1 for that key
            worddictionary[word] += 1
        else:
            # add to dictionary
            worddictionary[word] = 1
        # sorting to get the top words
    sortedwords = sorted(worddictionary.items(), key=operator.itemgetter(1), reverse=True)


    # Remove articles and ignored words within the sorted dictionary
    for word, count in reversed(sortedwords):
        if word in ignorelist:
            sortedwords.remove((word,count))

    #Bokeh
    top_ten_words = dict(sortedwords[0:11])
    # Graph X and Y coordinates
    x, y = zip(*top_ten_words.items())
    words = list(x)
    counts = list(y)
    source = ColumnDataSource(data=dict(words=words, counts=counts))
    # Dictionary for word filtering
    colorpal = Spectral11
    top_ten_coloring_dict = dict(zip(words, colorpal))


    p = figure(x_range=words, plot_height=350, plot_width= 850, x_axis_label = "Word Name", y_axis_label = "Frequency")
    p.vbar(x='words', top='counts', width=0.9, source=source, legend="words",
           line_color='white', fill_color=factor_cmap('words', palette=Spectral11,factors=words))
    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    p.y_range.end = counts[0] + 1
    p.legend.orientation = "horizontal"
    p.legend.location = "top_center"
    p.xaxis.axis_label_text_font_style = "bold"
    p.yaxis.axis_label_text_font_style = "bold"
    hover = HoverTool()
    hover.tooltips = [
        ('Count', '@counts'),
    ]

    p.add_tools(hover)
    #store components
    script, div = components(p)

    return render_to_response('count.html', {'top_ten_coloring_dict': top_ten_coloring_dict, 'fulltext':fulltext, 'count':len(wordlist), 'sortwords':sorted(top_ten_words.items(),
                                                                                                                                                           key=operator.itemgetter(1), reverse= True), 'script':script, 'div':div})

