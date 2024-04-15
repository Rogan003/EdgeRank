class TrieNode:
    def __init__(self):
        self.children = [None]*26
        self.isEndOfWord = False
        self.statuses = []
        self.popularity = 0
 
class Trie:
    def __init__(self):
        self.root = self.getNode()
 
    def getNode(self):
        return TrieNode()
 
    def _charToIndex(self,ch):
        return ord(ch.lower())-ord('a')
 
 
    def insert(self,key,status_index):
        pCrawl = self.root
        length = len(key)
        for level in range(length):
            index = self._charToIndex(key[level])
 
            if not pCrawl.children[index]:
                pCrawl.children[index] = self.getNode()
            pCrawl = pCrawl.children[index]
 
        pCrawl.isEndOfWord = True
        pCrawl.popularity += 1
        pCrawl.statuses.append(status_index)
    
    def search(self, key):
        pCrawl = self.root
        length = len(key)
        for level in range(length):
            index = self._charToIndex(key[level])
            if not pCrawl.children[index]:
                return False
            pCrawl = pCrawl.children[index]
 
        if pCrawl.isEndOfWord:
            return pCrawl.statuses
        else:
            False
    
    def autocomplete_word(self,word):
        pCrawl = self.root
        length = len(word)
        words = []
        for level in range(length):
            index = self._charToIndex(word[level])
            if not pCrawl.children[index]:
                return words
            pCrawl = pCrawl.children[index]
 
        self.search_autocomplete(pCrawl,words,word)
          
        return words
        
    def search_autocomplete(self,node,words,word):
        for i in range(26):
            if node.children[i] is not None:
                if node.children[i].isEndOfWord:
                    if len(words) == 5:
                        if words[0][1] < node.children[i].popularity:
                            words[0] = (word+chr(ord('a') + i),node.children[i].popularity)
                            words.sort(key=lambda elem : elem[1])
                    else:
                        words.append((word+chr(ord('a') + i),node.children[i].popularity))
                        words.sort(key=lambda elem : elem[1])
                else:
                    self.search_autocomplete(node.children[i],words,word+chr(ord('a') + i))