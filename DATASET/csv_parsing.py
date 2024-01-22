import csv
import nltk
import string

#-------------------------------------------------
# Supporting functions:

# Loads the csv file
def load_csv_data(filename): 
    mylist = []
    with open(filename,'r') as infile:
        infile_data =csv.reader(infile, delimiter=',')
        print(next(infile_data)) #skip the header
        for row in infile_data: #iterates the file row by row
            mylist.append(row)
    return mylist

# Reads a txt file line by line
def load_txt_data(filename): 
    mylist = []
    with open(filename,'r') as infile:
        infile_data= infile.read().splitlines() #remove the '\n' at the end
        for row in infile_data:
            mylist.append(row)
    return mylist

# Extracts the text of those issues classified as SATD 
def get_satd_issues_text(list): 
    issues_list = []
    print("Total entries in the file = " + str(len(list)))
    for row in list:
        if(row[4]!='non_debt'):
            issues_list.append([row[3],row[4],row[5]])
    return issues_list

# Extracts the text of those commits classified as SATD 
def get_satd_commits_text(list): 
    issues_list = []
    print("Total entries in the file = " + str(len(list)))
    for row in list:
        if(row[3]!='non_debt'):
            issues_list.append([row[2],row[3],row[4]])
    return issues_list

# Extracts the text of those comments classified as SATD
def get_satd_comments_text(list): 
    comments_list = []
    print("Total entries in the file = " + str(len(list)))
    for row in list:
        if(row[2]!='non_debt'):
            comments_list.append([row[1],row[2],'N/A'])
    return comments_list

# Extracts the text of those pull requests classified as SATD
def get_satd_pullreq_text(list): 
    comments_list = []
    print("Total entries in the file = " + str(len(list)))
    for row in list:
        if(row[5]!='non_debt'):
            comments_list.append([row[4],row[5],row[6]])
    return comments_list

def process_satdfile(satd_entries, output_filename):

    # 3- Get a list of security keywords
    keywords = load_txt_data('security_keywords.txt')

    # 4- Get a list of security SATD (SSATD) candidates (those containing the keywords)
    ssatd_list = []
    for entry in satd_entries:
        nopunct_entry = entry[0].lower().translate(str.maketrans('', '', string.punctuation)).split()
        keylist= [key for key in keywords if (key in nopunct_entry)] 
        if (len(keylist)>0):
            ssatd_list.append([entry[0],keylist,len(keylist),entry[1],entry[2],0])
            
    # 5- Save to csv file
    print("Total SATD in the file = " + str(len(satd_entries)))
    print("Number of security SATD candidates = "+str(len(ssatd_list)))

    csv_header = ['text','keywords','count','classification','indicator','SSATD']
    with open(output_filename,'w') as file:
        writer = csv.writer(file)
        writer.writerow(csv_header)
        writer.writerows(ssatd_list)

#-------------------------------------------------
# Start of the csv processing pipeline:

# Comments
satd_comments= get_satd_comments_text(load_csv_data('satd-dataset-code_comments.csv'))
process_satdfile(satd_comments, 'ssatd/ssatd_candidates_comments.csv')

# Commits
satd_commits= get_satd_commits_text(load_csv_data('satd-dataset-commit_messages.csv'))
process_satdfile(satd_commits, 'ssatd/ssatd_candidates_commits.csv')

# Issues
satd_issues= get_satd_issues_text(load_csv_data('satd-dataset-issues.csv'))
process_satdfile(satd_issues, 'ssatd/ssatd_candidates_issues.csv')

# Pull requests
satd_pullreq= get_satd_pullreq_text(load_csv_data('satd-dataset-pull_requests.csv'))
process_satdfile(satd_pullreq, 'ssatd/ssatd_candidates_pull.csv')
