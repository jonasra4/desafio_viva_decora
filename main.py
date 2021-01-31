import report
import tree
            
if __name__ == '__main__':
    
    # url = 'https://github.com/frontpressorg/frontpress/tree/master'
    # url = 'https://github.com/jonasra4/Unity-Controller-Scenes/tree/master'
    url = 'https://github.com/jonasra4/snake/tree/master'

    # root = tree.TreeNode("Project frontpressorg/frontpress")
    project_name = 'frontpressorg/frontpress'
    
    current_report = report.Report(project_name)

    current_report.read_project()
    current_report.make_report()
    current_report.save_report()



