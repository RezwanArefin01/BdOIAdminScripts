#!/usr/bin/env python3

import argparse
import subprocess 
import os
import sys
import random
import string


###################
# Make the parser #
###################

parser = argparse.ArgumentParser()

parser.add_argument('code_name', help='the code name of the task')
parser.add_argument('full_name', help='the full name of the task')
parser.add_argument('--checker', help='if given, the task will use a checker', default=0, action='store_true')
parser.add_argument('--grader', help='if given, the task will use graders', default=0, action='store_true')
parser.add_argument('--communication', help='if given, the task directory will be set up for communication',  default=0, action='store_true')
parser.add_argument('--twostep', help='if given, the task directory will be set up for two step', default=0, action='store_true')
parser.add_argument('--outputonly', help='if given, the task will be initialized to be outputonly, defaults to False', default=0, action='store_true')
parser.add_argument('-t', '--timelimit', help='the time limit in seconds, defaults to 2 seconds', default=2)
parser.add_argument('-m', '--memorylimit', help='the memory limit in MiB, defaults to 256 MiB', default=256)

args = parser.parse_args()
code_name = args.code_name
full_name = args.full_name
timelimit = args.timelimit
memorylimit = args.memorylimit

if args.communication and not args.grader: 
  print("Communication tasks without graders are not supported.")
  sys.exit(0)

if args.twostep and not args.grader: 
  print("Two step tasks without graders are not supported.")
  sys.exit(0)

if args.twostep and args.communication: 
  print("A task can't be both TwoStep and Communication at the same time.")
  sys.exit(0)


#########################
# Create task directory #
#########################

subprocess.call(['mkdir', '-p', code_name])
os.chdir(code_name)

task = f"""name: "{code_name}"
title: "{full_name}"
time_limit: {timelimit}
memory_limit: {memorylimit}
score_mode: max_subtask
public_testcases: all 
max_submission_number: 50
min_submission_interval: 60
token_mode: disabled
primary_language: en
infile: ""
outfile: ""
"""

if args.outputonly: 
  task += 'output_only: True\n'
  subprocess.call(['mkdir', '-p', 'att'])

open('task.yaml', 'w').write(task)



########################
# Create statement.md  #
########################

subprocess.call(['mkdir', '-p', 'statement'])
os.chdir('statement')

statement_md = """# %s 
Story here. 

## Implementation Details
You should implement the following function:
```
procedure
```
* Explanation here 
* Explanation here


## Examples
### Example 1
Consider the following call:
```
call here
```
Explanation here. 


### Example 2
Consider the following call:
```
call here
```
Explanation here. 


## Constraints
* $n \\leq 100$


## Subtasks
1. (x points) $n \\leq 10$


## Sample grader
The sample grader reads the input in the following format:
* line $1$: 

""" % (full_name)

statement_json = f"""{{
    "task_name": "{code_name}",
    "language": "English", 
    "contest": "Contest"
}}
"""
open('statement.md', 'w').write(statement_md)
open('statement.json', 'w').write(statement_json)
os.chdir('..')


#############################
# Create attatchment folder #
#############################
if args.grader: 
  subprocess.call(['mkdir', '-p', 'att'])
  os.chdir('att')

  code = f'#include \"{code_name}.h\"\n\n'

  grader = f"""#include "{code_name}.h"

int main() {{ 
  return 0;
}}
"""

  compile_sh = f'#!/bin/bash\n/usr/bin/g++ -DEVAL -static -O2 -std=c++11 -o {code_name} grader.cpp {code_name}.cpp'

  open(f'{code_name}.h', 'w').write('\n')
  open(f'{code_name}.cpp', 'w').write(code)
  open('grader.cpp', 'w').write(grader)
  open('compile.sh', 'w').write(compile_sh)
  subprocess.call(['chmod', '+x', 'compile.sh'])
  os.chdir('..')


##################
# Create sol dir #
##################

