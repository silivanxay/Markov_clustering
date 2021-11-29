import csv


def export_graph(filename, subgraph):
    ref_file = filename + '.csv'

    with open(ref_file, 'w', newline='') as csv_file_wr:
        fieldnamesR = ['Source', 'Target', 'Weight']
        writerR = csv.DictWriter(csv_file_wr, fieldnames=fieldnamesR)
        writerR.writeheader()
        for node in subgraph.nodes:
            for next_node in subgraph.neighbors(node):
                writerR.writerow({'Source': subgraph._node[node]['old_label'], 'Target': next_node, 'Weight': 1})
    csv_file_wr.close()


def export_clusters(ref_file, clusters):
    with open(ref_file, 'w', newline='') as csv_file_wr:
        fieldnamesR = ['Id', 'Cluster']
        writerR = csv.DictWriter(csv_file_wr, fieldnames=fieldnamesR)
        writerR.writeheader()
        count = 0
        clusterPrint = []
        for cluster in clusters:
            clusterPrint.append(cluster)
            for node in cluster:
                writerR.writerow({'Id': node, 'Cluster': count})
            count = count + 1
    csv_file_wr.close()
