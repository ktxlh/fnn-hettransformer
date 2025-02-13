import os
import json

def stats(in_dir, node_types, edge_files):
    nodes = {t : [] for t in node_types}
    for (t0, t1), fname in edge_files:
        with open(os.path.join(in_dir, fname), 'r') as f:
            for line in f.readlines():
                info = line.strip().split()
                nodes[t0].append(info[0])
                nodes[t1].append(info[1])
    counts = {k : len(set(v)) for k, v in nodes.items()}
    return counts

if __name__ == "__main__":
    for dataset in ['pheme', 'politifact', 'gossipcop']:
        if dataset in ['politifact', 'gossipcop']:
            prefix = f'fnn_{dataset}_'
            in_dir = '/rwproject/kdd-db/20-rayw1/FakeNewsNet/graph_def'
            edge_dir = os.path.join(in_dir, dataset)
            node_types = ['n', 'p', 'u']
            edge_files = {
                ('n', 'n'): 'news-news edges.txt',
                ('n', 'p'): 'news-post edges.txt',
                ('p', 'u'): 'post-user edges.txt',
                ('u', 'u'): 'user-user edges.txt',
            }
            edges_to_enforce = {('p', 'u'),}
        elif dataset == 'pheme':
            prefix = 'pheme_'
            in_dir = '/rwproject/kdd-db/20-rayw1/pheme-figshare'
            edge_dir = in_dir
            node_types = ['n', 'p', 'u']
            edge_files = {
                # ('n', 'n'): 'PhemeNewsNews.txt',
                ('n', 'p'): 'PhemeNewsPost.txt',
                ('n', 'u'): 'PhemeNewsUser.txt',
                ('p', 'p'): 'PhemePostPost.txt',
                ('p', 'u'): 'PhemePostUser.txt',
                ('u', 'u'): 'PhemeUserUser.txt',
            }
            edges_to_enforce = {('n', 'u'), ('p', 'u'),}
        elif dataset == 'buzzfeed':
            prefix = 'buzzfeed_'
            in_dir = '/rwproject/kdd-db/20-rayw1/buzzfeed-kaggle'
            edge_dir = in_dir
            node_types = ['n', 's', 'u']
            edge_files = {
                ('s', 'n'): 'BuzzFeedSourceNews.txt',
                ('n', 'n'): 'BuzzFeedNewsNews.txt',
                ('n', 'u'): 'BuzzFeedNewsUser.txt',
                ('u', 'u'): 'BuzzFeedUserUser.txt',
            }
            edges_to_enforce = {('n', 'u'),}

        counts = stats(in_dir, node_types, edge_files)
        print(dataset)
        print(json.dumps(counts, indent=4))