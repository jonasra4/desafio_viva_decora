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
    
    # for i in range(0, len(lines_repo_file), 2):
        
    index = 0
    total_theads = 0
    list_thread = []

    while index < len(lines_repo_file):
        if total_theads <= 2:
            
            t = threading.Thread(target=create_report, args=(lines_repo_file[index], ))
            list_thread.append(t)
            t.start() 
            total_theads += 1
            index += 1
        else:
            for i in list_thread:
                if not i.is_alive():
                    index += 1
                    total_theads -= 1
                    print('NOVA THREAD')
                    list_thread.remove(i)





    # index = 2

    # t1 = threading.Thread(target=create_report, args=(lines_repo_file[0], ))
    # t2 = threading.Thread(target=create_report, args=(lines_repo_file[1], ))
    # t3 = threading.Thread(target=create_report, args=(lines_repo_file[2], ))
    

    # for i in lines_repo_file:
    # print('primeira theead')
    # t1 = threading.Thread(target=create_report, args=(lines_repo_file[1], ))
    # t1.start()
    # t1.join()
    # print('teminou primeira')
    # print('segunda thread')

    # threading.Thread(target=create_report, args=(lines_repo_file[2], )).start()
    # threading.Thread(target=create_report, args=(lines_repo_file[3], )).start()



