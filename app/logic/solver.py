import uuid
import json
from datetime import datetime
from pulp import *
from app.settings import LP_DATA_DIR
from pathlib import Path


def id():
    return str(uuid.uuid4())


def setObjective(problem, objective):
    problem['objective'] = objective
    return problem


def addConstraint(problem, constraint):
    problem['constraints'].append(constraint)
    return problem


def addConstraints(problem, constraints):
    problem['constraints'] += constraints
    return problem



def solveBigProblem(jsonProblem):
    solverStart = datetime.now()
    print('LPSolver receive a problem of size {} at {}'.format(len(jsonProblem), solverStart))

    prob = json.loads(jsonProblem)
    print('Problem loaded, took {}'.format(datetime.now() - solverStart))

    sol = solve(prob)
    jsonSol = json.dumps(sol)

    print('Problem solved, total time {}, finished at {}'.format(datetime.now() - solverStart, datetime.now()))
    return jsonSol



def solve(problem):
    solverStart = datetime.now()
    print('LPSolver started at {}'.format(solverStart))

    #problem
    p = LpProblem(problem['id'], LpMaximize if problem['objective']['isMaximize'] else LpMinimize)

    #variables
    variables = {}
    constraintVars = [e['lpVar'] for c in problem['constraints'] for e in c['expr']['expr']]
    objectiveVars = [e['lpVar'] for e in problem['objective']['expr']['expr']]
    uniqueVariables = {v['id']: v for v in constraintVars + objectiveVars}
    for var in uniqueVariables.values():
        if var['id'] not in variables:
            v = LpVariable(var['id'], lowBound=var.get('lowerBound', None), upBound=var.get('upperBound', None),
                              cat = LpBinary if var['isBinary'] else LpInteger if var['isInteger'] else LpContinuous)
            variables[var['id']] = v

    #constraints
    constraint_exprs = {}
    for c in problem['constraints']:
        ce = lpSum([e['coef'] * variables[e['lpVar']['id']] for e in c['expr']['expr']])
        if c['type'] in ['>=', 'GE', 'ge', 'Ge']:
            p += LpConstraint(e=ce, sense=LpConstraintGE, rhs=c['value'], name=c['id'])
        elif c['type'] in ['<=', 'LE', 'le', 'Le']:
            p += LpConstraint(e=ce, sense=LpConstraintLE, rhs=c['value'], name=c['id'])
        elif c['type'] in ['=', '==', 'EQ', 'eq', 'Eq']:
            p += LpConstraint(e=ce, sense=LpConstraintEQ, rhs=c['value'], name=c['id'])
        constraint_exprs[c['id']] = ce

    #objective
    oe = lpSum([e['coef'] * variables[e['lpVar']['id']] for e in problem['objective']['expr']['expr']])
    p += oe, problem['objective'].get('desc', '')

    #debug
    #path = Path(LP_DATA_DIR)
    #path.mkdir(parents=True, exist_ok=True)
    #p.writeLP(LP_DATA_DIR + '/' + problem['id'] + '.lp')

    p.solve()
    probSolved = LpStatus[p.status] == 'Optimal'

    #debug
    #print("Status:", LpStatus[p.status])
    #print("Objective value:", value(p.objective))

    sol = {
        'id': problem['id'],
        'problemID': problem['id'],
        'solutionExists': probSolved,
        'solverStatus': LpStatus[p.status],
        'objectiveValue': None if not probSolved else {
            'id': problem['objective']['id'],
            'objective': problem['objective'],
            'value': value(p.objective)
        },
        'variableValues': [] if not probSolved else [{
            'id': v.name,
            'variable': uniqueVariables[v.name],
            'value': v.varValue
        } for v in p.variables()],
        'constraintValues': [] if not probSolved else
            [{
                'id': c['id'],
                'constraint': c,
                'value': value(constraint_exprs[c['id']])
            } for c in problem['constraints']]
    }

    print('LPSolver took {}, finished at {}'.format(datetime.now() - solverStart, datetime.now()))
    return sol
