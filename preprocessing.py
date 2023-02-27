import os
import json
import pickle
from pprint import PrettyPrinter
from tqdm import tqdm
import networkx as nx


events = [i for i in os.listdir(".") if "." not in i]
graph_dict = {event: {"rumours": [], "non-rumours": []} for event in events}

for event in events:
    # non-rumours
    non_rumour_list = [i for i in os.listdir(f"./{event}/non-rumours") if "." not in i]

    for root_id in tqdm(non_rumour_list,
                        desc=f"preprocessing {event} non-rumours:"):
        graph = nx.DiGraph()

        # root node attribution
        with open(f"./{event}/non-rumours/{root_id}/source-tweets/{root_id}.json", "r") as f:
            root_info: dict = json.load(f)

        graph.add_node(root_info["id"])

        for k, v in root_info.items():
            graph.nodes[root_info["id"]][k] = v

        reactions = [i for i in os.listdir(f"./{event}/non-rumours/{root_id}/reactions") if "json" in i and "._" not in i]

        for reaction in reactions:
            with open(f"./{event}/non-rumours/{root_id}/reactions/{reaction}", "r") as f:
                data: dict = json.load(f)

            # node attributions
            graph.add_node(data["id"])

            for k, v in data.items():
                graph.nodes[data["id"]][k] = v

            try:
                graph.add_edge(data["id"], data["in_reply_to_status_id"])
            except ValueError:
                graph.add_node(data["id"])

        graph_dict[event]["non-rumours"].append(graph)

    # rumours
    rumour_list = [i for i in os.listdir(f"./{event}/rumours") if "." not in i]

    for root_id in tqdm(rumour_list,
                        desc=f"preprocessing {event} rumours:"):
        graph = nx.DiGraph()

        # root node attribution
        with open(f"./{event}/rumours/{root_id}/source-tweets/{root_id}.json", "r") as f:
            root_info: dict = json.load(f)

        graph.add_node(root_info["id"])

        for k, v in root_info.items():
            graph.nodes[root_info["id"]][k] = v

        reactions = [i for i in os.listdir(f"./{event}/rumours/{root_id}/reactions") if "json" in i and "._" not in i]

        for reaction in reactions:
            with open(f"./{event}/rumours/{root_id}/reactions/{reaction}", "r") as f:
                data: dict = json.load(f)

            # node attributions
            graph.add_node(data["id"])

            for k, v in data.items():
                graph.nodes[data["id"]][k] = v

            try:
                graph.add_edge(data["id"], data["in_reply_to_status_id"])
            except ValueError:
                graph.add_node(data["id"])

        graph_dict[event]["rumours"].append(graph)


with open("./graph_dict.pkl", "wb") as f:
    pickle.dump(graph_dict, f)

PrettyPrinter().pprint(graph_dict[events[0]]["rumours"][0].nodes)