subprocess.call(['mkdir', '-p', 'sol'])
os.chdir('sol')

open('solution.cpp', 'w').write(f'#include \"{code_name}.h\"\n\n' if args.grader else "\n")

if args.grader:
  if args.communication: 
    grader = f"""#include <bits/stdc++.h>
#include "{code_name}.h"
using namespace std; 

int main(int argc, char **argv) {{ 
  FILE *in = fopen(argv[1], "r");
  FILE *out = fopen(argv[2], "w");
  setvbuf(out, NULL, _IONBF, 0);

  return 0; 
}}
"""
  elif args.twostep: 
    grader = f"""#include <bits/stdc++.h>
#include "{code_name}.h"
using namespace std; 

int PROG; 

void first_pass() {{ 
  
}}

void second_pass() {{

}}

int main(int argc, char **argv) {{
  FILE *in = fopen(argv[1], "r");
  FILE *out = fopen(argv[2], "w");
  setvbuf(out, NULL, _IONBF, 0);

  fscanf(in, "%d", PROG); 
  if(PROG == 1) first_pass(); 
  else second_pass(); 

  return 0; 
}}
"""
  else: # batch
    grader = f"""#include <bits/stdc++.h>
#include "{code_name}.h"
using namespace std;

int main() {{

 return 0;   
}}
"""
  grader_name = "stub.cpp" if args.communication or args.twostep else "grader.cpp"
  open(f'{code_name}.h', 'w').write('\n')
  open(f'{grader_name}', 'w').write(grader)

os.chdir('..')



########################
# Create gen directory #
########################

subprocess.call(['mkdir', '-p', 'gen'])
os.chdir('gen')

generator = """#include <bits/stdc++.h>
#include "testlib.h"
using namespace std;

int main(int argc, char *argv[]) {
  registerGen(argc, argv, 1); 

  return 0;
}
"""

validator = """#include <bits/stdc++.h>
#include "testlib.h"
using namespace std;

int main(int argc, char *argv[]) {
  freopen(argv[1], "r", stdin);
  registerValidation(argc, argv);

  return 0;
}
"""

open('GEN', 'w').write('\n')
open('validator.cpp', 'w').write(validator)
open('generator.cpp', 'w').write(generator)

os.chdir('..')



############################
# Create checker directory #
############################

if args.checker or args.communication or args.twostep:
  subprocess.call(['mkdir', '-p', 'check'])
  os.chdir('check')

  if args.checker and not args.communication and not args.twostep: 
    checker = """#include <bits/stdc++.h>
#define CMS
#include \"testlib.h\"
using namespace std;

int main(int argc, char* argv[]) {
  registerTestlibCmd(argc, argv);
  // inf = input file 
  // ans = judge output file
  // ouf = user output file 

}
"""
    open('checker.cpp', 'w').write(checker)

  if args.communication: 
    manager = """#include <bits/stdc++.h>
using namespace std;

int main(int argc, char **argv) { 
  signal(SIGPIPE, SIG_IGN);
  FILE *to_user = fopen(argv[2], "w");
  FILE *from_user = fopen(argv[1], "r");
  setvbuf(to_user, NULL, _IONBF, 0);

  return 0;
}
""" 
    open('manager.cpp', 'w').write(manager)
  
  if args.twostep: 
    manager = """#include <bits/stdc++.h>
using namespace std;

int main(int argc, char **argv) { 
  FILE *to_prog1 = fopen(argv[2], "w");
  FILE *from_prog1 = fopen(argv[1], "r");
  FILE *to_prog2 = fopen(argv[4], "w");
  FILE *from_prog2 = fopen(argv[3], "r");

  setvbuf(to_prog1, NULL, _IONBF, 0);
  setvbuf(to_prog2, NULL, _IONBF, 0);

  fprintf(to_prog1, "1\\n");
  fprintf(to_prog2, "2\\n");

  return 0;
}
""" 
    open('manager.cpp', 'w').write(manager)

  os.chdir('..')

