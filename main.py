# file with the main function, the app starts here

from parse_files import *
from load_graph import *
from functionalites import *

if __name__ == "__main__":
    print("Dobro dosli! Ucitava se aplikacija...")
    adjust_date_time("dataset/dataset/test_statuses.csv", "dataset/dataset/test_comments.csv",
                     "dataset/dataset/test_shares.csv", "dataset/dataset/test_reactions.csv")
    graph, users = unpickle_graph()
    statuses = load_statuses("dataset/dataset/original_statuses.csv")
    shares = load_shares("dataset/dataset/original_shares.csv")
    comments = load_comments("dataset/dataset/original_comments.csv")
    reactions = load_reactions("dataset/dataset/original_reactions.csv")
    user = None
    test_statuses = load_statuses("dataset/dataset/test_statuses.csv")
    test_shares = load_shares("dataset/dataset/test_shares.csv")
    test_comments = load_comments("dataset/dataset/test_comments.csv")
    test_reactions = load_reactions("dataset/dataset/test_reactions.csv")
    add_affinity(graph,users,test_statuses,test_comments,test_reactions,test_shares)
    
    for status in test_statuses:
        statuses.append(status)
        
    trie = load_trie(statuses)
    
    while True:
        print("Ulogujte se: ")
        username = input("Unesite korisnicko ime: ")
            
        if username in users:
            user = users[username]
            print("Uspesno ste se ulogovali!\n")
            break
        else:
            print("Netacno korisnicko ime!\n")
            
    while True:
        izbor = input("Izaberite opciju(1 - prikaz objava, 2 - pretraga, 3 - kraj): ")
        if izbor == "1":
            print("Prikaz objava: ")
            show_feed(user,users,graph,statuses)
            
        elif izbor == "2":
            text = input("Pretraga(ukoliko stavite ? na kraj dajemo autocomplete, pod \"\" tretiramo kao frazu): ")
            if text != "" and text[-1] == "?":
                text = autocomplete(text,trie)
            
            print("Rezultati za: " + text)
            search(user,graph,text,statuses,trie,users)
        
        elif izbor == "3":
            print("Kraj aplikacije!")
            break
        
        else:
            print("Nepostojeca opcija!")