# file with functions that create, save or load the graph and trie

from parse_files import *
from graph import Graph
import pickle
from trie import Trie
import datetime

def create_initial_graph(path):
    graph = Graph(True)
    
    with open(path) as file:
        lines = file.readlines()
        lines.pop(0)

        for line in lines:
            items = line.strip().split(",")
            user = items[0]
            friends = items[2:]
            
            for vertex in graph.vertices():
                if vertex.element() == user:
                    user = vertex
                    break
                    
            if user == items[0]:
                user = graph.insert_vertex(user)
            
            for friend in friends:
                friend_vertex = None
                
                for vertex in graph.vertices():
                    if vertex.element() == friend:
                        friend_vertex = vertex
                        break
                
                if friend_vertex is None:
                    friend_vertex = graph.insert_vertex(friend)
                
                value = 1000
                if graph.get_edge(user,friend_vertex) is None:
                    graph.insert_edge(user,friend_vertex,value)
    
    return graph, {user.element() : user for user in graph.vertices()}

def add_affinity(graph,users,statuses,comments,reactions,shares):
    statuses = {status[0]:status for status in statuses}
    
    for share in shares:
        sharer = share[1]
        date = datetime.datetime.strptime(share[2],"%Y-%m-%d %H:%M:%S")
        
        if share[0] in statuses:
            status = statuses[share[0]]
        else:
            continue
        
        author = status[5]
        
        if author not in users:
            continue
        elif sharer not in users:
            continue
        else:
            author = users[author]
            sharer = users[sharer]
        
        value = 500
        
        if datetime.datetime.now() - date > timedelta(days = 365):
            value *= 0.05
        elif datetime.datetime.now() - date > timedelta(days = 50):
            value *= 0.2
        
        edge = graph.get_edge(sharer,author)
        if edge is not None:
            edge.set_element(edge.element() + value)
        else:
            graph.insert_edge(sharer,author,value)
            
    for comment in comments:
        sharer = comment[4]
        date = datetime.datetime.strptime(comment[5],"%Y-%m-%d %H:%M:%S")
        
        if comment[1] in statuses:
            status = statuses[comment[1]]
        else:
            continue
    
        author = status[5]
        
        if author not in users:
            continue
        elif sharer not in users:
            continue
        else:
            author = users[author]
            sharer = users[sharer]
        
        value = 350
        
        if datetime.datetime.now() - date > timedelta(days = 365):
            value *= 0.05
        elif datetime.datetime.now() - date > timedelta(days = 50):
            value *= 0.2
        
        edge = graph.get_edge(sharer,author)
        if edge is not None:
            edge.set_element(edge.element() + value)
        else:
            graph.insert_edge(sharer,author,value)
            
    for reaction in reactions:
        reactor = reaction[2]
        date = datetime.datetime.strptime(reaction[3],"%Y-%m-%d %H:%M:%S")
        
        if reaction[0] in statuses:
            status = statuses[reaction[0]]
        else:
            continue
    
        author = status[5]
        
        if author not in users:
            continue
        elif reactor not in users:
            continue
        else:
            author = users[author]
            reactor = users[reactor]
        
        value = 200
        if reaction[1] == "sads":
            value = 100
        elif reaction[1] == "loves":
            value = 250
        elif reaction[1] == "angrys":
            value = 50
        elif reaction[1] == "likes":
            value = 150
        
        if datetime.datetime.now() - date > timedelta(days = 365):
            value *= 0.05
        elif datetime.datetime.now() - date > timedelta(days = 50):
            value *= 0.2
        
        edge = graph.get_edge(reactor,author)
        if edge is not None:
            edge.set_element(edge.element() + value)
        else:
            graph.insert_edge(reactor,author,value)

            
def pickle_graph(graph):
    dbfile = open('graph.pickle', 'wb')
    pickle.dump(graph,dbfile)
    dbfile.close()
    
def unpickle_graph():
    dbfile = open('graph.pickle', 'rb')
    graph = pickle.load(dbfile)
    dbfile.close()
    
    return graph, {user.element() : user for user in graph.vertices()}

def load_trie(statuses):
    trie = Trie()
    
    indexes = 0
    for status in statuses:
        for word in status[1].split(" "):
            word = ''.join(letter.lower() for letter in word if (ord(letter.lower()) >= ord('a') and ord(letter.lower()) <= ord('z')))
            trie.insert(word,indexes)
            
        author = status[5].split(" ")
        
        for word in author:
            word = ''.join(letter.lower() for letter in word if (ord(letter.lower()) >= ord('a') and ord(letter.lower()) <= ord('z')))
            trie.insert(word,indexes)
    
        indexes += 1
        
    return trie