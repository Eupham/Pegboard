from graphviz import Digraph

# create a new graph
dot = Digraph()
dot.attr(rankdir='LR', layout='dot')

# add the first set of boxes
dot.node('b1', shape='box', label='Customer')
dot.node('b2', shape='box', label='CRM', pos='0,1!')
dot.node('middle', shape='box', label='MIS & DSS', pos='-1,0!')

# add the subgraphs for the Front-Office and Back-Office ERP systems
with dot.subgraph(name='cluster_erp_fo') as erp_fo:
    erp_fo.node('erp_fo', shape='none', label='Front-Office ERP')

    erp_fo.node('erp_fo_1', shape='box', label='Marketing Information System')
    erp_fo.node('erp_fo_2', shape='box', label='Sales Information System')
    erp_fo.node('erp_fo_3', shape='box', label='Customer Management Information System')

with dot.subgraph(name='cluster_erp_bo') as erp_bo:
    erp_bo.node('erp_bo', shape='none', label='Back-Office ERP')

    erp_bo.node('erp_bo_1', shape='box', label='HRIS')
    erp_bo.node('erp_bo_2', shape='box', label='Financial Information System')
    erp_bo.node('erp_bo_3', shape='box', label='Manufacturing Information System')
    erp_bo.node('erp_bo_4', shape='box', label='Inventory System')

# add the second set of boxes
dot.node('b3', shape='box', label='SCM', pos='2,0!')
dot.node('b4', shape='box', label='Suppliers', pos='2,1!')

# add the diamond nodes and position them
dot.node('d1', shape='diamond', label='Front-Office', pos='-1,0!')
dot.node('d2', shape='diamond', label='Back-Office', pos='2,0!')

# create edges between the diamond nodes and the boxes
dot.edge('d1', 'b1')
dot.edge('d1', 'b2')
dot.edge('d1', 'middle')
dot.edge('d1', 'erp_fo')
dot.edge('d2', 'middle')
dot.edge('d2', 'erp_bo')
dot.edge('d2', 'b3')
dot.edge('d2', 'b4')

# render the graph to a PDF file
dot.render('Federation of Information Systems (FIS)', view=True)
