import report
import tree
import threading

def create_report(repo):
    print(f'Looking for the repository: {repo}')
    current_report = report.Report(repo)
    current_report.read_project()
    current_report.make_report()
    current_report.save_report()
    print(f"{repo} complete!")
            
if __name__ == '__main__':
   
    repo_file = open(r"repositorios.txt", 'r')
    lines_repo_file = repo_file.read().splitlines()
    repo_file.close()
            
    index = 0
    list_thread = []
    max_threads = 3

    while index < len(lines_repo_file):

        if len(list_thread) <= max_threads - 1:            
            t = threading.Thread(target=create_report, args=(lines_repo_file[index], ))
            list_thread.append(t)
            t.start() 
            index += 1
        else:
            for i in list_thread:
                if not i.is_alive():
                    list_thread.remove(i)

    print('All repositores finalizados')



