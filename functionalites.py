# file with all functionalities for this app, like show feed, search and autocomplete

import datetime

def show_feed(user,users,graph,statuses):
    show_statuses = [None] * 10
    
    for status in statuses:
        author = users[status[5]]
        
        total = edge_rank_value(author,user,graph,status)
            
        if show_statuses[0] is None:
            for i in range(10):
                if show_statuses[9 - i] is None:
                    show_statuses[9 - i] = (status,total)
                    
                    if i == 9:
                        show_statuses.sort(key=lambda elem : elem[1])
                    break
            
        elif show_statuses[0][1] < total:
            show_statuses[0] = (status,total)
            show_statuses.sort(key=lambda elem : elem[1])
                
    for i in show_statuses[::-1]:
        print_status(i[0])

def search(user,graph,text,statuses,trie,users):
    show_statuses = {}
    if "\"" in text:
        if text[0] == "\"" and text [-1] == "\"":
            phrase = text[1:-1]
            text = ""
        
        elif text[0] == "\"":
            text = text.split("\"")[1:]
            phrase = text[0]
            text = text[1]
            if text[0] == " ":
                text = text[1:]
        
        elif text [-1] == "\"":
            text = text.split("\"")
            phrase =  text[1]
            text = text[0]
        
        else:
            text = text.split("\"")
            phrase =  text[1]
            if text[0][-1] == " " and text[2][0] == " ":
                text[0] = text[0][:-1]
            text = text[0] + text[2]
        
        phrase_list = phrase.split(" ")
        all_statuses = []
        first = True
        
        for word in phrase_list:
            search_result = trie.search(word)
            if search_result != False:
                search_result = set(search_result)
                if first:
                    for status in search_result:
                        all_statuses.append(status)
                    first = False
                
                else:
                    removing = []
                    for status in all_statuses:
                        if status not in search_result:
                            removing.append(status)
                            
                    for i in removing:
                        all_statuses.remove(i)
                        
        remove_statuses = []
        for status in all_statuses:
            if phrase not in statuses[status][1]:
                remove_statuses.append(status)
                
        for status in remove_statuses:
            all_statuses.remove(status)

        for status in all_statuses:
            show_statuses[status] = [1,[phrase]]
    
    if text != "" and text != " ":
        text = text.split(" ")
        for word in text:
            if word != "":
                search_result = trie.search(word)
                if search_result != False:
                    search_result = set(search_result)
                    for status in search_result:
                        if status in show_statuses:
                            show_statuses[status][0] += 1
                            show_statuses[status][1].append(word)
                        else:
                            show_statuses[status] = [1,[word]]
           
    if len(show_statuses) > 0:
        show_statuses = [(status,show_statuses[status]) for status in show_statuses]
        show_statuses.sort(key=lambda elem : elem[1][0])
        
        new_statuses = []
        sorting_statuses = []
        num_goods = show_statuses[0][1][0]
        for status in show_statuses:
            if status[1][0] == num_goods:
                sorting_statuses.append((status,edge_rank_value(users[statuses[status[0]][5]],user,graph,statuses[status[0]])))
            else:
                sorting_statuses.sort(key=lambda elem : elem[1])
                for i in sorting_statuses:
                    new_statuses.append(i[0])
                
                sorting_statuses = [(status,edge_rank_value(users[statuses[status[0]][5]],user,graph,statuses[status[0]]))]
                num_goods = status[1][0]
        
        sorting_statuses.sort(key=lambda elem : elem[1])
        for i in sorting_statuses:
            new_statuses.append(i[0])
            
        length = len(new_statuses) - 1
        num_tries = 10
        if length < 9:
            num_tries = length + 1
            
        for i in range(num_tries):
            print_status(statuses[new_statuses[length - i][0]],highlight = new_statuses[length - i][1][1])
    
    else:
        print("Nema statusa koji odgovaraju pretrazi!")

