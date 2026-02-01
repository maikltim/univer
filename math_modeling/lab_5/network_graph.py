import networkx as nx

def build_network(users, provider, websites):
    G = nx.Graph()

    for u in users:
        G.add_edge(u.name, "Provider")

    for w in websites:
        G.add_edge("Provider", w.name)

    return G
