import streamlit as st

# text form
query_script = st.text_area('Enter SQL script.', height=400)

try:
    # if SQL script has been entered, parse that and display the figure
    import regex
    # delete comment
    query_script = regex.sub(r'--.*\n|#.*\n|/\*([^*]|\*[^/])*\*/', '', query_script)

    # get CTEs
    cte_pattern = r'(?:with|,)\s*(\w+)\s+as\s*(?<rec>\((?:[^\(\)]+|(?&rec))*\))'
    ctes = regex.finditer(cte_pattern, query_script, regex.IGNORECASE)
    queries = {cte.group(1): cte.group(2) for cte in ctes}

    # get main query
    main_pattern = r'\)[;\s]*select' if any(queries) else r'select'
    start_main = regex.search(main_pattern, query_script, regex.IGNORECASE).span()[0] + 1
    queries['main'] = query_script[start_main:].strip()

    # find reference table or CTEs
    ref_pattern = r'(?:from|join)\s+([`.\-\w]+)'
    dependencies = dict()
    for name, script in queries.items():
        refs = regex.findall(ref_pattern, script, regex.IGNORECASE)
        dependencies[name] = [ref for ref in refs]
    
    from graphviz import Digraph

    # draw graph
    g = Digraph()
    g.attr('node', shape='box')
    with g.subgraph(name='querys') as c:
        c.attr(color='blue', label='querys')
        for name, refs in dependencies.items():
            for ref in refs:
                c.node(name, style='bold, filled' if name=='main' else 'solid, filled', fillcolor='#FFFFFF' if name=='main' else '#80CBC4')
                c.node(ref, style='solid, filled', fillcolor='#81C784' if '.' in ref else '#80CBC4')
                c.edge(name, ref)

    st.graphviz_chart(g)
except:
    # if SQL syntax is wrong or have not been entered raise message
    st.subheader('Check and modify script')
    