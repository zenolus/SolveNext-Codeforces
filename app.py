import requests
from operator import itemgetter



def initialize():
    user="nks43"
    ROUND=1000
    lower_bound=1700
    upper_bound=4000
    return user,ROUND,lower_bound,upper_bound





def getData():
    link="https://codeforces.com/api/problemset.problems?"
    response=requests.get(link)
    content=response.json()["result"]
    
    return content["problems"],content["problemStatistics"]




def modify(problems,stats,round):
    focus_problems={}
    problem_count=0

    for i in range (len(problems)):
        if problems[i]["contestId"]>=round and 'rating' in problems[i].keys():
            focus_problems[problem_count]=problems[i]
            focus_problems[problem_count]["solved"]=stats[i]["solvedCount"]
            problem_count=problem_count+1

    return focus_problems,problem_count




def sortProblems(problems):
    '''
    Sort according to the number of users solved
    '''
    problems_list=[]

    for i in range (len(problems)):
        problems_list.append(problems[i])

    sorted_list=sorted(problems_list,key=itemgetter('solved'),reverse=True)
    return sorted_list





def safeStr(obj):
    try: return str(obj)
    except UnicodeEncodeError:
        return obj.encode('ascii', 'ignore').decode('ascii')
    except: return ""





def filterProblems(problems,lower_bound,upper_bound):
    '''
    Filer between the ranges of problems
    parameters:
        problems list
        lower bound of rating
        upper bound of rating
    '''
    filtered_list=[]
    for i in range(len(problems)):
        if(problems[i]["rating"]>=lower_bound and problems[i]["rating"]<=upper_bound):
            filtered_list.append(problems[i])

    return filtered_list



#
# TO SAVE TO A TXT FILE, UNCOMMENT ALL THE COMMENTED LINES IN BELOW FUNCTION
#

def save_list(problems,solved_check):

    problem_count=0
    # TargetFile=open("rating1700.txt","a")
    for problem in problems:
        if str(problem["contestId"])+str(problem["index"]) not in solved_check.keys():      #COMMENT THIS LINE TO DISPLAY SOLVED QUESTIONS ALSO
            text="\tsolved by:"+str(problem["solved"])+"\t"+str(problem["contestId"])+str(problem["index"])+"\trating:"+str(problem["rating"])+"\t https://codeforces.com/problemset/problem/"+str(problem["contestId"])+"/"+str(problem["index"])+"\t"+safeStr(problem["name"]+'\n')
            print(text)
            # TargetFile.write(text)
            problem_count=problem_count+1
    
    # TargetFile.close()
    return problem_count




def get_solved(user):
    
    link="https://codeforces.com/api/user.status?handle="+user
    response=requests.get(link)
    content=response.json()["result"]
    
    solved_check={}
    count=0
    for i in range (len(content)):
        if content[i]["verdict"]=="OK":
            if str(content[i]["problem"]["contestId"])+str(content[i]["problem"]["index"]) not in solved_check.keys():
                count=count+1
                solved_check[str(content[i]["problem"]["contestId"])+str(content[i]["problem"]["index"])]="true"
    
    return count,solved_check



if __name__ == "__main__":
    user,ROUND,lower_bound,upper_bound=initialize()

    problems_orig,stats_orig=getData()
    print ("Total problems present :"+str(len(problems_orig)))
    print ("Total problem stats :"+str(len(stats_orig)))


    focus_problems,problem_count=modify(problems_orig,stats_orig,ROUND)
    sorted_list=sortProblems(focus_problems)
    problems=filterProblems(sorted_list,lower_bound,upper_bound)
    
    solved_count,solved_check=get_solved(user)
    print("Number of problems solved is "+str(solved_count))
    print("Final list length: "+str(len(problems)))

    remaining_problems=save_list(problems,solved_check)
    print("Remaining problems to solve in list:"+str(remaining_problems))
   
    
    