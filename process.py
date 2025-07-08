import os
import re
from collections import defaultdict
import matplotlib.pyplot as plt

def load_output_data(directory="cleaned"):
    # Nested dictionary: data[algorithm][cluster_size][msg_size] = content
    data = defaultdict(lambda: defaultdict(dict))

    # Regex to match filenames like: algorithm-cluster-msgsize.out
    pattern = re.compile(r'^([a-zA-Z0-9_]+)-(\d+)-(\d+)\.out$')

    if not os.path.isdir(directory):
        raise FileNotFoundError(f"Directory '{directory}' does not exist.")

    for filename in os.listdir(directory):
        match = pattern.match(filename)
        if not match:
            print(f"Skipping invalid filename: {filename}")
            continue

        algorithm, cluster_size, msg_size = match.groups()
        cluster_size = int(cluster_size)
        msg_size = int(msg_size)

        filepath = os.path.join(directory, filename)
        with open(filepath, 'r') as f:
            content = f.read()

        data[algorithm][cluster_size][msg_size] = content

    return data

def extract_max_ar(data):
    ar_pattern = re.compile(r'\(\d+\)\s+[^=]+=\s*([-\d.eE]+):')
    max_ar_values = defaultdict(lambda: defaultdict(dict))

    for algorithm in data:
        for cluster in data[algorithm]:
            for message in data[algorithm][cluster]:
                text = data[algorithm][cluster][message]
                ar_matches = ar_pattern.findall(text)

                if not ar_matches:
                    max_ar = None
                else:
                    ar_values = [float(ar) for ar in ar_matches]
                    max_ar = max(ar_values)

                max_ar_values[algorithm][cluster][message] = max_ar

    return max_ar_values

def plot_max_ar_per_cluster(max_ar_values, save_dir=None):
    # Collect all clusters
    clusters = set()
    for algorithm in max_ar_values:
        clusters.update(max_ar_values[algorithm].keys())

    for cluster in sorted(clusters):
        plt.figure(figsize=(10, 6))

        for algorithm in sorted(max_ar_values.keys()):
            # Get (MESSAGE, max_ar) pairs for this algorithm and cluster
            if cluster not in max_ar_values[algorithm]:
                continue

            message_ar = max_ar_values[algorithm][cluster]
            # Sort by message size
            sorted_msgs = sorted(message_ar.keys())
            x = sorted_msgs
            y = [message_ar[msg] for msg in sorted_msgs]

            plt.plot(x, y, label=algorithm, marker='o')

        plt.title(f"Max AR vs Message Size (Cluster Size = {cluster})")
        plt.xlabel("Message Size")
        plt.ylabel("Max AR")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()

        if save_dir:
            import os
            os.makedirs(save_dir, exist_ok=True)
            plt.savefig(f"{save_dir}/cluster_{cluster}.png")
        else:
            plt.show()

if __name__ == "__main__":
	plot_max_ar_per_cluster(extract_max_ar(load_output_data()))

