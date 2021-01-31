import report
import tree
import threading

def aaaa(ii):
    print(f'buscando {ii}')
    current_report = report.Report(ii)
    current_report.read_project()
    current_report.make_report()
    current_report.save_report()
            
if __name__ == '__main__':
    
    # urls = ['frontpressorg/frontpress','jonasra4/snake','jonasra4/Unity-Controller-Scenes']
    urls = ['frontpressorg/frontpress']

    project_name = 'jonasra4/snake'

    for i in urls:
        threading.Thread(target=aaaa, args=(i, )).start()



