import requests
import tree
from bs4 import BeautifulSoup
import re

def get_lines_and_size(url_project,navigation):
    new_url = url_project + navigation
    page = requests.get(new_url)
    soup = BeautifulSoup(page.text, 'html.parser')
    lines_size = soup.find(class_='text-mono f6 flex-auto pr-3 flex-order-2 flex-md-order-1 mt-2 mt-md-0')
    pattern = r"[0-9.]+[ ][A-Za-z]*"
   
    try:
        regex_lines_size = re.findall(pattern, lines_size.text)
        lines = int(regex_lines_size[1].split(' ')[0])
        size = regex_lines_size[2]
        return lines, size
    except:
        regex_lines_size = re.findall(pattern, lines_size.text)
        size = regex_lines_size[0]
        return 0, size

            
def get_arq(url_project, navigation, node):
    new_url = url_project + navigation
    page = requests.get(new_url)
    node_atual = node
    soup = BeautifulSoup(page.text, 'html.parser')
    # seleciona as linhas gerais
    arqs = soup.find_all(class_='Box-row Box-row--focus-gray py-2 d-flex position-relative js-navigation-item')

    for i in arqs:
        # pega o nome da pasta e ou arquivo
        nome = i.find(class_='js-navigation-open link-gray-dark').text
        pasta = i.find(class_='octicon-file-directory')
        
        if pasta:
            new_navigation = navigation + '/' + nome
            new_node = tree.TreeNode(nome)
            node_atual.add_child( new_node  )
            get_arq(url_project,new_navigation, new_node)
        else:
            new_navigation = navigation + '/' + nome
            new_node = tree.TreeNode(nome)
            new_node.lines, new_node.size = get_lines_and_size(url_project,new_navigation)
            new_node.convert_to_extension()
            new_node.convert_to_bytes()
            node_atual.add_child(new_node)

    return node




# url = 'https://github.com/frontpressorg/frontpress/tree/master'
# url = 'https://github.com/jonasra4/Unity-Controller-Scenes/tree/master'
url = 'https://github.com/jonasra4/snake/tree/master'

root = tree.TreeNode("frontpress")

aa = get_arq( url ,'', root)
# aa.print_tree()
aa.report()
relatorio = aa.rept

for key, value in relatorio.items():
    print(key, value)
# aa.print_ext()



