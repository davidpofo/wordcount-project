from bokeh.models import ColumnDataSource
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
    fulltext = request.GET['fulltext']
    wordlist = fulltext.split()

    worddictionary = {}
    for word in wordlist:
        if word in worddictionary:
            # increase by 1 for that key
            worddictionary[word] += 1
        else:
            # add to dictionary
            worddictionary[word] = 1
        sortedwords = sorted(worddictionary.items(), key=operator.itemgetter(1), reverse= True)

    # Remove articles within the sorted dictionary
    for word, count in sortedwords:
        articles = {'a': '', 'an': '', 'and': '', 'the': ''}
        if word in articles:
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


    p = figure(x_range=words, plot_height=350, plot_width= 850, title="Word Counts")
    p.vbar(x='words', top='counts', width=0.9, source=source, legend="words",
           line_color='white', fill_color=factor_cmap('words', palette=Spectral11,factors=words))
    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    p.y_range.end = counts[0] + 1
    p.legend.orientation = "horizontal"
    p.legend.location = "top_center"

    #store components
    script, div = components(p)

    return render_to_response('count.html', {'top_ten_coloring_dict': top_ten_coloring_dict, 'fulltext':fulltext, 'count':len(wordlist), 'sortwords':sorted(top_ten_words.items(),
                                                                                                                                                           key=operator.itemgetter(1), reverse= True), 'script':script, 'div':div})

