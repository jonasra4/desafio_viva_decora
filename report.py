import re
import tree
import requests
import threading
from tabulate import tabulate
import concurrent.futures
from bs4 import BeautifulSoup
import time
from random import randrange

class Report:
    def __init__(self, project_name):
        self.project_name = project_name
        self.url = f'https://github.com/{project_name}/tree/master'
        
        self.total_lines = 0
        self.total_bytes = 0
        
        self.table = {}
        self.project_structure = None

        self.table_string = ''
        self.project_string = ''

    def scraping_lines_size(self, navigation):
        time.sleep(10)
        new_url = self.url + navigation
        page = requests.get(new_url)

        if page.ok:
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
        else:
            # print("tentando denovo {navigation}")
            # time.sleep(10)
            # self.scraping_lines_size(navigation)
            print(page.status_code, new_url)
            return 0, 112312313

    def scraping_project(self, navigation, node):
        new_url = self.url + navigation
        current_node = node
        # print(new_url)
        page = requests.get(new_url)
        
        soup = BeautifulSoup(page.text, 'html.parser')

        all_lines = soup.find_all(class_='Box-row Box-row--focus-gray py-2 d-flex position-relative js-navigation-item')

        for i in all_lines:
            nome = i.find(class_='js-navigation-open link-gray-dark').text

            new_navigation = navigation + '/' + nome
            new_node = tree.TreeNode(nome)

            if i.find(class_='octicon-file-directory'):
                new_node.path = new_url
                current_node.add_child( new_node )
                self.scraping_project(new_navigation,new_node)
                # threading.Thread(target=self.scraping_project, args=(new_navigation,new_node, )).start()
            else:
                new_node.lines, new_node.size = 10, '13 Bytes'
                new_node.convert_to_extension()
                new_node.convert_to_bytes()
                new_node.path = new_url+'/'+nome
                current_node.add_child( new_node )

        return node

    def structure_to_string(self, node):
        spaces = '|  ' * (node.get_level()-1)
        prefix = spaces + "|__ " if node.parent else ""
        
        if node.extension is not None:
            self.project_string += f'{prefix + node.data} ({node.lines} lines)\n'
        else:
            self.project_string += f'{prefix}[{node.data}]\n'

        if node.children:
            for child in node.children:
                self.structure_to_string(child) 

    def print_arqs(self, node):        
        
        if node.extension:
            page = requests.get(node.path)
            # print(node.path)
            if page.ok:
                soup = BeautifulSoup(page.text, 'html.parser')
                lines_size = soup.find(class_='text-mono f6 flex-auto pr-3 flex-order-2 flex-md-order-1 mt-2 mt-md-0')
                pattern = r"[0-9.]+[ ][A-Za-z]*"

                try:
                    regex_lines_size = re.findall(pattern, lines_size.text)
                    node.lines = int(regex_lines_size[0].split(' ')[0])
                    node.size = regex_lines_size[2]
                    node.convert_to_bytes()
                except:
                    regex_lines_size = re.findall(pattern, lines_size.text)
                    node.lines = 0
                    node.size = regex_lines_size[0]
                    node.convert_to_bytes()

            else:
                print(page.status_code, node.path)
                node.lines = 0
                node.size = 0

        if node.children:
            for child in node.children:
                # threading.Thread(target=self.print_arqs, args=(child, )).start()
                self.print_arqs(child)

    def read_project(self):
        root = tree.TreeNode(f'Project {self.project_name}')
        self.project_structure = self.scraping_project('', root )
        self.print_arqs(self.project_structure)

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
            line_count = f'{value[0]} ({ int(100 * value[0] / self.total_lines)}%)'
            byte_count = f'{int(value[1])} ({ int(100 * value[1] / self.total_bytes)}%)'

            new_table.append([key, line_count, byte_count])
        
        self.table_string = tabulate(new_table, headers=headers, tablefmt="github")

    def make_report(self):
        self.count_total_lines_bytes_by_extension(self.project_structure)
        self.structure_to_string(self.project_structure)
        
        self.count_total_lines_bytes()
        self.table_to_string()

    def save_report(self):
        file = open('repositorios/' + self.project_name.replace('/','_') + '.txt',"w")

        file.write(f'Path: {self.project_name}\n') 
        file.write(f'Lines: {self.total_lines}\n') 
        file.write(f'Bytes: {self.total_bytes}\n\n\n') 

        file.write(self.table_string + '\n\n\n')
        file.write(self.project_string)
        
        file.close()