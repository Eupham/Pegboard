import graphviz

dot = graphviz.Digraph(comment='Knowledge Acquisition')
dot.attr(rankdir='LR', layout='dot')

# add nodes with fixed size
dot.node('User', shape='square', fixedsize='true', width='2.5', height='2.5')
dot.node('Discord', shape='square', fixedsize='true', width='2.5', height='2.5')
dot.node('Redis Knowledge Base', shape='square', fixedsize='true', width='2.5', height='2.5')

# add edges
dot.edge('User', 'Discord', label='input data')
dot.edge('Discord', 'Redis Knowledge Base', label='discord bot')

# display graph
dot.render('knowledge-acquisition', view=True)