def autocomplete(text,trie):
    new_search = text.split(" ")
    new_search = ''.join(letter for letter in new_search[-1] if (ord(letter.lower()) >= ord('a') and ord(letter.lower()) <= ord('z')))
    
    texts = trie.autocomplete_word(new_search.lower())
    
    if len(texts) == 0:
        print("Nema odgovarajucih opcija za autocomplete!")
        text = text[:-1]
        
    else:
        print("Unesite broj opcije za autocomplete(maksimalno 5 najpopularnijih je dato): ")
        for i in range(len(texts)):
            print(str(i + 1) + ". " + texts[len(texts) - 1 - i][0])
            
        choice = input("Opcija: ")
        add_text = ""
        
        if choice == "1":
            add_text = texts[len(texts) - 1][0]
        elif choice == "2":
            add_text = texts[len(texts) - 2][0]
        elif choice == "3":
            add_text = texts[len(texts) - 3][0]
        elif choice == "4":
            add_text = texts[len(texts) - 4][0]
        else:
            add_text = texts[len(texts) - 5][0]
            
        text = text.split(" ")
        text[-1] = add_text
        text = " ".join(text)
    
    return text

def print_status(status,highlight = []):
    text = status[1]
    if len(highlight) != 0:
        highlight = set(highlight)
        for word in highlight:
            text = text.replace(" " + word + " "," ***" + word + "*** ")
            text = text.replace(" " + word.upper() + " "," ***" + word.upper() + "*** ")
            text = text.replace(" " + word.capitalize() + " "," ***" + word.capitalize() + "*** ")
            text = text.replace("(" + word + " ","(***" + word + "*** ")
            text = text.replace("(" + word.upper() + " ","(***" + word.upper() + "*** ")
            text = text.replace("(" + word.capitalize() + " ","(***" + word.capitalize() + "*** ")
            text = text.replace(" " + word + ")"," ***" + word + "***)")
            text = text.replace(" " + word.upper() + ")"," ***" + word.upper() + "***)")
            text = text.replace(" " + word.capitalize() + ")"," ***" + word.capitalize() + "***)")
            text = text.replace("(" + word + ")","(***" + word + "***)")
            text = text.replace("(" + word.upper() + ")","(***" + word.upper() + "***)")
            text = text.replace("(" + word.capitalize() + ")","(***" + word.capitalize() + "***)")
    
    print("Text: " + text)
    print("Type: " + status[2])
    print("Link: " + status[3])
    print("Date: " + status[4])
    print("Author: " + status[5])
    print("Reactions: " + status[6] + " Comments: " + status[7] + " Shares: " + status[8])
    print("Likes: " + status[9] + " Loves: " + status[10] + " Wows: " + status[11] + " Hahas: " + status[12]
          + " Angrys: " + status[13] + " Sads: " + status[14])
    print()
    
def edge_rank_value(author,user,graph,status):
    affinity = 10
    edge = graph.get_edge(user,author)
    if edge is not None:
        affinity = edge.element()
            
    weight = 1
    if int(status[6]) > 10000:
        weight += 0.2
    elif int(status[6]) > 1000:
        weight += 0.1
    elif int(status[6]) > 100:
        weight += 0.05
                
    if int(status[7]) > 4000:
        weight += 0.25
    elif int(status[7]) > 700:
         weight += 0.1
    elif int(status[7]) > 50:
        weight += 0.05
                
    if int(status[8]) > 12000:
        weight += 0.3
    elif int(status[8]) > 2000:
        weight += 0.2
    elif int(status[8]) > 100:
        weight += 0.05
                
    if int(status[9]) > 3000:
        weight += 0.05
                
    if int(status[10]) > 1000:
        weight += 0.05
                
    if int(status[11]) > 1000:
        weight += 0.05
            
    if int(status[12]) > 1500:
        weight += 0.05
                
    if int(status[13]) > 200:
        weight += 0.05
                
    if int(status[14]) > 200:
        weight += 0.05
            
    date = datetime.datetime.strptime(status[4],"%Y-%m-%d %H:%M:%S")
    time = 0.01
    if datetime.datetime.now() - date < datetime.timedelta(hours=3):
        time = 1
    elif datetime.datetime.now() - date < datetime.timedelta(days=1):
        time = 0.8
    elif datetime.datetime.now() - date < datetime.timedelta(days=3):
        time = 0.3
    elif datetime.datetime.now() - date < datetime.timedelta(days=10):
        time = 0.1
    elif datetime.datetime.now() - date < datetime.timedelta(days=30):
        time = 0.05
    
    return affinity * weight * time