import sys
import os
import collections
import re
import CodeSmellHandlers.HandleLongMethodSmell.long_method as lm


def detect_long_method(directory):
    """ 
    Categorize smells based on their types and put filename, lineno, and metric info
    
    Parameters: 
        directory (string): path of the directory of source code files
    
    Return:
        output_lines (list[str]): list of pylint stdout
    
    """
    path, dirs, files = next(os.walk(directory))
    output = lm.output_long_methods(directory).decode('utf-8')
    # print (output.stdout)
    split_lines = output.splitlines()
    output_lines = [output for output in split_lines if len(output) > 3 and\
                    re.search("(R0915|R0913|R0912|R0904|R0902)", output) is not None]
    return output_lines


def analyze_result(smell_list):
    """ 
    Categorize smells based on their types and put filename, lineno, and metric info
    
    Parameters: 
        smell_list (list): list of lines parsed from the pylint stdout
    
    Return:
        smell_info (dict[list[dict]]): smell information categorized by smell_type
    
    """
    analyzed = collections.defaultdict(list)
    for elem in smell_list:
        elem = smell_to_obj(elem)
        analyzed[elem['smell_type']].append({'filename': elem['filename'], \
                'lineno': elem['lineno'], 'metric': elem['metric']})

    return analyzed

def smell_to_obj(smell):
    """ 
    Convert a smell statement into an object
    
    Parameters: 
        smell (string): line parsed from the pylint stdout
    
    Return:
        obj (dict): obj that contains filename, line, smell type, and metric
    
    """
    
    smell_name = {'R0915': 'long_method', 'R0913': 'long_parameter', \
                  'R0912': 'too_many_branches', 'R0904': 'too_many_methods', \
                  'R0902': 'too_many_attributes'}
    
    tokens = [tok.lstrip() for tok in smell.split(':')]
    filename, lineno = tokens[0], int(tokens[1])
    smell_type = tokens[3]
    first, sec = tokens[4].find('('), tokens[4].find('/')
    metric = int(tokens[4][first + 1 : sec])
    obj = {'filename': filename, 'lineno': lineno, 'smell_type': smell_name[smell_type], \
           'metric': metric}
        
    return obj

def generate_log(log_object):
    for smell in log_object:  
        log = open(r"\Users\YJ\Desktop\cs527_project\src\logs\{}_logs".format(smell), "w")
        for elem in log_object[smell]:
            log.write('filename: {}, smelly_lines: {}, metric: {}\n'.format(elem['filename'], str(elem['lineno']), str(elem['metric'])))

# TEST Runs
output_list = detect_long_method("../../code-dump/keras-master")
analyzed = analyze_result(output_list)
generate_log(analyzed)