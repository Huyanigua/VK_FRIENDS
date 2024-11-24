import json
import networkx as nx
import matplotlib.pyplot as plt

# Загрузка данных из файла
with open('friends_data.json', 'r') as f:
    data = json.load(f)

G = nx.Graph()

# Добавление узлов и рёбер в граф
for user in data:
    user_id = user['id']
    friends = user['friends']

    for friend_id in friends:
        G.add_edge(user_id, friend_id)

# Определяем людей для анализа
people = {
    26959263: 'Дарья Котенко',
    53802015: 'Миша Погосян',
    57521323: 'Ольга Илларионова'
}

# Удаляем изолированные узлы
G.remove_nodes_from(list(nx.isolates(G)))

# Вычисление центральностей
betweenness = nx.betweenness_centrality(G)
betweenness_results = {user_id: betweenness.get(user_id, 0) for user_id in people}

print('\nЦентральность по посредничеству:')
for id, result in betweenness_results.items():
    print(f'\t{people[id]}: {result}')

closeness = nx.closeness_centrality(G)
closeness_results = {user_id: closeness.get(user_id, 0) for user_id in people}

print('\nЦентральность по близости:')
for id, result in closeness_results.items():
    print(f'\t{people[id]}: {result}')

# Увеличиваем max_iter для eigenvector_centrality
try:
    eigenvector = nx.eigenvector_centrality(G, max_iter=300)  # Увеличиваем до 300
except nx.PowerIterationFailedConvergence as e:
    print(f"Ошибка сходимости: {e}")
    eigenvector = {}  # Возвращаем пустой словарь, если не удалось вычислить

eigenvector_results = {user_id: eigenvector.get(user_id, 0) for user_id in people}

print('\nЦентральность собственного вектора:')
for id, result in eigenvector_results.items():
    print(f'\t{people[id]}: {result}')

# Визуализация графа
plt.figure(figsize=(8, 8))
pos = nx.spring_layout(G)

# Рисуем граф
nx.draw(G, pos, node_color='skyblue', node_size=10, edge_color='gray')

# Рисуем выделенные узлы
nx.draw_networkx_nodes(G, pos, nodelist=people.keys(), node_color='red', node_size=50)
nx.draw_networkx_labels(G, pos, labels=people, font_size=8, font_color='black', font_weight='bold')

plt.title('Граф друзей')
plt.show()
