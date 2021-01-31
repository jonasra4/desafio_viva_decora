import requests
import tree
from bs4 import BeautifulSoup
import re
from tabulate import tabulate

class Report:
    def __init__(self, project_name):
        self.project_name = project_name
        self.url = 'https://github.com/' + project_name + '/tree/master'
        
        self.total_lines = 0
        self.total_bytes = 0
        
        self.table = {}
        self.project_structure = None

        self.table_string = ''
        self.project_string = ''

    def scraping_lines_size(self, navigation):
        new_url = self.url + navigation
        page = requests.get(new_url)
        soup = BeautifulSoup(page.text, 'html.parser')
        lines_size = soup.find(class_='text-mono f6 flex-auto pr-3 flex-order-2 flex-md-order-1 mt-2 mt-md-0')
        pattern = r"[0-9.]+[ ][A-Za-z]*"
    
        try:
            regex_lines_size = re.findall(pattern, lines_size.text)
            lines = int(regex_lines_size[0].split(' ')[0])
            size = regex_lines_size[2]
            return lines, size
        except:
            regex_lines_size = re.findall(pattern, lines_size.text)
            size = regex_lines_size[0]
            return 0, size

    def scraping_project(self, navigation, node):
        new_url = self.url + navigation
        page = requests.get(new_url)
        current_node = node
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
                current_node.add_child( new_node  )
                self.scraping_project(new_navigation, new_node)
            else:
                new_navigation = navigation + '/' + nome
                new_node = tree.TreeNode(nome)
                new_node.lines, new_node.size = self.scraping_lines_size(new_navigation)
                new_node.convert_to_extension()
                new_node.convert_to_bytes()
                current_node.add_child(new_node)
        return node
    
    def structure_to_string(self, node):
        spaces = '|  ' * (node.get_level()-1)
        prefix = spaces + "|__ " if node.parent else ""
        
        if node.extension is not None:
            self.project_string += prefix + node.data + " (" + str(node.lines)+ " linhas)\n"
        else:
            self.project_string += prefix + "[" + node.data + "]\n"

        if node.children:
            for child in node.children:
                self.structure_to_string(child) 

    def read_project(self):
        root = tree.TreeNode("Project " + self.project_name)
        self.project_structure = self.scraping_project('', root )

    def count_total_lines_bytes(self):
        count_lines = 0
        count_bytes = 0
        
        for key, value in self.table.items():
            count_lines += value[0]
            count_bytes += value[1]
        
        self.total_lines = count_lines
        self.total_bytes = int(count_bytes)
    
    def count_total_lines_bytes_by_extension(self, node):
        if node.extension:
            if node.extension in self.table:
                self.table[node.extension][0] += node.lines
                self.table[node.extension][1] += node.size
            else:
                self.table[node.extension] = [node.lines, node.size]
                
        if node.children:
            for child in node.children:
                self.count_total_lines_bytes_by_extension(child)

    def table_to_string(self):
        headers = ['Extension', 'Lines', 'Bytes']
        new_table = []

        for key, value in self.table.items():
            new_table.append([key, value[0], value[1]])
        
        self.table_string = tabulate(new_table, headers=headers, tablefmt="github")

    def make_report(self):
        self.count_total_lines_bytes_by_extension(self.project_structure)
        self.structure_to_string(self.project_structure)
        
        self.count_total_lines_bytes()
        self.table_to_string()

    def save_report(self):
        file = open(self.project_name.replace('/','_') + '.txt',"w")

        file.write('Path: ' + self.project_name + '\n') 
        file.write('Lines: ' + str(self.total_lines) + '\n') 
        file.write('Bytes: ' + str(self.total_bytes) + '\n\n\n\n') 
        file.write(self.table_string + '\n\n\n')
        file.write(self.project_string)
        
        file.close()